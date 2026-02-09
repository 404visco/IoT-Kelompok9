from PBOperator import *
from PohonNnerOperator import *
from listoperator import *
from loloperator import *


def f(x):
    return x+1
def mapNTree(f,PN):
    if isTreeEmpty(PN):
        return []
    # if isOneElmt(PN):
    #     return MakePN(f(Akar(PN)), ())
    else:
        return Konso(mapNTree(f,FirstElmt(PN)) , mapNTree(f, Tail(PN)))

# def mapNTreeChild(f,PN):
#     if isTreeEmpty(PN):
#         return []
#     else:
#         return Konso(mapNTree(f,FirstElmt(PN)) , mapNTreeChild(f, Tail(PN)))
print(mapNTree(f,(1, [])))