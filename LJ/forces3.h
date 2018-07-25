#ifndef LJ_H
#define LJ_H

#include "math.h"

inline float pair_energ_2(float rsq, float energy_cut, float eps, float sigma);
inline float pair_force_mod_2(float rsq, float eps, float sigma);

float forces3(float *x, long int* pairs, long int npairs, float eps,
             float sigma, float rcut, float *force);
#endif
