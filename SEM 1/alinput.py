#misal fungsi 2D ke 3D
u= [1,2,3]
v= [4,5,6]
k= 3
#tempat fungsi
ekspresi = input("Masukkan fungsi: ")
tempat_fungsi= eval(ekspresi)
print(tempat_fungsi)
def f(fungsi):
    x= fungsi[0]
    y=fungsi[1]
    z= fungsi[2]
    ekspresi = input("Masukkan fungsi: ")
    return 

#fungsi untuk menambahkan! bisa untuk f(u+v) dan fu + fv
def tambah(titik_u,titik_v):
    return [titik_u[i]+titik_v[i] for i in range(len(titik_u))]

#fungsi untuk mengkali! bisa untuk f(k.u) atau k.f(u)
def kali(skalar, titik_u):
    return [skalar*titik_u[i] for i in range(len(titik_u))]

#Fungsi untuk mengecek suatu fungsi itu linear atau tidak
def cek_linier(fungsi):
    #SYARAT 1 : f(u+v) = f
    f_utambahv= f(tambah(u,v))
    fu_tambah_fv= tambah(f(u),f(v))

    print(f''' === SYARAT 1 ===
f(u+v)= {f_utambahv}
f(u)+f(v)= {fu_tambah_fv}
    ''')

    #SYARAT 2 : f(k.u) = k.f(u)
    f_ku = f(kali(k,u))
    k_fu = kali(k,f(u))
    print(f'''=== SYARAT 2 ===
f(k.u)= {f_ku}
k.f(u)= {k_fu}
    ''')
    #CEK APAKAH SYARAT 1 dan 2 terpenuhi atau tidak (keduanya harus terpenuhi)
    aditif = f_utambahv == fu_tambah_fv
    homogen = f_ku == k_fu

    if homogen or aditif:
        return True
    else:
        return False
    # for i in range(len(f_utambahv)):
    #     if f_utambahv[i] == fu_tambah_fv[i] and f_ku[i] == k_fu[i]:
    #         continue
    #     else: return "Tidak Linier"
    # return "Linier"

#cek apakah f(x,y): x, x+y, x-y itu linier atau tidak
#parameter f adalah fungsi python yang menampung sebuah fungsi yang kita cari
#fungsi yang dicari dapat diubah dengan mengubah isi dari fungsi f di paling atas
print(cek_linier(f))

"""
2x + y, 3y - z, x + 4z
X - 2y + 4z, 4x + y, - 3z
0, 5x - y + 2z, 7x
X + Y + 3, 2y, z
x^2, y + z, 2x
"""