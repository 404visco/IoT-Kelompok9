import json
import time
import threading
from collections import deque
from datetime import datetime

import streamlit as st
import paho.mqtt.client as mqtt
import pandas as pd

# ===== KONFIGURASI =====
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_SPEED = "driveguard/kelompok4/speed"
TOPIC_STATUS = "driveguard/kelompok4/status"

BATAS_AMAN = 45
BATAS_BAHAYA = 65

st.set_page_config(
    page_title="DriveGuard Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 DriveGuard Dashboard")
st.caption("Real-time monitoring kecepatan kendaraan")

# ===== DATA BERSAMA =====
@st.cache_resource
def get_data():
    return {
        "lock": threading.Lock(),
        "connected": False,
        "speed": 0.0,
        "status": "MENUNGGU DATA",
        "updated": None,
        "history": deque(maxlen=60),
        "client": None,
    }

data = get_data()


# ===== MQTT =====
@st.cache_resource
def start_mqtt():
    client = mqtt.Client(
        client_id=f"driveguard_dash_{int(time.time())}"
    )

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("[MQTT] Connected")
            with data["lock"]:
                data["connected"] = True

            client.subscribe(TOPIC_SPEED)
            client.subscribe(TOPIC_STATUS)
        else:
            print(f"[MQTT] Connection failed: {rc}")

    def on_disconnect(client, userdata, rc):
        with data["lock"]:
            data["connected"] = False
        print(f"[MQTT] Disconnected: {rc}")

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            now = datetime.now()

            with data["lock"]:
                if msg.topic == TOPIC_SPEED:
                    speed = float(payload["speed_kmh"])
                    data["speed"] = speed
                    data["history"].append({
                        "waktu": now.strftime("%H:%M:%S"),
                        "kecepatan": speed
                    })
                    data["updated"] = now

                elif msg.topic == TOPIC_STATUS:
                    data["status"] = payload["status"]

        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            print(f"[MQTT] Invalid message: {e}")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_start()
    data["client"] = client

    return client


try:
    start_mqtt()
except Exception as e:
    st.error(f"Gagal menghubungkan MQTT: {e}")


# ===== DASHBOARD LIVE =====
@st.fragment(run_every="1s")
def dashboard():
    with data["lock"]:
        connected = data["connected"]
        speed = data["speed"]
        status = data["status"]
        updated = data["updated"]
        history = list(data["history"])

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "⚡ Koneksi MQTT",
        "🟢 ONLINE" if connected else "🔴 OFFLINE"
    )
    c2.metric("🚦 Status", status)
    c3.metric(
        "⏱️ Update terakhir",
        updated.strftime("%H:%M:%S") if updated else "--:--:--"
    )

    st.divider()

    colors = {
        "AMAN": "#16A34A",
        "HATI-HATI": "#EAB308",
        "BAHAYA": "#DC2626"
    }
    color = colors.get(status, "#64748B")

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:30px;
            border:3px solid {color};
            border-radius:16px;
            background:{color}15;
        ">
            <h1 style="color:{color};font-size:3.5rem">
                {speed:.1f} km/jam
            </h1>
            <h2 style="color:{color}">{status}</h2>
            <p>Batas aman: {BATAS_AMAN} km/jam |
               Batas bahaya: {BATAS_BAHAYA} km/jam</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📊 Riwayat Kecepatan")

    if history:
        df = pd.DataFrame(history)
        st.line_chart(
            df.set_index("waktu")["kecepatan"],
            height=300
        )

        speeds = df["kecepatan"]
        a, b, c = st.columns(3)
        a.metric("Minimum", f"{speeds.min():.1f} km/jam")
        b.metric("Maksimum", f"{speeds.max():.1f} km/jam")
        c.metric("Rata-rata", f"{speeds.mean():.1f} km/jam")
    else:
        st.info("Menunggu data kecepatan dari HP 1...")

    st.caption(
        f"Broker: {BROKER}:{PORT} | "
        f"Data tersimpan: {len(history)} titik"
    )

dashboard()