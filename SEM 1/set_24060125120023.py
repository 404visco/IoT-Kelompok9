from list_24060125120023 import *

# DEFINISI DAN SPESIFIKASI OPERASI LIST YANG DIPERLUKAN UNTUK SET
 # Rember2: elemen, List -> List
 #  {Rember2(x, L) menghapus sebuah elemen dari list L.
 #   Jika x ada di list L, maka elemen L berkurang 1.
 #   Jika x tidak ada di list L, maka L tidak berubah.
 #   List kosong tetap menjadi list kosong.}
 # MultiRember: elemen, List -> List
 #  {MultiRember(x, L) menghapus semua kemunculan elemen x dari list L.
 #   List baru yang dihasilkan tidak lagi memiliki elemen x.
 #   List kosong tetap menjadi list kosong.}
 # DEFINISI DAN SPESIKASI KONSTRUKTOR SET DARI LIST
 # MakeSet_V1: List -> Set
 #  {MakeSet_V1(L) membuat set dari list L dengan menghapus semua
 #   elemen yang muncul lebih dari satu, menyisakan elemen yang 
#   sama yang terakhir muncul.}
 # MakeSet_V2: List -> Set
 #  {MakeSet_V2(L) membuat set dari list L dengan menghapus semua
 #   elemen yang muncul lebih dari satu, menyisakan elemen yang 
#   sama yang pertama muncul.}
 # DEFINISI DAN SPESIKASI KONSTRUKTOR SET
 # KonsoSet: elemen, Set -> Set
 #  {KonsoSet(e, H) menambahkan elemen e sebagai elemen pertama dari set H
 #   dengan syarat e belum merupakan anggota dari set H.}
 # DEFINISI DAN SPESIFIKASI PREDIKAT
 # IsSet: List -> boolean
 #  {IsSet(L) bernilai True apabila list L merupakan sebuah set.}
 # IsSubSet: 2 Set -> boolean
 #  {IsSubset(H1, H2) bernilai True apabila H1 merupakan subset dari H2.}
 # IsEqualSet_V1: 2 Set -> boolean
 #  {IsEqualSet_V1(H1, H2) bernilai True apabila H1 adalah 
#   set yang sama dengan H2, dengan mengecek bahwa H1 
#   merupakan subset dari H2, dan sebaliknya.}
 # IsEqualSet_V2: 2 Set -> boolean
 #  {IsEqualSet_V2(H1, H2) bernilai True apabila H1 adalah 
#   set yang sama dengan H2, dengan mengecek setiap elemen H1 
#   merupakan elemen dari H2 juga dan kedua set memiliki besar yang sama.}
 # IsIntersect: 2 Set -> boolean
 #  {IsIntersect(H1, H2) bernilai True apabila H1 beririsan dengan H2.}
 # DEFINISI DAN SPESIFIKASI OPERASI TERHADAP SET
 # MakeIntersect_H1: 2 Set -> Set
 #  {MakeIntersect_H1(H1, H2) menghasilkan set baru yang berisikan
 #   irisan antara elemen H1 dan H2, dengan elemen pertama H1 yang 
#   beririsan dengan H2 diprioritaskan untuk dimasukkan ke set yang baru.}
 # MakeIntersect_H2: 2 Set -> Set
 #  {MakeIntersect_H2(H1, H2) menghasilkan set baru yang berisikan
 #   irisan antara elemen H1 dan H2, dengan elemen pertama H2 yang 
#   beririsan dengan H1 diprioritaskan untuk dimasukkan ke set yang baru.}
 # MakeUnion_H1: 2 Set -> Set
 #  {MakeUnion_H1(H1, H2) menghasilkan set baru yang merupakan
 #   gabungan dari elemen H1 dan H2, dengan elemen H1 yang bukan merupakan
 #   elemen H2 diletakkan di belakang sebagai elemen terakhir dari set baru.}
 # MakeUnion_H2: 2 Set -> Set
 #  {MakeUnion_H2(H1, H2) menghasilkan set baru yang merupakan
 #   gabungan dari elemen H1 dan H2, dengan elemen H2 yang bukan merupakan
 #   elemen H1 diletakkan di belakang sebagai elemen terakhir dari set baru.}
 # NBIntersect: 2 Set -> integer
 #  {NBIntersect(H1, H2) menghasilkan jumlah elemen yang beririsan pada H1 dan H2
 #   tanpa memanfaatkan fungsi MakeIntersect sebelumnya.}
 # NBUnion: 2 Set -> integer
 #  {NBUnion(H1, H2) menghasilkan jumlah elemen gabungan pada H1 dan H2
 #   tanpa memanfaatkan fungsi MakeUnion sebelumnya.}

