#ifndef F8_H
#define F8_H

#include "math.h"

inline float pair_energ_force_mod_2(float r, float req, float D, float alpha,
              float* energy, float energy_cut);

float forces8(float *x, long int* pairs, long int npairs,
              float alpha,float D, float req, float rcut, float *force);

#endif
