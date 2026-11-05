import json
import math
import os
import time
import threading
from collections import deque
from datetime import datetime, timedelta
from html import escape as esc

import altair as alt
import pandas as pd
import pydeck as pdk
import paho.mqtt.client as mqtt
import streamlit as st

# ===== KONFIGURASI (samakan dengan server.py) =====
BROKER = "ve168e89.ala.asia-southeast1.emqxsl.com"
PORT = 8883
MQTT_USER = "kelompok9-idiot"        # <-- ISI SENDIRI (Access Control > Authentication di EMQX)
MQTT_PASS = "fuckcollege#67"   
CA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emqxsl-ca.crt")   # taruh sefolder dengan file ini
PREFIX = "driveguard/kelompok9"          # harus sama di semua file
TOPIC_POS = f"{PREFIX}/pos/+"
TOPIC_STATUS = f"{PREFIX}/status/+"          # status per HP, dikirim server.py
STATUS_PREFIX = f"{PREFIX}/status/"
POS_PREFIX = f"{PREFIX}/pos/"
 
PHONE_IDS = ["hp1", "hp2"]               # HP yang selalu punya kartu status (walau belum mengirim data)
PERAN = {"hp1": "Kendaraan belakang", "hp2": "Kendaraan depan"}
VIBRASI = {"AMAN": "tidak bergetar", "HATI-HATI": "getar pendek", "BAHAYA": "getar panjang terus"}
ME_ID = "hp2"                        # HP yang DIBERI PERINGATAN = kendaraan depan (samakan dengan ME_ID di server.py)
RADIUS_M = 30                            # hanya untuk tampilan; samakan dengan server.py
# Aturan status (samakan dengan server.py): kec_relatif = kecepatan pemicu - kecepatan hp2, km/jam
REL_HATI = 10                            # km/jam
REL_BAHAYA = 20                          # km/jam
JARAK_BAHAYA = 20                        # m
REL_NAIK = 6                             # km/jam, HATI-HATI kalau tren NAIK
STALE_TAMPIL = 10                        # HP dianggap tidak aktif jika data lebih tua (detik)
STATUS_STALE = 5                         # server dianggap diam jika status lebih tua (detik)
 
# ===== PALET =====
BROWN = "#9E6751"
RED = "#CE3515"
TEAL = "#304954"
TAUPE = "#C8BAAA"
PEACH = "#E8AE90"
TEAL_L = "#6FA3B5"   # turunan teal yang lebih terang, untuk teks dan garis di latar gelap
BG = "#121D22"       # turunan teal (sangat gelap)
SURFACE = "#1A2A32"
INK = "#EFE8DF"      # turunan taupe (sangat terang)
SOFT = "#A9B6BB"
LINE = "#2B404A"
 
WARNA_ID = [PEACH, TEAL_L, TAUPE, "#9DB8C2", "#B58B7A", "#7E8F96", "#D9C4B0", "#5E8798"]   # warna tetap per HP
 
