//Nama File         : sumGanjilGenap.c
//Deskripsi         : Menjumlahkan N bilangan. Dengan aturan, pada waktu bilangan genap, jumlahan +3. jika ganjil, jumlahan +2
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int N; //Masukan bilangan N
    int i; //Counter
    int sum; //Jumlah Ganjil Genap
    
    sum = 0;

    printf("Masukkan bilangan N: \n");
    scanf("%d", &N);
    if (N > 0){
        for (i = 1; i <= N; i++){
            if (i % 2 == 0){
                sum = sum + (i + 3);
            }
            else{//bilangan ganjil
                sum = sum + (i + 2);
            }
        }
    }
    else{ //N<=0
        printf("Bilangan harus positif");
    }
    printf("Jumlah ganjil genap : %d", sum);
}