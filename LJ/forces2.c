#include "forces2.h"
#include <stdio.h>
#include <time.h>
#include <unistd.h>

float pair_energ(float r6inv, float lje1, float lje2){

  return r6inv * (lje1 * r6inv - lje2);

}

float pair_force_mod(float r2inv, float r6inv, float ljf1, float ljf2){

  return r2inv * r6inv * (ljf1 * r6inv - ljf2);

}

// Desacopladas, devuelve modulo
float forces2(float *x, long int* pairs, long int npairs, float eps,
              float sigma, float rcut, float *force) {
  float energ = 0.0;
  float ljf1 = 48 * eps * pow(sigma, 12);
  float ljf2 = 24 * eps * pow(sigma, 6);
  float lje1 = 4 * eps * pow(sigma, 12);
  float lje2 = 4 * eps * pow(sigma, 6);
  float rcutsq = rcut * rcut;
  float energcut = pow(rcutsq, -3) * (lje1 * pow(rcutsq, -3) - lje2);
  for (int ii = 0; ii < npairs; ii++) {
    float delr[3];
    long int i = pairs[2*ii];
    long int j = pairs[2*ii + 1];

    for (int k = 0; k < 3; k++) {
      delr[k] = x[3*i + k] - x[3*j + k];
    }

    float rsq = 0.0;
    for (int k = 0; k < 3; k++) {
      rsq += delr[k] * delr[k];
    }
    if (rsq < rcutsq) {
      float r2inv = 1.0/rsq;
      float r6inv = r2inv * r2inv * r2inv;
      float forcelj = pair_force_mod(r2inv, r6inv, ljf1, ljf2);
      for (int k = 0; k < 3; k++) {
        force[3*i + k] += forcelj * delr[k];
        force[3*j + k] -= forcelj * delr[k];
      }
      energ += pair_energ(r6inv, lje1, lje2)- energcut;
    }
  }
  return energ;
}
