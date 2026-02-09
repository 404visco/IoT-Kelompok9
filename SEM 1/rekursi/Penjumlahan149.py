# Nama File: Penjumlahan149.py
# Nama / NIM: Visco Argatha T.T /24060125120023
# Tanggal: 10/10/2025

def der(x):
    if x==0:
        return 0
    else:
        return x**2 + der(x-1)