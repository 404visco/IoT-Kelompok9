//Nama File         : kkonsBiner.c
//Deskripsi         : Konversi desimal ke Biner.
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int N; //Masukan bilangan N>=0
    int biner; //Hasil konversi biner
    int faktor; //pengkali periterasi
    int sisa; // menyimpan nilai 0 atau 1
    
    //Algoritma
    printf("Masukkan Bilangan integer sembarang: ");
    scanf("%d", &N);
    printf("Desimal: %d\n", N); 

    if (N < 0){
        printf("Bilangan N harus >=0");
    }
    else{ //N >=0
        biner = 0;
        faktor = 1;
        do{
            sisa = N % 2;
            biner = biner + (sisa * faktor);
            faktor = faktor * 10;
            N = N /2;
        } while (N > 0);
    }
    printf("Biner: %d\n", biner);

}