def FirstElmt(L):
    return L[0]
def LastElmt(L):
    return L[-1]
def Konso(E,L):
    return [E]+L
def Konsi(L,E):
    return L+[E]
def Head(L):
    return L[:-1]
def Tail(L):
    return L[1:]
def IsEmpty(L):
    return L == []
def NbElmt(L):
    if IsEmpty(L):
        return 0
    else:
        return 1+NbElmt(Tail(L))
    
# DEFINISI DAN SPESIFIKASI PREDIKAT KHUSUS LIST
 # isEmpty: List of List -> boolean
 #   {isEmpty(S) benar jika S adalah list of list kosong.}
 # Realisasi:
def isEmpty(S):
    return S == []
# isAtom: List of List -> boolean
 #   {isAtom(S) benar jika S adalah sebuah atom.}
 # Realisasi:
def isAtom(S):
    return type(S)!=list
 # isList: List of List -> boolean
 #   {isList(S) benar jika S adalah sebuah list.}
 # Realisasi:
def isList(S):
    return type(S)==list

# DEFINISI DAN SPESIFIKASI KONSTRUKTOR
 # konsLo: List, List of List -> List of List
 #   {konsLo(L, S) membentuk list baru dengan list (L) sebagai 
#    elemen pertama list of list (S).}
 # Realisasi:
def konsLo(L,S):
    return [L]+S
 # konsLi: List of List, List -> List of List
 #   {konsLi(S, L) membentuk list baru dengan list (L) sebagai 
#    elemen terakhir list of list (S).}
 # Realisasi:
def konsLi(S,L):
    return S+[L]

 # DEFINISI DAN SPESIFIKASI SELEKTOR
 # firstList: List of List tidak kosong -> List
 #   {firstList(S) menghasilkan elemen pertama list (mungkin sebuah list atau atom).}
 # Realisasi:
def firstList(S):
    return S[0]
 # lastList: List of List tidak kosong -> List
 #   {lastList(S) menghasilkan elemen terakhir list (mungkin sebuah list atau atom).}
 # Realisasi:
def lastList(S):
    return S[-1]
 # tailList: List of List tidak kosong -> List of List
 #   {tailList(S) menghasilkan sisa list of list S tanpa elemen pertamanya.}
 # Realisasi:
def tailList(S):
    return S[1:]
 # headList: List of List tidak kosong -> List of List
 #   {headList(S) menghasilkan sisa list of list S tanpa elemen terakhirnya.}
 # Realisasi:
def headList(S):
    return S[:-1]
def isEmpty(S):
    return S == []
# isAtom: List of List -> boolean
 #   {isAtom(S) benar jika S adalah sebuah atom.}
 # Realisasi:
def isAtom(S):
    return type(S)!=list
 # isList: List of List -> boolean
 #   {isList(S) benar jika S adalah sebuah list.}
 # Realisasi:
def isList(S):
    return type(S)==list

# DEFINISI DAN SPESIFIKASI KONSTRUKTOR
 # konsLo: List, List of List -> List of List
 #   {konsLo(L, S) membentuk list baru dengan list (L) sebagai 
#    elemen pertama list of list (S).}
 # Realisasi:
def konsLo(L,S):
    return [L]+S
 # konsLi: List of List, List -> List of List
 #   {konsLi(S, L) membentuk list baru dengan list (L) sebagai 
#    elemen terakhir list of list (S).}
 # Realisasi:
def konsLi(S,L):
    return S+[L]

 # DEFINISI DAN SPESIFIKASI SELEKTOR
 # firstList: List of List tidak kosong -> List
 #   {firstList(S) menghasilkan elemen pertama list (mungkin sebuah list atau atom).}
 # Realisasi:
def firstList(S):
    return S[0]
 # lastList: List of List tidak kosong -> List
 #   {lastList(S) menghasilkan elemen terakhir list (mungkin sebuah list atau atom).}
 # Realisasi:
def lastList(S):
    return S[-1]
 # tailList: List of List tidak kosong -> List of List
 #   {tailList(S) menghasilkan sisa list of list S tanpa elemen pertamanya.}
 # Realisasi:
def tailList(S):
    return S[1:]
 # headList: List of List tidak kosong -> List of List
 #   {headList(S) menghasilkan sisa list of list S tanpa elemen terakhirnya.}
 # Realisasi:
def headList(S):
    return S[:-1]

def IsOneElmt(L):
    if isEmpty(Tail(L)) and isEmpty(Head(L)):
        return True
    else:
        return False

def BanyakElmt(L):
    if IsEmpty(L):
        return 0
    else:
        return 1+BanyakElmt(Tail(L))
    
def uniformLength(lol):
    if isEmpty(lol):
        return True
    if IsOneElmt(lol):
        return True
    if BanyakElmt(firstList(lol))!= BanyakElmt(firstList(tailList(lol))):
        return False
    else:
        return uniformLength(tailList(lol))

print(uniformLength([[1,2], [3,4]]))


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
def Anak(PB):
    return PB[1]
def Seimbang(PB):
    if isBTEmpty(PB):
        return True
    if isBTDaun(PB):
        return True
    else:
        if NBElmt(Left(Anak(PB)))== NBElmt(Right(Anak(PB))):
            return Seimbang(Left(PB)) and Seimbang(Right(PB))
        else:
            return False

# P= MakePB('A', MakePB('B', (), MakePB('E',(),())), MakePB('C', MakePB('F', (), ()), ()))  
# print(Seimbang(P))
# A= MakePB('A', MakePB('B', MakePB('D', (), ()), ()), MakePB('C', MakePB('F', (), ()), ()))  

# def mapNTree(f, PN):
#     return MakePN(f(Akar), (Anak(PN)))