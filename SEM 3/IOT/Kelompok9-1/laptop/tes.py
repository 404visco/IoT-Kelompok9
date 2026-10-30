"""
tes_getar.py - kirim status PALSU ke getar.py (tanpa server.py, tanpa data posisi).

Jalankan di laptop:
    python tes_getar.py          # manual: ketik a / h / b lalu Enter
    python tes_getar.py --auto   # otomatis: AMAN -> HATI-HATI -> AMAN -> BAHAYA -> AMAN

PENTING: server.py harus DIMATIKAN, kalau tidak dia ikut mengirim status AMAN tiap detik
dan menimpa status palsu dari sini.
"""
import json, sys, time, threading
import paho.mqtt.client as mqtt

PREFIX = "driveguard/kelompok9"   # samakan dengan getar.py
TOPIK = f"{PREFIX}/status"

SEKUENSI = [                      # (status, lama dalam detik, yang seharusnya terjadi di HP)
    ("AMAN",      5,  "tidak bergetar"),
    ("HATI-HATI", 5,  "getar pendek 1x (0,3 dtk)"),
    ("AMAN",      5,  "tidak bergetar"),
    ("BAHAYA",    15, "getar terus menerus"),
    ("AMAN",      5,  "getar langsung berhenti"),
]
KUNCI = {"a": "AMAN", "h": "HATI-HATI", "b": "BAHAYA"}

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)   # paho-mqtt 2.x
except AttributeError:
    client = mqtt.Client()                                   # paho-mqtt 1.x
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

status = "AMAN"


def kirim_terus():
    """Kirim status tiap 1 detik, persis seperti server.py."""
    while True:
        client.publish(TOPIK, json.dumps({"status": status}))
        time.sleep(1)


threading.Thread(target=kirim_terus, daemon=True).start()

try:
    if "--auto" in sys.argv:
        for s, lama, harap in SEKUENSI:
            status = s
            print(f"Status {s:<10} selama {lama:2d} dtk -> harapan: {harap}")
            time.sleep(lama)
        print("Selesai.")
    else:
        print("Ketik a = AMAN, h = HATI-HATI, b = BAHAYA, q = keluar")
        while True:
            k = input("> ").strip().lower()
            if k == "q":
                break
            if k in KUNCI:
                status = KUNCI[k]
                print(f"Status sekarang: {status}")
finally:
    status = "AMAN"
    time.sleep(1.5)       # pastikan HP dapat status AMAN supaya getaran berhenti