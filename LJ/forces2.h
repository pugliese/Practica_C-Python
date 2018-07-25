#ifndef LJ_H
#define LJ_H

#include "math.h"
inline float pair_energ(float r6inv, float lje1, float lje2);
inline float pair_force_mod(float r2inv, float r6inv, float ljf1, float ljf2);

float forces2(float *x, long int* pairs, long int npairs, float eps,
             float sigma, float rcut, float *force);

#endif
