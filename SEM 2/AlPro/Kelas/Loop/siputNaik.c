//Nama File         : siputNaik.c
//Deskripsi         : Menghitung berapa hari waktu yang dibutuhkan oleh siput tersebut untuk mencapai ketinggin N meter
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    float N; //Ketinggian N meter di dalam tanah
    int sumhari; //jumlah hari siput naik
    float tinggi; //proggress kenaikan siput

    //Algoritma
    scanf("%f", &N);
    
    sumhari = 0;
    tinggi = 0.0;
    if (N <= 0.0){
        printf("N harus positif");
    }
    else{ // N > 0
        while (tinggi < N){
            sumhari = sumhari +1;
            tinggi = tinggi + 0.2;
        }
        printf("Jumlah hari yang dibutuhkan: %d", sumhari);
    }
}