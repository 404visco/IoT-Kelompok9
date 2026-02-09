#Definisi dan spesifikasi
#fx_abs(x) real -> real
    #fx_abs(x) menghasilkan nilai absolut dari x

#Realisasi
def fx_abs(x):
    if x>=0:
        return x
    else:
        return -x

#Aplikasi
print(fx_abs(2)) #2
print(fx_abs(0)) #0
print(fx_abs(-5)) #5