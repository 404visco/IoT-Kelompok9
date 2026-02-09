from list_operator import *

#2.1 Tipe Mahasiswa
def MakeMhs(nim,nama):
    return (nim,nama)
def getNama(Mhs):
    return Mhs[1]
def getNim(Mhs):
    return Mhs[0]

#2.2 Tipe Matkul
#Konstruktor
def MakeMatkul(nama, sks, list_nilai):
    return (nama, sks, list_nilai)
#Selektor
def getNamaMK(Matkul):
    return Matkul[0]
def getSKS(Matkul):
    return Matkul[1]
def getNilai(Matkul):
    return Matkul[2]
#Operator
def NilaiSekarangMK(Matkul):
    if IsEmpty(getNilai(Matkul)):
        return -1.0
    else:
        return LastElmt(getNilai(Matkul))

def SudahAmbilMK(Matkul):
    if not IsEmpty(getNilai(Matkul)):
        return True
    else:
        return False

def MengulangMK(Matkul):
    if NbElmt(getNilai(Matkul))>1:
        return True
    else:
        return False

def LulusMK(Matkul):
    if IsEmpty(Matkul):
        return -1.0
    else:
        if LastElmt(getNilai(Matkul)) >= 2.0:
            return True
        else: False

def MakeTranskrip(Mhs, listMK):
    return (Mhs, listMK)

def GetMhs(Transkrip):
    return Transkrip[0]
def GetListMatkul(Transkrip):
    return Transkrip[-1]

def CariMatkul(Transkrip, namaMK):
    if IsEmpty((GetListMatkul(Transkrip))):
        return False
    elif getNamaMK(FirstElmt(GetListMatkul(Transkrip))) == namaMK :
        return FirstElmt(GetListMatkul(Transkrip))
    else:
        return CariMatkul(MakeTranskrip(GetMhs(Transkrip),Tail(GetListMatkul(Transkrip))), namaMK)

def TotalSKSLulus(Transkrip):
    if IsEmpty(GetListMatkul(Transkrip)):
        return False
    elif LulusMK(FirstElmt(GetListMatkul(Transkrip))):
        return getSKS(FirstElmt(GetListMatkul(Transkrip))) + TotalSKSLulus(MakeTranskrip(GetMhs(Transkrip), Tail(GetListMatkul(Transkrip))))
    else:
        return TotalSKSLulus(MakeTranskrip(GetMhs(Transkrip), Tail(GetListMatkul(Transkrip))))

def JumlahMatkulMengulang(Transkrip):
    if IsEmpty(GetListMatkul(Transkrip)):
        return 0
    elif MengulangMK(FirstElmt(GetListMatkul(Transkrip))):
        return 1+ JumlahMatkulMengulang(MakeTranskrip(GetMhs(Transkrip), Tail(GetListMatkul(Transkrip))))
    else:
        return JumlahMatkulMengulang(MakeTranskrip(GetMhs(Transkrip), Tail(GetListMatkul(Transkrip))))

def IPKTranskrip(Transkrip):
    def bobot(L):
        if IsEmpty(L):
            return 0.0
        else:
            return NilaiSekarangMK(FirstElmt(L))*getSKS(FirstElmt(L)) + bobot(Tail(L))
    def sks(L):
        if IsEmpty(L):
            return 0.0
        else:
            return getSKS(FirstElmt(L)) + sks(Tail(L))
    if sks(GetListMatkul(Transkrip)) == 0:
        return 0
    else:
        return bobot(GetListMatkul(Transkrip))/sks(GetListMatkul(Transkrip))
    # if IsEmpty(GetListMatkul(Transkrip)):
    #     return 0
    # else:
        # ListMatkul=GetListMatkul(Transkrip)
        # Matkul= FirstElmt(ListMatkul)
        # NilaiAkhir= NilaiSekarangMK(Matkul)
        # SKS = getSKS(Matkul)
        # Bobot = NilaiAkhir*SKS+IPKTranskrip(MakeTranskrip(GetMhs(Transkrip), Tail(ListMatkul)))
        # JumlahSKS = SKS+IPKTranskrip(MakeTranskrip(GetMhs(Transkrip), Tail(ListMatkul)))
        # return JumlahSKS
        #return (NilaiSekarangMK(FirstElmt(GetListMatkul(Transkrip)))*getSKS(FirstElmt(GetListMatkul(Transkrip)))) / getSKS(FirstElmt(GetListMatkul(Transkrip)))+ IPKTranskrip(MakeTranskrip(GetMhs(Transkrip), Tail(GetListMatkul(Transkrip))))


M = MakeMhs("A11.2020.01234", "Reno")
MK1 = MakeMatkul("Daspro", 3, [2.0, 3.0])
print(LulusMK(MK1))
MK2 = MakeMatkul("Matdis", 2, [3.0, 4.0])
T = MakeTranskrip(M, [MK1, MK2])
print("=== Cari Matkul ===")
print(CariMatkul(T, "Daspro"))
print("=== Total SKS ===")
print(TotalSKSLulus(T))
print("=== Matkul Ngulang ===")
print(JumlahMatkulMengulang(T))
print("=== IPK Transkrip ===")
print(IPKTranskrip(T))

#3 SET
def MakeSetTranskrip():
    return []

def AddTranskrip(S,T):
    if IsEmpty(S):
        return Konsi(S,T)
    else:
        if getNama(GetMhs((T)))== getNama(GetMhs(FirstElmt(S))):
            return AddTranskrip(Tail(S), T)
        else:
            return Konsi(S,T)

def AddNilaiMatkul(S, nim, namaMK, nilai):
    if IsEmpty(S):
        return []
    elif getNim(GetMhs(FirstElmt(S))) == nim:
        if IsEmpty(GetListMatkul(S)):
            return AddNilaiMatkul(MakeTranskrip(GetMhs(S), ))
        if GetNamaMK(FirstELmt(GetListMatkul(FirstElmt(S)))) == namaMK:
            return MakeSetTranskrip(Konsi(GetNilai(FirstElmt(GetListMatkul(FirstElmt(S)))), nilai))
        else:
            return AddNilaiMatkul(MakeTranskrip(GetMhs(S), Tail(GetListMatkul(FirstElmt(S)))), nim, namaMK, nilai)


S1 = MakeSetTranskrip()
M1 =MakeMhs("A11.01", "Reno")
T1 =MakeTranskrip(M1,[MK1, MK2])
S2 =AddTranskrip(S1,T1)
S3= AddTranskrip(S2,T1)
M2 =MakeMhs("A11.02", "Andi")
MK3 =MakeMatkul("Daspro",3, [3.0])
MK4 =MakeMatkul("Matdis",2, [4.0])
T2 =MakeTranskrip(M2,[MK3, MK4])
print(AddTranskrip(S3,T2))