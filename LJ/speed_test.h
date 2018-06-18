#ifndef LJ_H
#define LJ_H

#include "math.h"
inline float pair_energ(float r6inv, float lje1, float lje2);
inline float pair_force_mod(float r2inv, float r6inv, float ljf1, float ljf2);

inline float pair_energ_2(float rsq, float energy_cut, float eps, float sigma);
inline float pair_force_mod_2(float rsq, float eps, float sigma);

float forces1(float *x, long int* pairs, long int npairs, float eps,
             float sigma, float rcut, float *force);
float forces2(float *x, long int* pairs, long int npairs, float eps,
             float sigma, float rcut, float *force);
float forces3(float *x, long int* pairs, long int npairs, float eps,
             float sigma, float rcut, float *force);
#endif

/*
1) Sin funciones aparte
2) Desacopladas, devuelve modulo de fuerza, toma parametros
3) Desacopladas, devuelve modulo, encapsula potencial y calcula energy_cut 1 vez
*/
