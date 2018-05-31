#include "speed_test.h"
#include <stdio.h>
#include <time.h>
#include <unistd.h>

// OPCIONES DESACOPLADAS
float pair_energ(float energy_cut, float mexp, float D){

  return D*(1-mexp)*(1-mexp) - energy_cut;

}

inline void pair_force(float r, float* delta_r, float mexp, float D,
  float alpha, float* force){

  float m_force = -2*D*alpha*(1-mexp)*mexp/r;
  for(int k=0;k<3;k++){
    force[k] = m_force*delta_r[k];
  }

  return;

}

// OPCION DEVOLVIENDO SOLO MODULO DE FUERZA
float pair_force_mod(float r, float mexp, float D, float alpha){

  return -2*D*alpha*(1-mexp)*mexp/r;

}

// OPCION DE FORCES6

float pair_energ_2(float r, float rcut, float req, float D, float alpha){

  float mexp = exp(-alpha*(r-req));
  float energy_cut = exp(-alpha*(rcut-req));
  return D*(1-mexp)*(1-mexp) - energy_cut;

}

float pair_force_mod_2(float r, float req, float D, float alpha){

  float mexp = exp(-alpha*(r-req));
  return -2*D*alpha*(1-mexp)*mexp/r;

}

// OPCION DE FORCES7

float pair_energ_force_mod(float r, float rcut, float req, float D,
  float alpha, float* energy){

  float mexp = exp(-alpha*(r-req));
  float energy_cut = exp(-alpha*(rcut-req));
  *energy = (float) D*(1-mexp)*(1-mexp) - energy_cut;
  return -2*D*alpha*(1-mexp)*mexp/r;
}

// OPCION DE FORCES8

float pair_energ_force_mod_2(float r, float req, float D,
  float alpha, float* energy, float energy_cut){

  float mexp = exp(-alpha*(r-req));
  *energy = (float) D*(1-mexp)*(1-mexp) - energy_cut;
  return -2*D*alpha*(1-mexp)*mexp/r;
}

// OPCION COMBINADA SIN PARAMETROS
float pair_force_energ_sin_param(float r, float* delta_r, float req, float D,
      float alpha, float* force){

  float mexp = exp(-alpha*(r-req));
  float m_force = -2*alpha*D*(1-mexp)*mexp/r;
  for (int k = 0; k < 3; k++){
    force[k] = m_force*delta_r[k];
  }
  return D*(1-mexp)*(1-mexp);

}

// OPCION COMBINADA CON PARAMETROS
float pair_force_energ_con_param(float r, float* delta_r, float mexp, float D,
      float alpha, float* force){

  float m_force = -2*alpha*D*(1-mexp)*mexp/r;
  for (int k = 0; k < 3; k++){
    force[k] = m_force*delta_r[k];
  }
  return D*(1-mexp)*(1-mexp);

}


// Sin funciones aparte
float forces1(float *x, long int* pairs, long int npairs,
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
      float mexp = exp(-alpha*(r-req));
      float m_force = -2*alpha*D*(1-mexp)*mexp/r;
      for(int k=0;k<3;k++){
        force[3*i+k] += m_force*delta_r[k];
        force[3*j+k] -= m_force*delta_r[k];
      }
      energy = energy + D*(1-mexp)*(1-mexp) - energy_cut;
    }
  }

  return energy;

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
      energy += pair_force_energ_sin_param(r,delta_r,req,D,alpha,force_temp);
      for (int k = 0; k < 3; k++){
        force[3*i+k] += force_temp[k];
        force[3*j+k] -= force_temp[k];
      }
      energy -= energy_cut;
    }
  }

  return energy;

}


// Usando F+E (sin parametros precalculados)

float forces3(float *x, long int* pairs, long int npairs,
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
      float mexp = exp(-alpha*(r-req));
      energy += pair_force_energ_con_param(r,delta_r,mexp,D,alpha,force_temp);
      for (int k = 0; k < 3; k++){
        force[3*i+k] += force_temp[k];
        force[3*j+k] -= force_temp[k];
      }
      energy -= energy_cut;
    }
  }

  return energy;

}


// Desacopladas, devuelve vector

float forces4(float *x, long int* pairs, long int npairs,
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
      float mexp = exp(-alpha*(r-req));
      pair_force(r,delta_r,mexp,D,alpha,force_temp);
      for (int k = 0; k < 3; k++){
        force[3*i+k] += force_temp[k];
        force[3*j+k] -= force_temp[k];
      }
      energy += pair_energ(energy_cut,mexp,D);
    }
  }

  return energy;

}

// Desacopladas, devuelve modulo

float forces5(float *x, long int* pairs, long int npairs,
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
      float mexp = exp(-alpha*(r-req));
      float m_force = pair_force_mod(r,mexp,D,alpha);
      for (int k = 0; k < 3; k++){
        force[3*i+k] += m_force*delta_r[k];
        force[3*j+k] -= m_force*delta_r[k];
      }
      energy += pair_energ(energy_cut,mexp,D);
    }
  }

  return energy;

}


// Desacopladas, devuelve modulo, encapsula potencial

float forces6(float *x, long int* pairs, long int npairs,
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

// F+E, devuelve modulo, encapsula potencial y calcula energy_cut 1 vez

float forces8(float *x, long int* pairs, long int npairs,
  float alpha,float D, float req, float rcut, float *force){

  float energy = 0;
  float energy_cut = 0;
  pair_energ_force_mod_2(rcut,req,D,alpha, &energy_cut, 0);

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
      float m_force = pair_energ_force_mod_2(r,req,D,alpha, &energy, energy_cut);
      for (int k = 0; k < 3; k++){
        force[3*i+k] += m_force*delta_r[k];
        force[3*j+k] -= m_force*delta_r[k];
      }
    }
  }

  return energy;

}
