import json, time, math
import paho.mqtt.client as mqtt

# ================= KONFIGURASI =================
PREFIX = "driveguard/kelompok9"   # samakan di server.py, sender.py, getar.py, simulasi.py
TOPIK_POS = f"{PREFIX}/pos/+"
TOPIK_STATUS = f"{PREFIX}/status"

ME_ID = "hp_saya"
RADIUS_M = 30            # radius deteksi (m)
BATAS_AMAN = 45          # km/j
BATAS_BAHAYA = 65        # km/j
STALE_DETIK = 5          # data lebih tua dari ini diabaikan (sender pakai -r once, ~1-4 detik/data)
MAX_ACC_M = 25           # abaikan data GPS dengan akurasi lebih buruk dari ini (m)
TAHAN_BAHAYA = 5         # detik BAHAYA ditahan setelah kondisi hilang
LONJAKAN_KMH = 25        # selisih speed antar sampel yang dicurigai noise
ACC_MIN = 0.8            # m/s^2, di bawah ini dianggap tidak ada percepatan
MAX_TOLAK = 3            # maksimal penolakan lonjakan beruntun
MARGIN_MENDEKAT_M = 0.5  # jarak harus berkurang lebih dari ini agar dianggap mendekat

# ================= STATE =================
posisi = {}              # id -> data terakhir (+ waktu terima "t")
prev_speed = {}          # id -> speed terfilter terakhir
prev_jarak = {}          # id -> jarak saat data terakhir dievaluasi
prev_t = {}              # id -> timestamp data yang terakhir dievaluasi
mendekat_cache = {}      # id -> hasil cek "mendekat" terakhir
tolak = {}               # id -> jumlah penolakan lonjakan beruntun
status_sekarang = "AMAN"
waktu_keluar_bahaya = None

URUTAN = {"AMAN": 0, "HATI-HATI": 1, "BAHAYA": 2}


def reset_state():
    global status_sekarang, waktu_keluar_bahaya
    for d in (posisi, prev_speed, prev_jarak, prev_t, mendekat_cache, tolak):
        d.clear()
    status_sekarang = "AMAN"
    waktu_keluar_bahaya = None


def buat_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)   # paho-mqtt 2.x
    except AttributeError:
        return mqtt.Client()                                   # paho-mqtt 1.x


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def valid(p, sekarang):
    if sekarang - p["t"] > STALE_DETIK:
        return False
    if p.get("acc") is not None and p["acc"] > MAX_ACC_M:
        return False
    return True


def status_dari_kecepatan(v):
    if v > BATAS_BAHAYA:
        return "BAHAYA"
    if v >= BATAS_AMAN:
        return "HATI-HATI"
    return "AMAN"


def proses_data(data):
    """Terima satu paket posisi dari sebuah HP, saring lonjakan GPS palsu, simpan."""
    id_ = data["id"]
    v = float(data["speed_kmh"])
    acc = data.get("acc_dyn")

    v_lama = prev_speed.get(id_)
    # hanya lonjakan NAIK yang dicurigai (penyebab alarm palsu). Penurunan selalu diterima,
    # supaya filter tidak "terkunci" di nilai tinggi palsu.
    spike = (v_lama is not None and acc is not None
             and (v - v_lama) > LONJAKAN_KMH and acc < ACC_MIN)
    if spike and tolak.get(id_, 0) < MAX_TOLAK:
        tolak[id_] = tolak.get(id_, 0) + 1
        print(f"[{id_}] lonjakan {v_lama:.0f}->{v:.0f} km/j diabaikan (akselerometer diam)")
        v = v_lama
    else:
        tolak[id_] = 0
    prev_speed[id_] = v

    data["speed_kmh"] = v
    data["t"] = time.time()          # pakai waktu terima server
    posisi[id_] = data


def evaluasi():
    sekarang = time.time()
    me = posisi.get(ME_ID)
    if not me or not valid(me, sekarang):
        return "AMAN", None, None

    terburuk, jarak_terburuk, id_terburuk = "AMAN", None, None

    for id_, p in list(posisi.items()):
        if id_ == ME_ID:
            continue
        if not valid(p, sekarang):
            for d in (prev_jarak, prev_t, mendekat_cache, prev_speed, tolak):
                d.pop(id_, None)      # data basi/buruk: reset riwayat
            continue

        jarak = haversine(me["lat"], me["lon"], p["lat"], p["lon"])

        # perbarui riwayat jarak HANYA saat ada data baru dari HP itu
        if p["t"] != prev_t.get(id_):
            jarak_lama = prev_jarak.get(id_)
            mendekat_cache[id_] = (jarak_lama is not None
                                   and jarak < jarak_lama - MARGIN_MENDEKAT_M)
            prev_jarak[id_] = jarak
            prev_t[id_] = p["t"]

        if jarak > RADIUS_M:
            continue
        # hanya yang mendekat (atau sudah sangat dekat) yang dihitung
        if not (mendekat_cache.get(id_, False) or jarak < RADIUS_M / 3):
            continue

        s = status_dari_kecepatan(p["speed_kmh"])
        if URUTAN[s] > URUTAN[terburuk]:
            terburuk, jarak_terburuk, id_terburuk = s, jarak, id_

    return terburuk, jarak_terburuk, id_terburuk


def tahan_bahaya(status_baru):
    """Pertahankan BAHAYA selama TAHAN_BAHAYA detik setelah kondisi hilang."""
    global status_sekarang, waktu_keluar_bahaya
    sekarang = time.time()
    if status_baru == "BAHAYA":
        status_sekarang = "BAHAYA"
        waktu_keluar_bahaya = None
    elif status_sekarang == "BAHAYA":
        if waktu_keluar_bahaya is None:
            waktu_keluar_bahaya = sekarang
        if sekarang - waktu_keluar_bahaya >= TAHAN_BAHAYA:
            status_sekarang = status_baru
            waktu_keluar_bahaya = None
    else:
        status_sekarang = status_baru


def langkah():
    """Satu siklus: evaluasi + penahanan. Mengembalikan (status, jarak, id_hp_pemicu)."""
    status_baru, jarak, id_ = evaluasi()
    tahan_bahaya(status_baru)
    return status_sekarang, jarak, id_


def on_connect(client, userdata, flags, rc):
    print("Server siap! Terhubung ke HiveMQ.")
    client.subscribe(TOPIK_POS)


def on_message(client, userdata, msg):
    try:
        proses_data(json.loads(msg.payload.decode()))
    except Exception as e:
        print("Payload error:", e)


def main():
    client = buat_client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_start()

    while True:
        status, jarak, id_ = langkah()
        ket = f" | {id_} @ {jarak:.0f} m" if id_ else ""
        print(f"Status: {status}{ket}")
        client.publish(TOPIK_STATUS, json.dumps({"status": status}))
        time.sleep(1)


if __name__ == "__main__":
    main()
