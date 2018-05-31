#ifndef LJ_H
#define LJ_H

#include "math.h"
void pair_force(float r, float* delta_r, float mexp, float D,
              float alpha, float* force);
float pair_energ(float energy_cut, float mexp, float D);
float pair_force_mod(float r, float mexp, float D, float alpha);
float pair_force_energ_con_param(float r, float* delta_r, float req, float D,
      float alpha, float* force);
float pair_force_energ_sin_param(float r, float* delta_r, float mexp, float D,
            float alpha, float* force);

float forces1(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);
float forces2(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);
float forces3(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);
float forces4(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);
float forces5(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);


float pair_energ_2(float r, float rcut, float req, float D, float alpha);
float pair_force_mod_2(float r, float req, float D, float alpha);
float pair_energ_force_mod(float r, float rcut, float req, float D, float alpha, float* energy);
float pair_energ_force_mod_2(float r, float req, float D, float alpha,
              float* energy, float energy_cut);

float forces6(float *x, long int* pairs, long int npairs,
              float alpha,float D, float req, float rcut, float *force);
float forces7(float *x, long int* pairs, long int npairs,
              float alpha,float D, float req, float rcut, float *force);
float forces8(float *x, long int* pairs, long int npairs,
              float alpha,float D, float req, float rcut, float *force);



#endif

/*
1) Sin funciones aparte
2) F+E con parametros precalculados
3) F+E sin parametros precalculados
4) Desacopladas, devuelve vector fuerza
5) Desacopladas, devuelve modulo de fuerza

6) Desacopladas, devuelve modulo, encapsula potencial
7) F+E, devuelve modulo, encapsula potencial
8) F+E, devuelve modulo, encapsula potencial y calcula energy_cut 1 vez
*/
