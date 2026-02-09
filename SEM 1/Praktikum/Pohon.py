from operator import *
# Nama/NIM  : Visco Argatha Tawa Tawa / 24060125120023
# Tanggal   : 25 November 2025
#-------------------------------------------------------------------------------------
#KONSTRUKTOR
#DEFINISI DAN SPESIFIKASI KONSTRUKTOR
# MakePN: elemen, list of Pohon N-ner-> Pohon N-ner
# {MakePN(A, C) membuat pohon N-ner dengan A sebagai akar dan C 
# sebagai anak-anaknya. 
# Bisa berupa daun maupun pohonN-ner utuh.}

#REALISASI
def MakePN(A,C):
    return (A,C)

#-------------------------------------------------------------------------------------
#Selektor
# DEFINISI DAN SPESIFIKASI SELEKTOR
# Akar: PohonN-ner tidak kosong-> elemen
#   {Akar(PN) memberikan elemen akar dari pohon PN}

# Anak: PohonN-ner tidak kosong-> List of PohonN-ner
#   {Anak(PN) adalah list of pohon N-ner yang merupakan anak dari pohon PN}

#REALISASI
def Akar(PN):
    return PN[0]
def Anak(PN):
    return PN[1]

#-------------------------------------------------------------------------------------
#Predikat
# DEFINISI DAN SPESIFIKASI PREDIKAT
# isTreeNEmpty: PohonN-ner-> boolean
#   {IsTreeNEmpty(PN) bernilai True jika PN kosong : []}

# IsOneElmt: PohonN-ner-> boolean
#   {IsOneElmt(PN) bernilai True jika PN hanya memiliki satu elemen}

#REALISASI
def isTreeEmpty(PN):
    return PN == []
def isOneElmt(PN):
    return (not isTreeEmpty(PN) and isTreeEmpty(Anak(PN)))

#-------------------------------------------------------------------------------------
#Operator
# DEFINISI DAN SPESIFIKASI OPERATOR
# NBNElmt: PohonN-ner-> integer >= 0
#   {NBNElmt(PN) memberikan banyaknya elemen dari pohon PN: 
#   Basis 0: IsTreeNEmpty(PN) = 0
#   Basis 1: IsOneElmt(PN) = 1
#   Rekurens: NBNElmt(PN) = NBNElmtChild(PN)}

#REALISASI
def NBNElmt(PN):
    if isTreeEmpty(PN):
        return 0
    if isOneElmt(PN):
        return 1
    else:
        1+ NBNElmtChild(Anak(PN))
def NBNElmtChild(PN):
    if isTreeEmpty(PN):
        return 0
    else:
        return NBNElmt(FirstElmt(PN))+ NBNElmtChild(Tail(PN))

#---------------------------------------------------------------------------------------------------------------------
#TUGAS
#---------------------------------------------------------------------------------------------------------------------

#BANYAK DAUN POHON
#DEFINISI DAN SPESIFIKASI
# NBNDaunPN: PohonN-ner-> integer >= 0
#   {NBNDaunPN(PN) memberikan banyaknya daun dari pohon PN: 
#   Basis 0: IsTreeNEmpty(PN) = 0
#   Basis 1: IsOneElmt(PN) = 1
#   Rekurens: NBNDaun(PN) = NBNDaunChild(PN)}
# NBNDaunChildPN: PohonN-ner-> integer>=0
#   {NBNDaunChildPN(PN) memberikan banyaknya daun dari child pohon PN}

#REALISASI
def NBNDaun(PN):
    if isTreeEmpty(PN):
        return 0
    if isOneElmt(PN):
        return 1
    else:
        return NBNDaunChild(Anak(PN))
def NBNDaunChild(PN):
    if isTreeEmpty(PN):
        return 0
    else:
        return NBNDaun(FirstElmt(PN))+ NBNDaunChild(Tail(PN))

#APLIKASI
#asumsikan Pohon P adalah [2, [[3, [[1, []], [4, []], [5, [[9, []]]]]], [7, [[6, []], [8, []]]]]]
P = [2, [[3, [[1, []], [4, []], [5, [[9, []]]]]], [7, [[6, []], [8, []]]]]]
print(NBNDaun(P))
# asumsikan Pohon Q adalah [1,[[2,[[3,[]],[4,[]]]], [ [5,[] ]]]] --> daun = 3
Q = [1, [[2, [[3, []], [4, []], [5,[] ]] ]]]
print(NBNDaun(Q))
# asumsikan R adalah pohon yang hanya berisi akar, [2,[]] --> daun = 1
R = [9, []]
print(NBNDaun(R))

#---------------------------------------------------------------------------------------------------------------------

#APAKAH MEMBER POHON?
#DEFINISI DAN SPESIFIKASI
# IsMemberPN: PohonN-ner, elemen-> boolean
#   {IsMemberPN(PN, E) mengembalikan True jika E merupakan bagian dari P.
#   Basis 0: IsTreeNEmpty(PN) = False
#   Basis 1: Akar(PN) = A == E
#   Rekurens: IsMember(PN, E) = IsMemberPN(PN)}
# IsMemberChildPN: PohonN-ner, elemen-> boolean
#   {IsMemberChildPN(PN,E) mengembalikan True jika E adalah bagian dari child Pohon PN}

#REALISASI
def IsMemberPN(PN,E):
    if isTreeEmpty(PN):
        return False
    # if isOneElmt(PN):
    #     return FirstElmt(PN)==E
    if Akar(PN)==E:
        return True
    else:
        return IsMemberChildPN(Anak(PN),E)
def IsMemberChildPN(PN,E):
    if isTreeEmpty(PN):
        return False
    else:
        return IsMemberPN(FirstElmt(PN), E) or IsMemberChildPN(Tail(PN),E)

#APLIKASI
#asumsikan Pohon P adalah [2, [[3, [[1, []], [4, []], [5, [[9, []]]]]], [7, [[6, []], [8, []]]]]]
P = [2, [[3, [[1, []], [4, []], [5, [[9, []]]]]], [7, [[6, []], [8, []]]]]]
print(IsMemberPN(P, 2))
print(IsMemberPN(P, 10))
print(IsMemberPN(P, 0))