#REALISASI
def Rember2(x, L):
    if IsKosong(L):
        return []
    else:
        if LastElmt(L)==x:
            return Head(L)
        else:
            return Konsi(Rember2(x, Head(L)),LastElmt(L), )

def MultiRember(x,L):
    if IsKosong(L):
        return []
    else:
        if FirstElmt(L)==x:
            return MultiRember(x,Tail(L))
        else:    
            return Konso(FirstElmt(L), MultiRember(x,Tail(L)))


def MakeSet_V1(L):
    if IsKosong(L):
        return L
    else:
        if IsMember(FirstElmt(L), Tail(L)):
            return MakeSet_V1(Tail(L))
        else:
            return Konso(FirstElmt(L), MakeSet_V1(Tail(L)))

def MakeSet_V2(L):
    if IsKosong(L):
        return L
    else:
        return Konso(FirstElmt(L),MakeSet_V2(MultiRember(FirstElmt(L),Tail(L))))

def MakeSet_V3(L):
    if IsKosong(L):
        return L
    else:
        if IsMember(LastElmt(L), Head(L)):
            return MakeSet_V3(Head(L))
        else:
            return Konsi(MakeSet_V3(Head(L)), LastElmt(L))

def KonsoSet(e,L):
    if IsMember(e,L):
        return L
    else:
        return Konso(e, L)

def IsSet(L):
    if IsKosong(L):
        return True
    else:
        if IsMember(FirstElmt(L),Tail(L)):
            return False
        else:
            return IsSet(Tail(L))

def IsSubSet(L1,L2):
    if IsKosong(L1):
        return True
    else:
        if not IsMember(FirstElmt(L1),L2):
            return False
        else:
            return IsSubSet(Tail(L1),L2)

def IsEqualSet_V1(L1,L2):
    return IsSubSet(L1,L2) and IsSubSet(L2,L1)


def IsEqualSet_V2(L1,L2):
    if IsKosong(L1) and IsKosong(L2):
        return True
    elif not IsKosong(L1) and IsKosong(L2) :
        return False
    elif IsKosong(L1) and not IsKosong(L2):
        return True
    else:
        if IsMember(FirstElmt(L1), L2):
            return IsEqualSet_V2(Tail(L1),L2)
        else: return False

def IsInterSect(L1,L2):
    if IsKosong(L1) and IsKosong(L2):
        return False
    elif not IsKosong(L1) and IsKosong(L2):
        return False
    elif IsKosong(L1) and not IsKosong(L2):
        return False
    else:
        if IsMember(FirstElmt(L1), L2):
            return True
        else:
            return IsInterSect(Tail(L1),L2)

def MakeIntersect_H1(L1,L2):
    if IsKosong(L1) and IsKosong(L2):
        return []
    elif not IsKosong(L1) and IsKosong(L2):
        return []
    elif IsKosong(L1) and not IsKosong(L2):
        return []
    else:
        if IsMember(FirstElmt(L1), L2):
            return Konso(FirstElmt(L1),MakeIntersect_H1(Tail(L1),L2))
        else:
            return MakeIntersect_H1(Tail(L1),L2)

def MakeIntersect_H2(L1,L2):
    if IsKosong(L1) and IsKosong(L2):
        return []
    elif not IsKosong(L1) and IsKosong(L2):
        return []
    elif IsKosong(L1) and not IsKosong(L2):
        return []
    else:
        if IsMember(FirstElmt(L2), L1):
            return Konso(FirstElmt(L2),MakeIntersect_H2(L1,Tail(L2)))
        else:
            return MakeIntersect_H2(L1,Tail(L2))