st.set_page_config(page_title="DriveGuard", page_icon="🚗", layout="wide")
 
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
:root{color-scheme:dark;--teal:#304954;--teal-l:#6FA3B5;--red:#CE3515;--brown:#9E6751;--taupe:#C8BAAA;--peach:#E8AE90;
      --bg:#121D22;--surface:#1A2A32;--line:#2B404A;--ink:#EFE8DF;--soft:#A9B6BB;}
html, body, .stApp, [class*="st-"], button, input, textarea{font-family:'Manrope',system-ui,-apple-system,'Segoe UI',sans-serif;}
.stApp{background:radial-gradient(1100px 480px at 50% -8%, rgba(48,73,84,.6), transparent 70%), var(--bg);color:var(--ink);}
header[data-testid="stHeader"]{background:transparent;}
#MainMenu, footer{visibility:hidden;}
.block-container{padding-top:1.4rem;padding-bottom:3rem;max-width:1280px;}
[data-testid="stSidebar"]{background:#0E171B;border-right:1px solid var(--line);}
[data-testid="stSidebar"] .block-container{padding-top:1.5rem;}
 
.dg-top{background:var(--teal);color:#F5F0EA;border-radius:18px;padding:20px 26px;margin-bottom:18px;
        border:1px solid rgba(232,174,144,.22);
        display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;}
.dg-brand{font-size:1.6rem;font-weight:800;letter-spacing:-.02em;line-height:1.1;}
.dg-sub{font-size:.88rem;color:var(--taupe);margin-top:4px;}
.dg-pills{display:flex;gap:8px;flex-wrap:wrap;}
.dg-pill{display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:999px;font-size:.82rem;
         font-weight:600;background:rgba(18,29,34,.35);border:1px solid rgba(245,240,234,.2);}
.dg-dot{display:inline-block;width:9px;height:9px;border-radius:50%;flex:none;}
 
.dg-hero{border-radius:18px;padding:28px 32px;min-height:290px;display:flex;flex-direction:column;justify-content:space-between;}
.dg-hero.danger{animation:dg-pulse 1.6s ease-in-out infinite;}
@keyframes dg-pulse{0%,100%{box-shadow:0 0 0 0 rgba(206,53,21,.6);}50%{box-shadow:0 0 0 14px rgba(206,53,21,0);}}
@media (prefers-reduced-motion:reduce){.dg-hero.danger{animation:none;}}
.dg-hero-label{font-size:.9rem;font-weight:600;opacity:.8;}
.dg-hero-status{font-size:clamp(2.4rem,5vw,4rem);font-weight:800;letter-spacing:-.03em;line-height:1.05;margin:6px 0 4px;}
.dg-hero-note{font-size:1.05rem;font-weight:600;opacity:.92;}
.dg-hero-near{font-size:.95rem;margin-top:14px;opacity:.9;}
.dg-prox{margin-top:16px;}
.dg-track{position:relative;height:6px;border-radius:6px;background:rgba(127,127,127,.35);}
.dg-ring{position:absolute;top:-6px;width:2px;height:18px;background:currentColor;opacity:.65;}
.dg-me{position:absolute;top:-5px;width:16px;height:16px;border-radius:50%;background:currentColor;
       transform:translateX(-50%);transition:left .6s ease;}
.dg-prox-l{display:flex;justify-content:space-between;font-size:.74rem;opacity:.75;margin-top:10px;}
.dg-limits{display:flex;gap:18px;flex-wrap:wrap;font-size:.8rem;opacity:.85;margin-top:16px;font-weight:600;}
 
.dg-duo{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:16px;}
.dg-phone{border-radius:18px;padding:22px 26px;display:flex;flex-direction:column;gap:4px;border:1px solid rgba(245,240,234,.12);}
.dg-phone.danger{animation:dg-pulse 1.6s ease-in-out infinite;}
@media (prefers-reduced-motion:reduce){.dg-phone.danger{animation:none;}}
.dg-phone-top{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;}
.dg-phone-name{font-size:1.15rem;font-weight:800;}
.dg-role{font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:999px;background:rgba(18,29,34,.35);border:1px solid rgba(245,240,234,.25);}
.dg-phone-status{font-size:clamp(2rem,4vw,3.1rem);font-weight:800;letter-spacing:-.03em;line-height:1.05;margin:4px 0 2px;}
.dg-phone-status.kecil{font-size:1.5rem;}
.dg-phone-gauge{background:rgba(18,29,34,.55);border-radius:14px;padding:8px 10px 6px;margin-top:12px;text-align:center;}
.dg-phone-gauge svg{width:100%;max-width:230px;}
.dg-phone-gauge .z{font-size:.78rem;font-weight:700;color:var(--soft);}
.dg-vib{margin-top:12px;font-size:.85rem;font-weight:700;padding:7px 14px;border-radius:999px;background:rgba(18,29,34,.35);border:1px solid rgba(245,240,234,.2);align-self:flex-start;}
 
.dg-card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px 20px;}
.dg-gauge{min-height:290px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;}
.dg-gauge .t{font-size:.9rem;font-weight:700;color:var(--soft);}
.dg-gauge svg{width:100%;max-width:300px;margin-top:4px;}
.dg-gauge .z{font-size:.85rem;font-weight:700;margin-top:2px;}
.dg-k-label{font-size:.82rem;font-weight:600;color:var(--soft);}
.dg-k-val{font-size:1.75rem;font-weight:800;letter-spacing:-.02em;margin-top:2px;font-variant-numeric:tabular-nums;color:var(--ink);}
.dg-k-sub{font-size:.78rem;color:var(--soft);margin-top:2px;}
 
.dg-chips{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 8px;}
.dg-chip{display:inline-flex;align-items:center;gap:9px;padding:8px 14px;border-radius:12px;background:var(--surface);
         border:1px solid var(--line);font-size:.85rem;color:var(--ink);}
.dg-chip.off{opacity:.45;}
.dg-chip .m{color:var(--soft);font-variant-numeric:tabular-nums;}
.dg-empty{border:1.5px dashed #3A525C;border-radius:14px;padding:34px 20px;text-align:center;color:var(--soft);font-weight:600;}
 
.dg-hps{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:10px;margin:16px 0 8px;}
.dg-hp{background:var(--surface);border:1px solid var(--line);border-left:5px solid var(--line);border-radius:14px;padding:12px 16px;}
.dg-hp.off{opacity:.45;}
.dg-hp-top{display:flex;justify-content:space-between;align-items:center;gap:8px;}
.dg-hp-name{font-weight:800;display:flex;align-items:center;gap:8px;}
.dg-badge{font-size:.7rem;font-weight:800;padding:3px 10px;border-radius:999px;letter-spacing:.03em;white-space:nowrap;}
.dg-hp-m{font-size:.8rem;color:var(--soft);margin-top:6px;font-variant-numeric:tabular-nums;}
.stTabs [data-baseweb="tab-list"]{gap:4px;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{padding:10px 16px;color:var(--soft);font-weight:700;}
.stTabs [aria-selected="true"]{color:var(--peach);}
.stTabs [data-baseweb="tab-highlight"]{background:var(--peach);}
.stButton>button, .stDownloadButton>button{border-radius:10px;border:1px solid #3A525C;font-weight:700;background:var(--surface);color:var(--ink);}
.stButton>button:hover, .stDownloadButton>button:hover{border-color:var(--peach);color:var(--peach);}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)
 
 
def h(s):
    """Rapikan HTML jadi satu baris supaya tidak terbaca sebagai blok kode oleh markdown."""
    return " ".join(line.strip() for line in s.splitlines())
 
 
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))
 
 
# ===== DATA BERSAMA =====
@st.cache_resource
def get_data():
    return {
        "lock": threading.Lock(),
        "connected": False,
        "devices": {},                   # id -> data terakhir
        "hist": deque(maxlen=400),       # riwayat kecepatan + akselerometer per HP
        "jarak": deque(maxlen=1500),     # riwayat jarak antar pasangan HP
        "status_hp": {},                 # id -> {status, jarak, pemicu, t} dari server
        "urutan": [],                    # urutan HP pertama kali terlihat (untuk warna tetap)
        "log_status": deque(maxlen=40),  # perubahan status terbaru di depan
    }
 
 
data = get_data()
 
 
# ===== MQTT =====
@st.cache_resource
def start_mqtt():
    cid = f"driveguard_dash_{int(time.time())}"
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=cid)  # paho 2.x
    except AttributeError:
        client = mqtt.Client(client_id=cid)                                    # paho 1.x
 
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("[MQTT] Connected")
            with data["lock"]:
                data["connected"] = True
            client.subscribe(TOPIC_POS)
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
 
            if msg.topic.startswith(STATUS_PREFIX):
                id_ = msg.topic[len(STATUS_PREFIX):]
                status = payload["status"]
                with data["lock"]:
                    lama = data["status_hp"].get(id_, {}).get("status")
                    if status != lama:
                        data["log_status"].appendleft({
                            "waktu": now.strftime("%H:%M:%S"), "HP": id_,
                            "status": status, "pemicu": payload.get("pemicu") or "-",
                            "jarak": round(payload["jarak"]) if payload.get("jarak") is not None else None,
                            "tren AI": payload.get("tren") or "-",
                        })
                    data["status_hp"][id_] = {
                        "status": status, "jarak": payload.get("jarak"),
                        "pemicu": payload.get("pemicu"),
                        "tren": payload.get("tren"), "tren_id": payload.get("tren_id"), "t": now,
                    }
 
            elif msg.topic.startswith(POS_PREFIX):
                id_ = payload.get("id") or msg.topic[len(POS_PREFIX):]
                d = {
                    "lat": float(payload["lat"]),
                    "lon": float(payload["lon"]),
                    "speed": float(payload["speed_kmh"]),
                    "acc": payload.get("acc"),
                    "acc_dyn": payload.get("acc_dyn"),
                    "t": now,
                }
                with data["lock"]:
                    if id_ not in data["urutan"]:
                        data["urutan"].append(id_)
                    data["devices"][id_] = d
                    data["hist"].append({
                        "waktu": now, "id": id_,
                        "speed": d["speed"], "acc_dyn": d["acc_dyn"],
                    })
                    for k, o in data["devices"].items():
                        if k != id_:
                            data["jarak"].append({
                                "waktu": now, "a": id_, "b": k,
                                "jarak": haversine(d["lat"], d["lon"], o["lat"], o["lon"]),
                            })
 
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            print(f"[MQTT] Invalid message: {e}")
 
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    if os.path.exists(CA_FILE):
        client.tls_set(ca_certs=CA_FILE)
    else:
        client.tls_set()   # pakai CA bawaan sistem
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    return client
 
 
if not (MQTT_USER and MQTT_PASS):
    st.warning("MQTT_USER / MQTT_PASS belum diisi (environment variable atau Secrets).")
