#ifndef LJ_H
#define LJ_H

#include "math.h"

float forces1(float *x, long int* pairs, long int npairs, float eps,
             float sigma, float rcut, float *force);

#endif
