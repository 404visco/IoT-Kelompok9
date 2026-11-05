"""
ai_tren.py - AI prediksi TREN KECEPATAN (turun / stabil / naik) pada 1, 3, 5, dan 10 detik ke depan,
plus aturan untuk menggabungkannya dengan status AMAN / HATI-HATI / BAHAYA.

Satu file, tiga kegunaan:
  python ai_tren.py latih [folder]        # bangun dataset + latih + evaluasi (default: data_sintetis)
  python ai_tren.py demo file.jsonl       # putar ulang satu sesi seperti sistem live, ukur akurasinya
  from ai_tren import PrediksiTren, gabung_status     # dipakai di server.py
"""
import glob, json, os, sys, threading
from collections import defaultdict, deque

import joblib
import numpy as np
import pandas as pd

# ===================== PENGATURAN =====================
ID_A, ID_B = "hp2", "hp1"          # hp2 = depan, hp1 = belakang (dipakai saat melatih)
HORIZONS = [1, 3, 5, 10]           # detik ke depan
WIN = 10                           # jendela riwayat (detik)
# "Stabil" jika perubahan kecepatan masih di dalam +/- TAU (m/s). 1 m/s = 3,6 km/jam.
TAU = {1: 0.8, 3: 1.2, 5: 1.5, 10: 2.0}
KELAS = ["turun", "stabil", "naik"]
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models_tren", "tren.joblib")

# Satu kata tren (NAIK / STABIL / TURUN) dari gabungan 4 horizon:
BOBOT = {1: 0.15, 3: 0.30, 5: 0.30, 10: 0.25}
AMBANG_TREN = 0.35                 # skor >= +ambang -> NAIK, <= -ambang -> TURUN, selain itu STABIL

# Aturan status sederhana (nilai awal, sesuaikan dengan server.py):
URUT = ["AMAN", "HATI-HATI", "BAHAYA"]
BATAS_AMAN = 45                    # km/jam: di atas ini mulai HATI-HATI
BATAS_BAHAYA = 65                  # km/jam: di atas ini BAHAYA
RADIUS_M = 30                      # hanya HP dalam radius ini yang dianggap ancaman
BATAS_TREN = 30                    # km/jam: tren NAIK baru dihitung kalau sudah secepat ini
JARAK_DEKAT = 15                   # meter: sedekat ini, tren TURUN tidak menurunkan status
# =======================================================

SERI = ["v", "acc", "vo", "dist", "rel", "tunda"]   # v = kecepatan HP yang diprediksi, vo = HP lain


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    a = (np.sin((p2 - p1) / 2) ** 2
         + np.cos(p1) * np.cos(p2) * np.sin(np.radians(lon2 - lon1) / 2) ** 2)
    return 2 * R * np.arcsin(np.sqrt(a))


# ---------- pengolahan data (dipakai bersama oleh pelatihan DAN server) ----------
def siapkan(df):
    """Pesan mentah (format log) -> kolom standar. Satuan kecepatan jadi m/s."""
    df = df.copy()
    if "t_send" not in df:
        df["t_send"] = df["t_recv"]
    df["t_send"] = df["t_send"].fillna(df["t_recv"])
    df["speed"] = df["speed_kmh"].astype(float) / 3.6
    df["acc"] = df["acc_dyn"].astype(float)
    df["latency"] = df["t_recv"] - df["t_send"]
    return df


def ke_1hz(df):
    """Satu baris per detik; lubang sampai 3 detik ditambal linear."""
    df = df.copy()
    df["sec"] = df["t_send"].round().astype(int)
    g = df.groupby("sec").agg(lat=("lat", "last"), lon=("lon", "last"),
                              speed=("speed", "last"), acc=("acc", "max"),
                              latency=("latency", "max"))
    g = g.reindex(range(g.index.min(), g.index.max() + 1))
    return g.interpolate(limit=3)


