#REALISASI
def MakePN(A,C):
    return (A,C)

#-------------------------------------------------------------------------------------
#Selektor
# DEFINISI DAN SPESIFIKASI SELEKTOR
# Akar: PohonN-ner tidak kosong-> elemen
#   {Akar(PN) memberikan elemen akar dari pohon PN}

# Anak: PohonN-ner tidak kosong-> List of PohonN-ner
#   {Anak(PN) adalah list of pohon N-ner yang merupakan anak dari pohon PN}

#REALISASI
def Akar(PN):
    return PN[0]
def Anak(PN):
    return PN[1]

#-------------------------------------------------------------------------------------
#Predikat
# DEFINISI DAN SPESIFIKASI PREDIKAT
# isTreeNEmpty: PohonN-ner-> boolean
#   {IsTreeNEmpty(PN) bernilai True jika PN kosong : []}

# IsOneElmt: PohonN-ner-> boolean
#   {IsOneElmt(PN) bernilai True jika PN hanya memiliki satu elemen}

#REALISASI
def isTreeEmpty(PN):
    return PN == []
def isOneElmt(PN):
    return (not isTreeEmpty(PN) and isTreeEmpty(Anak(PN)))