//diskon
//Menghitung besarnya diskon belanja

#include <stdio.h>

int main(){
    //Kamus
    int totalbelanja; //{total belanja}
    char jenis; //jenis pembayaran, K = kredit, C = Cash 
    float diskon; //besarnya diskon
    float totbayar; //total pembayaran

    //Algoritma
    printf("Total belanja:\n");
    scanf("%d", &totalbelanja);
    printf("Jenis: (C = Cash, K = Kredit)\n");
    scanf(" %c", &jenis);  

    if (totalbelanja >= 1000000){
        if (jenis == 'K'){
            diskon = totalbelanja*0.15;
            printf("Diskon: 15%%\n");
        }
        else{
            diskon = totalbelanja*0.10;
            printf("Diskon: 10%%\n");
        }
    }
    else if (totalbelanja >= 500000 && totalbelanja <= 999999){
        diskon = totalbelanja*0.05;
        printf("Diskon: 5%%\n");
    }
    else{
        diskon = totalbelanja*0.0;
        printf("Tidak diberikan output\n");
    }
    totbayar = totalbelanja - diskon;

    printf("Total Bayar: %.2f\n", totbayar);
    printf("Diskon: %.2f\n", diskon);

    return 0;
}