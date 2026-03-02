/*kabisat*/
/*{Mengecek apakah suatu tahun merupakan tahun kabisat}*/
#include <stdio.h>

int main(){
/*Kamus*/
    int Y;  /*Tahun Y*/
/*Algoritma*/
    printf("Masukkan tahun bebas:\n");
    scanf("%d", &Y);

    if ( Y % 4 == 0){
        printf("%d adalah tahun kabisat", Y);
    }
    else{
        printf("%d bukan tahun kabisat", Y);
    }
    return 0;
}