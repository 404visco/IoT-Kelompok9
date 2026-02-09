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