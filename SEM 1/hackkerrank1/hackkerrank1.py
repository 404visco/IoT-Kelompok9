# Nama File: aljabar.py
# Nama / NIM: Visco Argatha Tawa Tawa / 24060125120023
# Tanggal: 16 September 2025

def D(x,y,z):
     return y*y-4*x*z
def x1(x,y,z):
    return ((-y)+D(x,y,z)**0.5)/2*x
def x2(x,y,z):
    return ((-y)-D(x,y,z)**0.5)/2*x
def absol(x):
    if x>= 0:
        return x
    else:
        return x*-1
def Aljabar(x,y,z):
    if D(x,y,z)<0:
        return -999
    elif absol(x1(x,y,z))>=absol(x2(x,y,z)):
        return round(absol(x2(x,y,z))/absol(x1(x,y,z)),5)
    else:
        return round(absol(x1(x,y,z))/absol(x2(x,y,z)),5)

#JANGAN DIUBAH!
print(eval(input()))


# Nama File: bagiapel.py
# Nama / NIM: Visco Argatha Tawa Tawa / 24060125120023
# Tanggal: 16 September 2025

def bagiApel(x):
    if x%2==0 and x>2:
        return 'Bisa'
    else:
        return 'Tidak'

#JANGAN DIUBAH!
print(eval(input()))


# Nama File: bawapayung.py
# Nama / NIM: Visco Argatha Tawa Tawa / 24060125120023
# Tanggal: 16 September 2025

def BawaPayung(suhu,prob):
    if suhu>35 or prob>=50:
        return 'Bawa'
    else:
        return 'Tidak bawa'

#JANGAN DIUBAH!
print(eval(input()))


# Nama File: SearchJadwal.py
# Nama / NIM: Visco Argatha Tawa Tawa / 24060125120023
# Tanggal: 23 September 2025

def SearchJadwal(hari, awal, akhir):
    if hari == "sen":
        if akhir > 13 and awal < 15:
            return "Dasar Pemrograman"
        else:
            return "Tidak ada"

    elif hari == "sel":
        if akhir > 13 and awal < 15:
            return "Aljabar Linier"
        else:
            return "Tidak ada"

    elif hari == "rab":
        if (akhir > 7 and awal < 10) and (akhir > 15 and awal < 16):
            return "Dasar Sistem & Bahasa Inggris I"
        elif akhir > 7 and awal < 10:
            return "Dasar Sistem"
        elif akhir > 15 and awal < 16:
            return "Bahasa Inggris I"
        else:
            return "Tidak ada"

    elif hari == "kam":
        if (akhir > 7 and awal < 9) and (akhir > 13 and awal < 15):
            return "Pancasila & Matematika I"
        elif akhir > 7 and awal < 9:
            return "Pancasila"
        elif akhir > 13 and awal < 15:
            return "Matematika I"
        else:
            return "Tidak ada"

    elif hari == "jum":
        if (akhir > 7 and awal < 9) and (akhir > 13 and awal < 16):
            return "Bahasa Indonesia & Struktur Diskrit"
        elif akhir > 7 and awal < 9:
            return "Bahasa Indonesia"
        elif akhir > 13 and awal < 16:
            return "Struktur Diskrit"
        else:
            return "Tidak ada"

    elif hari == "sab" or hari == "min":
        return "Tidak ada"

    else:
        return "Tidak ada"


#JANGAN DIUBAH!
print(eval(input()))


# Nama File: TaxCollector.py
# Nama / NIM: Visco Argatha Tawa Tawa / 24060125120023
# Tanggal: 23 September 2025

def TaxCollector(g,j):
    if g<50.0:
        return g*j*0.85
    elif g>=50.0 and g<=150.0:
        return g*j*0.9
    elif g>150.0 and g<=500.0:
        return g*j*0.95
    else:
        return g*j

#JANGAN DIUBAH!
print(eval(input()))


# Nama File: determine.py
# Nama / NIM: Visco Argatha T.T
# Tanggal: 23/9/2025

def Determine(x):
    if x>1:
        if x==2 or x==3 or x==5 or x==7 or x==11:
            return 'Ya'
        elif x%2==0 or x%3==0 or x%5==0 or x%7==0 or x&11==0:
            return 'Tidak'
        else:
            return 'Ya'

#JANGAN DIUBAH!
print(eval(input()))