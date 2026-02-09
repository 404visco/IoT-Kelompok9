# Nama File: Perkalian.py
# Nama / NIM: Visco Argatha T.T /24060125120023
# Tanggal: 10/10/2025

def kali(x,y):
    if y==0:
        return y
    else:
        return x+ kali(x,y-1)