#ifndef F9_H
#define F9_H

#include "math.h"

inline float pair_force_mod_3(float r, float req, float D, float alpha);
inline float pair_energ_3(float r, float energy_cut, float req, float D, float alpha);

float forces9(float *x, long int* pairs, long int npairs,
              float alpha,float D, float req, float rcut, float *force);

#endif
