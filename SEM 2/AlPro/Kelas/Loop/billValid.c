//Nama File         : billValid.c
//Deskripsi         : Melakukan validasi bahwa bilangan N yang dimasukan berada pada pada range [1 … 50].
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int N; //bilangan sembarang N
    
    //Algoritma
    do{
        printf("Masukkan bilangan sembarang N: \n");
        scanf(" %d", &N);
    } while (!(N >= 1 && N <= 50));
    printf("Bilangan Valid : %d", N);
}