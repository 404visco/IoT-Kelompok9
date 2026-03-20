//Nama File         : viewBil.c
//Deskripsi         : Buat teks algoritma untuk menampilkan bilangan 1 sampai dengan N. Bilangan N harus positif.
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int i; //counter
    int N; //Masukan bilangan

    //Algoritma
    printf("Masukkan bilangan N: ");
    scanf("%d", &N);
    if (N <= 0){
        printf("N harus Positif!\n");
    }
    else{ //N>0
        for (i = 1; i <= N; i++ ){
            printf("%d ", i);   
        }
    }
}