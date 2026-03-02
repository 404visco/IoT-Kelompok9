#include <stdio.h>

/*kelipatanX*/
/*{Mengecek apakah suatu bilangan integer i merupakan kelipatan 5}*/


int main(){
 /*Kamus*/
    int tb; /*Bilangan float tb*/
    int bb; /*Bilangan float bb*/
    int bmi; /*Bilangan float, bmi = bb/(tb*tb) i*/
 /*Algoritma*/
    printf("Masukkan tb (meter):\n", tb);
    scanf("%f", &tb);
    printf("Masukkan bb (kg):\n", bb);
    scanf("%f", &bb);

    bmi = bb/(tb*tb);

    if (bmi < 18.5){
        printf("Kurus\n");
    }
    else if (bmi>=18.5 && bmi<=24.9){
        printf("Normal\n");
    }
    else if (bmi>=25 && bmi<=29.9){
        printf("Overweight\n")
    }

    return 0;
}