# Nama/NIM: Visco Argatha Tawa Tawa/24060125120023
# Tanggal: 30 September 2025

# Definisi TanggalXaverich
# type TanggalXaverich: <hari: int, bulan: int, tahun: int>
# {}
type TanggalXaverich = tuple[int, int, int]

# -------------------------------------
# Definisi dan Spesifikasi Konstruktor
# MakeTanggalXaverich: 3 integer -> TanggalXaverich
# {}
# Realisasi:
def MakeTanggalXaverich(hari: int, bulan: int, tahun: int) -> TanggalXaverich:
    return (hari, bulan, tahun)

# -------------------------------------
# Definisi dan Spesifikasi Selektor
# hari(TX): TanggalXaverich -> int
#     {}
# bulan(TX): TanggalXaverich -> int
#     {}
# tahun(TX): TanggalXaverich -> int
#     {}
# Realisasi:
def hari(TX: TanggalXaverich) -> int:
    return TX[0]
def bulan(TX: TanggalXaverich) -> int:
    return TX[1]
def tahun(TX: TanggalXaverich) -> int:
    return TX[2]
    
def ClassifyXaverichDate(d):
    if tahun(d)%21==0 and hari(d)==7:
        return 'Hari Pengingat'
            
    elif bulan(d) >= 1 and bulan(d) <= 4:
        if hari(d) % 2 == 1:
            return "Hari Kerja"
        else:
            return "Hari Libur"
    elif bulan(d) >= 5 and bulan(d) <= 8:
        if hari(d) % 3 == 0:
            return "Hari Istirahat"
        else:
            return "Hari Produktif"
    elif bulan(d) >= 9 and bulan(d) <= 13:
        if hari(d) % 2 == 1:
            return "Hari Pengingat"
        else:
            return "Hari Biasa"

# --
# DENGAN INI SAYA MENYATAKAN BAHWA SAYA MENGERJAKAN SENDIRI TANPA BANTUAN KECERDASAN ARTIFISAL
# --
# JANGAN DIUBAH
print(eval(input()))