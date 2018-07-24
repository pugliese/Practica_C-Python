#include "forces2.h"
#include <stdio.h>
#include <time.h>
#include <unistd.h>

float pair_force_energ_con_param(float r, float* delta_r, float mexp, float D,
      float alpha, float* force){

  float m_force = -2*alpha*D*(1-mexp)*mexp/r;
  for (int k = 0; k < 3; k++){
    force[k] = m_force*delta_r[k];
  }
  return D*(1-mexp)*(1-mexp);

}

// Usando F+E (con parametros precalculados)
float forces2(float *x, long int* pairs, long int npairs,
  float alpha,float D, float req, float rcut, float *force){

  float energy = 0;
  float energy_cut = (1-exp(-alpha*(rcut-req)));
  energy_cut = D*energy_cut*energy_cut;

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
      float force_temp[3];
      energy += pair_force_energ_con_param(r,delta_r,req,D,alpha,force_temp);
      for (int k = 0; k < 3; k++){
        force[3*i+k] += force_temp[k];
        force[3*j+k] -= force_temp[k];
      }
      energy -= energy_cut;
    }
  }

  return energy;

}
