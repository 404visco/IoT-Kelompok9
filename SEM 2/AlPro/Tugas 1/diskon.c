#include <stdio.h>

int main(){
    int total;
    char metode;
    printf("Total belanja:\n");
    scanf("%d", &total);
    printf("Metode: (C = Cash, K = Kredit)\n");
    scanf(" %c", &metode);  

    if (total >= 1000000){
        if (metode == 'K'){
            printf("Diskon: 15%%");
        }
        else{
            printf("Diskon: 10%%");
        }
    }
    else if (total >= 500000 && total <= 999999){
        printf("Diskon: 5%%");
    }
    else{
        printf("Tidak diberikan output");
    }

}