# Nama/NIM: Visco Argatha Tawa Tawa / 24060125120023
# Tanggal: 30 September 2025

# Definisi Point
# type Point: <x: real, y: real, z:real>
#     {<x, y, z> adalah tipe bentukan point tiga dimensi.}
type ThreeDPoint = tuple[float, float, float]

# -------------------------------------
# Definisi dan Spesifikasi Konstruktor
# Make3DPoint: 3 real -> point
#     {Make3DPoint(x, y, z) membentuk tipe data point 3D dari input (x, y, z).}
# Realisasi:
def Make3DPoint(x: float, y: float, z: float) -> ThreeDPoint:
    return (x, y, z)

# -------------------------------------
# Definisi dan Spesifikasi Selektor
# getAbsis(p): Point -> real
#     {getAbsis(p) mengembalikan absis dari point (p).}
# getOrdinat(p): Point -> real
#     {getOrdinat(p) mengembalikan ordinat dari point (p).}
# getApotema(p): Point -> real
#     {getApotema(p) mengembalikan apotema dari point (p).}
# Realisasi:
def getAbsis(p: ThreeDPoint) -> float:
    return p[0]
def getOrdinat(p: ThreeDPoint) -> float:
    return p[1]
def getApotema(p: ThreeDPoint) -> float:
    return p[2]
  
def akar(x: float, y:float) -> float:
    return (x*x + y*y)**0.5

def abs(x: float) -> float:
    if x < 0:
        return -x
    else:
        return x

def DBT(tdp1: ThreeDPoint, tdp2: ThreeDPoint) -> float:
      return round(akar(akar(abs(getAbsis(tdp1) - getAbsis(tdp2)), abs(getOrdinat(tdp1) - getOrdinat(tdp2))), abs(getApotema(tdp1) - getApotema(tdp2))), 5)

# --
# DENGAN INI SAYA MENYATAKAN BAHWA SAYA MENGERJAKAN SENDIRI TANPA BANTUAN KECERDASAN ARTIFISAL
# --
# JANGAN DIUBAH
print(eval(input()))