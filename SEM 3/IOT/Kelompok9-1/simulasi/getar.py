import json, subprocess
import paho.mqtt.client as mqtt

PREFIX = "driveguard/kelompok9"   # samakan dengan server.py
TOPIK_STATUS = f"{PREFIX}/status"

status_sebelumnya = None
getaran_bahaya = None


def on_connect(client, userdata, flags, rc):
    print("Aktuator siap! Menunggu instruksi dari server...")
    client.subscribe(TOPIK_STATUS)


def getar(durasi):
    subprocess.Popen(
        ["termux-vibrate", "-f", "-d", str(durasi)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def on_message(client, userdata, msg):
    global status_sebelumnya, getaran_bahaya
    try:
        status = json.loads(msg.payload.decode())["status"]
    except Exception as e:
        print("Payload error:", e)
        return

    if status != status_sebelumnya:
        print("Menerima Status:", status)

    if status == "BAHAYA":
        # dicek di setiap pesan, jadi getaran diperpanjang otomatis setelah 60 detik
        if getaran_bahaya is None or getaran_bahaya.poll() is not None:
            getaran_bahaya = subprocess.Popen(
                ["termux-vibrate", "-f", "-d", "60000"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    else:
        if getaran_bahaya is not None:
            getaran_bahaya.terminate()
            getar(1)                      # paksa getaran lama berhenti
            getaran_bahaya = None
        if status == "HATI-HATI" and status_sebelumnya != "HATI-HATI":
            getar(300)

    status_sebelumnya = status


try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)   # paho-mqtt 2.x
except AttributeError:
    client = mqtt.Client()                                   # paho-mqtt 1.x
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
