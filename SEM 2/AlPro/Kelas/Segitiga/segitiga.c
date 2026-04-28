#include<stdio.h>

void bintang(int n){
    //Kamus
    int i; //counter

    //Algoritma
    for (i = 1; i <= n; i++){
        printf("*");
    }
}

void spasi(int n){
    //Kamus
    int i;

    //Algoritma
    for (i = 1; i <= n; i++){
        printf(" ");
    }
}

// 1. Segitiga siku kiri
void segitiga_siku_kiri(int sisi){
    //Kamus
    int i; //counter

    //Algoritma
    for (i = 1; i <= sisi; i++){
        bintang(i);
        printf("\n");
    }
}

// 2. Segitiga siku kiri terbalik
void segitiga_siku_kiri_terbalik(int sisi){
    //Kamus
    int i; //counter

    //Algoritma
    for (i = sisi; i >= 1; i--){
        bintang(i);
        printf("\n");
    }
}

// 3. Segitiga siku kanan
void segitiga_siku_kanan(int sisi){
    //Kamus
    int i; //counter

    //Algoritma
    for (i = 1; i <= sisi; i++){
        spasi(sisi - i);
        bintang(i);
        printf("\n");
    }
}

// 4. Segitiga siku kanan terbalik
void segitiga_siku_kanan_terbalik(int sisi){
    //Kamus
    int i; //counter

    //Algoritma
    for (i = sisi; i >= 1; i--){
        spasi(sisi - i);
        bintang(i);
        printf("\n");
    }
}

// 5. Segitiga sama sisi (piramida)
void segitiga_samasisi(int sisi){
    //Kamus
    int i; //counter

    //Algoritma
    for (i = 1; i <= sisi; i++){
        spasi(sisi - i);
        bintang(2*i - 1);
        printf("\n");
    }
}

// 6. Segitiga sama sisi terbalik
void segitiga_samasisi_terbalik(int sisi){
    //Kamus
    int i; //counter

    //Algoritma
    for (i = sisi; i >= 1; i--){
        spasi(sisi - i);
        bintang(2*i - 1);
        printf("\n");
    }
}

// 7. Diamond
void ketupat(int sisi){
    //Kamus
    int i; //counter

    //Algoritma

    // atas
    for (i = 1; i <= sisi; i++){
        spasi(sisi - i);
        bintang(2*i - 1);
        printf("\n");
    }

    // bawah
    for (i = sisi - 1; i >= 1; i--){
        spasi(sisi - i);
        bintang(2*i - 1);
        printf("\n");
    }
}

// 8. Ketupat kosong
void ketupat_kosong(int sisi){
    //Kamus
    int i, j; //counter

    //Algoritma

    // atas
    for (i = 1; i <= sisi; i++){
        spasi(sisi - i);
        for (j = 1; j <= 2*i - 1; j++){
            if (j == 1 || j == 2*i - 1){
                printf("*");
            } else {
                printf(" ");
            }
        }
        printf("\n");
    }

    // bawah
    for (i = sisi - 1; i >= 1; i--){
        spasi(sisi - i);
        for (j = 1; j <= 2*i - 1; j++){
            if (j == 1 || j == 2*i - 1){
                printf("*");
            } else {
                printf(" ");
            }
        }
        printf("\n");
    }
}

// 9. Gunung (Sama sisi x2)
void gunung(int sisi){
    //Kamus
    int i; //counter

    //Algoritma
    for (i = 1; i <= sisi; i++){
        
        // gunung kiri
        spasi(sisi - i);
        bintang(2*i - 1);

        // spasi tengah
        spasi(2*(sisi - i) + 1);

        // gunung kanan
        bintang(2*i - 1);

        printf("\n");
    }
}


int main(){
    //Kamus
    int sisi; //Masukan sisi

    //Algoritma
    printf("Masukkan sisi: ");
    scanf("%d", &sisi);

    printf("\n1. Segitiga siku kiri:\n");
    segitiga_siku_kiri(sisi);

    printf("\n2. Segitiga siku kiri terbalik:\n");
    segitiga_siku_kiri_terbalik(sisi);

    printf("\n3. Segitiga siku kanan:\n");
    segitiga_siku_kanan(sisi);

    printf("\n4. Segitiga siku kanan terbalik:\n");
    segitiga_siku_kanan_terbalik(sisi);

    printf("\n5. Segitiga sama sisi:\n");
    segitiga_samasisi(sisi);

    printf("\n6. Segitiga sama sisi terbalik:\n");
    segitiga_samasisi_terbalik(sisi);

    printf("\n7. Ketupat:\n");
    ketupat(sisi);

    printf("\n8. Ketupat kosong:\n");
    ketupat_kosong(sisi);

    printf("\n9. Gunung:\n");
    gunung(sisi);
}
