# Nama File: Pembagian.py
# Nama / NIM: Visco Argatha T.T /24060125120023
# Tanggal: 10/10/2025

def bagi(x,y):
    if y==0:
        return 'undefined'
    if x >= 0 and y > 0: #x,y positif
        if x < y:
            return 0
        return 1 + bagi(x-y,y)
    
    elif x<0 and y>0: # x negatif
        if x+y>0:
            return -1
        else:
            return -1 + bagi(x+y,y)
    elif x>=0 and y<0: # y negatif
        if x+y<0:
            return -1
        else:
            return 1+ bagi(x+y,y)
    else: #x,y negatif
        if x>y:
            return 0
        else:
            return 1+ bagi(x-y,y)