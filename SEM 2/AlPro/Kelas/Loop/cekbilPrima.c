//Nama File         : cekbilPrima.c
//Deskripsi         : Mengecek apakah bilangan N adalah bilangan prima
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int N; //Masukan bilangan N
    int faktor; //Banyak faktor
    int i; //counter

    //Algoritma
    faktor = 0;
    scanf("%d", &N);
    if (N <= 0){
        printf("Bilangan N harus positif");
    }
    else{
        for (i = 1; i <= N; i++){
            if (N % i == 0){
                faktor = faktor + 1;
            }
            else{ // N mod i <> 0
                faktor = faktor + 0;
            }
        }
        if (faktor > 2){
            printf("%d bukan bilangan prima", N);
        }
        else{//faktor <= 2
            printf("%d bilangan Prima", N);
        }
    }
}