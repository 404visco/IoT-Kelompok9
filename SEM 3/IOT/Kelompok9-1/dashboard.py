import json
import math
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
BROKER = "broker.hivemq.com"
PORT = 1883
PREFIX = "driveguard/kelompok9"          # harus sama di semua file
TOPIC_POS = f"{PREFIX}/pos/+"
TOPIC_STATUS = f"{PREFIX}/status"
POS_PREFIX = f"{PREFIX}/pos/"

ME_ID = "hp_saya"                        # sama dengan ME_ID di server.py
RADIUS_M = 30                            # hanya untuk tampilan; samakan dengan server.py
BATAS_AMAN = 45
BATAS_BAHAYA = 65
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

WARNA_LINE = [TEAL_L, TAUPE, "#9DB8C2", "#B58B7A", "#7E8F96"]   # warna garis untuk HP selain ME_ID

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
        "jarak": deque(maxlen=400),      # riwayat jarak hp_saya -> HP lain
        "status": None,
        "status_t": None,
        "log_status": deque(maxlen=20),  # perubahan status terbaru di depan
    }


data = get_data()


# ===== MQTT (tidak diubah) =====
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

            if msg.topic == TOPIC_STATUS:
                status = payload["status"]
                with data["lock"]:
                    if status != data["status"]:
                        data["log_status"].appendleft(
                            {"waktu": now.strftime("%H:%M:%S"), "status": status}
                        )
                    data["status"] = status
                    data["status_t"] = now

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
                    data["devices"][id_] = d
                    data["hist"].append({
                        "waktu": now, "id": id_,
                        "speed": d["speed"], "acc_dyn": d["acc_dyn"],
                    })
                    me = data["devices"].get(ME_ID)
                    if me:
                        if id_ != ME_ID:
                            targets = [id_]
                        else:
                            targets = [k for k in data["devices"] if k != ME_ID]
                        for k in targets:
                            o = data["devices"][k]
                            data["jarak"].append({
                                "waktu": now, "id": k,
                                "jarak": haversine(me["lat"], me["lon"], o["lat"], o["lon"]),
                            })

        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            print(f"[MQTT] Invalid message: {e}")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    return client


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
    st.multiselect("Sembunyikan HP", options=known_ids, key="hidden",
                   placeholder="Semua HP ditampilkan",
                   help="Daftar HP diperbarui setiap kali kamu mengubah kontrol.")
    st.toggle(f"Pusatkan peta ke {ME_ID}", value=True, key="center_me")

    st.divider()
    st.download_button(
        "Unduh riwayat (CSV)",
        data=pd.DataFrame(hist_snapshot).to_csv(index=False) if hist_snapshot else "",
        file_name=f"driveguard_riwayat_{datetime.now():%Y%m%d_%H%M%S}.csv",
        mime="text/csv",
        disabled=not hist_snapshot,
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


def peta_warna(ids):
    """Warna konsisten per HP: ME_ID selalu teal, sisanya bergilir."""
    out, i = {}, 0
    for k in sorted(ids):
        if k == ME_ID:
            out[k] = PEACH
        else:
            out[k] = WARNA_LINE[i % len(WARNA_LINE)]
            i += 1
    return out


def zona(v):
    if v <= BATAS_AMAN:
        return "AMAN", TEAL_L
    if v <= BATAS_BAHAYA:
        return "HATI-HATI", PEACH
    return "BAHAYA", RED


def kpi(label, value, sub=""):
    return h(f'<div class="dg-card"><div class="dg-k-label">{label}</div>'
             f'<div class="dg-k-val">{value}</div><div class="dg-k-sub">{sub or "&nbsp;"}</div></div>')


def kosong(teks):
    st.markdown(f'<div class="dg-empty">{teks}</div>', unsafe_allow_html=True)


def gauge_svg(v):
    vmax = max(100, math.ceil(max(v or 0, BATAS_BAHAYA * 1.5) / 10) * 10)
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

    parts = [arc(0, BATAS_AMAN, TEAL_L), arc(BATAS_AMAN, BATAS_BAHAYA, PEACH), arc(BATAS_BAHAYA, vmax, RED)]
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
        jarak_hist = list(data["jarak"])
        status = data["status"]
        status_t = data["status_t"]
        log_status = list(data["log_status"])

    umur = {k: (now - v["t"]).total_seconds() for k, v in devices.items()}
    aktif = [k for k in devices if umur[k] <= STALE_TAMPIL]
    warna = peta_warna(set(devices) | {r["id"] for r in hist})

    # status dari server (bukan dihitung ulang di dashboard)
    if status is None:
        status_tampil = "MENUNGGU DATA"
    elif status_t and (now - status_t).total_seconds() > STATUS_STALE:
        status_tampil = "SERVER TIDAK MENGIRIM"
    else:
        status_tampil = status

    # notifikasi saat status berubah
    prev = st.session_state.get("_last_status")
    if status_tampil != prev:
        if prev is not None and status_tampil in TONE:
            st.toast(f"Status berubah menjadi {status_tampil}", icon=TONE[status_tampil]["ikon"])
        st.session_state["_last_status"] = status_tampil

    # kendaraan terdekat dari ME_ID
    terdekat = None
    me = devices.get(ME_ID)
    if me and ME_ID in aktif:
        for k in aktif:
            if k == ME_ID or k in hidden:
                continue
            j = haversine(me["lat"], me["lon"], devices[k]["lat"], devices[k]["lon"])
            if terdekat is None or j < terdekat[1]:
                terdekat = (k, j, devices[k]["speed"])

    # ---- header ----
    dot_conn = PEACH if connected else RED
    teks_conn = "MQTT online" if connected else "MQTT offline"
    terakhir = max((v["t"] for v in devices.values()), default=None)
    st.markdown(h(f"""
        <div class="dg-top">
          <div>
            <div class="dg-brand">DriveGuard</div>
            <div class="dg-sub">Pemantauan posisi, kecepatan, dan jarak kendaraan secara langsung</div>
          </div>
          <div class="dg-pills">
            <span class="dg-pill"><span class="dg-dot" style="background:{dot_conn}"></span>{teks_conn}</span>
            <span class="dg-pill">Server: {esc(status_tampil)}</span>
            <span class="dg-pill">{"Live" if interval else "Dijeda"}</span>
          </div>
        </div>"""), unsafe_allow_html=True)

    # ---- hero + speedometer ----
    tone = TONE.get(status_tampil, TONE_DEFAULT)
    if me is None:
        ringkas = f"Menunggu data dari {esc(ME_ID)}..."
    elif ME_ID not in aktif:
        ringkas = f"Data {esc(ME_ID)} tidak aktif (lebih dari {STALE_TAMPIL} detik)"
    elif terdekat is None:
        ringkas = "Belum ada HP lain yang aktif"
    else:
        ringkas = (f"Terdekat: <b>{esc(terdekat[0])}</b> &nbsp; {terdekat[1]:.0f} m "
                   f"&nbsp; {terdekat[2]:.1f} km/jam")

    prox = ""
    if terdekat:
        pos = min(terdekat[1] / (2 * RADIUS_M), 1) * 100
        prox = (f'<div class="dg-prox"><div class="dg-track"><span class="dg-ring" style="left:50%"></span>'
                f'<span class="dg-me" style="left:{pos:.1f}%"></span></div>'
                f'<div class="dg-prox-l"><span>0 m</span><span>Radius deteksi {RADIUS_M} m</span>'
                f'<span>{2 * RADIUS_M} m</span></div></div>')

    col_hero, col_gauge = st.columns([1.75, 1])
    with col_hero:
        st.markdown(h(f"""
            <div class="dg-hero {'danger' if status_tampil == 'BAHAYA' else ''}"
                 style="background:{tone['bg']};color:{tone['fg']};">
              <div>
                <div class="dg-hero-label">Status dari server</div>
                <div class="dg-hero-status">{esc(status_tampil)}</div>
                <div class="dg-hero-note">{tone['note']}</div>
                <div class="dg-hero-near">{ringkas}</div>
                {prox}
              </div>
              <div class="dg-limits">
                <span>Aman sampai {BATAS_AMAN} km/jam</span>
                <span>Bahaya di atas {BATAS_BAHAYA} km/jam</span>
              </div>
            </div>"""), unsafe_allow_html=True)

    with col_gauge:
        if me and ME_ID in aktif:
            nama_zona, warna_zona = zona(me["speed"])
            zona_html = f'<div class="z" style="color:{warna_zona}">Zona {nama_zona.lower()}</div>'
            svg = gauge_svg(me["speed"])
        else:
            zona_html = f'<div class="z" style="color:{SOFT}">Belum ada data</div>'
            svg = gauge_svg(None)
        st.markdown(h(f"""
            <div class="dg-card dg-gauge">
              <div class="t">Kecepatan {esc(ME_ID)} (km/jam)</div>
              {svg}
              {zona_html}
            </div>"""), unsafe_allow_html=True)

    # ---- KPI ----
    st.write("")
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi("Jarak ke terdekat", f"{terdekat[1]:.0f} m" if terdekat else "-",
                    esc(terdekat[0]) if terdekat else ""), unsafe_allow_html=True)
    k2.markdown(kpi("Kecepatan terdekat", f"{terdekat[2]:.1f} km/jam" if terdekat else "-",
                    esc(terdekat[0]) if terdekat else ""), unsafe_allow_html=True)
    k3.markdown(kpi("HP aktif", f"{len(aktif)} / {len(devices)}",
                    f"Aktif jika data kurang dari {STALE_TAMPIL} dtk"), unsafe_allow_html=True)
    k4.markdown(kpi("Data terakhir", terakhir.strftime("%H:%M:%S") if terakhir else "--:--:--",
                    f"{(now - terakhir).total_seconds():.0f} dtk lalu" if terakhir else ""),
                unsafe_allow_html=True)

    # ---- chip perangkat ----
    chips = ""
    for k in sorted(devices):
        if k in hidden:
            continue
        v = devices[k]
        on = k in aktif
        chips += (f'<div class="dg-chip{"" if on else " off"}">'
                  f'<span class="dg-dot" style="background:{warna[k] if on else TAUPE}"></span>'
                  f'<b>{esc(k)}</b><span class="m">{v["speed"]:.1f} km/jam</span>'
                  f'<span class="m">{umur[k]:.0f} dtk lalu</span></div>')
    if chips:
        st.markdown(f'<div class="dg-chips">{chips}</div>', unsafe_allow_html=True)

    # ---- tab ----
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Kecepatan", "Jarak", "Akselerometer", "Peta", "Data dan log"])

    with tab1:
        df = to_df(hist, "speed", window, hidden, now)
        if df is not None:
            st.altair_chart(
                grafik(df, "km/jam", warna, [(BATAS_AMAN, "#C98A6E"), (BATAS_BAHAYA, RED)]))
            st.caption(f"Garis putus-putus: batas hati-hati {BATAS_AMAN} km/jam (cokelat), "
                       f"batas bahaya {BATAS_BAHAYA} km/jam (merah). Geser dan zoom dengan mouse.")
        else:
            kosong("Menunggu data kecepatan...")

    with tab2:
        df = to_df(jarak_hist, "jarak", window, hidden, now)
        if df is not None:
            st.altair_chart(grafik(df, "meter", warna, [(RADIUS_M, RED)]))
            st.caption(f"Jarak {ME_ID} ke HP lain. Garis merah menandai radius deteksi {RADIUS_M} m.")
        else:
            kosong(f"Menunggu data jarak. Dibutuhkan {esc(ME_ID)} dan minimal satu HP lain.")

    with tab3:
        df = to_df(hist, "acc_dyn", window, hidden, now)
        if df is not None:
            st.altair_chart(grafik(df, "m/s²", warna))
            st.caption("Percepatan dinamis. Nilai rendah saat speed GPS melonjak "
                       "berarti lonjakan itu dianggap noise GPS.")
        else:
            kosong("Menunggu data akselerometer...")

    with tab4:
        pts = [{
            "id": k, "lat": v["lat"], "lon": v["lon"], "speed": round(v["speed"], 1),
            "umur": round(umur[k]),
            "color": hex_rgb(warna[k], 255 if k in aktif else 90),
        } for k, v in devices.items() if k not in hidden]
        if pts:
            if center_me and me:
                lat0, lon0 = me["lat"], me["lon"]
            else:
                lat0 = sum(p["lat"] for p in pts) / len(pts)
                lon0 = sum(p["lon"] for p in pts) / len(pts)
            layers = []
            if me and ME_ID not in hidden:
                layers.append(pdk.Layer(
                    "ScatterplotLayer", data=[{"lat": me["lat"], "lon": me["lon"]}],
                    get_position="[lon, lat]", get_radius=RADIUS_M, radius_units="meters",
                    get_fill_color=hex_rgb(RED, 28), get_line_color=hex_rgb(RED, 200),
                    stroked=True, filled=True, line_width_min_pixels=2, pickable=False))
            layers.append(pdk.Layer(
                "ScatterplotLayer", data=pts, get_position="[lon, lat]", get_radius=4,
                radius_units="meters", radius_min_pixels=7, get_fill_color="color",
                get_line_color=[255, 255, 255, 255], stroked=True, line_width_min_pixels=2, pickable=True))
            layers.append(pdk.Layer(
                "TextLayer", data=pts, get_position="[lon, lat]", get_text="id", get_size=14,
                get_color=hex_rgb(INK), get_pixel_offset=[0, -20], pickable=False))
            st.pydeck_chart(pdk.Deck(
                layers=layers,
                initial_view_state=pdk.ViewState(latitude=lat0, longitude=lon0, zoom=17, pitch=0),
                map_style="dark",
                tooltip={"html": "<b>{id}</b><br/>{speed} km/jam<br/>{umur} dtk lalu",
                         "style": {"backgroundColor": TEAL, "color": "#F5F0EA"}},
            ))
            st.caption(f"Lingkaran merah: radius deteksi {RADIUS_M} m dari {ME_ID}. "
                       "Matikan Live update di sidebar agar peta bisa digeser tanpa ter-reset.")
        else:
            kosong("Belum ada HP yang mengirim posisi.")

    with tab5:
        rows = [{
            "HP": k,
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
                    "speed (km/jam)", min_value=0, max_value=max(100, BATAS_BAHAYA * 1.5), format="%.1f")},
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