def pasangan(e, o):
    """Gabungkan HP yang diprediksi (e) dan HP lain (o). rel > 0: e lebih cepat dari o."""
    d = e.join(o, lsuffix="_e", rsuffix="_o", how="inner")
    return pd.DataFrame({
        "v": d.speed_e, "acc": d.acc_e, "vo": d.speed_o,
        "dist": haversine(d.lat_e, d.lon_e, d.lat_o, d.lon_o),
        "rel": d.speed_e - d.speed_o,
        "tunda": d[["latency_e", "latency_o"]].max(axis=1),
    })


def fitur_window(w):
    """w: array (WIN, len(SERI)) -> ringkasan angka (rata-rata, tren, dst)."""
    t = np.arange(len(w)) - (len(w) - 1) / 2.0
    st = (t ** 2).sum()
    f = {}
    for j, nama in enumerate(SERI):
        x = w[:, j]
        f[f"{nama}_last"] = x[-1]
        f[f"{nama}_mean"] = x.mean()
        f[f"{nama}_std"] = x.std()
        f[f"{nama}_min"] = x.min()
        f[f"{nama}_max"] = x.max()
        f[f"{nama}_slope"] = float((t * (x - x.mean())).sum() / st)
    return f


FITUR = list(fitur_window(np.zeros((WIN, len(SERI)))).keys())


def label_tren(v, i, h):
    """0 turun, 1 stabil, 2 naik. Dibanding kecepatan sekarang, dirata-ratakan 2 titik agar tahan noise."""
    a, b = v[i - 1:i + 1], v[i + h - 1:i + h + 1]
    if len(a) < 2 or len(b) < 2 or np.isnan(a).any() or np.isnan(b).any():
        return np.nan
    d = b.mean() - a.mean()
    return 0 if d < -TAU[h] else (2 if d > TAU[h] else 1)


# ---------- dataset dan pelatihan ----------
def bangun_dataset(folder):
    rows, files = [], sorted(glob.glob(os.path.join(folder, "pos_*.jsonl")))
    for path in files:
        raw = pd.read_json(path, lines=True)
        if raw.empty:
            continue
        raw = siapkan(raw)
        A, B = raw[raw.id == ID_A], raw[raw.id == ID_B]
        if len(A) < 5 or len(B) < 5:
            continue
        a1, b1 = ke_1hz(A), ke_1hz(B)
        for hp, e, o in ((ID_A, a1, b1), (ID_B, b1, a1)):    # tiap HP jadi "yang diprediksi"
            d = pasangan(e, o)
            M, v = d.to_numpy(), d["v"].to_numpy()
            for i in range(WIN - 1, len(d) - max(HORIZONS)):
                w = M[i - WIN + 1:i + 1]
                if np.isnan(w).any():
                    continue
                row = {"session": os.path.basename(path), "hp": hp, **fitur_window(w)}
                for h in HORIZONS:
                    row[f"y_{h}"] = label_tren(v, i, h)
                rows.append(row)
    return pd.DataFrame(rows), len(files)


def latih(folder="data_sintetis"):
    from lightgbm import LGBMClassifier
    from sklearn.metrics import accuracy_score, f1_score, recall_score
    from sklearn.model_selection import GroupKFold

    df, n_file = bangun_dataset(folder)
    print(f"{len(df)} baris dari {n_file} sesi di folder {folder}\n")
    if df.empty:
        print("Dataset kosong. Cek nama folder dan isi pos_*.jsonl.")
        return

    def buat():
        return LGBMClassifier(n_estimators=250, learning_rate=0.05, num_leaves=15,
                              min_child_samples=30, subsample=0.8, subsample_freq=1,
                              colsample_bytree=0.8, random_state=0, verbose=-1)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    final = {}
    print("Pembagian kelas (turun / stabil / naik) dan hasil uji per sesi (5-fold):")
    print(f"{'horizon':>8} {'kelas %':>16} | {'akurasi':>14} {'F1 makro':>14} {'recall naik':>12}")
    print(f"{'':>8} {'':>16} | {'model/dasar':>14} {'model/dasar':>14} {'model/dasar':>12}")
    for h in HORIZONS:
        ok = df[f"y_{h}"].notna()
        X, y, g = df.loc[ok, FITUR], df.loc[ok, f"y_{h}"].astype(int), df.loc[ok, "session"]
        oof = np.zeros(len(y), dtype=int)
        for tr, te in GroupKFold(min(5, g.nunique())).split(X, y, g):     # pisah PER SESI
            oof[te] = buat().fit(X.iloc[tr], y.iloc[tr]).predict(X.iloc[te])
        # pembanding: "tren sekarang berlanjut" (ekstrapolasi kemiringan kecepatan)
        dlt = X["v_slope"].to_numpy() * h
        dasar = np.where(dlt < -TAU[h], 0, np.where(dlt > TAU[h], 2, 1))
        share = np.bincount(y, minlength=3) / len(y) * 100
        rc = lambda p: recall_score(y, p, labels=[2], average=None, zero_division=0)[0]
        print(f"{'t+' + str(h):>8} {'/'.join(f'{s:.0f}' for s in share):>16} | "
              f"{accuracy_score(y, oof):.2f} / {accuracy_score(y, dasar):.2f}  "
              f"{f1_score(y, oof, average='macro'):.2f} / {f1_score(y, dasar, average='macro'):.2f}  "
              f"{rc(oof):.2f} / {rc(dasar):.2f}")
        final[h] = buat().fit(X, y)
    joblib.dump({"fitur": FITUR, "model": final}, MODEL_PATH)
    print(f"\nModel disimpan: {MODEL_PATH}")


