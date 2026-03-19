//Nama File         : kabisat.c
//Deskripsi         : Mengecek apakah suatu tahun merupakan tahun kabisat
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Minggu, 1 Maret 2026

#include <stdio.h>

int main(){
//Kamus
    int i;  //Tahun i

//Algoritma
    scanf("%d", &i);

    if ( i % 4 == 0){
        printf("Tahun kabisat");
    }
    else{
        printf("Bukan tahun kabisat");
    }
    return 0;
}