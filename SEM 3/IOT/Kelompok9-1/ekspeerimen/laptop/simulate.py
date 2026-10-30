"""
Simulasi DriveGuard dengan data sintetis.

MODE OFFLINE (default) - tanpa internet, tanpa HP, selesai dalam sekejap:
    python simulasi.py            # jalankan semua skenario, tampilkan LULUS/GAGAL
    python simulasi.py -v         # + timeline per detik
    python simulasi.py --pilih 1,4,7

MODE MQTT - mengirim data palsu lewat HiveMQ ke server.py yang sedang jalan:
    1) Jalankan  python server.py  (laptop)   -> harus sudah jalan
    2) (opsional) jalankan  python getar.py  di HP agar terasa getarannya
    3) Hentikan sender.py yang asli (supaya tidak bercampur dengan data palsu)
    4) python simulasi.py --mqtt
   Di mode ini cek dilonggarkan (status maksimum + status akhir), karena server
   dan simulator berjalan di jam yang tidak sinkron.
"""
import sys, json, time, argparse

PREFIX = "driveguard/kelompok9"   # samakan dengan server.py
LAT0, LON0 = -7.0000, 110.4000    # titik acuan sembarang (posisi "hp_saya")
M_PER_DEG = 111_320.0
URUTAN = {"AMAN": 0, "HATI-HATI": 1, "BAHAYA": 2}


# ---------- pembuat data sintetis ----------
def titik(jarak_m):
    """Titik 'jarak_m' meter di utara hp_saya."""
    return LAT0 + jarak_m / M_PER_DEG, LON0


def p_saya():
    lat, lon = titik(0)
    return {"id": "hp_saya", "lat": lat, "lon": lon,
            "speed_kmh": 0.0, "acc": 5.0, "acc_dyn": 0.1}


def p_lain(jarak, speed, acc_dyn=0.2, acc=5.0):
    lat, lon = titik(jarak)
    return {"id": "hp_lain", "lat": lat, "lon": lon,
            "speed_kmh": float(speed), "acc": acc, "acc_dyn": acc_dyn}


def lurus(jarak0, closing_ms, speed, **kw):
    """HP lain mendekat dengan laju closing_ms (m/s) dari jarak0 (m)."""
    return lambda t: p_lain(jarak0 - closing_ms * t, speed, **kw)


def semua(s, nilai):
    return all(x == nilai for x in s)


K70, K50, K30 = 70 / 3.6, 50 / 3.6, 30 / 3.6

# ---------- skenario ----------
# gen(t)  : paket hp_lain pada detik ke-t (None = tidak mengirim)
# cek(s)  : validasi ketat mode offline, s = daftar status per detik
# maks    : status tertinggi yang diharapkan (dipakai mode MQTT)
# akhir   : status terakhir yang diharapkan (dipakai mode MQTT, opsional)
SKENARIO = [
    dict(nama="Mendekat 70 km/j dari 100 m -> BAHAYA saat masuk radius",
         durasi=6, gen=lurus(100, K70, 70), maks="BAHAYA", akhir="BAHAYA",
         cek=lambda s: semua(s[:4], "AMAN") and semua(s[4:], "BAHAYA")),

    dict(nama="Mendekat 50 km/j dari 100 m -> HATI-HATI (bukan BAHAYA)",
         durasi=7, gen=lurus(100, K50, 50), maks="HATI-HATI", akhir="HATI-HATI",
         cek=lambda s: semua(s[:6], "AMAN") and s[6] == "HATI-HATI"),

    dict(nama="Menjauh 70 km/j dari 20 m -> tidak boleh alert",
         durasi=5, gen=lambda t: p_lain(20 + K70 * t, 70), maks="AMAN", akhir="AMAN",
         cek=lambda s: semua(s, "AMAN")),

    dict(nama="Lonjakan GPS palsu 30->90 km/j, akselerometer diam -> diabaikan",
         durasi=6,
         gen=lambda t: p_lain(60 - 8.33 * t, 30 if t < 4 else 90, acc_dyn=0.2),
         maks="AMAN", akhir="AMAN",
         cek=lambda s: semua(s, "AMAN")),

    dict(nama="Lonjakan 30->90 km/j, akselerometer aktif (nyata) -> BAHAYA",
         durasi=6,
         gen=lambda t: p_lain(60 - 8.33 * t, 30 if t < 4 else 90,
                              acc_dyn=0.2 if t < 4 else 4.0),
         maks="BAHAYA", akhir="BAHAYA",
         cek=lambda s: semua(s[:4], "AMAN") and semua(s[4:], "BAHAYA")),

    dict(nama="Speed 80 km/j stabil (GPS baru dapat fix) -> filter tidak boleh macet",
         durasi=8,
         gen=lambda t: p_lain(29 - 1.0 * t, 30 if t < 2 else 80, acc_dyn=0.2),
         maks="BAHAYA", akhir="BAHAYA",
         cek=lambda s: semua(s[:5], "AMAN") and semua(s[5:], "BAHAYA")),

    dict(nama="HP lain berhenti kirim (mati) -> alert padam setelah stale + tahan 5 dtk",
         durasi=19,
         gen=lambda t: p_lain(40 - 3.0 * t, 70) if t <= 5 else None,
         maks="BAHAYA", akhir="AMAN",
         cek=lambda s: s[3] == "AMAN" and semua(s[4:16], "BAHAYA") and semua(s[16:], "AMAN")),

    dict(nama="Sejajar 8 m, 70 km/j (jarak tetap) -> tetap BAHAYA",
         durasi=6, gen=lambda t: p_lain(8, 70), maks="BAHAYA", akhir="BAHAYA",
         cek=lambda s: semua(s, "BAHAYA")),

    dict(nama="70 km/j tapi di luar radius (60 m) -> AMAN",
         durasi=5, gen=lambda t: p_lain(60, 70), maks="AMAN", akhir="AMAN",
         cek=lambda s: semua(s, "AMAN")),

    dict(nama="Akurasi GPS buruk (40 m) -> data dibuang -> AMAN",
         durasi=5, gen=lambda t: p_lain(8, 70, acc=40.0), maks="AMAN", akhir="AMAN",
         cek=lambda s: semua(s, "AMAN")),

    dict(nama="Data hanya tiap 2 detik -> HATI-HATI tidak boleh berkedip",
         durasi=11,
         gen=lambda t: p_lain(35 - 3.0 * t, 50) if t % 2 == 0 else None,
         maks="HATI-HATI", akhir="HATI-HATI",
         cek=lambda s: semua(s[:2], "AMAN") and semua(s[2:], "HATI-HATI")),
]


