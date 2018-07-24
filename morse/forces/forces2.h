#ifndef F2_H
#define F2_H

#include "math.h"

inline float pair_force_energ_con_param(float r, float* delta_r, float req, float D,
      float alpha, float* force);

float forces2(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);

#endif
