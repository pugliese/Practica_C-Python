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
      float force_temp[3];
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

float tiempo(struct timespec t, struct timespec t0){
  return ((long long)t.tv_sec - (long long)t0.tv_sec)+(t.tv_nsec-t0.tv_nsec)*1E-9;
}


int main(int argc, char **argv){
// Parametro; cantidad de iteraciones
  long int N;
  sscanf(argv[1], "%ld", &N);
// Parametros dummies
  float x[9];
  x[0] = 0;
  x[1] = 0;
  x[2] = 0;
  x[3] = 1;
  x[4] = 2;
  x[5] = 3;
  x[6] = -1;
  x[7] = -2;
  x[8] = -3;
  float force[9];
  for (int l = 0; l < 6; l++){
    force[l] = 0;
  }
  long int pairs[4] = {0,1,0,2};

// Corrida principal
// Datos
  int t0,t1,t2,t3,t4,t5;
  t0 = time(NULL);
  for (int l = 0; l < N; l++){
    forces1(x,pairs,2,1,1,1,5,force);
  }
  t1 = time(NULL)-t0;
  t0 = time(NULL);
  for (int l = 0; l < N; l++){
    forces2(x,pairs,2,1,1,1,5,force);
  }
  t2 = time(NULL)-t0;
  t0 = time(NULL);
  for (int l = 0; l < N; l++){
    forces3(x,pairs,2,1,1,1,5,force);
  }
  t3 = time(NULL)-t0;
  t0 = time(NULL);
  for (int l = 0; l < N; l++){
    forces4(x,pairs,2,1,1,1,5,force);
  }
  t4 = time(NULL)-t0;
  t0 = time(NULL);
  for (int l = 0; l < N; l++){
    forces5(x,pairs,2,1,1,1,5,force);
  }
  t5 = time(NULL)-t0;

  printf("%ld: %d %d %d %d %d\n", N, t1, t2, t3, t4, t5);

// // Corrida principal
//   struct timespec t0, t1, t2, t3, t4, t5;
//   int a;
//   a = clock_gettime( CLOCK_REALTIME, &t0);
//   printf( "%d\n", a);
//   for (int l = 0; l < N; l++){
//     forces1(x,pairs,2,1,1,1,5,force);
//   }
//   a = clock_gettime( CLOCK_REALTIME, &t1);
//   printf( "%d\n", a);
//   for (int l = 0; l < N; l++){
//     forces2(x,pairs,2,1,1,1,5,force);
//   }
//   a = clock_gettime( CLOCK_REALTIME, &t2);
//   printf( "%d\n", a);
//   for (int l = 0; l < N; l++){
//     forces3(x,pairs,2,1,1,1,5,force);
//   }
//   a = clock_gettime( CLOCK_REALTIME, &t3);
//   printf( "%d\n", a);
//   for (int l = 0; l < N; l++){
//     forces4(x,pairs,2,1,1,1,5,force);
//   }
//   a = clock_gettime( CLOCK_REALTIME, &t4);
//   printf( "%d\n", a);
//   for (int l = 0; l < N; l++){
//     forces5(x,pairs,2,1,1,1,5,force);
//   }
//   a = clock_gettime( CLOCK_REALTIME, &t5);
//   printf( "%d\n", a);
//
//   printf("%d; %2.9f %2.9f %2.9f %2.9f %2.9f\n", N, tiempo(t1,t0), tiempo(t2,t1), tiempo(t3,t2), tiempo(t4,t3), tiempo(t5,t4));
}
