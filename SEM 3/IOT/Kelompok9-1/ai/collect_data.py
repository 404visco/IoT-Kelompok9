import csv
import json
from pathlib import Path
from datetime import datetime

import paho.mqtt.client as mqtt

# Konfigurasi harus sama dengan sender.py
BROKER = "broker.hivemq.com"
PORT = 1883
PREFIX = "driveguard/kelompok9"
TOPIC = f"{PREFIX}/pos/+"

# Lokasi penyimpanan dataset
FOLDER = Path(__file__).parent / "dataset"
FOLDER.mkdir(exist_ok=True)
FILE = FOLDER / "raw_data.csv"

KOLOM = [
    "timestamp",
    "id",
    "latitude",
    "longitude",
    "speed_kmh",
    "gps_accuracy",
    "acc_dyn",
]


def simpan_data(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        row = {
            "timestamp": datetime.now().astimezone().isoformat(
                timespec="milliseconds"
            ),
            "id": data.get("id"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "speed_kmh": data.get("speed_kmh"),
            "gps_accuracy": data.get("acc"),
            "acc_dyn": data.get("acc_dyn"),
        }

        file_baru = not FILE.exists() or FILE.stat().st_size == 0

        with open(FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=KOLOM)

            if file_baru:
                writer.writeheader()

            writer.writerow(row)

        print(
            f"[TERSIMPAN] {row['id']} | "
            f"{row['speed_kmh']} km/jam | "
            f"acc_dyn={row['acc_dyn']}"
        )

    except Exception as e:
        print("Gagal menyimpan data:", e)


def buat_client():
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    except AttributeError:
        return mqtt.Client()


client = buat_client()
client.on_message = simpan_data


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Collector terhubung ke HiveMQ!")
        print("Merekam data kendaraan...")
        client.subscribe(TOPIC)
    else:
        print("Koneksi gagal:", rc)


client.on_connect = on_connect

print("Memulai pengumpulan dataset...")
client.connect(BROKER, PORT, 60)
client.loop_forever()
