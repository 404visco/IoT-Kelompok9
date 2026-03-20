//Nama File         : faktorialBill.c
//Deskripsi         : Menghitung N Faktorial.
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int N; //Masukan bilangan N
    int i; //Counter
    int faktorial; //hasil faktorial
    
    faktorial = 1;

    printf("Masukkan bilangan N: ");
    scanf("%d", &N);
    if (N >= 0){
        if (N == 0){
            faktorial = faktorial;
        }
        else{ //N >0
            for (i = 1; i <= N; i++){
                faktorial = faktorial * i;
            }
        }
        printf("Hasil Faktorial: %d", faktorial);
    }
    else{ //N < 0
        printf("Bilangan N harus >=0");
    }
}