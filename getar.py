import json, subprocess
import paho.mqtt.client as mqtt

# ================= KONFIGURASI BROKER (EMQX Cloud) =================
MQTT_HOST = "ve168e89.ala.asia-southeast1.emqxsl.com"
MQTT_PORT = 8883
MQTT_USER = "kelompok9-idiot"        # <-- ISI SENDIRI (Access Control > Authentication di EMQX)
MQTT_PASS = "fuckcollege#67"        # <-- ISI SENDIRI
CA_FILE = "emqxsl-ca.crt"         # file CA hasil unduhan EMQX, taruh sefolder dengan file ini

PREFIX = "driveguard/kelompok9"   # samakan dengan server.py
TOPIK_STATUS = f"{PREFIX}/status"

status_sebelumnya = None
getaran_bahaya = None


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Aktuator siap! Menunggu instruksi dari server...")
        client.subscribe(TOPIK_STATUS)
    else:
        print(f"GAGAL terhubung, rc={rc} (4/5 biasanya username/password salah)")


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
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set(ca_certs=CA_FILE)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
