# DEFINISI DAN SPESIFIKASI KONSTRUKTOR
 # MakePB: elemen, PohonBiner, PohonBiner -> PohonBiner
 #  {MakePB(A, L, R) membuat pohon biner dengan A sebagai akar, L sebagai anak kiri dari
 #   pohon, dan R sebagai anak kanan dari pohon. L dan R bisa berupa daun maupun
 #   pohon biner utuh.
def MakePB(A,L,R):
    return(A,L,R)
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
    return PB==()
 # isBTDaun: Pohon Biner -> boolean
 #  { isBTDaun(PB) bernilai True jika PB hanya terdiri dari Akar. }
def isBTDaun(PB):
    return(not isBTEmpty(PB))and(isBTEmpty(Left(PB)))and(isBTEmpty(Right(PB)))
# NBElmt: PohonBiner -> integer >= 0
 #  {NBElmt(PB) memberikan banyaknya node dari pohon P:
 #     Basis 0: IsTreeNEmpty(()) = 0
 #     Basis 1: IsOneElmt((A)) = 1
 #     Rekurens: NBElmt((A, L, R)) = 1 + NBElmt(L) + NBElmt(R) }
def NBElmtPB(PB):
 # Basis: Jika pohon kosong
    if isBTEmpty(PB):
        return 0
 # Basis 2: Jika merupakan daun
    if isBTDaun(PB):
        return 1
# Hitung 1 untuk akar, lalu rekursif pada anak kiri dan kanan pohon
    return 1+ NBElmtPB(Left(PB))+NBElmtPB(Right(PB))

#---------------------------------------------------------------------------------------------------