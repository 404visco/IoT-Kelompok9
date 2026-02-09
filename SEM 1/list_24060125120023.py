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
def IsKosong(L):
    return L == []
def BanyakElmt(L):
    if IsKosong(L):
        return 0
    else:
        return 1+BanyakElmt(Tail(L))


#TUGAS
def ElmtKeN(N,L):
    if N==1:
        return FirstElmt(L)
    else:
        return ElmtKeN(N-1, Tail(L))
print('=== ELEMENT KE N ===')
print(ElmtKeN(3,[1,2,3]))

def IsMember(N,L):
    if L==[]:
        return False
    elif N== FirstElmt(L):
        return True
    else:
        return IsMember(N,Tail(L))
print('=== IsMEMBER ===')
print(IsMember(5,[1,2,3]))

def Copy(L):
    if L==[]:
        return []
    else:
        return Konso(FirstElmt(L),Copy(Tail(L)))
print('=== COPY ===')
print(Copy([1,2,3,4,5]))

def Inverse(L):
    if L==[]:
        return []
    else:
        return Konso(LastElmt(L),Inverse(Head(L)))
print('=== INVERSE ===')
print(Inverse([1,2,3,4,5]))

def Konkat(L1,L2):
    if L1==[]:
        return L2
    else:
        return Konso(FirstElmt(L1), Konkat(Tail(L1),L2))
print('=== KONKAT ===')
print(Konkat([1,2,3],[2,3,4]))

def SumElmt(L):
    if IsKosong(L):
        return 0
    else:
        return FirstElmt(L)+SumElmt(Tail(L))
print('=== SUM ELEMENT ===')
print(SumElmt([1,2,3]))

def AvgElmt(L):
    if IsKosong(L):
        return 0
    else:
        return SumElmt(L)/BanyakElmt(L)
print('=== AVG ELEMENT ===')
print(AvgElmt([1,2,3]))

def MaxElmt(L):
    if IsKosong(L):
        return 0
    else:
        if FirstElmt(L)>MaxElmt(Tail(L)):
            return FirstElmt(L)
        else:
            return MaxElmt(Tail(L))
print('=== MAX ELEMENT ===')
print(MaxElmt([3,24,56,21,3,44]))

def Banyakint(K,L):
    if IsKosong(L):
        return 0
    else:
        if K==FirstElmt(L):
            return 1+ Banyakint(K,Tail(L))
        else:
            return Banyakint(K,Tail(L))
print(Banyakint(1,[1,2,3,1,2,5]))

def BanyakMax(L):
    return(MaxElmt(L),Banyakint(MaxElmt(L), L))
print('=== NbMAX ===')
print(BanyakMax([1,2,3,2,1,3,1]))

def AddList(L1,L2):
    if IsKosong(L1) and IsKosong(L2):
        return []
    elif not IsKosong(L1) and IsKosong(L2):
        return L1
    elif  IsKosong(L1) and not IsKosong(L2):
        return L2
    else:
        return Konso(FirstElmt(L1)+FirstElmt(L2), AddList(Tail(L1),Tail(L2)))
print('=== ADDLIST ===')
print(AddList([2,1],[2,1]))
print(AddList([2,],[2,1]))
print(AddList([2,1],[]))
print(AddList([2,1],[2,1,1]))

def IsPalindrom(kata):
    if IsKosong(kata):
        return None
    else:
        if kata==Inverse(kata):
            return True
        else:
            return False
print('=== PALINDROM ===')
print(IsPalindrom([]))
print(IsPalindrom(['m','a','l','a','m']))
print(IsPalindrom(['a','p','p','a']))
print(IsPalindrom(['m','a','l','m']))