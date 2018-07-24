#ifndef F6_H
#define F6_H

#include "math.h"
inline float pair_energ_2(float r, float rcut, float req, float D, float alpha);
inline float pair_force_mod_2(float r, float req, float D, float alpha);

float forces6(float *x, long int* pairs, long int npairs,
              float alpha,float D, float req, float rcut, float *force);

#endif
