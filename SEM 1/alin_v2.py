import random
# misal fungsi 2D ke 3D

#fungsi untuk menambahkan! bisa untuk f(u+v) dan fu + fv
def tambah(titik_u, titik_v):
    return [titik_u[i] + titik_v[i] for i in range(len(titik_u))]

#fungsi untuk mengkali! bisa untuk f(k.u) atau k.f(u)
def kali(skalar, titik_u):
    return [skalar * titik_u[i] for i in range(len(titik_u))]

# fungsi cek linearitas
def cek_linier(str_fungsi):
    #memasukkan titik u dan v ke dalam bentuk fungsi 
    def f(vektor):
        if len(vektor)==3:
            x, y, z = vektor
        elif len(vektor)==2:
            x,y = vektor
        return eval(str_fungsi)

    f_utambahv = f(tambah(u, v))
    fu_tambah_fv = tambah(f(u), f(v))
    print(f'''=== SYARAT 1 ===
f(u+v) = {f_utambahv}
f(u)+f(v) = {fu_tambah_fv}
''')

    f_ku = f(kali(k, u))
    k_fu = kali(k, f(u))

    print(f'''=== SYARAT 2 ===
f(k.u) = {f_ku}
k.f(u) = {k_fu}
''')
    #Membandingkan f(u+v) dengan f(u) + f(v)
    aditif = f_utambahv == fu_tambah_fv
    homogen = f_ku == k_fu

    if aditif and homogen:
        return "✅ Linier"
    else:
        return "❌ Tidak Linier"

#Penginputan fungsi
while True:
    u = []
    v = []
    k = random.randint(-5,5)
    dimensi_asal= int(input("Dari Dimensi (maks 3): "))
    for i in range(dimensi_asal
    ):
        angka_u= random.randint(-5,5)
        angka_v= random.randint(-5,5)
        u.append(angka_u)
        v.append(angka_v)
    print(f"""U: {u}
V: {v}
misal, skalar: {k}""")
    print("-"*40)
    pilihan = int(input("""1. Cek Fungsi
2. Exit
Pilih angka: """))
    if pilihan== 1:
        ekspresi = input("Masukkan fungsi: (contoh: [x,x+y] *pakai variable x/y/z)\n")
    elif pilihan== 2:
        print("Program Selesai😉👍")
        break
    try:
        hasil = cek_linier(ekspresi)
        print("Hasil:", hasil)
    except Exception as e:
        print("ERROR BOS+++++😵‍💫\n", e)
    print("-" * 40)