# ---------- dipakai saat sistem berjalan ----------
class PrediksiTren:
    """Simpan riwayat pesan tiap HP, lalu prediksi tren kecepatan satu HP."""

    def __init__(self, path=MODEL_PATH, maks_pesan=40):
        b = joblib.load(path)
        self.fitur, self.model = b["fitur"], b["model"]
        self.buf = defaultdict(lambda: deque(maxlen=maks_pesan))
        self.kunci = threading.Lock()      # on_message (thread MQTT) dan loop status berjalan bersamaan

    def update(self, pesan):
        """pesan: dict dengan id, lat, lon, speed_kmh, acc_dyn, t_send, t_recv."""
        with self.kunci:
            self.buf[pesan["id"]].append(dict(pesan))

    def reset(self):
        with self.kunci:
            self.buf.clear()

    def _seri(self, hp):
        if len(self.buf[hp]) < 3:
            return None
        return ke_1hz(siapkan(pd.DataFrame(list(self.buf[hp]))))

    def prediksi(self, hp, lawan):
        """Tren kecepatan `hp` (dengan `lawan` sebagai HP pembanding). None jika data belum cukup."""
        with self.kunci:
            e, o = self._seri(hp), self._seri(lawan)
        if e is None or o is None:
            return None
        d = pasangan(e, o)
        if len(d) < WIN:
            return None
        w = d.to_numpy()[-WIN:]
        if np.isnan(w).any():
            return None
        x = pd.DataFrame([fitur_window(w)])[self.fitur]
        hasil = {"t_ref": int(d.index[-1]), "v_kmh": float(w[-1, 0] * 3.6)}
        for h, m in self.model.items():
            p = m.predict_proba(x)[0]
            hasil[h] = {"label": KELAS[int(np.argmax(p))], "p": dict(zip(KELAS, map(float, p)))}
        return hasil


def skor_tren(pred):
    """-1 (pasti turun) ... +1 (pasti naik), digabung dari 4 horizon."""
    return sum(BOBOT[h] * (pred[h]["p"]["naik"] - pred[h]["p"]["turun"]) for h in HORIZONS)


def _kata(skor):
    return "NAIK" if skor >= AMBANG_TREN else ("TURUN" if skor <= -AMBANG_TREN else "STABIL")


def tren_satu_kata(pred):
    """Hasil AI dalam satu kata: "NAIK" / "STABIL" / "TURUN". Data belum cukup -> "STABIL"."""
    return "STABIL" if pred is None else _kata(skor_tren(pred))


