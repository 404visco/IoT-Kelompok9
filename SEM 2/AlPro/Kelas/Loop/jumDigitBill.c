//Nama File         : jumDigitBill.c
//Deskripsi         : Menghitung jumlah digit dan penjumlahan digit.
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Sabtu, 7 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int N; //bilangan integer bebas
    int digit; //jumlah  digit
    int sumdigit; //penjumlahan digit

    digit = 0;
    printf("Masukkan bilangan N sembarang: \n");
    scanf("%d", &N);

    if (N <= 0) {
        printf("Bilangan harus > 0\n");
        return 0;
    }
    else{
        sumdigit = 0;
        while (N > 0) {
            sumdigit += N % 10;
            N /= 10;
            digit++;
        }
    }
    printf("Digit: %d\n", digit);
    printf("Sum Digit: %d", sumdigit);
}