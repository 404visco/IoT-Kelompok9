import json, time, math, os, sys
from collections import deque
import paho.mqtt.client as mqtt

# [AI] folder tempat ai_tren.py berada. Kalau ai_tren.py sefolder dengan server.py, baris ini boleh dihapus.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "AI"))
try:
    from tren_ai import PrediksiTren, tren_satu_kata
except ImportError as e:
    PrediksiTren = None
    print("[AI] ai_tren.py tidak ditemukan, server jalan tanpa AI:", e)

# ================= KONFIGURASI BROKER (EMQX Cloud) =================
MQTT_HOST = "ve168e89.ala.asia-southeast1.emqxsl.com"
MQTT_PORT = 8883
MQTT_USER = "kelompok9-idiot"        # <-- ISI SENDIRI (Access Control > Authentication di EMQX)
MQTT_PASS = "fuckcollege#67"        # <-- ISI SENDIRI
CA_FILE = "emqxsl-ca.crt"         # file CA hasil unduhan EMQX, taruh sefolder dengan file ini

# ================= KONFIGURASI =================
PREFIX = "driveguard/kelompok9"   # samakan di server.py, sender.py, getar.py, simulasi.py
TOPIK_POS = f"{PREFIX}/pos/+"
TOPIK_STATUS = f"{PREFIX}/status"
 
# HP yang DIBERI PERINGATAN = kendaraan DEPAN. HP lain (kendaraan belakang yang mendekat) = pemicu.
# Di sim_hp.py kendaraan depan adalah hp2.
ME_ID = "hp2"
RADIUS_M = 30            # m: di luar jarak ini selalu AMAN
STALE_DETIK = 5          # data lebih tua dari ini diabaikan (sender pakai -r once, ~1-4 detik/data)
MAX_ACC_M = 25           # abaikan data GPS dengan akurasi lebih buruk dari ini (m)
TAHAN_BAHAYA = 5         # detik BAHAYA ditahan setelah kondisi hilang
LONJAKAN_KMH = 25        # selisih speed antar sampel yang dicurigai noise
ACC_MIN = 0.8            # m/s^2, di bawah ini dianggap tidak ada percepatan
MAX_TOLAK = 3            # maksimal penolakan lonjakan beruntun
 
# ---------- ATURAN STATUS (sederhana) ----------
# kec_relatif = kecepatan pemicu (hp1) - kecepatan hp2, dalam km/jam. Positif = pemicu lebih cepat (mendekat).
REL_HATI = 10            # km/jam: selisih kecepatan untuk HATI-HATI
REL_BAHAYA = 20          # km/jam: selisih kecepatan untuk BAHAYA
REL_NAIK = 6             # km/jam: selisih kecepatan untuk HATI-HATI kalau tren AI = NAIK
JARAK_BAHAYA = 20        # m
PAKAI_AI = True          # [AI] False = tanpa AI (tren diabaikan)
 
# Dua HP mengirim pada waktu berbeda (selisih bisa 2-4 detik). Posisi terakhir keduanya diperkirakan
# ke waktu SEKARANG supaya jarak dihitung pada saat yang sama (pada 15 m/s, selisih 3 detik = salah 45 m).
EKSTRAPOLASI = True
MAX_EKSTRAPOLASI = 6.0   # detik: batas maksimal memproyeksikan posisi ke depan
 
# ================= STATE =================
posisi = {}              # id -> data terakhir (+ waktu terima "t")
prev_speed = {}          # id -> speed terfilter terakhir
fix = {}                 # id -> 2 titik posisi terakhir (waktu terima, lat, lon), untuk arah gerak
tolak = {}               # id -> jumlah penolakan lonjakan beruntun
status_sekarang = "AMAN"
waktu_keluar_bahaya = None
 
ai = None                # [AI] diisi oleh siapkan_ai()
tren_hp = {}             # [AI] id -> tren terakhir ("NAIK" / "STABIL" / "TURUN" / "-")
 
# [LOG] file log, dibuka di main() saja (supaya tidak terbuat saat file ini di-import)
log_pos = None
log_status = None
 
URUTAN = {"AMAN": 0, "HATI-HATI": 1, "BAHAYA": 2}
NAMA_STATUS = ["AMAN", "HATI-HATI", "BAHAYA"]
 
 
def siapkan_ai():
    """[AI] Muat model. Kalau gagal, server tetap jalan dengan aturan lama."""
    global ai
    ai = None
    if not PAKAI_AI or PrediksiTren is None:
        return
    try:
        ai = PrediksiTren()
        print("[AI] Model tren kecepatan dimuat.")
    except Exception as e:
        print("[AI] Model belum ada / gagal dimuat, server jalan tanpa AI:", e)
 
 
