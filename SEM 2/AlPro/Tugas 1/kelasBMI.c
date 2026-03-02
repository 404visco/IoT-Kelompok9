#include <stdio.h>

/*kelipatanX*/
/*{Mengecek apakah suatu bilangan integer i merupakan kelipatan 5}*/


int main(){
 /*Kamus*/
    float tb; /*Bilangan float tb*/
    float bb; /*Bilangan float bb*/
    float bmi; /*Bilangan float, bmi = bb/(tb*tb) i*/
    
 /*Algoritma*/
    printf("Masukkan tb (meter):\n", tb);
    scanf("%f", &tb);
    printf("Masukkan bb (kg):\n", bb);
    scanf("%f", &bb);

    bmi = bb/(tb*tb);

    if (bmi < 18.5){
        printf("BMI = %f --> Kurus\n", bmi);
    }
    else if (bmi>=18.5 && bmi<=24.9){
        printf("BMI = %f --> Normal\n", bmi);
    }
    else if (bmi>=25 && bmi<=29.9){
        printf("BMI = %f --> Overweight\n", bmi);
    }
    else {
        printf("BMI = %f --> Obesitas\n", bmi);
    }

    return 0;
}