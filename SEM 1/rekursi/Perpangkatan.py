# Nama File: Perpangkatan.py
# Nama / NIM: Visco Argatha T.T /24060125120023
# Tanggal: 10/10/2025

def pangkat(x,y):
    if y==0:
        return 1
    else:
        return x*pangkat(x,y-1)