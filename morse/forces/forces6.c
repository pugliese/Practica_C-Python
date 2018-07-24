#include "forces6.h"
#include <stdio.h>
#include <time.h>
#include <unistd.h>

float pair_energ_2(float r, float rcut, float req, float D, float alpha){

  float mexp = exp(-alpha*(r-req));
  float energy_cut = exp(-alpha*(rcut-req));
  return D*(1-mexp)*(1-mexp) - energy_cut;

}

float pair_force_mod_2(float r, float req, float D, float alpha){

  float mexp = exp(-alpha*(r-req));
  return -2*D*alpha*(1-mexp)*mexp/r;

}

// Desacopladas, devuelve modulo, encapsula potencial
float forces6(float *x, long int* pairs, long int npairs,
  float alpha,float D, float req, float rcut, float *force){

  float energy = 0;

  for (int l = 0; l < npairs; l++) {
    float delta_r[3];
    int i = pairs[2*l];
    int j = pairs[2*l+1];

    for (int k = 0; k < 3; k++) {
      delta_r[k] = x[3*i+k]-x[3*j+k];
    }

    float r = 0;
    for (int k = 0; k < 3; k++) {
      r = r + delta_r[k]*delta_r[k];
    }
    r = sqrt(r);

    if (r<rcut) {
      float m_force = pair_force_mod_2(r,req,D,alpha);
      for (int k = 0; k < 3; k++){
        force[3*i+k] += m_force*delta_r[k];
        force[3*j+k] -= m_force*delta_r[k];
      }
      energy += pair_energ_2(r,rcut,req,D,alpha);
    }
  }

  return energy;

}
