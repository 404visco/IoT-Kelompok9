//Nama File         : diskon.c
//Deskripsi         : menghitung besarnya diskon
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Minggu, 1 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int lama; //lamanya parkir dalam jam
    char jenis; //jenis kendaraan, M = Motor, L = Mobil
    int biaya; //besarnya biaya parkir

    //Algoritma
    printf("Lama parkir: ");
    scanf("%d", &lama);

    printf("Jenis Kendaraan (M = Motor, L = Mobil): ");
    scanf(" %c", &jenis);

    if (jenis == 'M'){
        if (lama <= 2){
            biaya = 3000;
        }
        else if (lama >2 && lama <=24){
            biaya = 3000 + (lama-2)*1500;
        }
        else{ //lama > 24
            biaya = 3000 + (lama-2)*15000 + 25000;
        }
    }
    else{ //jenis == 'L'
        if (lama <= 2){
            biaya = 5000;
        }
        else if (lama > 2 && lama < 24){
            biaya = 5000 + (lama-2)*2500;
        }
        else{ //lama >24
            biaya = 5000 + (lama-2)*2500 +75000;
        }
    }
    printf("Biaya Parkir: %d", biaya);

    return 0;
}