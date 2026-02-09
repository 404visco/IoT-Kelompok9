# Nama/NIM: Visco Argatha Tawa Tawa / 24060125120023
# Tanggal: 30 September 2025

# Definisi Point
# type Point: <x: real, y: real>
#     {<x, y> adalah tipe bentukan point pada koordinat kartesian.}
type Point = tuple[float, float]

# -------------------------------------
# Definisi dan Spesifikasi Konstruktor
# MakePoint: 2 real -> point
#     {MakePoint(x, y) membentuk tipe data point dari input (x, y).}
# Realisasi:
def MakePoint(x: float, y: float) -> Point:
    return (x, y)

# -------------------------------------
# Definisi dan Spesifikasi Selektor
# getAbsis(p): Point -> real
#     {getAbsis(p) mengembalikan absis dari point (p).}
# getOrdinat(p): Point -> real
#     {getOrdinat(p) mengembalikan ordinat dari point (p).}
# Realisasi:
def getAbsis(p: Point) -> float:
    return p[0]
def getOrdinat(p: Point) -> float:
    return p[1]

def Reverse(P,RF):
    if RF=='Y':
        return MakePoint(-getAbsis(P), getOrdinat(P))
    elif RF=='X':
        return MakePoint(getAbsis(P),-getOrdinat(P))
  
def DivineMirror(P,RF,RT):
    if getAbsis(P)==0 and getOrdinat(P)==0:
        return MakePoint(getAbsis(P), getOrdinat(P))
    elif RT== 0 or RT==360:
        return MakePoint(getAbsis(Reverse(P,RF)), getOrdinat(Reverse(P,RF)))
    elif RT== 90:
        return MakePoint(-getOrdinat(Reverse(P,RF)), getAbsis(Reverse(P,RF)))
    elif RT== 180:
        return MakePoint(-getAbsis(Reverse(P,RF)), -getOrdinat(Reverse(P,RF)))
    elif RT==270:
        return MakePoint(getOrdinat(Reverse(P,RF)), -getAbsis(Reverse(P,RF)))

# --
# DENGAN INI SAYA MENYATAKAN BAHWA SAYA MENGERJAKAN SENDIRI TANPA BANTUAN KECERDASAN ARTIFISAL
# --


# JANGAN DIUBAH
print(eval(input()))