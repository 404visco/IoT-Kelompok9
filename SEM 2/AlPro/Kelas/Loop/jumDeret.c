//Nama File         : jumDeret.c
//Deskripsi         : Menjumlahkan deret 1/1 sampai 1/N.
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    float jum; //jumlah deret
    int N; //masukan bilangan N
    int i; //counter

    //Algoritma
    jum = 0;
    
    printf("Masukkan bilangan N: \n");
    scanf("%d", &N);
    if (N <=0){
        printf("Bilangan N harus positif\n");
    }
    else{ //N > 0
        for (i = 1; i <=N; i++){
            jum = jum + 1.0/i;
        }
        printf("Jumlah deret = %f", jum);
    }
}