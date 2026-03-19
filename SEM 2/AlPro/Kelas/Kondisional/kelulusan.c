/*kelulusan*/
/*{Mengecek apakah seorang mahasiswa lulus berdasarkan persentase kehadiran dan nilai akhir}*/

#include <stdio.h>
 
int main(){
/*Kamus*/
    float hadir;
    float na;

/*Algoritma*/
    printf("Masukkan persentase hadir: ");
    scanf("%f", &hadir);
    printf("Masukkan nilai akhir: ");
    scanf("%f", &na);

    if (hadir >= 75 && na >= 70){
        printf("Lulus");
    }
    else if (hadir >= 75 && na < 70){
        printf("Tidak lulus karena nilai akhir");
    }
    else if (hadir < 75 && na >= 70){
        printf("Tidak lulus karena kehadiran");
    }
    else{
        printf("Tidak lulus karena nilai akhir dan kehadiran");
    }
}