def reset_state():
    global status_sekarang, waktu_keluar_bahaya
    for d in (posisi, prev_speed, tolak, tren_hp, fix):
        d.clear()
    if ai:
        ai.reset()
    status_sekarang = "AMAN"
    waktu_keluar_bahaya = None
 
 
def buat_client():
    try:
        c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)   # paho-mqtt 2.x
    except AttributeError:
        c = mqtt.Client()                                   # paho-mqtt 1.x
    c.username_pw_set(MQTT_USER, MQTT_PASS)
    if os.path.exists(CA_FILE):
        c.tls_set(ca_certs=CA_FILE)
    else:
        c.tls_set()                                         # CA bawaan sistem
    return c
 
 
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))
 
 
def valid(p, sekarang):
    if sekarang - p["t"] > STALE_DETIK:
        return False
    if p.get("acc") is not None and p["acc"] > MAX_ACC_M:
        return False
    return True
 
 
def tentukan_status(kec_relatif, jarak, tren="STABIL"):
    """kec_relatif: km/jam (pemicu - hp2) | jarak: meter | tren: "NAIK" / "STABIL" / "TURUN"."""
    naik = (tren == "NAIK")
    turun = (tren == "TURUN")
 
    # BAHAYA: dekat dan jauh lebih cepat, ATAU dekat dan lebih cepat dan AI bilang makin ngebut
    if jarak <= JARAK_BAHAYA and (kec_relatif >= REL_BAHAYA or (naik and kec_relatif >= REL_HATI)):
        return "BAHAYA"
 
    # HATI-HATI: dalam radius dan lebih cepat (kecuali AI bilang melambat dan masih agak jauh),
    # ATAU AI bilang makin ngebut walau selisihnya masih kecil
    if jarak <= RADIUS_M and ((kec_relatif >= REL_HATI and (not turun or jarak <= JARAK_BAHAYA))
                              or (naik and kec_relatif >= REL_NAIK)):
        return "HATI-HATI"
 
    return "AMAN"
 
 
def proses_data(data):
    """Terima satu paket posisi dari sebuah HP, saring lonjakan GPS palsu, simpan."""
    id_ = data["id"]
    v = float(data["speed_kmh"])
    acc = data.get("acc_dyn")
 
    v_lama = prev_speed.get(id_)
    # hanya lonjakan NAIK yang dicurigai (penyebab alarm palsu). Penurunan selalu diterima,
    # supaya filter tidak "terkunci" di nilai tinggi palsu.
    spike = (v_lama is not None and acc is not None
             and (v - v_lama) > LONJAKAN_KMH and acc < ACC_MIN)
    if spike and tolak.get(id_, 0) < MAX_TOLAK:
        tolak[id_] = tolak.get(id_, 0) + 1
        print(f"[{id_}] lonjakan {v_lama:.0f}->{v:.0f} km/j diabaikan (akselerometer diam)")
        v = v_lama
    else:
        tolak[id_] = 0
    prev_speed[id_] = v
 
    data["speed_kmh"] = v
    data["t"] = time.time()          # pakai waktu terima server
    posisi[id_] = data
    fix.setdefault(id_, deque(maxlen=2)).append((data["t"], data["lat"], data["lon"]))
 
 
def posisi_perkiraan(id_, T):
    """Perkirakan posisi HP `id_` pada waktu T: posisi terakhir + kecepatan x selisih waktu,
    searah gerak dari dua titik terakhir. Hampir diam / belum ada arah -> pakai posisi terakhir."""
    p = posisi[id_]
    lat, lon = p["lat"], p["lon"]
    dt = min(max(T - p["t"], 0.0), MAX_EKSTRAPOLASI)
    h = fix.get(id_)
    if not EKSTRAPOLASI or dt <= 0 or not h or len(h) < 2:
        return lat, lon
    (_, lat_a, lon_a), (_, lat_b, lon_b) = h
    dy = (lat_b - lat_a) * 111320.0
    dx = (lon_b - lon_a) * 111320.0 * math.cos(math.radians(lat_b))
    n = math.hypot(dx, dy)
    if n < 2.0:                                  # perpindahan kecil = diam atau noise GPS
        return lat, lon
    jarak_tempuh = p["speed_kmh"] / 3.6 * dt
    return (lat + dy / n * jarak_tempuh / 111320.0,
            lon + dx / n * jarak_tempuh / (111320.0 * math.cos(math.radians(lat))))
 
 
