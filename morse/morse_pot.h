#ifndef LJ_H
#define LJ_H

#include "math.h"
float* pair_force(float delta_r, float D, float alpha, float* force);
float pair_energ(float energy_cut, float mexp, float D);
float pair_force_energ(float delta_r, float D, float alpha, float* force);
float forces(float *x, long int* pairs, long int npairs, float alpha,
             float D, float req, float rcut, float *force);
#endif
