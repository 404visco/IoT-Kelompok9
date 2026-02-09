from PBOperator import *
from PohonNnerOperator import *
from listoperator import *
from loloperator import *

def uniformLength(lol):
    if IsOneElmt(lol):
        return True
    if NbElmt(firstList(lol))!= NbElmt(firstList(tailList(lol))):
        return False
    else:
        return uniformLength(tailList(lol))

print(uniformLength([[1], []]))

# def Seimbang(PB): #berdassarkan banyak elmt
#     if isBTEmpty(PB):
#         return True
#     if isBTDaun(PB):
#         return True
#     else:
#         if NBElmtPB(Left(Anak(PB)))== NBElmtPB(Right(Anak(PB))):
#             return Seimbang(Left(PB)) and Seimbang(Right(PB))
#         else:
#             return False

# P= MakePB('A', MakePB('B', (), MakePB('E',(),())), MakePB('C', MakePB('F', (), ()), ()))  
# print(Seimbang(P))

def f(x):
    return x+1

def mapNTree(f,PN):
    if isTreeEmpty(PN):
        return []
    # if isOneElmt(PN):
    #     return MakePN(f(Akar(PN)), ())
    else:
        return MakePN(f(Akar(PN)),mapNTreeChild(f,Anak(PN)))

def mapNTreeChild(f,PN):
    if isTreeEmpty(PN):
        return []
    else:
        return Konso(mapNTree(f,FirstElmt(PN)) , mapNTreeChild(f, Tail(PN)))

P = MakePN(1, [
        MakePN(2, []),
        MakePN(3, [])
    ])
print(P)
print(Anak(P))
print('mapNTree(f,P)')
print(mapNTree(f,P))
print(mapNTree(f,(1, [])))


def max2(a,b):
    if a>b:
        return a
    else:
        return b
def Level(PB):
    if isBTEmpty(PB):
        return 0
    else:
        return 1+ max2(Level(Left(PB)), Level(Right(PB)))
def SelisihLevel(PB):
    if Level(Left(PB)) > Level(Right(PB)):
        return Level(Left(PB)) - Level(Right(PB))
    else:
        return Level(Right(PB)) - Level(Left(PB))
def Selisih(a,b):
    if a>b:
        return a-b
    else:
        return b-a

def Seimbang(PB): #(Selisih tinggi max 1)
    # if isBTEmpty(PB):
    #     return True
    # if isBTDaun(PB):
    #     return True
    # if SelisihLevel(PB) <=1:
    #     return Seimbang(Left(PB)) and Seimbang(Right(PB))
    # else:
    #     return False
    if isBTEmpty(PB):
        return True
    if Selisih(Level(Left(PB)),Level(Right(PB)))<=1:
        return Seimbang(Left(PB)) and Seimbang(Right(PB))
    else:
        return False
P= MakePB(1, 
          MakePB(2, MakePB(3, (), ()), MakePB(4, (), ())),
          MakePB(5, (), MakePB(6,(),())))
print(Seimbang(P))
Q = MakePB(
        1,
        MakePB(
            2,
            MakePB(4, (), ()),
            MakePB(5, (), ())
        ),
        MakePB(
            3,
            MakePB(
                6,
                MakePB(7, (), ()),
                ()
            ),
            ()
        )
    )


print(Seimbang(Q))