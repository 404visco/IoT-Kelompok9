"""
sim_hp.py - simulasi dua HP untuk DEMO langsung (tanpa HP asli).

  hp2 = kendaraan DEPAN, yang diberi peringatan (ME_ID di server.py)
  hp1 = kendaraan BELAKANG, pemicu yang mendekat

Skenario berulang sekitar 45 detik:
  AMAN (hp1 mengikuti dari jauh) -> hp1 tancap gas mendekat (HATI-HATI)
  -> hampir menabrak (BAHAYA) -> hp1 mengerem darurat dan menjauh -> AMAN lagi

Pakai : python sim_hp.py [interval_detik]
        interval 2.0 (bawaan) meniru HP asli; 1.0 membuat status lebih responsif.
Format pesan sama dengan sender.py: id, lat, lon, speed_kmh, acc (akurasi GPS, m), acc_dyn, t_send.
"""
import json, math, os, random, sys, time
import paho.mqtt.client as mqtt

HOST = "ve168e89.ala.asia-southeast1.emqxsl.com"
PORT = 8883
MQTT_USER = "kelompok9-idiot"        # <-- ISI SENDIRI (Access Control > Authentication di EMQX)
MQTT_PASS = "fuckcollege#67"        # <-- ISI SENDIRI
CA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emqxsl-ca.crt")
PREFIX = "driveguard/kelompok9"
ID_DEPAN = "hp2"
ID_BELAKANG = "hp1"

INTERVAL = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0

LAT0, LON0 = -7.05, 110.44
M_PER_DEG = 111320.0

V_DEPAN = 45 / 3.6       # 45 km/jam
JARAK_AWAL = 60.0        # meter
DT = 0.1


def bangun_profil(g0=JARAK_AWAL, dt=DT):
    """
    Membuat profil selisih kecepatan (belakang - depan) dan jarak.

    Ambang yang disesuaikan dengan server.py:
    - HATI-HATI: jarak <= 30 m dan selisih kecepatan >= 10 km/jam.
    - BAHAYA: jarak <= 20 m dan selisih kecepatan >= 20 km/jam.

    Setiap fase dibuat cukup lama agar status terlihat saat demo.
    """
    r = []
    g = [g0]
    fase = []

    def langkah(nilai, nama):
        r.append(nilai)
        g.append(g[-1] - nilai * dt)
        fase.append(nama)

    def ramp(durasi, awal, akhir, nama):
        n = max(1, int(durasi / dt))
        for k in range(n):
            nilai = awal + (akhir - awal) * (k + 0.5) / n
            langkah(nilai, nama)

    def tahan_sampai(jarak_target, nilai, nama):
        while g[-1] > jarak_target:
            langkah(nilai, nama)

    # 1. Aman: kedua kendaraan memiliki kecepatan sama dan berjarak jauh.
    for _ in range(int(12 / dt)):
        langkah(0.0, "AMAN")

    # 2. Hati-hati: kendaraan belakang mempercepat, lalu mendekat
    #    sampai sekitar 27 meter dengan selisih kecepatan 19,8 km/jam.
    ramp(2.0, 0.0, 5.5, "MENDEKAT")
    tahan_sampai(27.0, 5.5, "HATI-HATI")

    # 3. Bahaya: kendaraan belakang menambah kecepatan dan masuk
    #    ke jarak di bawah 20 meter dengan selisih > 20 km/jam.
    ramp(1.0, 5.5, 9.0, "MENDEKAT")
    tahan_sampai(18.0, 9.0, "BAHAYA")

    # 4. Rem darurat: selisih kecepatan turun hingga negatif.
    ramp(2.0, 9.0, -4.0, "MENGEREM")
    tahan_sampai(g0 - 4.0, -4.0, "MENJAUH")
    ramp(2.0, -4.0, 0.0, "MENJAUH")

    # Jeda aman sebelum siklus dimulai kembali.
    for _ in range(int(6 / dt)):
        langkah(0.0, "AMAN")

    return r, g, fase


