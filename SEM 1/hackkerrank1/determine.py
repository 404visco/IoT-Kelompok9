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