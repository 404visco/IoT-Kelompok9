/*namaHari*/
/*{Mengubah masukan keyboard 1 - 7, menjadi hari senin-minggu}*/

#include <stdio.h>

int main(){
/*Kamus*/
    int key;
    

/*Algoritma*/
    printf("Masukkan key: ");
    scanf("%d", &key);
    if  (key >= 1 && key <=7){
        if (key == 1){
            printf("Senin");
        }
        else if (key == 2){
            printf("Selasa");
        }
        else if (key == 3){
            printf("Rabu");
        }
        else if (key == 4){
            printf("Kamis");
        }
        else if (key == 5){
            printf("Jumat");
        }
        else if (key == 6){
            printf("Sabut");
        }
        else{
            printf("Minggu");
        }
    }
    else{
        printf("Bukan nama hari");
    }
}