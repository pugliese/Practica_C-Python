/* file: arrays.c */
#include <stdio.h>

int add_int_array(int *a, int *b, int *c, int n) {
  int i;
  printf("%d \n", n);
  for (i = 0; i < n; i++) {
    c[i] = a[i] + b[i];
  }
  return 0;
}

float dot_product(float *a, float *b, int n) {
  float res;
  int i;
  res = 0;
  for (i = 0; i < n; i++) {
    res = res + a[i] * b[i];
  }
  return res;
}
