import json, subprocess, time
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

def baca_kecepatan():
    hasil = subprocess.run(
        ["termux-location", "-p", "gps", "-r", "once"],
        capture_output=True, text=True, timeout=20
    )
    if hasil.returncode != 0:
        return None
    data = json.loads(hasil.stdout)
    speed = data.get("speed")
    if speed is None:
        return None
    return max(0.0, float(speed) * 3.6)

while True:
    try:
        speed = baca_kecepatan()
        if speed is None:
            print("Kecepatan GPS belum tersedia (mencari sinyal...)")
        else:
            print(f"Mengirim Kecepatan: {speed:.1f} km/jam")
            # Kirim data ke internet (HiveMQ)
            client.publish("driveguard/kelompok4/speed", json.dumps({"speed_kmh": speed}))
    except Exception as error:
        print("Error:", error)
    
    time.sleep(1)