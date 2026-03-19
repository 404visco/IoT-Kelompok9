//Nama File         : kelipatanX.c
//Deskripsi         : Mengecek apakah suatu bilangan integer i merupakan kelipatan 5
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Minggu, 1 Maret 2026

#include <stdio.h>

int main(){
 //Kamus
    int i; //Bilangan integer i
 //Algoritma
    printf("Masukkan bilangan integer sembarang:\n", i);
    scanf("%d", &i);

    if (i % 5 == 0){
        printf("%d adalah kelipatan 5\n", i);
    }

    return 0;
}