#ifndef F7_H
#define F7_H

#include "math.h"

inline float pair_energ_force_mod(float r, float rcut, float req, float D, float alpha, float* energy);

float forces7(float *x, long int* pairs, long int npairs,
              float alpha,float D, float req, float rcut, float *force);

#endif
