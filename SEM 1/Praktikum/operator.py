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