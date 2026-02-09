u = [1, 2, 3]
v = [4, 5, 6]
k = 3

# fungsi dasar
def tambah(titik_u, titik_v):
    return [titik_u[i] + titik_v[i] for i in range(len(titik_u))]

def kali(skalar, titik_u):
    return [skalar * titik_u[i] for i in range(len(titik_u))]

# fungsi cek linearitas
def cek_linier(str_fungsi):
    def f(fungsi):
        x, y, z = fungsi
        return eval(str_fungsi)

    f_utambahv = f(tambah(u, v))
    fu_tambah_fv = tambah(f(u), f(v))
    print(f(u))

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
    pilihan = int(input("""=== FUNGSI CEK LINIER ===
1. Cek Fungsi
2. Exit
Pilih angka: """))
    if pilihan== 1:
        ekspresi = input("Masukkan fungsi: (contoh: [x,y])\n")
    elif pilihan== 2:
        break
    try:
        hasil = cek_linier(ekspresi)
        print("Hasil:", hasil)
        # time.sleep(3)
    except Exception as e:
        print("ERROR BOS😵‍💫\n", e)
    print("-" * 40)