import json, subprocess
import paho.mqtt.client as mqtt

status_sebelumnya = None
getaran_bahaya = None

def getar(durasi):
    subprocess.Popen(
        ["termux-vibrate", "-d", str(durasi)], 
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def on_connect(client, userdata, flags, rc):
    print("Aktuator siap! Menunggu instruksi dari server...")
    client.subscribe("driveguard/kelompok4/status")

def on_message(client, userdata, msg):
    global status_sebelumnya, getaran_bahaya
    data = json.loads(msg.payload.decode())
    status = data["status"]

    if status != status_sebelumnya:
        print("Menerima Status:", status)

        if status == "BAHAYA":
            if getaran_bahaya is None or getaran_bahaya.poll() is not None:
                getaran_bahaya = subprocess.Popen(["termux-vibrate", "-d", "60000"])
        else:
            if getaran_bahaya is not None:
                getaran_bahaya.terminate()
                getaran_bahaya = None
            
            if status == "HATI-HATI" and status_sebelumnya != "HATI-HATI":
                getar(300)

    status_sebelumnya = status

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()