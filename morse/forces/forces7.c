#include "forces7.h"
#include <stdio.h>
#include <time.h>
#include <unistd.h>

float pair_energ_force_mod(float r, float rcut, float req, float D,
  float alpha, float* energy){

  float mexp = exp(-alpha*(r-req));
  float energy_cut = exp(-alpha*(rcut-req));
  *energy = (float) D*(1-mexp)*(1-mexp) - energy_cut;
  return -2*D*alpha*(1-mexp)*mexp/r;
}

// F+E, devuelve modulo, encapsula potencial
float forces7(float *x, long int* pairs, long int npairs,
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
      float m_force = pair_energ_force_mod(r,rcut,req,D,alpha, &energy);
      for (int k = 0; k < 3; k++){
        force[3*i+k] += m_force*delta_r[k];
        force[3*j+k] -= m_force*delta_r[k];
      }
    }
  }

  return energy;

}