try:
    start_mqtt()
except Exception as e:
    st.error(f"Gagal menghubungkan MQTT: {e}")
 
 
# ===== SIDEBAR: KONTROL =====
WINDOWS = {"1 menit": 60, "5 menit": 300, "15 menit": 900, "Semua": None}
 
with data["lock"]:
    known_ids = sorted(data["devices"])
    hist_snapshot = list(data["hist"])
 
with st.sidebar:
    st.markdown(
        h(f'<div style="font-size:1.25rem;font-weight:800;letter-spacing:-.02em;">DriveGuard</div>'
          f'<div style="font-size:.82rem;color:{SOFT};margin-bottom:10px;">Kontrol dashboard</div>'),
        unsafe_allow_html=True,
    )
    st.toggle("Live update", value=True, key="live",
              help="Matikan untuk membekukan layar, lalu geser dan zoom grafik atau peta tanpa ter-reset.")
    st.select_slider("Interval refresh", options=[1, 2, 5, 10], value=1, key="refresh",
                     format_func=lambda s: f"{s} dtk")
    st.select_slider("Rentang grafik", options=list(WINDOWS), value="5 menit", key="window")
    st.selectbox("HP fokus", ["Otomatis"] + known_ids, key="fokus",
                 help=f"Sudut pandang jarak terdekat, grafik jarak, dan peta (kartu status selalu menampilkan semua HP). Otomatis = {ME_ID} bila ada. "
                      "Daftar HP diperbarui setiap kali kamu mengubah kontrol.")
    st.multiselect("Sembunyikan HP", options=known_ids, key="hidden",
                   placeholder="Semua HP ditampilkan",
                   help="Daftar HP diperbarui setiap kali kamu mengubah kontrol.")
    st.toggle("Pusatkan peta ke HP fokus", value=True, key="center_me")
 
    st.divider()
    # Sidebar tidak ikut refresh live (hanya area utama yang di-refresh), jadi data CSV
    # diambil saat tombol ini ditekan, bukan saat halaman pertama dibuka.
    if st.button("Siapkan riwayat (CSV)", help="Ambil data riwayat terbaru, lalu tombol unduh muncul."):
        with data["lock"]:
            rows = list(data["hist"])
        if rows:
            st.session_state["csv_data"] = pd.DataFrame(rows).to_csv(index=False)
            st.session_state["csv_name"] = f"driveguard_riwayat_{datetime.now():%Y%m%d_%H%M%S}.csv"
            st.session_state["csv_n"] = len(rows)
        else:
            st.session_state.pop("csv_data", None)
            st.toast("Belum ada data untuk diunduh", icon="⚠️")
    if st.session_state.get("csv_data"):
        st.download_button(
            f"Unduh CSV ({st.session_state['csv_n']} titik)",
            data=st.session_state["csv_data"],
            file_name=st.session_state["csv_name"],
            mime="text/csv",
        )
    if st.button("Hapus riwayat grafik"):
        with data["lock"]:
            data["hist"].clear()
            data["jarak"].clear()
            data["log_status"].clear()
        st.toast("Riwayat grafik dihapus", icon="🧹")
 
    st.markdown(
        h(f'<div style="font-size:.76rem;color:{SOFT};margin-top:18px;line-height:1.6;">'
          f'Broker: {esc(BROKER)}:{PORT}<br>Topik: {esc(PREFIX)}/...</div>'),
        unsafe_allow_html=True,
    )
 
 
