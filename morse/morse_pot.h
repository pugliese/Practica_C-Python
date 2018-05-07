#ifndef LJ_H
#define LJ_H

#include "math.h"
void pair_force1(float r, float* delta_r, float mexp, float D,
              float alpha, int i, int j, float* force)
void pair_force2(float r, float* delta_r, float mexp, float D,
              float alpha, float* force);
float pair_energ(float energy_cut, float mexp, float D);
float pair_force_energ1(float r, float delta_r, float req, float D,
              float alpha, int i, int j, float* force);
float pair_force_energ2(float r, float delta_r, float req, float D,
                    float alpha, float* force);
float forces(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);
#endif
