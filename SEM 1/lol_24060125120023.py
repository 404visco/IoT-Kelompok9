from list_operators import *

#DEFINISI DAN SPESIFIKASI FUNGSI

# IsMemberS: elemen, list of list -> boolean
#   {IsMemberS(x,S) mengembalikan true jika elemen x ada di dalam list of list S.
#     Contoh aplikasi:
#        IsMemberS(3, []) -> False
#        IsMemberS(3, [2, 4, 3, [1], [4,5]]) -> True
#        IsMemberS(3, [2, 4, 7, [1], [3,5]]) -> True
#   }
# RemberList: elemen, List of List -> List of List
#   {RemberList(x,S) menghapus semua elemen x yang ada di list of list S.
#     Contoh aplikasi:
#        Rember*(3, []) -> []
#        Rember*(3, [4, 3, [2,4], 3]) -> [4, [2,4]]
#        Rember*(3, [2, 4, [3,6,9], 5, 3]) -> [2, 4, [6,9], 5]
#   }
# MaxLOL: List of List -> elemen
#   {MaxLOL(S) mengembalikan elemen maksimum di dalam list of list S.
#     Contoh aplikasi:
#        Max([4, 5, 6, [8,9,10], [12,0], 8]) -> 12
#        Max([4, 15, 6, [8,9,10], [12,0], 8]) -> 15
#   }
# NBElmtAtom: List of List -> integer
#   {NBElmtAtom(S) mengembalikan banyaknya elemen list of list S yang berupa atom.
#     Contoh aplikasi:
#        NBElmtAtom([4, 5, 6, [8, 9, 10], [12, 0], 8]) -> 4
#        NBElmtAtom([4, 15, 6, [8, 9], 10, [12], 8]) -> 5
#        NBElmtAtom([[8, 9, 10]]) -> 0}
# NBElmtList: List of List -> integer
#   {NBElmtList(S) mengembalikan banyaknya elemen list of list S yang berupa list.
#     Contoh aplikasi:
#        NBElmtList([4, 5, 6, [8, 9, 10], [12, 0], 8]) -> 2
#        NBElmtList([[4, 15], 6, [8, 9], 10, [12], 8]) -> 3
#        NBElmtList([[8, 9, 10]]) -> 1
#   }
# SumLoL: List of List -> integer
#   {SumLoL(S) mengembalikan jumlah semua elemen dalam list of list S.
#     Contoh aplikasi:
#        SumLoL([[]]) -> 0
#        SumLoL([4, 5, 6, [2, 3, 1]]) -> 21
#        SumLoL([[2, 3, 4]]) -> 9
#   }
# MaxNBElmtList: List of List -> integer
#   {MaxNBElmtList(S) mengembalikan banyaknya elemen list 
#    maksimum yang ada pada list of list S.
#     Contoh aplikasi:
#        MaxNBElmtList([[4,5,6,7], [8,9,10], [12,0], 8]) -> 4
#        MaxNBElmtList([[4,15], 6, [8, 9], 10, [12], 8]) -> 2
#        MaxNBElmtList([8, 9, 10]) -> 10
#   }
# MaxSumElmt: List of List -> integer
#   {MaxSumElmt(S) mengembalikan elemen maksimum pada list of list S;
#   Jika elemen berupa list, maka dihitung sum dari elemen dalam list tersebut;
#   Jika elemen berupa atom, maka nilainya adalah elemen tersebut.
#     Contoh aplikasi:
#        MaxSumElmt([1, 2], 9, [4, 5, 6], 8]) -> 15
#        MaxSumElmt([1, 2], 90, [4, 5, 6], 8]) -> 90
#        MaxSumElmt([8, 9, 10]) -> 10
#        MaxSumElmt([[8, 9, 10]]) -> 27

#REALISASI
#Tugas
def IsMemberS(x, S):
    if isEmpty(S):
        return False
    if isAtom(firstList(S)):
        if firstList(S)==x:
            return True
        else:
            return IsMemberS(x, tailList(S))
    else:
        if IsMemberS(x, firstList(S)):
            return True
        else:
            return IsMemberS(x,tailList(S))

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
            if IsMember(x,firstList(S)):
                return konsLo(RemberList(x,firstList(S)), RemberList(x,tailList(S)))
            else:
                return konsLo(firstList(S), RemberList(x, tailList(S)))

            # if firstList(firstList(S))== x:
            #     return RemberList(x, konsLo(tailList(firstList(S)), tailList(S)))
            # else:
            #     return konsLo(RemberList(x,firstList(S)), RemberList(x,tailList(S)))

def MaxLOL(S): 
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            if firstList(S) > MaxLOL(tailList(S)):
                return firstList(S)
            else:
                return MaxLOL(tailList(S))
        if isList(firstList(S)):
            if MaxLOL(firstList(S))> MaxLOL(tailList(S)):
                return MaxLOL(firstList(S))
            else:
                return MaxLOL(tailList(S))

def NBElmtAtom(S):
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            return 1+NBElmtAtom(tailList(S))
        else:
            return NBElmtAtom(tailList(S))

def NBElmtList(S):
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            return NBElmtList(tailList(S))
        else:
            return 1+NBElmtList(tailList(S))

def SumLOL(S):
    if isEmpty(S):
        return 0
    else:
        if isAtom(firstList(S)):
            return firstList(S)+ SumLOL(tailList(S))
        else:
            return SumLOL(firstList(S))+ SumLOL(tailList(S))

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

#APLIKASI
print("=== IS MEMBER ===")
print(IsMemberS(3, [])) #-> False
print(IsMemberS(3, [2, 4, 3, [1], [4,5]])) #-> True
print(IsMemberS(3, [2, 4, 7, [1], [3,5]])) #-> True
print("=== REMBER LIST ===")
print(RemberList(3, []))
print(RemberList(3, [4, 3, [2,3,4], 3]))
print(RemberList(3,[2, 4, [3,6,9], 5, 3]))
print("=== MAX LOL ===")
print(MaxLOL([2,[3,5,1],100,4,99]))
print(MaxLOL([5,1]))
print(MaxLOL([[],[1,99,3],3]))
print("=== NBElmtAtom ===")
print(NBElmtAtom([1,2,[3,4,5],6,[7,8],9]))
print(NBElmtAtom([[]]))
print(NBElmtAtom([1]))
print("=== NBElmtList ===")
print(NBElmtList([1,2,[3,4,5],6,[7,8],9,[10]]))
print(NBElmtList([1,5,7,8]))
print(NBElmtList([[]]))
print("=== SumLOL ===")
print(SumLOL([1,2,[3,4,5],6,[7,8],9,[10]]))
print(SumLOL([2,4,[6]]))
print(SumLOL([[2]]))
print("=== MaxNBElmtList ===")
print(MaxNBElmtList([1,[2],[1,2],[1,2,3],[1],1,2,3,4,5]))
print(MaxNBElmtList([1,4,5]))
print(MaxNBElmtList([[1,2,3,4]]))
print("=== MaxSumElmt ===")
print(MaxSumElmt([[1, 2], 9, [4, 5, 6], 8])) #-> 15
print(MaxSumElmt([[1, 2], 90, [4, 5, 6], 8])) #-> 90
print(MaxSumElmt([8, 9, 10])) #-> 10
print(MaxSumElmt([[8, 9, 10]])) #-> 27