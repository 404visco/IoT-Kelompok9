//Nama File         : cekSempurna.c
//Deskripsi         : Mengecek apakah bilangan N adalah bilangan sempurna
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int N; //Masukan bilangan N
    int sumfaktor; //jumlahan faktor
    int i; //Counter
    
    //Algoritma
    scanf("%d", &N);

    sumfaktor = 0;
    if (N <=0){
        printf("Bilangan N harus positif");
    }
    else{// N > 0
        for (i = 1; i <N; i++){
            if (N % i == 0){
                sumfaktor = sumfaktor + i;
            }
            else{ // N % i <> 0
                sumfaktor = sumfaktor + 0;
            }
        }
        if (sumfaktor == N){
            printf("%d adalah bilangan sempurna", N);
        }
        else{ // sumfaktor <> N
            printf("%d bukan bilangan sempurna", N);
        }
    }
}