def ringkas(s):
    out = []
    for st in s:
        if out and out[-1][0] == st:
            out[-1][1] += 1
        else:
            out.append([st, 1])
    return " -> ".join(f"{a}x{b}" for a, b in out)


def pilih_skenario(teks):
    if not teks:
        return list(enumerate(SKENARIO, 1))
    idx = [int(x) for x in teks.split(",")]
    return [(i, SKENARIO[i - 1]) for i in idx]


# ---------- MODE OFFLINE ----------
def jalankan_offline(daftar, verbose):
    import server

    class Jam:                       # jam palsu: waktu maju 1 detik per tick
        t = 0.0

        def time(self):
            return Jam.t

    server.time = Jam()
    T0 = 1_000_000.0
    lulus = 0
    for no, sk in daftar:
        server.reset_state()
        s = []
        if verbose:
            print(f"\n--- [{no}] {sk['nama']}")
        for t in range(sk["durasi"]):
            Jam.t = T0 + t
            lain = sk["gen"](t)
            for p in (p_saya(), lain):
                if p:
                    server.proses_data(dict(p))
            status, jarak, _ = server.langkah()
            s.append(status)
            if verbose:
                sp = f"{lain['speed_kmh']:.0f} km/j" if lain else "(tidak kirim)"
                jr = f"{jarak:.0f} m" if jarak is not None else "-"
                print(f"  t={t:2d}  hp_lain={sp:>14}  jarak_pemicu={jr:>6}  status={status}")
        ok = sk["cek"](s)
        lulus += ok
        print(f"[{'LULUS' if ok else 'GAGAL'}] {no:2d}. {sk['nama']}")
        print(f"          hasil: {ringkas(s)}")
    print(f"\n{lulus}/{len(daftar)} skenario lulus")
    return lulus == len(daftar)


# ---------- MODE MQTT ----------
def buat_client():
    import paho.mqtt.client as mqtt
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    except AttributeError:
        return mqtt.Client()


def jalankan_mqtt(daftar, jeda):
    diterima = []
    client = buat_client()

    def on_connect(c, u, f, rc):
        c.subscribe(f"{PREFIX}/status")

    def on_message(c, u, msg):
        try:
            diterima.append(json.loads(msg.payload.decode())["status"])
        except Exception:
            pass

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_start()
    time.sleep(2)

    lulus = 0
    for no, sk in daftar:
        print(f"\n[{no}] {sk['nama']}")
        print(f"    menunggu server tenang {jeda} dtk ...")
        time.sleep(jeda)
        diterima.clear()
        for t in range(sk["durasi"]):
            for p in (p_saya(), sk["gen"](t)):
                if p:
                    client.publish(f"{PREFIX}/pos/{p['id']}", json.dumps(p))
            time.sleep(1)
        time.sleep(1.5)                      # tunggu status terakhir tiba
        seen = list(diterima)
        if not seen:
            print("    [GAGAL] tidak ada status dari server. server.py sudah jalan?")
            continue
        maks = max(seen, key=lambda x: URUTAN[x])
        ok = maks == sk["maks"] and (sk["akhir"] is None or seen[-1] == sk["akhir"])
        lulus += ok
        print(f"    [{'LULUS' if ok else 'GAGAL'}] status maks={maks} (harap {sk['maks']}), "
              f"akhir={seen[-1]} (harap {sk['akhir']})")
        print(f"    diterima: {ringkas(seen)}")
    client.loop_stop()
    print(f"\n{lulus}/{len(daftar)} skenario lulus")
    return lulus == len(daftar)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mqtt", action="store_true", help="kirim lewat HiveMQ ke server.py")
    ap.add_argument("-v", "--verbose", action="store_true", help="timeline per detik (offline)")
    ap.add_argument("--pilih", help="nomor skenario, mis. 1,4,7")
    ap.add_argument("--jeda", type=int, default=13, help="jeda antar skenario di mode MQTT (dtk)")
    a = ap.parse_args()

    daftar = pilih_skenario(a.pilih)
    ok = jalankan_mqtt(daftar, a.jeda) if a.mqtt else jalankan_offline(daftar, a.verbose)
    sys.exit(0 if ok else 1)
