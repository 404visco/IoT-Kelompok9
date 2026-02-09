from PBOperator import *
from PohonNnerOperator import *
from listoperator import *
from loloperator import *

def NbElmtL(S):
    if isEmpty(S):
        return 0
    if isAtom(firstList(S)):
        return NbElmtL(tailList(S))
    else:
        return NbElmt(firstList(S))
# print(NbElmtL([1,2,[2,3,5],3,[4,5,6,7],4]))
def uniformlenght(S):
    if isEmpty(S):
        return True
    if isList(firstList(S)):
        return isSameL(NbElmt(firstList(S)), tailList(S))
    else:
        return uniformlenght(tailList(S))
    
def isSameL(x,S):
    if isEmpty(S):
        return True
    if isList(firstList(S)):
        return (NbElmt(firstList(S)) == x) and isSameL(x,tailList(S))
    else:
        return isSameL(x,tailList(S))
# print(uniformlenght([1,2,[2,3,5],3,[1,4,5],[2,3,4],4]))
def NbElmtAtom(LOL):
    if isEmpty(LOL):
        return 0
    if isAtom(firstList(LOL)):
        return 1+ NbElmtAtom(tailList(LOL))
    else:
        return NbElmtAtom(tailList(LOL))

def BanyakAnak(PN):
    if isEmpty(Anak(PN)):
        return 0
    else:
        return NbElmt(Anak(PN))
    
# print(FirstElmt((1,[2])))

def NBNChild(PN):
    if isEmpty(Anak(PN)):
        return 0
    else:
        return NbElmt(Anak(PN))
def isFraktal(PN):
    if NBNChild(PN)== 0:
        return True
    else:
        return cekfraktal(NBNChild(firstList(Anak(PN))),Anak(PN))

def cekfraktal(x,LPN):
    if IsEmpty(LPN):
        return True
    else:
        return (NBNChild(firstList(LPN)) == x) and isFraktal(firstList(LPN)) and cekfraktal(x, tailList(LPN))

F= MakePN(1, [
    MakePN(2, [
        MakePN(5, [
            MakePN(14, []),
            MakePN(15, []),
            MakePN(16, [])
        ]),
        MakePN(6, [
            MakePN(17, []),
            MakePN(18, []),
            MakePN(19, [])
        ]),
        MakePN(7, [
            MakePN(20, []),
            MakePN(21, []),
            MakePN(22, [])
        ])
    ]),
    MakePN(3, [
        MakePN(8, [
            MakePN(23, []),
            MakePN(24, []),
            MakePN(25, [])
        ]),
        MakePN(9, [
            MakePN(26, []),
            MakePN(27, []),
            MakePN(28, [])
        ]),
        MakePN(10, [
            MakePN(29, []),
            MakePN(30, []),
            MakePN(31, [])
        ])
    ]),
    MakePN(4, [
        MakePN(11, [
            MakePN(32, []),
            MakePN(33, []),
            MakePN(34, [])
        ]),
        MakePN(12, [
            MakePN(35, []),
            MakePN(36, []),
            MakePN(37, [])
        ]),
        MakePN(13, [
            MakePN(38, []),
            MakePN(39, []),
            MakePN(40, [])
        ])
    ])
])
# print(isFraktal(F))

def FilterGenap(L):
    if isEmpty(L):
        return []
    if FirstElmt(L)%2==0:
        return Konso(FirstElmt(L), FilterGenap(Tail(L)))
    else:
        return FilterGenap(Tail(L))
    
# print(FilterGenap([1,2,3,4,5,6,7,1,3,11,8,22]))

def isContainList(lol):
    if isEmpty(lol):
        return False
    if isList(firstList(lol)):
        return True
    else:
        return isContainList(tailList(lol))
    
# print(isContainList([1,2,3,4,5,6,1,4,6]))

# def isThere(x,PN):
#     if isEmpty(Anak(PN)):
#         return []
#     if Akar(FirstElmt(Anak(PN)))== x:
#         return FirstElmt(Anak(PN))
#     else:
#         return isThereChild(x, Anak(PN))
    
# def isThereChild(x, PN):
#     if isEmpty(PN):
#         return []
#     else:
#         return isThere(x, FirstElmt(PN)) or isThereChild(x, Tail(PN))
def isThere(x,PN):
    if Akar(PN)== x:
        return PN
    else:
        return isThereChild(x, Anak(PN))
    
def isThereChild(x, PN):
    if isEmpty(PN):
        return []
    else:
        if isThere(x, FirstElmt(PN)) != []:
            return isThere(x,FirstElmt(PN))
        else:
            return isThereChild(x,Tail(PN)) 

visco= MakePN('V',[MakePN('I',[MakePN('C', []), MakePN('O', [])]),
                   MakePN('S',[MakePN('A', []), MakePN('R', []),MakePN('G', [])]),
                   MakePN('T',[MakePN('H', []), MakePN('W', [])])])
# print(isThere('O',visco))

def AddX(P,X):
    if isBTEmpty(P):
        return MakePB(X, (), ())
    else:
        if X<Akar(P):
            return MakePB(Akar(P), AddX(Left(P), X), Right(P))
        else:
            return MakePB(Akar(P), Left(P), AddX(Right(P), X))

def MakeBinSearchTree(L):
    if isEmpty(L):
        return ()
    else:
        return AddX(MakeBinSearchTree(Tail(L)), FirstElmt(L))
    
# print(MakeBinSearchTree([2,1,3,3,4,51,32,4]))

def isListUrut(L):
    if isEmpty(L):
        return True
    if IsOneElmt(L):
        return True
    else:
        if FirstElmt(L) <= FirstElmt(Tail(L)):
            return isListUrut(Tail(L))
        else:
            return False
        
# print(isListUrut([1,2]))

def Ada(x, L):
    if isEmpty(L):
        return False
    if FirstElmt(L) == x:
        return True
    else:
        return Ada(x, Tail(L))

def OnlyWeb(W,G):
    if isEmpty(W):
        return []
    if Ada(FirstElmt(W), G):
        return OnlyWeb(Tail(W), G)
    else:
        return Konso(FirstElmt(W), OnlyWeb(Tail(W), G))
# print(Ada(8, [1,4,5,2,6,7]))
W= ["Ardi", "Yogi", "Indun"]
G= ["Nanang", "Jenggo", "Indun"]

print(OnlyWeb(W,G))