# ===== HELPER TAMPILAN =====
def hex_rgb(c, a=255):
    c = c.lstrip("#")
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)] + [a]
 
 
def peta_warna(urutan):
    """Warna tetap per HP, berdasarkan urutan pertama kali terlihat."""
    return {k: WARNA_ID[i % len(WARNA_ID)] for i, k in enumerate(urutan)}
 
 
STATUS_WARNA = {"AMAN": TEAL_L, "HATI-HATI": PEACH, "BAHAYA": RED}
 
 
def selisih_kec(v_pemicu, v_me):
    """Kecepatan relatif (km/jam): pemicu - penerima. Positif = pemicu lebih cepat."""
    if v_pemicu is None or v_me is None:
        return None
    return v_pemicu - v_me
 
 
TREN_IKON = {"NAIK": "&#9650; NAIK", "TURUN": "&#9660; TURUN", "STABIL": "&#9644; STABIL"}
 
 
def kpi(label, value, sub=""):
    return h(f'<div class="dg-card"><div class="dg-k-label">{label}</div>'
             f'<div class="dg-k-val">{value}</div><div class="dg-k-sub">{sub or "&nbsp;"}</div></div>')
 
 
def kosong(teks):
    st.markdown(f'<div class="dg-empty">{teks}</div>', unsafe_allow_html=True)
 
 
def gauge_svg(v, warna_isi=TEAL_L):
    vmax = max(100, math.ceil((v or 0) * 1.3 / 10) * 10)
    cx, cy, r = 110, 105, 85
 
    def pt(val, rad=r):
        t = min(max(val / vmax, 0), 1)
        a = math.pi * (1 - t)
        return cx + rad * math.cos(a), cy - rad * math.sin(a)
 
    def arc(v0, v1, color):
        x0, y0 = pt(v0)
        x1, y1 = pt(v1)
        return (f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}" '
                f'stroke="{color}" stroke-width="13" fill="none"/>')
 
    parts = [arc(0, vmax * 0.999, LINE)]
    if v is not None and v > 0.5:
        parts.append(arc(0, min(v, vmax * 0.999), warna_isi))
    if v is not None:
        nx, ny = pt(v, r - 24)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{INK}" '
                     f'stroke-width="3.5" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="7" fill="{INK}"/>')
    parts.append(f'<text x="{cx - r}" y="125" font-size="10" fill="{SOFT}" text-anchor="middle">0</text>'
                 f'<text x="{cx + r}" y="125" font-size="10" fill="{SOFT}" text-anchor="middle">{vmax}</text>')
    teks = f"{v:.1f}" if v is not None else "-"
    parts.append(f'<text x="{cx}" y="150" font-size="26" font-weight="800" fill="{INK}" '
                 f'text-anchor="middle">{teks}</text>')
    return f'<svg viewBox="0 0 220 160" role="img" aria-label="Speedometer">{"".join(parts)}</svg>'
 
 
