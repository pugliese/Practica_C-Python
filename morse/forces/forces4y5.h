#ifndef F4_H
#define F4_H

#include "math.h"
void pair_force(float r, float* delta_r, float mexp, float D,
              float alpha, float* force);
float pair_energ(float energy_cut, float mexp, float D);
inline float pair_force_mod(float r, float mexp, float D, float alpha);
float forces4(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);
float forces5(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);
#endif
