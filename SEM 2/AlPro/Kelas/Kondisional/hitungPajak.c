//Nama File         : hitungPajak.c
//Deskripsi         : menghitung besarnya pajak penghasilan
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Minggu, 1 Maret 2026

#include <stdio.h>

int main(){
    //Kamus
    int gajibulan; //gaji kotor diterima per bulan
    char status; //status pernikahan M=Menikah B=Belum
    int anak; //jumlah anak
    float pajak; //besarnya pajak per bulan
    float penghasilan; //penghasilan bersih setelah dikurangi pajak

    //Algoritma
    printf("Gaji: ");
    scanf("%d", &gajibulan);

    printf("Status (M = menikah, B = Belum): ");
    scanf(" %c", &status);
    
    printf("Jumlah anak: ");
    scanf("%d", &anak);

    if (gajibulan < 5000000){
        pajak = gajibulan*0.05;
    }
    else if (gajibulan >= 5000000 && gajibulan <= 10000000){
        if (status == 'M'){
            pajak = gajibulan*0.10;
        }
        else{ //status == 'B'
            pajak = gajibulan*0.12;
        }
    }
    else{ //gajibulan>100000000
        if (anak>=2){
            pajak = gajibulan*0.15;
        }
        else{ //anak>2
            pajak = gajibulan*0.12;
        }
    }
    penghasilan = gajibulan - pajak;

    printf("Penghasilan bersih: %.2f\n", penghasilan);
    printf("Pajak: %.2f\n", pajak);
}