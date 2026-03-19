/*kabisat*/
/*{Mengecek apakah suatu tahun merupakan tahun kabisat}*/
#include <stdio.h>

int main(){
/*Kamus*/
    int i;  /*Tahun i*/

/*Algoritma*/
    scanf("%d", &i);

    if ( i % 4 == 0){
        printf("Tahun kabisat");
    }
    else{
        printf("Bukan tahun kabisat");
    }
    return 0;
}