def to_df(rows, nilai, window, hidden, now):
    cutoff = now - timedelta(seconds=window) if window else None
    out = [{"waktu": r["waktu"], "id": r["id"], "nilai": r[nilai]}
           for r in rows
           if r.get(nilai) is not None and r["id"] not in hidden
           and (cutoff is None or r["waktu"] >= cutoff)]
    if not out:
        return None
    df = pd.DataFrame(out)
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce")
    df = df.dropna()
    return df if not df.empty else None
 
 
def grafik(df, judul_y, warna, aturan=()):
    ids = sorted(df["id"].unique())
    base = (
        alt.Chart(df)
        .mark_line(interpolate="monotone", strokeWidth=2.6,
                   point=alt.OverlayMarkDef(size=20, filled=True))
        .encode(
            x=alt.X("waktu:T", title=None,
                    axis=alt.Axis(format="%H:%M:%S", grid=False, tickCount=5)),
            y=alt.Y("nilai:Q", title=judul_y),
            color=alt.Color("id:N", scale=alt.Scale(domain=ids, range=[warna[i] for i in ids]),
                            legend=alt.Legend(orient="top", title=None, symbolType="stroke")),
            tooltip=[alt.Tooltip("id:N", title="HP"),
                     alt.Tooltip("waktu:T", title="Waktu", format="%H:%M:%S"),
                     alt.Tooltip("nilai:Q", title=judul_y, format=".1f")],
        )
        .interactive()
    )
    layers = [base]
    for v, c in aturan:
        layers.append(
            alt.Chart(pd.DataFrame({"y": [v]}))
            .mark_rule(strokeDash=[5, 4], strokeWidth=1.6, color=c)
            .encode(y=alt.Y("y:Q", title=judul_y))
        )
    return (
        alt.layer(*layers)
        .properties(height=300, width="container")
        .configure(background="transparent")
        .configure_view(stroke=None)
        .configure_axis(gridColor=LINE, domain=False, tickColor=LINE,
                        labelColor=SOFT, titleColor=SOFT, labelFont="Manrope", titleFont="Manrope")
        .configure_legend(labelColor=INK, labelFont="Manrope")
    )
 
 