def tentukan_status(kecepatan, jarak, tren):
    """kecepatan: km/jam HP pemicu | jarak: meter | tren: "NAIK" / "STABIL" / "TURUN"."""
    if jarak > RADIUS_M:                                   # di luar radius: bukan ancaman
        return "AMAN"
    if kecepatan > BATAS_BAHAYA:
        level = 2
    elif kecepatan > BATAS_AMAN:
        level = 1
    else:
        level = 0
    if tren == "NAIK" and kecepatan > BATAS_TREN:          # makin ngebut -> naik satu tingkat
        level += 1
    if tren == "TURUN" and jarak > JARAK_DEKAT:            # melambat dan tidak terlalu dekat -> turun satu
        level -= 1
    return URUT[min(max(level, 0), 2)]


# ---------- demo: putar ulang satu sesi seperti sistem live ----------
def label_gabungan_aktual(akt):
    """Kunci jawaban untuk satu kata tren: rumus skor yang sama, dipakai pada label aktual."""
    return _kata(sum(BOBOT[h] * {2: 1, 0: -1}.get(int(akt[h]), 0) for h in HORIZONS))


def demo(path, hp="hp1", lawan="hp2"):
    from sklearn.metrics import accuracy_score, f1_score
    pesan = sorted((json.loads(x) for x in open(path)), key=lambda m: m["t_recv"])
    ai = PrediksiTren()
    kunci = ke_1hz(siapkan(pd.DataFrame(pesan)).query("id == @hp"))
    v, t0 = kunci["speed"].to_numpy(), int(kunci.index[0])
    nyata, tebak = {h: [] for h in HORIZONS}, {h: [] for h in HORIZONS}
    kata_ai, kata_nyata = [], []
    terakhir, cetak = None, -99
    print("Memutar ulang " + path + " (prediksi untuk " + hp + ")\n")
    print(f"{'detik':>6} {'km/jam':>7} | {'AI 1/3/5/10 dtk':<27} | {'aktual 1/3/5/10 dtk':<27} | {'AI':<6} | aktual")
    for m in pesan:
        ai.update(m)                                   # hanya data yang SUDAH diterima
        if m["id"] != hp:
            continue
        r = ai.prediksi(hp, lawan)
        if r is None or r["t_ref"] == terakhir:
            continue
        terakhir, i = r["t_ref"], r["t_ref"] - t0
        akt = {h: label_tren(v, i, h) for h in HORIZONS}
        for h in HORIZONS:
            if not np.isnan(akt[h]):
                nyata[h].append(int(akt[h]))
                tebak[h].append(KELAS.index(r[h]["label"]))
        if any(np.isnan(a) for a in akt.values()):
            continue
        kata_ai.append(tren_satu_kata(r))
        kata_nyata.append(label_gabungan_aktual(akt))
        if r["t_ref"] - cetak >= 10:
            cetak = r["t_ref"]
            pr = " ".join(r[h]["label"][:5].ljust(5) for h in HORIZONS)
            ak = " ".join(KELAS[int(akt[h])][:5].ljust(5) for h in HORIZONS)
            print(f"{i:>6} {r['v_kmh']:>7.1f} | {pr:<27} | {ak:<27} | {kata_ai[-1]:<6} | {kata_nyata[-1]}")
    print("\nAkurasi per horizon (hanya memakai data yang sudah masuk saat itu):")
    for h in HORIZONS:
        if nyata[h]:
            print(f"  t+{h:<2}: akurasi {accuracy_score(nyata[h], tebak[h]):.2f} | "
                  f"F1 makro {f1_score(nyata[h], tebak[h], average='macro'):.2f} | {len(nyata[h])} titik")
    if kata_ai:
        cocok = np.mean([a == b for a, b in zip(kata_ai, kata_nyata)])
        porsi = {k: 100 * kata_ai.count(k) / len(kata_ai) for k in ("NAIK", "STABIL", "TURUN")}
        print(f"\nSatu kata tren: akurasi {cocok:.2f} dari {len(kata_ai)} titik | AI mengeluarkan "
              + ", ".join(f"{k} {p:.0f}%" for k, p in porsi.items()))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "latih"
    if cmd == "latih":
        latih(sys.argv[2] if len(sys.argv) > 2 else "data_sintetis")
    elif cmd == "demo" and len(sys.argv) > 2:
        demo(*sys.argv[2:5])
    else:
        print(__doc__)
