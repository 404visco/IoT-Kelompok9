#include <stdio.h>

/*kelipatanX*/
/*{Mengecek apakah suatu bilangan integer i merupakan kelipatan 5}*/


int main(){
 /*Kamus*/
    int i; /*Bilangan integer i*/
 /*Algoritma*/
    printf("Masukkan bilangan integer sembarang:\n", i);
    scanf("%d", &i);

    if (i % 5 == 0){
        printf("%d adalah kelipatan 5\n", i);
    }

    return 0;
}