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