#1
print('=== SEARCH JADWAL ===\n')

def SearchJadwal(hari,awal,akhir):
    if hari== 'sen':
        if awal<=15 and akhir>=13:
            return 'Dasar Pemrograman'
        else:
            return 'Tidak Ada'
    elif hari== 'sel':
        if awal>=13 and akhir<=15:
            return 'Aljabar Linear'
        else:
            return 'Tidak Ada'
    elif hari== 'rab':
        if awal>=7 and akhir<=10:
            return 'Dasar Sistem'
        elif awal>=15 and akhir<=16:
            return 'Bahasa Inggris I'
        else:
            return 'Tidak Ada'
    elif hari== 'kam':
        if awal>=7 and akhir<=9:
            return 'Pancasila'
        elif awal>=13 and akhir<=15:
            return 'Matematika I'
        else:
            return 'Tidak Ada'
    elif hari== 'jum':
        if awal>=7 and akhir<=9:
            return 'Bahasa Indonesia'
        elif awal>=13 and akhir<=16:
            return 'Struktur Diskrit'
        else:
            return 'Tidak Ada'
    else:
        return 'Tidak Ada'
    
print(SearchJadwal('sen',12, 14))
print(SearchJadwal('sel',13, 15))
print(SearchJadwal('rab', 15, 16))
print(SearchJadwal('kam',12, 15))
print(SearchJadwal('jum',8, 9))

#2
print('\n=== BAGI BUAH ===\n')

def Buah(x):
    return 'Bisa' if x%2==0 and x>0 else 'Tidak Bisa'

print(Buah(201))
print(Buah(0))
print(Buah(-4))
print(Buah(6))

#3
#def Aljabar(a,b,c):
def Bagi(x,y):
    return round(x/y, 4)

print(Bagi(2,3))