//Nama File         : bonusKinerja.c
//Deskripsi         : menghitung besarnya bonus kinerja berdasarkan gaji pokok, lama kerja, dan status
//Pembuat           : Visco Argatha Tawa Tawa
//Tanggal Pembuatan : Minggu, 1 Maret 2026
#include <stdio.h>

int main(){
    //Kamus
    int kinerja; //nilai kinerja 0 ... 100
    int gajipokok; //besarnya gajipokok
    int lama; //lama kerja dalam tahun
    char status; //T = Pegawai Tetap, K = Kontrak
    float bonus; //besarnya bonus

    //Algoritma
    printf("Nilai Kinerja: ");
    scanf("%d", &kinerja);

    printf("Besar gaji pokok: ");
    scanf(" %d", &gajipokok);
    
    printf("Lama Kerja (Tahun): ");
    scanf(" %d", &lama);

    printf("Status (T = Tetap, K = Kontrak): ");
    scanf(" %c", &status);

    if (kinerja>=0 && kinerja<=100){
        if (kinerja >= 90){
            if (lama >= 5){
                if (status == 'T'){
                    bonus = gajipokok * 0.35;
                }
                else{ //status == 'K
                    bonus = gajipokok * 0.25;
                }
            }
            else{ //lama<5
                bonus = gajipokok * 0.20;
            }
        }
        else if(kinerja >= 80 && kinerja <90){
            if (lama >= 3){
                bonus = gajipokok * 0.15;
            }
            else{ //lama<3
                bonus = gajipokok * 0.10;
            }
        }
        else if (kinerja >= 70 && kinerja <80){
            bonus = gajipokok * 0.05;
        }
        else{ //kinerja < 70
            bonus = 0;
        }
        printf("Bonus Kinerja = %2.f", bonus);
    }
    else{ //kinerja <0 OR kinerja > 100
        printf("Nilai kinerja  hanya 0 s/d 100\n");
    }
}