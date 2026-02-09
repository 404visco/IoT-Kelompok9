# Nama File: Fotosintesis.py
# NIM/Nama: 24060125120023 / Visco Argatha Tawa Tawa
# Lab: C2

# DEFINISI DAN SPESIFIKASI KONSTRUKTOR
# MakePB: elemen, PohonBiner, PohonBiner -> PohonBiner
#  {MakePB(A, L, R) membuat pohon biner dengan A sebagai akar, L sebagai anak kiri dari pohon,
#   dan R sebagai anak kanan dari pohon. L dan R bisa berupa daun maupun pohon biner utuh.}
def MakePB(A, L, R):
    return (A, L, R)

# DEFINISI DAN SPESIFIKASI SELEKTOR
# Akar: Pohon Biner tidak kosong -> Elemen
#  {Akar(PB) adalah Akar dari PB. 
#   Jika PB adalah (A, L, R) = Akar(PB) adalah A.}
def Akar(PB):
    return PB[0]

# Left: Pohon Biner -> Pohon Biner
#  {Left(PB) adalah pohon Biner yang merupakan anak kiri dari P. 
#   Jika PB adalah (A, L, R) = Right(PB) adalah L.}
def Left(PB):
    return PB[1]

# Right: Pohon Biner -> Pohon Biner
#  {Right(PB) adalah pohon Biner yang merupakan anak kanan dari P. 
#   Jika PB adalah (A, L, R) = Right(PB) adalah R.}
def Right(PB):
    return PB[2]

# DEFINISI DAN SPESIFIKASI PREDIKAT
# isBTEmpty: Pohon Biner -> boolean
#  { isBTEmpty(PB) bernilai True jika PB kosong : () }
def isBTEmpty(PB):
    return PB == ()

# isBTDaun: Pohon Biner -> boolean
#  { isBTDaun(PB) bernilai True jika PB hanya terdiri dari Akar. }
def isBTDaun(PB):
    return (not isBTEmpty(PB)) and (isBTEmpty(Left(PB))) and (isBTEmpty(Right(PB)))
  
# Happy Coding!
def AddDaun(P, X, Y, Kiri):
    if isBTEmpty(P):
        return ()
    if isBTDaun(P) and Akar(P)==X:
        if Kiri == True:
            return MakePB(Akar(P),MakePB(Y,(),()),())
        else:
            return MakePB(Akar(P),(),MakePB(Y,(),()))
    else:
        return MakePB(Akar(P), AddDaun(Left(P), X, Y, Kiri), AddDaun(Right(P), X, Y, Kiri))