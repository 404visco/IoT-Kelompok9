#titik dan skalar untuk tes
u= [1,2,4]
v= [3,4,5]
k= 3


def f(v):
    x= v[0]
    y= v[1]
    z= v[2]
    return [2*x+y,3*y-z,x+4*z]

def cek_lin(f):
    def tambah(titik1,titik2): # u, v adalah titik
        return [titik1[i] + titik2[i] for i in range(len(titik1))]
    def skalar(k, titik1):
        return [k*titik1[i] for i in range(len(titik1))]
    
    #f(u+v)= fu+fv
    f_utambahv= f(tambah(u,v))
    fu_tambah_fv= tambah(f(u), f(v))

    #f(k*u)= k*f(u)
    f_ku= f(skalar(k,u))
    k_fu= skalar(k,f(u))

    #cek kesamaan
    for i in range(len(f(u))):
        if f_utambahv[i] == fu_tambah_fv[i] or f_ku[i]==k_fu[i]:
            continue
        else:
            return "Tidak Linear"
    return "Linear"

print(cek_lin(f))
# test_titik2d1= (1,2)
# test_titik2d2= (3,4)
# test titik3d1= (1,2,3)
# test_titik2d2= (2,3,4)
# a= test_titik2d1
# b= test_titik2d2
# c= test_titik3d1
# d= test_titik3d2
'''
misal f(x,y): x, x+y, x-y
Apakah fungsi di atas linier atau tidak?
Cek!
1. f(x1+x2, y1+y2)== f(x1,y1)+f(x2,y2)
2. f(k*x1,k*y1)== k*f(x1,y1)

eks:
def f_adivitas(titik1,titik2):
    for i in range(len(titik1)):
        titik1[i] + titik2[i]
        

def cl(fungsi):
    if f_adivitas and f_homogenitas:
        return "Linier"
    else:
        return "Tidak Linier"


PR:
1. Inputan yang diminta bentuknya gimana?
'''
# u= (1,2)
# v= (3,4)
# k= 3
# adivitas= (u[0]+v[0], u[1]+v[1]) #u+v
# homogenitas= (k*u[0],k*u[1]) #k*u
# fungsi = (x, x+y, x-y)
# print(adivitas)
# print(homogenitas)


# def cek_lin(fungsi):
#     =fungsi(adivitas)
# def fungsi (x,y):
#     return (x, x+y, x-y)
