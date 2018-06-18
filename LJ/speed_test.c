#include "speed_test.h"
#include <stdio.h>
#include <time.h>
#include <unistd.h>

// OPCION DE FORCES2
float pair_energ(float r6inv, float lje1, float lje2){

  return r6inv * (lje1 * r6inv - lje2);

}

float pair_force_mod(float r2inv, float r6inv, float ljf1, float ljf2){

  return r2inv * r6inv * (ljf1 * r6inv - ljf2);

}

// OPCION DE FORCES3

float pair_energ_2(float rsq, float energy_cut, float eps, float sigma){

  float lje1 = 4 * eps * pow(sigma, 12);
  float lje2 = 4 * eps * pow(sigma, 6);
  float r2inv = sigma*sigma/rsq;    // 1/r2 en unidades de sigma
  float r6inv = r2inv*r2inv*r2inv;  // 1/r6 en unidades de sigma
  return r6inv * (lje1 * r6inv - lje2);// - energy_cut;
  //return 4*eps*r6inv * (r6inv - 1) - energy_cut;

}

float pair_force_mod_2(float rsq, float eps, float sigma){

  float ljf1 = 48 * eps * pow(sigma, 12);
  float ljf2 = 24 * eps * pow(sigma, 6);
  float r2inv = sigma*sigma/rsq;    // 1/r2 en unidades de sigma
  float r6inv = r2inv*r2inv*r2inv;  // 1/r6 en unidades de sigma
  return r2inv * r6inv * (ljf1 * r6inv - ljf2);
  //return 24*eps*r6inv *(2*r6inv - 1)/rsq;

}


// Sin funciones aparte
float forces1(float *x, long int* pairs, long int npairs, float eps,
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
      float forcelj = r2inv * r6inv * (ljf1 * r6inv - ljf2);
      float energlj = r6inv * (lje1 * r6inv - lje2) - energcut;
      for (int k = 0; k < 3; k++) {
        force[3*i + k] += forcelj * delr[k];
        force[3*j + k] -= forcelj * delr[k];
      }
      energ += energlj;
    }
  }
  return energ;
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

// Desacopladas, devuelve modulo, encapsula potencial y calcula energy_cut 1 vez
float forces3(float *x, long int* pairs, long int npairs, float eps,
              float sigma, float rcut, float *force) {

  float energy = 0;
  float energy_cut = 0;
  float rcutsq = rcut*rcut;
  energy_cut = pair_energ_2(rcutsq, energy_cut, eps, sigma);

  for (int l = 0; l < npairs; l++) {
    float delta_r[3];
    int i = pairs[2*l];
    int j = pairs[2*l+1];

    for (int k = 0; k < 3; k++) {
      delta_r[k] = x[3*i+k]-x[3*j+k];
    }

    float rsq = 0;
    for (int k = 0; k < 3; k++) {
      rsq = rsq + delta_r[k]*delta_r[k];
    }

    if (rsq<rcutsq) {
      float mod_force = pair_force_mod_2(rsq, eps, sigma);
      for (int k = 0; k < 3; k++){
        force[3*i+k] += mod_force*delta_r[k];
        force[3*j+k] -= mod_force*delta_r[k];
      }
      //energy += pair_energ_2(rsq, energy_cut, eps, sigma);
      energy += pair_energ_2(rsq, 0, eps, sigma) - energy_cut;
    }
  }

  return energy;

}
