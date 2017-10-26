#include<stdio.h>

int main() {
    char *name[] = {"Follow Me", "BASIC", "Great Wall", "FORTRAN", "Computer design"};
    char **p;
    int i;
    for (i=0; i<5; i++) {
        p = name + i;
        printf("%s\n", *p);
    }

    int a[] = {1,3,5,7,9};
    int **pi;
    int * num[] = {&a[0], &a[1], &a[2], &a[3], &a[4]};
    pi = num;
    for (i=0; i<5; i++) {
        printf("%d\t", **pi);
        pi ++;
    }
    printf("\n");
    return 0;
}
