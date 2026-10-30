import json, subprocess, time, sys, math, statistics
import paho.mqtt.client as mqtt

PREFIX = "driveguard/kelompok9"   # samakan dengan server.py
DEVICE_ID = sys.argv[1] if len(sys.argv) > 1 else "hp_saya"
TOPIK = f"{PREFIX}/pos/{DEVICE_ID}"

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)   # paho-mqtt 2.x
except AttributeError:
    client = mqtt.Client()                                   # paho-mqtt 1.x
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()


def baca_akselerasi():
    """Median percepatan dinamis (m/s^2) dari 5 sampel ~0,25 detik.
    Median (bukan maksimum) supaya satu sentakan tidak membuat nilainya tinggi terus."""
    try:
        hasil = subprocess.run(
            ["termux-sensor", "-s", "accelerometer", "-n", "5", "-d", "50"],
            capture_output=True, text=True, timeout=5
        )
        dec, teks, i, nilai = json.JSONDecoder(), hasil.stdout, 0, []
        while i < len(teks):
            while i < len(teks) and teks[i].isspace():
                i += 1
            if i >= len(teks):
                break
            obj, i = dec.raw_decode(teks, i)
            for sensor in obj.values():
                x, y, z = sensor["values"][:3]
                nilai.append(abs(math.sqrt(x * x + y * y + z * z) - 9.81))
        return round(statistics.median(nilai), 2) if nilai else None
    except Exception:
        return None


def baca_gps():
    hasil = subprocess.run(
        ["termux-location", "-p", "gps", "-r", "once"],
        capture_output=True, text=True, timeout=20
    )
    if hasil.returncode != 0:
        return None
    d = json.loads(hasil.stdout)
    # speed None = belum ada data kecepatan, JANGAN dianggap 0 km/j
    if d.get("latitude") is None or d.get("longitude") is None or d.get("speed") is None:
        return None
    return {
        "id": DEVICE_ID,
        "lat": d["latitude"],
        "lon": d["longitude"],
        "speed_kmh": max(0.0, float(d["speed"]) * 3.6),
        "acc": d.get("accuracy"),
        "acc_dyn": baca_akselerasi(),
    }


while True:
    try:
        data = baca_gps()
        if data is None:
            print("GPS belum tersedia (mencari sinyal...)")
        else:
            print(f"[{DEVICE_ID}] {data['lat']:.5f},{data['lon']:.5f} | "
                  f"{data['speed_kmh']:.1f} km/j | acc_dyn={data['acc_dyn']}")
            client.publish(TOPIK, json.dumps(data))
    except Exception as e:
        print("Error:", e)
    time.sleep(1)
