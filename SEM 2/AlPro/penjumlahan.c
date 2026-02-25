#include <stdio.h>

int main()
{
    float a,b;
    float hasil;

    printf("a = ");
    scanf("%f", &a);
     
    printf("b = ");
    scanf("%f", &b);

    hasil = a+b;
    printf("%f + %f = %.2f", a , b, hasil);
}