from list_24060125120023 import *
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

#Tugas
def IsMemberS(x, S):
    if isEmpty(S):
        return False
    elif isAtom(firstList(S)):
        if x== firstList(S):
            return True
        else:
            return IsMemberS(x, tailList(S))
    else:
        if IsMemberS(x, firstList(S)):
            return True
        else:
            return IsMemberS(x,tailList(S))

# print(IsMemberS(2, [1,[3,1],3,2,3]))
print(IsMemberS(3, [])) #-> False
print(IsMemberS(3, [2, 4, 3, [1], [4,5]])) #-> True
print(IsMemberS(3, [2, 4, 7, [1], [3,5]])) #-> True

def RemberList(x,S):
    if isEmpty(S):
        return S
    else:
        if isAtom(firstList(S)):
            if firstList(S) == x:
                return RemberList(x, tailList(S))
            else:
                return konsLo(firstList(S), RemberList(x,tailList(S)))
        else:
            if firstList(firstList(S))== x:
                return RemberList(x, konsLo(tailList(firstList(S)), tailList(S)))
            else:
                return konsLo(RemberList(x,firstList(S)), RemberList(x,tailList(S)))
                #return konsLo(Konso(firstList(firstList(S)), MultiRember(x,tailList(firstList(S)))), RemberList(x, tailList(S)))
            # return konsLo(MultiRember(x, firstList(S)), Tail(S))
# print(RemberList(2, [1,2,[3,2,1],4,2,1]))
print(RemberList(3, []))
print(RemberList(3, [4, 3, [2,4], 3]))
print(RemberList(3,[2, 4, [3,6,9], 5, 3]))

def MaxLOL(S):
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            if firstList(S) > MaxLOL(tailList(S)):
                return firstList(S)
            else:
                return MaxLOL(tailList(S))
        else:
            return MaxLOL(konsLo(MaxLOL(firstList(S)),tailList(S)))

print(MaxLOL([2,[3,5,1],100,4,99]))

def NBElmtAtom(S):
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            return 1+NBElmtAtom(tailList(S))
        else:
            return NBElmtAtom(tailList(S))

print(NBElmtAtom([1,2,[3,4,5],6,[7,8],9]))

def NBElmtList(S):
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            return NBElmtList(tailList(S))
        else:
            return 1+NBElmtList(tailList(S))
print(NBElmtList([1,2,[3,4,5],6,[7,8],9,[10]]))

def SumLOL(S):
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            return firstList(S)+ SumLOL(tailList(S))
        else:
            return SumLOL(firstList(S))+ SumLOL(tailList(S))
print(SumLOL([1,2,[3,4,5],6,[7,8],9,[10]]))

def MaxNBElmtList(S):
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            return MaxNBElmtList(tailList(S))
        else:
            if NBElmtAtom(firstList(S))> MaxNBElmtList(tailList(S)):
                return NBElmtAtom(firstList(S))
            else:
                return MaxNBElmtList(tailList(S))
print(MaxNBElmtList([1,[2],[1,2],[1,2,3],[1],1,2,3,4,5]))

def MaxSumElmt(S):
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            if firstList(S)> MaxSumElmt(tailList(S)):
                return firstList(S)
            else:
                return MaxSumElmt(tailList(S))
        else:
            if SumLOL(firstList(S))> MaxSumElmt(tailList(S)):
                return SumLOL(firstList(S))
            else:
                return MaxSumElmt(tailList(S))

# print(MaxSumElmt([1,[2],[1,2],[1,2,3],[1],1,2,3,4,5,10]))   #->10

#APLIKASI
print(MaxSumElmt([[1, 2], 9, [4, 5, 6], 8])) #-> 15
print(MaxSumElmt([[1, 2], 90, [4, 5, 6], 8])) #-> 90
print(MaxSumElmt([8, 9, 10])) #-> 10
print(MaxSumElmt([[8, 9, 10]])) #-> 27