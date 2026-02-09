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