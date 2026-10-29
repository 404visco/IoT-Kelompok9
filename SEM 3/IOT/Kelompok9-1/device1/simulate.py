import json, time
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

def kirim_kecepatan(speed):
    data = json.dumps({"speed_kmh": speed})
    client.publish("driveguard/kelompok4/speed", data)

def simulasi(speed, durasi):
    print(f"--- Simulasi {speed} km/jam selama {durasi} detik ---")
    akhir = time.monotonic() + durasi
    while time.monotonic() < akhir:
        kirim_kecepatan(speed)
        time.sleep(1)

try:
    simulasi(30, 3)  # AMAN
    simulasi(50, 3)  # HATI-HATI
    simulasi(70, 3)  # BAHAYA
    simulasi(50, 7)  # Keluar dari BAHAYA setelah 5 dtk
    simulasi(30, 3)  # AMAN
except Exception as error:
    print(f"Error: {error}")