//Nama File         : sumBil.c
//Deskripsi         : Menghitung dan menampilkan jumlahan bilangan N. Proses penjumlahan diakhiri jika yang dimasukan adalah nilai 999, dan nilai 999 tidak ikut dijumlahkan. 
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int N; //Masukan bilangan N
    int jumlah; //Hasil penjumlahan bilangan N

    //Algoritma
    jumlah = 0;
    do {
        printf("N = ");
        scanf(" %d", &N);

        if (N != 999){
            jumlah = jumlah + N;
        }
    } while(N != 999);

    printf("Sum N: %d", jumlah);
}