TONE = {
    "AMAN": dict(bg=TEAL, fg="#F5F0EA", note="Kondisi terkendali", ikon="✅"),
    "HATI-HATI": dict(bg=PEACH, fg="#3A2418", note="Perhatikan kendaraan di sekitar", ikon="⚠️"),
    "BAHAYA": dict(bg=RED, fg="#FFF7F2", note="Kurangi kecepatan sekarang", ikon="🚨"),
}
TONE_DEFAULT = dict(bg="#26393F", fg=TAUPE, note="Belum ada status terbaru", ikon="")
 
 
# ===== DASHBOARD LIVE =====
live = st.session_state.get("live", True)
interval = f"{st.session_state.get('refresh', 1)}s" if live else None
 
 
@st.fragment(run_every=interval)
def dashboard():
    now = datetime.now()
    hidden = set(st.session_state.get("hidden", []))
    window = WINDOWS[st.session_state.get("window", "5 menit")]
    center_me = st.session_state.get("center_me", True)
 
    with data["lock"]:
        connected = data["connected"]
        devices = {k: dict(v) for k, v in data["devices"].items()}
        hist = list(data["hist"])
        jarak_raw = list(data["jarak"])
        status_hp = {k: dict(v) for k, v in data["status_hp"].items()}
        urutan = list(data["urutan"])
        log_status = list(data["log_status"])
 
    umur = {k: (now - v["t"]).total_seconds() for k, v in devices.items()}
    aktif = [k for k in devices if umur[k] <= STALE_TAMPIL]
    vis_aktif = [k for k in aktif if k not in hidden]
    warna = peta_warna(urutan + sorted((set(devices) | {r["id"] for r in hist}) - set(urutan)))
 
    # HP fokus (sudut pandang)
    pilih = st.session_state.get("fokus", "Otomatis")
    if pilih in devices:
        fokus = pilih
    elif ME_ID in devices:
        fokus = ME_ID
    else:
        fokus = sorted(devices)[0] if devices else None
    me = devices.get(fokus) if fokus else None
    fokus_aktif = fokus in aktif if fokus else False
 
    # Status tiap HP. server.py mengirim status/<ME_ID>. Kalau sebuah HP belum punya status sendiri,
    # ia ikut status itu, karena getar.py di semua HP berlangganan ke topik status yang sama.
    def segar(sp):
        return sp is not None and (now - sp["t"]).total_seconds() <= STATUS_STALE
 
    sp_ref = status_hp.get(ME_ID) if segar(status_hp.get(ME_ID)) else None
    st_hp, sp_hp, bersama = {}, {}, {}
    for k in devices:
        own = status_hp.get(k)
        if segar(own):
            st_hp[k], sp_hp[k], bersama[k] = own["status"], own, False
        elif sp_ref is not None:
            st_hp[k], sp_hp[k], bersama[k] = sp_ref["status"], sp_ref, True
        else:
            st_hp[k], sp_hp[k], bersama[k] = None, None, False
 
    # situasi pasangan: penerima peringatan (kendaraan depan) dan pemicunya
    penerima_id = ME_ID if ME_ID in devices else fokus
    penerima = devices.get(penerima_id) if penerima_id else None
    sp_pair = status_hp.get(penerima_id) if penerima_id and segar(status_hp.get(penerima_id)) else None
    pemicu_id = sp_pair.get("pemicu") if sp_pair else None
    tren_ai = (sp_pair.get("tren") if sp_pair else None) or "-"
    tren_id = (sp_pair.get("tren_id") if sp_pair else None) or pemicu_id
    p_pemicu = devices.get(pemicu_id) if pemicu_id else None
    rem = None
    if penerima and p_pemicu and sp_pair:
        rem = selisih_kec(p_pemicu["speed"], penerima["speed"])
 
    n_bahaya = sum(1 for k in vis_aktif if st_hp.get(k) == "BAHAYA")
    n_hati = sum(1 for k in vis_aktif if st_hp.get(k) == "HATI-HATI")
 
    # notifikasi saat status sebuah HP berubah
    prev = st.session_state.setdefault("_last_status_hp", {})
    for k in vis_aktif:
        s_k = st_hp.get(k)
        if s_k and prev.get(k) != s_k:
            if prev.get(k) is not None:
                st.toast(f"{k}: {s_k}", icon=TONE[s_k]["ikon"])
            prev[k] = s_k
 
    # kendaraan terdekat dari HP fokus
    terdekat = None
    if me and fokus_aktif:
        for k in vis_aktif:
            if k == fokus:
                continue
            j = haversine(me["lat"], me["lon"], devices[k]["lat"], devices[k]["lon"])
            if terdekat is None or j < terdekat[1]:
                terdekat = (k, j, devices[k]["speed"])
 
    # ---- header ----
    dot_conn = PEACH if connected else RED
    teks_conn = "MQTT online" if connected else "MQTT offline"
    terakhir = max((v["t"] for v in devices.values()), default=None)
    pill_alarm = (f'<span class="dg-pill"><span class="dg-dot" style="background:{RED}"></span>'
                  f'{n_bahaya} HP BAHAYA</span>' if n_bahaya else
                  f'<span class="dg-pill"><span class="dg-dot" style="background:{TEAL_L}"></span>'
                  f'Tidak ada HP bahaya</span>')
    st.markdown(h(f"""
        <div class="dg-top">
          <div>
            <div class="dg-brand">DriveGuard</div>
            <div class="dg-sub">Pemantauan posisi, kecepatan, dan jarak kendaraan secara langsung</div>
          </div>
          <div class="dg-pills">
            <span class="dg-pill"><span class="dg-dot" style="background:{dot_conn}"></span>{teks_conn}</span>
            <span class="dg-pill">Fokus: {esc(fokus or "-")}</span>
            {pill_alarm}
            <span class="dg-pill">{"Live" if interval else "Dijeda"}</span>
          </div>
        </div>"""), unsafe_allow_html=True)
 
    # ---- kartu status: satu per HP ----
    def catatan(k, s):
        if s == "HATI-HATI":
            return (f"Anda mendekati {penerima_id}, kurangi kecepatan" if k == pemicu_id
                    else "Ada kendaraan mendekat dari belakang")
        if s == "BAHAYA":
            return (f"Rem sekarang, {penerima_id} terlalu dekat" if k == pemicu_id
                    else "Kendaraan di belakang mendekat cepat")
        return TONE.get(s, TONE_DEFAULT)["note"]
 
    ids_kartu = ([k for k in PHONE_IDS if k not in hidden]
                 + [k for k in sorted(devices) if k not in PHONE_IDS and k not in hidden])
    phones = ""
    for k in ids_kartu:
        v = devices.get(k)
        on = v is not None and k in aktif
        s_k = st_hp.get(k) if on else None
        if v is None:
            teks, sub = "MENUNGGU", "Belum ada data dari HP ini"
        elif not on:
            teks, sub = "TIDAK AKTIF", f"Data lebih dari {STALE_TAMPIL} detik"
        elif s_k is None:
            teks = "SERVER TIDAK MENGIRIM" if status_hp else "MENUNGGU DATA"
            sub = "Belum ada status terbaru dari server"
        else:
            teks, sub = s_k, catatan(k, s_k)
        tone = TONE.get(s_k, TONE_DEFAULT)
        kecil = "" if s_k else " kecil"
        bahaya_cls = " danger" if s_k == "BAHAYA" else ""
 
        if on and s_k in ("HATI-HATI", "BAHAYA") and sp_hp.get(k) and sp_hp[k].get("pemicu"):
            jr = sp_hp[k].get("jarak")
            info = (f"Pemicu: <b>{esc(sp_hp[k]['pemicu'])}</b>"
                    + (f" &nbsp; {jr:.0f} m" if jr is not None else "")
                    + (f" &nbsp; selisih {rem:+.0f} km/jam" if rem is not None else "")
                    + (f" &nbsp; tren {TREN_IKON.get(tren_ai, esc(tren_ai))}" if tren_ai != "-" else ""))
        elif on:
            info = f"{v['speed']:.1f} km/jam &nbsp; data {umur[k]:.0f} dtk lalu"
        else:
            info = "&nbsp;"
 
        sumber = (f"Status {esc(k)} (ikut {esc(ME_ID)})" if bersama.get(k) else f"Status {esc(k)} (dari server)")
        peran_t = PERAN.get(k, "HP lain") + (" &middot; pemicu" if k == pemicu_id else "")
        fokus_t = " &#9678;" if k == fokus else ""
        svg = gauge_svg(v["speed"] if on else None, STATUS_WARNA.get(s_k, TEAL_L))
        vib = VIBRASI.get(s_k, "-")
        phones += (
            f'<div class="dg-phone{bahaya_cls}" style="background:{tone["bg"]};color:{tone["fg"]};">'
            f'<div class="dg-phone-top"><span class="dg-phone-name">{esc(k)}{fokus_t}</span>'
            f'<span class="dg-role">{peran_t}</span></div>'
            f'<div class="dg-hero-label">{sumber}</div>'
            f'<div class="dg-phone-status{kecil}">{esc(teks)}</div>'
            f'<div class="dg-hero-note">{sub}</div>'
            f'<div class="dg-hero-near">{info}</div>'
            f'<div class="dg-phone-gauge">{svg}<div class="z">km/jam</div></div>'
            f'<div class="dg-vib">Getaran: {vib}</div>'
            f'</div>')
    if phones:
        st.markdown(f'<div class="dg-duo">{phones}</div>', unsafe_allow_html=True)
    else:
        kosong("Semua HP disembunyikan.")
 
    # ---- jarak antar HP + batas aturan ----
    if terdekat:
        pos = min(terdekat[1] / (2 * RADIUS_M), 1) * 100
        prox = (f'<div class="dg-prox" style="color:{TEAL_L}"><div class="dg-track"><span class="dg-ring" style="left:50%"></span>'
                f'<span class="dg-me" style="left:{pos:.1f}%"></span></div>'
                f'<div class="dg-prox-l"><span>0 m</span><span>Radius deteksi {RADIUS_M} m</span>'
                f'<span>{2 * RADIUS_M} m</span></div></div>')
        judul_prox = f"Jarak {esc(fokus)} ke {esc(terdekat[0])}: <b>{terdekat[1]:.0f} m</b>"
    else:
        prox = ""
        judul_prox = "Belum ada pasangan HP yang aktif"
    st.markdown(h(f"""
        <div class="dg-card" style="margin-top:14px;">
          <div class="dg-k-label" style="color:{INK};font-size:.95rem;">{judul_prox}</div>
          {prox}
          <div class="dg-limits" style="color:{SOFT};">
            <span>Hati-hati: lebih cepat &ge; {REL_HATI:g} km/jam (atau &ge; {REL_NAIK:g} kalau tren NAIK), jarak &le; {RADIUS_M:g} m</span>
            <span>Bahaya: jarak &le; {JARAK_BAHAYA:g} m dan lebih cepat &ge; {REL_BAHAYA:g} km/jam (atau &ge; {REL_HATI:g} kalau tren NAIK)</span>
            <span>Tren TURUN: tidak HATI-HATI kalau jarak &gt; {JARAK_BAHAYA:g} m</span>
          </div>
        </div>"""), unsafe_allow_html=True)
 
    # ---- KPI ----
    st.write("")
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("Jarak ke terdekat", f"{terdekat[1]:.0f} m" if terdekat else "-",
                    esc(terdekat[0]) if terdekat else ""), unsafe_allow_html=True)
    k2.markdown(kpi("Kecepatan relatif pemicu", f"{rem:+.0f} km/jam" if rem is not None else "-",
                    f"{esc(pemicu_id)} vs {esc(penerima_id)}"
                    if (rem is not None and p_pemicu and penerima) else "tidak ada pemicu"), unsafe_allow_html=True)
    k3.markdown(kpi("Tren kecepatan pemicu (AI)", TREN_IKON.get(tren_ai, "-"),
                    f"prediksi 1-10 dtk &middot; {esc(tren_id)}" if tren_id and tren_ai != "-" else "menunggu data AI"),
                unsafe_allow_html=True)
    k4.markdown(kpi("Data terakhir", terakhir.strftime("%H:%M:%S") if terakhir else "--:--:--",
                    f"{(now - terakhir).total_seconds():.0f} dtk lalu" if terakhir else ""),
                unsafe_allow_html=True)
 
    # ---- tab ----
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Kecepatan", "Jarak", "Akselerometer", "Peta", "Data dan log"])
 
    with tab1:
        df = to_df(hist, "speed", window, hidden, now)
        if df is not None:
            st.altair_chart(grafik(df, "km/jam", warna))
            st.caption("Status ditentukan dari selisih kecepatan dan jarak, bukan kecepatan absolut. "
                       "Geser dan zoom dengan mouse.")
        else:
            kosong("Menunggu data kecepatan...")
 
    with tab2:
        rows_j = [{"waktu": r["waktu"], "id": r["b"] if r["a"] == fokus else r["a"],
                   "jarak": r["jarak"]}
                  for r in jarak_raw if fokus and fokus in (r["a"], r["b"])]
        df = to_df(rows_j, "jarak", window, hidden, now)
        if df is not None:
            st.altair_chart(grafik(df, "meter", warna, [(RADIUS_M, RED)]))
            st.caption(f"Jarak {fokus} ke HP lain. Garis merah menandai radius deteksi {RADIUS_M} m.")
        else:
            kosong("Menunggu data jarak. Dibutuhkan HP fokus dan minimal satu HP lain.")
 
    with tab3:
        df = to_df(hist, "acc_dyn", window, hidden, now)
        if df is not None:
            st.altair_chart(grafik(df, "m/s²", warna))
            st.caption("Percepatan dinamis (HP asli lemah dan berisik). Nilai rendah saat speed GPS melonjak "
                       "berarti lonjakan itu dianggap noise GPS.")
        else:
            kosong("Menunggu data akselerometer...")
 
    with tab4:
        pts = [{
            "id": k, "lat": v["lat"], "lon": v["lon"], "speed": round(v["speed"], 1),
            "umur": round(umur[k]),
            "status": st_hp.get(k) or "-",
            "color": hex_rgb(warna[k], 255 if k in aktif else 90),
            "line": hex_rgb(STATUS_WARNA.get(st_hp.get(k), "#FFFFFF")),
        } for k, v in devices.items() if k not in hidden]
        if pts:
            if center_me and me:
                lat0, lon0 = me["lat"], me["lon"]
            else:
                lat0 = sum(p["lat"] for p in pts) / len(pts)
                lon0 = sum(p["lon"] for p in pts) / len(pts)
            layers = []
            if me and fokus not in hidden:
                layers.append(pdk.Layer(
                    "ScatterplotLayer", data=[{"lat": me["lat"], "lon": me["lon"]}],
                    get_position="[lon, lat]", get_radius=RADIUS_M, radius_units="meters",
                    get_fill_color=hex_rgb(RED, 28), get_line_color=hex_rgb(RED, 200),
                    stroked=True, filled=True, line_width_min_pixels=2, pickable=False))
            layers.append(pdk.Layer(
                "ScatterplotLayer", data=pts, get_position="[lon, lat]", get_radius=4,
                radius_units="meters", radius_min_pixels=7, get_fill_color="color",
                get_line_color="line", stroked=True, line_width_min_pixels=3, pickable=True))
            layers.append(pdk.Layer(
                "TextLayer", data=pts, get_position="[lon, lat]", get_text="id", get_size=14,
                get_color=hex_rgb(INK), get_pixel_offset=[0, -20], pickable=False))
            st.pydeck_chart(pdk.Deck(
                layers=layers,
                initial_view_state=pdk.ViewState(latitude=lat0, longitude=lon0, zoom=17, pitch=0),
                map_style="dark",
                tooltip={"html": "<b>{id}</b><br/>{speed} km/jam<br/>Status: {status}<br/>{umur} dtk lalu",
                         "style": {"backgroundColor": TEAL, "color": "#F5F0EA"}},
            ))
            st.caption(f"Lingkaran merah: radius deteksi {RADIUS_M} m dari {fokus}. "
                       "Garis tepi titik = status HP itu. "
                       "Matikan Live update di sidebar agar peta bisa digeser tanpa ter-reset.")
        else:
            kosong("Belum ada HP yang mengirim posisi.")
 
    with tab5:
        rows = [{
            "HP": k,
            "status": st_hp.get(k) or ("pemicu" if k == pemicu_id else "-"),
            "lat": round(v["lat"], 6),
            "lon": round(v["lon"], 6),
            "speed (km/jam)": round(v["speed"], 1),
            "akurasi GPS (m)": v["acc"],
            "acc_dyn (m/s²)": v["acc_dyn"],
            "umur data (dtk)": round(umur[k], 1),
        } for k, v in sorted(devices.items()) if k not in hidden]
        if rows:
            st.dataframe(
                pd.DataFrame(rows), hide_index=True,
                column_config={"speed (km/jam)": st.column_config.ProgressColumn(
                    "speed (km/jam)", min_value=0, max_value=100, format="%.1f")},
            )
        else:
            kosong("Belum ada HP yang mengirim data.")
        st.markdown("**Riwayat perubahan status**")
        if log_status:
            st.dataframe(pd.DataFrame(log_status), hide_index=True)
        else:
            st.caption("Belum ada perubahan status.")
 
    st.caption(f"Titik riwayat tersimpan: {len(hist)}")
 
 
dashboard()