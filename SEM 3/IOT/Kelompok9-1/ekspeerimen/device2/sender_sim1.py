"""
sender_palsu.py - pengganti sender.py yang datanya sintetis tapi berperilaku seperti HP asli.

Jalankan di DUA terminal (= dua "HP"), server.py tetap yang asli:

    python sender_palsu.py hp_saya                 # HP kamu: diam di titik acuan
    python sender_palsu.py hp_lain --profil ngebut # HP lain: mendekat 70 km/j

Opsi:
    --profil  diam | pelan | sedang | ngebut | menjauh | spike
    --interval 1.0,3.0   rentang jeda antar kiriman (detik, acak) - meniru termux-location -r once
    --dry                tampilkan saja, tidak kirim ke MQTT

Yang disimulasikan agar mirip HP asli:
  - posisi dihitung dari integrasi kecepatan (jarak antar HP muncul dari posisi, bukan ditulis tangan)
  - noise GPS berkorelasi (melayang pelan, bukan loncat acak) + akurasi 4-9 m
  - noise kecepatan GPS ~1 km/j
  - interval kirim acak, jadi jarak antar sampel tidak seragam
  - akselerometer = percepatan sebenarnya + getaran kendaraan
  - profil 'spike': sesekali speed GPS melonjak palsu padahal akselerometer diam
"""
import json, time, sys, math, random, argparse

PREFIX = "driveguard/kelompok9"   # samakan dengan server.py
LAT0, LON0 = -7.0000, 110.4000    # titik acuan (posisi hp_saya)
M_PER_DEG_LAT = 111_320.0
M_PER_DEG_LON = 111_320.0 * math.cos(math.radians(LAT0))

# y = meter ke utara dari titik acuan. arah -1 = bergerak ke selatan (menuju titik acuan)
PROFIL = {
    "diam":    dict(y0=0,   arah=0,  kmh=0,  tempuh=0,   ket="diam di titik acuan"),
    "pelan":   dict(y0=150, arah=-1, kmh=30, tempuh=300, ket="mendekat 30 km/j"),
    "sedang":  dict(y0=150, arah=-1, kmh=50, tempuh=300, ket="mendekat 50 km/j"),
    "ngebut":  dict(y0=150, arah=-1, kmh=70, tempuh=300, ket="mendekat 70 km/j"),
    "menjauh": dict(y0=20,  arah=+1, kmh=70, tempuh=150, ket="menjauh 70 km/j"),
    "spike":   dict(y0=150, arah=-1, kmh=30, tempuh=300, ket="30 km/j + lonjakan GPS palsu"),
}


class Kendaraan:
    def __init__(self, id_, profil, rng=None):
        self.id, self.profil, self.p = id_, profil, PROFIL[profil]
        self.rng = rng or random.Random()
        self.putaran = 0              # berapa kali lintasan selesai & diulang
        self.reset()

    def reset(self):
        self.y = float(self.p["y0"])
        self.v = self.p["kmh"] / 3.6
        self.nx = self.ny = 0.0       # noise GPS (m)
        self.t = 0.0

    def langkah(self, dt):
        """Majukan simulasi dt detik, kembalikan paket seperti yang dikirim sender.py."""
        p, r = self.p, self.rng
        self.t += dt
        v_old = self.v
        if p["kmh"] > 0:
            target = p["kmh"] / 3.6 * (1 + 0.03 * math.sin(self.t / 4))
            self.v += max(-3 * dt, min(3 * dt, target - self.v))   # maks 3 m/s^2
        self.y += p["arah"] * (v_old + self.v) / 2 * dt
        if p["tempuh"] and abs(self.y - p["y0"]) > p["tempuh"]:
            self.putaran += 1
            self.reset()                                           # lintasan selesai, ulang

        self.nx = 0.8 * self.nx + r.gauss(0, 1.2)
        self.ny = 0.8 * self.ny + r.gauss(0, 1.2)

        if p["kmh"] == 0:
            kmh = abs(r.gauss(0, 0.3))
            acc_dyn = 0.05 + abs(r.gauss(0, 0.03))
        else:
            kmh = max(0.0, self.v * 3.6 + r.gauss(0, 1.0))
            acc_dyn = abs((self.v - v_old) / dt) + 0.15 + abs(r.gauss(0, 0.2))
        if self.profil == "spike" and r.random() < 0.10:
            kmh += r.choice([50, 60, 70])        # lonjakan palsu, akselerometer tetap tenang

        return {
            "id": self.id,
            "lat": LAT0 + (self.y + self.ny) / M_PER_DEG_LAT,
            "lon": LON0 + self.nx / M_PER_DEG_LON,
            "speed_kmh": round(kmh, 2),
            "acc": round(r.uniform(4, 9), 1),
            "acc_dyn": round(acc_dyn, 2),
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id", nargs="?", default="hp_saya")
    ap.add_argument("--profil", choices=PROFIL)
    ap.add_argument("--interval", default="1.0,3.0")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    profil = a.profil or ("diam" if a.id == "hp_saya" else "ngebut")
    lo, hi = (float(x) for x in a.interval.split(","))
    kend = Kendaraan(a.id, profil)
    topik = f"{PREFIX}/pos/{a.id}"
    print(f"[{a.id}] profil '{profil}': {PROFIL[profil]['ket']} | interval {lo}-{hi} dtk")

    client = None
    if not a.dry:
        import paho.mqtt.client as mqtt
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)   # paho-mqtt 2.x
        except AttributeError:
            client = mqtt.Client()                                   # paho-mqtt 1.x
        client.connect("broker.hivemq.com", 1883, 60)
        client.loop_start()

    t_prev = time.time()
    while True:
        time.sleep(random.uniform(lo, hi))
        now = time.time()
        data = kend.langkah(now - t_prev)
        t_prev = now
        print(f"[{a.id}] y={kend.y:7.1f} m | {data['speed_kmh']:5.1f} km/j | acc_dyn={data['acc_dyn']}")
        if client:
            client.publish(topik, json.dumps(data))


if __name__ == "__main__":
    main()
