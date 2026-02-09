# Nama File: SearchJadwal.py
# Nama / NIM: Visco Argatha Tawa Tawa / 24060125120023
# Tanggal: 23 September 2025

def SearchJadwal(hari, awal, akhir):
    if hari == "sen":
        if akhir > 13 and awal < 15:
            return "Dasar Pemrograman"
        else:
            return "Tidak ada"

    elif hari == "sel":
        if akhir > 13 and awal < 15:
            return "Aljabar Linier"
        else:
            return "Tidak ada"

    elif hari == "rab":
        if (akhir > 7 and awal < 10) and (akhir > 15 and awal < 16):
            return "Dasar Sistem & Bahasa Inggris I"
        elif akhir > 7 and awal < 10:
            return "Dasar Sistem"
        elif akhir > 15 and awal < 16:
            return "Bahasa Inggris I"
        else:
            return "Tidak ada"

    elif hari == "kam":
        if (akhir > 7 and awal < 9) and (akhir > 13 and awal < 15):
            return "Pancasila & Matematika I"
        elif akhir > 7 and awal < 9:
            return "Pancasila"
        elif akhir > 13 and awal < 15:
            return "Matematika I"
        else:
            return "Tidak ada"

    elif hari == "jum":
        if (akhir > 7 and awal < 9) and (akhir > 13 and awal < 16):
            return "Bahasa Indonesia & Struktur Diskrit"
        elif akhir > 7 and awal < 9:
            return "Bahasa Indonesia"
        elif akhir > 13 and awal < 16:
            return "Struktur Diskrit"
        else:
            return "Tidak ada"

    elif hari == "sab" or hari == "min":
        return "Tidak ada"

    else:
        return "Tidak ada"


#JANGAN DIUBAH!
print(eval(input()))