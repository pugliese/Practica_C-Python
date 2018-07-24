#ifndef F3_H
#define F3_H

#include "math.h"
inline float pair_force_energ_sin_param(float r, float* delta_r, float mexp, float D,
            float alpha, float* force);
            
float forces3(float *x, long int* pairs, long int npairs, float alpha,
              float D, float req, float rcut, float *force);
#endif