def evaluasi():
    sekarang = time.time()
    me = posisi.get(ME_ID)
    if not me or not valid(me, sekarang):
        return "AMAN", None, None
 
    terburuk, jarak_terburuk, id_terburuk = "AMAN", None, None
 
    for id_, p in list(posisi.items()):
        if id_ == ME_ID:
            continue
        if not valid(p, sekarang):
            for d in (prev_speed, tolak, tren_hp, fix):
                d.pop(id_, None)      # data basi/buruk: reset riwayat
            continue
 
        la_me, lo_me = posisi_perkiraan(ME_ID, sekarang)
        la_p, lo_p = posisi_perkiraan(id_, sekarang)
        jarak = haversine(la_me, lo_me, la_p, lo_p)
 
        # [AI] (dijalankan untuk semua HP aktif, bukan hanya pemicu) prediksi tren kecepatan pemicu (1/3/5/10 detik ke depan) jadi satu kata
        tren = "STABIL"
        tren_hp[id_] = "-"
        if ai:
            try:
                pred = ai.prediksi(id_, ME_ID)
                if pred:
                    tren = tren_satu_kata(pred)
                    tren_hp[id_] = tren
            except Exception as e:
                print("[AI] error prediksi:", e)
 
        kec_relatif = p["speed_kmh"] - me["speed_kmh"]
        s = tentukan_status(kec_relatif, jarak, tren)
        if URUTAN[s] > URUTAN[terburuk]:
            terburuk, jarak_terburuk, id_terburuk = s, jarak, id_
 
    return terburuk, jarak_terburuk, id_terburuk
 
 
def tahan_bahaya(status_baru):
    """Pertahankan BAHAYA selama TAHAN_BAHAYA detik setelah kondisi hilang."""
    global status_sekarang, waktu_keluar_bahaya
    sekarang = time.time()
    if status_baru == "BAHAYA":
        status_sekarang = "BAHAYA"
        waktu_keluar_bahaya = None
    elif status_sekarang == "BAHAYA":
        if waktu_keluar_bahaya is None:
            waktu_keluar_bahaya = sekarang
        if sekarang - waktu_keluar_bahaya >= TAHAN_BAHAYA:
            status_sekarang = status_baru
            waktu_keluar_bahaya = None
    else:
        status_sekarang = status_baru
 
 
def langkah():
    """Satu siklus: evaluasi + penahanan. Mengembalikan (status, jarak, id_hp_pemicu)."""
    status_baru, jarak, id_ = evaluasi()
    tahan_bahaya(status_baru)
    return status_sekarang, jarak, id_
 
 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Server siap! Terhubung ke EMQX.")
        client.subscribe(TOPIK_POS)
    else:
        print(f"GAGAL terhubung, rc={rc} (4/5 biasanya username/password salah)")
 
 
def on_message(client, userdata, msg):
    try:
        t_recv = time.time()
        data = json.loads(msg.payload.decode())
        if log_pos:                                   # [LOG] catat data mentah SEBELUM difilter
            log_pos.write(json.dumps({"t_recv": t_recv, **data}) + "\n")
        proses_data(data)
        if ai:                                        # [AI] beri data ke model tren
            ai.update({**data, "t_recv": t_recv})
    except Exception as e:
        print("Payload error:", e)
 
 
def main():
    global log_pos, log_status
    os.makedirs("logs", exist_ok=True)                # [LOG]
    stamp = time.strftime("%Y%m%d_%H%M%S")
    log_pos = open(f"logs/pos_{stamp}.jsonl", "a", buffering=1)
    log_status = open(f"logs/status_{stamp}.jsonl", "a", buffering=1)
 
    siapkan_ai()                                      # [AI]
 
    client = buat_client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
 
    while True:
        status, jarak, id_ = langkah()
        id_tren = id_
        if not id_tren:                               # tidak ada pemicu: tetap kirim tren HP lain terdekat
            lain = [k for k in tren_hp if k != ME_ID and tren_hp.get(k) not in (None, "-")]
            id_tren = lain[0] if lain else None
        tren = tren_hp.get(id_tren, "-") if id_tren else "-"
        ket = f" | {id_} @ {jarak:.0f} m | tren {tren}" if id_ else ""
        print(f"Status: {status}{ket}")
        log_status.write(json.dumps({"t": time.time(), "status": status,   # [LOG]
                                     "jarak": jarak, "pemicu": id_, "tren": tren, "tren_id": id_tren}) + "\n")
        client.publish(TOPIK_STATUS, json.dumps({"status": status}))       # untuk getar.py
        client.publish(f"{TOPIK_STATUS}/{ME_ID}",                          # untuk dashboard.py
                       json.dumps({"status": status, "jarak": jarak, "pemicu": id_,
                                   "tren": tren, "tren_id": id_tren}))
        time.sleep(1)
 
 
if __name__ == "__main__":
    main() 