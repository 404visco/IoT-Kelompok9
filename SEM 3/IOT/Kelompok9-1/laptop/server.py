import json, time
import paho.mqtt.client as mqtt

BATAS_AMAN = 45
BATAS_BAHAYA = 65
status_sekarang = "AMAN"
waktu_keluar_bahaya = None

def klasifikasi(kecepatan):
    if kecepatan < BATAS_AMAN: return "AMAN"
    elif kecepatan <= BATAS_BAHAYA: return "HATI-HATI"
    else: return "BAHAYA"

def on_connect(client, userdata, flags, rc):
    print("Server siap! Terhubung ke HiveMQ.")
    client.subscribe("driveguard/kelompok4/speed") # Dengarkan kecepatan dari HP 1

def on_message(client, userdata, msg):
    global status_sekarang, waktu_keluar_bahaya
    data = json.loads(msg.payload.decode())
    kecepatan = data["speed_kmh"]
    status_baru = klasifikasi(kecepatan)
    sekarang = time.time()

    # Logika penahanan mode BAHAYA selama 5 detik
    if status_baru == "BAHAYA":
        status_sekarang = "BAHAYA"
        waktu_keluar_bahaya = None
    elif status_sekarang == "BAHAYA":
        if waktu_keluar_bahaya is None:
            waktu_keluar_bahaya = sekarang
        if sekarang - waktu_keluar_bahaya >= 5:
            status_sekarang = status_baru
            waktu_keluar_bahaya = None
    else:
        status_sekarang = status_baru

    print(f"Kecepatan: {kecepatan} km/j | Status: {status_sekarang}")
    
    # Siarkan status terbaru ke HP 2
    client.publish("driveguard/kelompok4/status", json.dumps({"status": status_sekarang}))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()