#Buat definisi, spesifikasi, realisasi dan aplikasi dari suatu fungsi yang bertugas untuk mengetahui posisi
#suatu titik terhadap suatu lingkaran. Diketahui bahwa titik yang dimaksud mempunyai absis x dan
#ordinat y, sedangkan lingkaran memiliki titik pusat di (a,b) dan jari-jari sepanjang r. Posisi yang
#diharapkan adalah apakah titik tersebut berada di dalam lingkaran, tepat pada tepi lingkaran atau titik
#tersebut berada di luar lingkaran.

#Def Spek type
#type Titik: <x: int, y: int> 
#   {<x,y> adalah titik dengan x sebagai absis dan y sebagai ordinat}

#Selektor
# getAbsis: Titik --> int
# getOrdinat: Titik --> int

#Konstruktor
# MakeTitik

def MakeTitik (x,y):
    return (x,y)

def Titik(x,y):
    return (x,y)

def getAbsis (x):
    return x[0]
def getOrdinat(y):
    return y[1]

def Lingk(pusat,titik,r):
    d= (((getAbsis(titik)-getAbsis(pusat))**2+(getOrdinat(titik)-getOrdinat(pusat))**2)**0.5)
    if d == r:
        return "Tepat"
    elif d> r:
        return "Luar"
    else:
        return "Dalam"

print(Lingk((2,3),(5,7),5))
print(Lingk((4,7),(-2,4),3))
print(Lingk((0,0),(0,0),1))