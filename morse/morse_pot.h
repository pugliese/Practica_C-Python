#ifndef LJ_H
#define LJ_H

#include "math.h"
float forces(float *x, long int* pairs, long int npairs, float alpha,
             float D, float req, float rcut, float *force);
#endif
