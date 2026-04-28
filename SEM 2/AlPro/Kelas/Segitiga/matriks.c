#include <stdio.h>

// Tampilkan matriks
void tampil_matriks(int M[3][4]){
    //Kamus
    int i, j;

    //Algoritma
    for (i = 0; i < 3; i++){
        for (j = 0; j < 4; j++){
            printf("%d ", M[i][j]);
        }
        printf("\n");
    }
}

// 1. Input angka → output index
void cari_index(int M[3][4], int x){
    //Kamus
    int i, j, ketemu = 0;

    //Algoritma
    for (i = 0; i < 3; i++){
        for (j = 0; j < 4; j++){
            if (M[i][j] == x){
                printf("Ditemukan di index: [%d][%d]\n", i, j);
                ketemu = 1;
            }
        }
    }

    if (ketemu == 0){
        printf("Angka tidak ditemukan\n");
    }
}

// 2. Input angka → output bulan & kota
void cari_lokasi(int M[3][4], int x){
    //Kamus
    int i, j, ketemu = 0;
    char *bulan[3] = {"Jan", "Feb", "Mar"};
    char *kota[4] = {"Jkt", "Smg", "Bdg", "Sby"};

    //Algoritma
    for (i = 0; i < 3; i++){
        for (j = 0; j < 4; j++){
            if (M[i][j] == x){
                printf("Ditemukan di: %s - %s\n", bulan[i], kota[j]);
                ketemu = 1;
            }
        }
    }

    if (ketemu == 0){
        printf("Angka tidak ditemukan\n");
    }
}

// 3. Rata-rata per bulan
void rata_bulan(int M[3][4]){
    //Kamus
    int i, j;
    float rata;
    char *bulan[3] = {"Jan", "Feb", "Mar"};

    //Algoritma
    for (i = 0; i < 3; i++){
        int sum = 0;
        for (j = 0; j < 4; j++){
            sum += M[i][j];
        }
        rata = sum / 4.0;
        printf("Rata-rata %s = %.2f\n", bulan[i], rata);
    }
}

// 4. Input bulan & kota → output nilai
void cari_nilai(int M[3][4]){
    //Kamus
    int i, j;
    int b, k;
    char *bulan[3] = {"Jan", "Feb", "Mar"};
    char *kota[4] = {"Jkt", "Smg", "Bdg", "Sby"};

    //Algoritma
    printf("Pilih bulan (0=Jan,1=Feb,2=Mar): ");
    scanf("%d", &b);

    printf("Pilih kota (0=Jkt,1=Smg,2=Bdg,3=Sby): ");
    scanf("%d", &k);

    if (b >= 0 && b < 3 && k >= 0 && k < 4){
        printf("Nilai pada %s - %s = %d\n", bulan[b], kota[k], M[b][k]);
    } else {
        printf("Input tidak valid\n");
    }
}

int main(){
    //Kamus
    int M[3][4] = {
        {10, 6, 5, 7},
        {15, 10, 7, 4},
        {12, 10, 8, 3}
    };

    int x;

    //Algoritma
    printf("Matriks:\n");
    tampil_matriks(M);

    printf("\nInput angka untuk cari index: ");
    scanf("%d", &x);
    cari_index(M, x);

    printf("\nInput angka untuk cari bulan & kota: ");
    scanf("%d", &x);
    cari_lokasi(M, x);
    
    printf("\nCari nilai berdasarkan bulan & kota:\n");
    cari_nilai(M);

    printf("\nRata-rata per bulan:\n");
    rata_bulan(M);
}
