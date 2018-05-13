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

//float tiempo(struct timespec t, struct timespec t0);
#endif
