from treeoperator import *
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
def NBElmt(PB):
 # Basis: Jika pohon kosong
    if isBTEmpty(PB):
        return 0
 # Basis 2: Jika merupakan daun
    if isBTDaun(PB):
        return 1
# Hitung 1 untuk akar, lalu rekursif pada anak kiri dan kanan pohon
    return 1+ NBElmt(Left(PB))+NBElmt(Right(PB))

#---------------------------------------------------------------------------------------------------
#TUGAS LATIHAN
P = (2, 
      (8, 
         (), 
         (7,
             (6,
                (4,
                   (),
                   ()
                ), 
               (5,
                   (),
                   ()
                )
             ),
             ()
          )
       ), 
      (1,
          (), 
         (9,
             (),
             (8,
                (), 
               ()
             ) 
         )
       )
 )

# NBNDaun: Pohon Biner -> integer >= 0
 #  {NBNDaun(P) memberikan banyaknya daun dari pohon P:
 #  Basis 0: IsTreeNEmpty(()) = 0
 #  Basis 1: IsOneElmt((A)) = 1
 #  Rekurens: NBNDaun((A, L, R)) = NBNDaun(L) + NBNDaun(R)}
 #  Contoh: 
#  NBNDaun(P) -> 3
#  {terdapat 3 daun pada pohon biner P}
def NBNDaun(PB):
    if isBTEmpty(PB):
        return 0
    if isBTDaun(PB):
        return 1
    return NBNDaun(Left(PB))+NBNDaun(Right(PB))
print("NBNDaun(P)")
print(NBNDaun(P))

 # IsMemberPB: Pohon Biner, elemen -> boolean
 #  {IsMemberPB(P, X) mengembalikan True jika X merupakan bagian dari P.}
 #  Contoh: 
#  IsMemberPB(P, 10) -> False 
#  {Tidak ada 10 pada pohon}
 #  IsMemberPB(P, 8) -> True 
#  {Elemen 8 ada pada pohon}
def IsMemberPB(PB,X):
    if isBTEmpty(PB):
        return False
    if Akar(PB)==X:
        return True
    return IsMemberPB(Left(PB),X) or IsMemberPB(Right(PB),X)
print("IsMemberPB(P,10)")
print(IsMemberPB(P,10))
print("IsMemberPB(P,8)")
print(IsMemberPB(P,8))

 # IsSkewLeft: Pohon Biner -> boolean
 #  {IsSkewLeft(P) mengembalikan True jika P condong kiri.}
def IsSkewLeft(PB):
    if isBTEmpty(PB):
        return True
    # if isBTDaun(PB):
    #     return True
    return IsSkewLeft(Left(PB)) and isBTEmpty(Right(PB))
print("IsSkewLeft(P)")
Q= MakePB(1,(),())
print(IsSkewLeft(Q))

 # IsSkewRight: Pohon Biner -> boolean
 #  {IsSkewRight(P) mengembalikan True jika P condong kanan.}
def IsSkewRight(PB):
    if isBTEmpty(PB):
        return True
    if isBTDaun(PB):
        return True
    return IsSkewRight(Right(PB)) and isBTEmpty(Left(PB))
print("IsSkewRight(P)")
print(IsSkewRight(P))

 # LevelOfX: Pohon Biner, elemen -> boolean
 #  {LevelOfX(P, X) mengembalikan level dari elemen X pada P.}

def Max2(a,b):
    if a>b:
        return a
    else:
        return b
def LevelOfX(PB,X):
    if isBTEmpty(PB):
        return 0
    if Akar(PB)==X:
        return 0
    else:
        return 1+Max2(LevelOfX(Left(PB),X), LevelOfX(Right(PB),X))
def SumPB(PB):
    if isBTEmpty(PB):
        return 0
    else:
        return Akar(PB)+ SumPB(Left(PB))+SumPB(Right(PB))
print(SumPB(P))

# print("LevelOfX(P,8)")
# print(LevelOfX(P,8))
# print("LevelOfX(P,2)")
# print(LevelOfX(P,2))
