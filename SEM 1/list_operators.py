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


#TUGAS
def ElmtKeN(N,L):
    if N==1:
        return FirstElmt(L)
    else:
        return ElmtKeN(N-1, Tail(L))
# print('=== ELEMENT KE N ===')
# print(ElmtKeN(3,[1,2,3]))

def IsMember(N,L):
    if L==[]:
        return False
    elif N== FirstElmt(L):
        return True
    else:
        return IsMember(N,Tail(L))
# print('=== IsMEMBER ===')
# print(IsMember(5,[1,2,3]))
def MultiRember(x,L):
    if IsEmpty(L):
        return []
    else:
        if FirstElmt(L)==x:
            return MultiRember(x,Tail(L))
        else:    
            return Konso(FirstElmt(L), MultiRember(x,Tail(L)))

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