class Skenario:
    def __init__(self):
        self.r, self.g, self.fase = bangun_profil()
        self.periode = len(self.r) * DT
        self.ex = {ID_DEPAN: 0.0, ID_BELAKANG: 0.0}
        self.ey = {ID_DEPAN: 0.0, ID_BELAKANG: 0.0}

    def indeks(self, t):
        return min(int((t % self.periode) / DT), len(self.r) - 1)

    def jarak_nyata(self, t):
        return self.g[self.indeks(t)]

    def fase_demo(self, t):
        return self.fase[self.indeks(t)]

    def _akselerometer(self, a):
        nx = a + random.gauss(0, 0.25)
        ny = random.gauss(0, 0.5)
        nz = 9.81 + random.gauss(0, 0.25)
        return abs(math.sqrt(nx * nx + ny * ny + nz * nz) - 9.81)

    def pesan_pada(self, t, t_send):
        i = self.indeks(t)
        r_now = self.r[i]
        r_next = self.r[min(i + 1, len(self.r) - 1)]

        x_depan = V_DEPAN * t
        x_belakang = x_depan - self.g[i]

        kecepatan = {
            ID_DEPAN: V_DEPAN,
            ID_BELAKANG: V_DEPAN + r_now,
        }
        percepatan = {
            ID_DEPAN: 0.0,
            ID_BELAKANG: (r_next - r_now) / DT,
        }
        posisi_x = {
            ID_DEPAN: x_depan,
            ID_BELAKANG: x_belakang,
        }

        hasil = []
        for id_ in (ID_DEPAN, ID_BELAKANG):
            self.ex[id_] = 0.9 * self.ex[id_] + random.gauss(0, 0.9)
            self.ey[id_] = 0.9 * self.ey[id_] + random.gauss(0, 0.9)

            hasil.append({
                "id": id_,
                "lat": LAT0 + (posisi_x[id_] + self.ex[id_]) / M_PER_DEG,
                "lon": LON0 + self.ey[id_] / (
                    M_PER_DEG * math.cos(math.radians(LAT0))
                ),
                "speed_kmh": max(
                    kecepatan[id_] * 3.6 + random.gauss(0, 0.8), 0.0
                ),
                "acc": round(random.uniform(3.0, 8.0), 1),
                "acc_dyn": round(self._akselerometer(percepatan[id_]), 2),
                "t_send": t_send,
            })

        return hasil


def buat_client():
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    except AttributeError:
        client = mqtt.Client()

    client.username_pw_set(MQTT_USER, MQTT_PASS)
    if os.path.exists(CA_FILE):
        client.tls_set(ca_certs=CA_FILE)
    else:
        client.tls_set()

    return client


def main():
    if MQTT_USER == "ISI_USERNAME_EMQX" or MQTT_PASS == "ISI_PASSWORD_EMQX":
        raise SystemExit(
            "Isi MQTT_USER dan MQTT_PASS melalui environment variable terlebih dahulu."
        )

    if INTERVAL <= 0:
        raise SystemExit("Interval harus lebih besar dari 0.")

    client = buat_client()

    def on_connect(c, userdata, flags, rc):
        if rc == 0:
            print("Terhubung ke EMQX.")
        else:
            print(f"GAGAL terhubung, rc={rc}.")

    client.on_connect = on_connect
    client.connect(HOST, PORT, 60)
    client.loop_start()

    sk = Skenario()
    print(
        f"Siklus demo sekitar {sk.periode:.0f} detik. "
        f"Pengiriman tiap {INTERVAL:g} detik. Ctrl+C untuk berhenti."
    )
    print("Urutan: AMAN -> HATI-HATI -> BAHAYA -> MENJAUH -> AMAN")

    t0 = time.time()
    try:
        while True:
            t = time.time() - t0
            for pesan in sk.pesan_pada(t, time.time()):
                client.publish(
                    f"{PREFIX}/pos/{pesan['id']}",
                    json.dumps(pesan)
                )

            print(
                f"t={t % sk.periode:5.1f}s"
                f" | fase simulasi={sk.fase_demo(t):10s}"
                f" | jarak={sk.jarak_nyata(t):5.1f} m"
            )
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nSimulasi dihentikan.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