def MakeUnion_H1(L1,L2):
    if IsKosong(L1) and IsKosong(L2):
        return []
    elif not IsKosong(L1) and IsKosong(L2):
        return L1
    elif IsKosong(L1) and not IsKosong(L2):
        return L2
    else:
        if IsMember(FirstElmt(L1),L2):
            return MakeUnion_H1(Tail(L1),L2)
        else:
            return MakeUnion_H1(Tail(L1),Konsi(L2,FirstElmt(L1)))

def MakeUnion_H2(L1,L2):
    if IsKosong(L1) and IsKosong(L2):
        return []
    elif not IsKosong(L1) and IsKosong(L2):
        return L1
    elif IsKosong(L1) and not IsKosong(L2):
        return L2
    else:
        if IsMember(FirstElmt(L2),L1):
            return MakeUnion_H2(L1,Tail(L2))
        else:
            return MakeUnion_H2(Konsi(L1,FirstElmt(L2)),Tail(L2))

def NbIntersect(L1,L2):
    if IsKosong(L1):
        return 0
    elif IsMember(FirstElmt(MakeSet_V1(L1)),MakeSet_V1(L2)):
        return 1+ NbIntersect(Tail(MakeSet_V1(L1)),Tail(MakeSet_V1(L2)))
    else:
        return NbIntersect(MakeSet_V1(Tail(L1)),MakeSet_V1(L2))

def NbUnion(L1,L2):
    if IsKosong(L1):
        return 0
    elif IsMember(FirstElmt(MakeSet_V1(L1)),MakeSet_V1(L2)):
        return 1+ NbUnion(Tail(MakeSet_V1(L1)),Tail(MakeSet_V1(L2)))
    else:
        return 1+NbUnion(MakeSet_V1(Tail(L1)),MakeSet_V1(L2))

#APLIKASI
print("=== Rember 2, [2,3,4,2,1])) ===")
print(Rember2(2, [2,3,4,2,1]))
print("=== MultiRember 2, [2,3,4,2,1])) ===")
print(MultiRember(2, [2,3,4,2,1]))
print("=== MakeSet_V1 [2,3,4,2,1,4,1])) ===")
print(MakeSet_V1([2,3,4,2,1,4,1]))
print("=== MakeSet_V2 [2,3,4,2,1,4,1])) ===")
print(MakeSet_V2([2,3,4,2,1,4,1]))
print("=== MakeSet_V2.1 [2,3,4,2,1,4,1])) ===")
print(MakeSet_V3([2,3,4,2,1,4,1]))
print("=== KonsoSet (3,[2,4,5])) ===")
print(KonsoSet(3,[2,4,5]))
print("=== IsSet [2,3,4,1] ===")
print(IsSet([2,3,4,1]))
print("=== IsSubSet [1,2,3],[4,2,6,5] ===")
print(IsSubSet([1,2,3],[4,2,6,5]))
print(IsSubSet([],[4,2,6,5]))
print("=== IsEqualSet_V1 [1,2,3],[2,1,3] ===")
print(IsEqualSet_V1([1,2,3],[2,1,3]))
print("=== IsEqualSet_V2 [1,2,3],[2,1,3] ===")
print(IsEqualSet_V2([1,2,3],[2,1,3]))
print(IsEqualSet_V2([],[]))
print("=== IsInterSect [1,2,3,4],[4,2,6,5] ===")
print(IsInterSect([1,2,3,4],[4,2,6,5]))
print("=== MAKE Intersect 1 ===")
print(MakeIntersect_H1([1,2,3],[3,2,4]))
print("=== MAKE Intersect 2 ===")
print(MakeIntersect_H2([1,2,3],[3,2,4]))
print(MakeIntersect_H2([],[3,9,5]))
print(MakeIntersect_H2([4,1,9],[9,4,5,8]))
print("=== MAKE UNION 1 ===")
print(MakeUnion_H1([1,2,3,4],[1,2,5,10,7]))
print("=== MAKE UNION 2 ===")
print(MakeUnion_H2([1,2,3,4],[1,2,5,10,7]))
print("=== Nb Intersect [1,1,2,3],[22,3,1,4] ===")
print(NbIntersect([1,1,2,3],[22,3,1,4]))
print("=== Nb Union [1,1,2,3],[22,3,1,4] ===")
print(NbUnion([1,1,2,3],[22,3,1,4]))