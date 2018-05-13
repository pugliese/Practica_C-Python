#include "morse_pot.h"

float forces(float *x, long int* pairs, long int npairs,
  float alpha,float D, float req, float rcut, float *force){

  float energy = 0;
  float energy_cut = (1-exp(-alpha*(rcut-req)));
  energy_cut = D*energy_cut*energy_cut;

  for (int l = 0; l < npairs; l++) {
    float delta_r[3];
    int i = pairs[2*l];
    int j = pairs[2*l+1];

    for (int k = 0; k < 3; k++) {
      delta_r[3] = x[3*i+k]-x[3*j+k];
    }

    float r = 0;
    for (int k = 0; k < 3; k++) {
      r = r + delta_r[k]*delta_r[k];
    }
    r = sqrt(r);

    if (r<rcut) {
      float mexp = exp(-alpha*(r-req));
      float m_force = -2*alpha*D*(1-mexp)*mexp/r;
      for(int k=0;k<3;k++){
        force[3*i+k] = force[3*i+k] + m_force*delta_r[k];
        force[3*j+k] = force[3*j+k] - m_force*delta_r[k];
      }
      energy = energy + D*(1-mexp)*(1-mexp) - energy_cut;
    }
  }

  return energy;

}

// OPCIONES DESACOPLADAS
float pair_energ(float energy_cut, float mexp, float D){

  return D*(1-mexp)*(1-mexp) - energy_cut;

}

inline void pair_force(float r, float* delta_r, float mexp, float D,
  float alpha, float* force){

  float m_force = -2*D*alpha*(1-mexp)*mexp/r;
  for(int k=0;k<3;k++){
    force[k] = m_force*delta_r[k];
  }

  return;

}

// OPCION DEVOLVIENDO SOLO MODULO DE FUERZA
float pair_force_mod(float r, float mexp, float D, float alpha){

  return -2*D*alpha*(1-mexp)*mexp/r;

}

// OPCION COMBINADA SIN PARAMETROS
float pair_force_energ_sin_param(float r, float* delta_r, float req, float D,
      float alpha, float* force){

  float mexp = exp(-alpha*(r-req));
  float m_force = -2*alpha*D*(1-mexp)*mexp/r;
  for(int k=0;k<3;k++){
    force[k] = m_force*delta_r[k];
  }
  return D*(1-mexp)*(1-mexp);

}

// OPCION COMBINADA CON PARAMETROS
float pair_force_energ_con_param(float r, float delta_r, float mexp, float D,
      float alpha, float* force){

  float m_force = -2*alpha*D*(1-mexp)*mexp/r;
  for(int k=0;k<3;k++){
    force[k] = m_force*delta_r[k];
  }
  return D*(1-mexp)*(1-mexp);

}



// Cuestiones:
// 1) ¿Donde calculo r y chequeo con rcut?
// 2) ¿Donde calculo mexp?
// 3) Combinando ambas funciones, me ahorro calcular las cosas
//    de arriba 2 veces; util en forces, un poco menos en python.
// 4) Si las paso por parametro, gran parte de las cuentas se
//    hacen fuera de la funcion.
// 5) ¿Devuelvo un vector de fuerzas o modifico uno dado?
//    Devolver lo hace mejor en python pero peor en C.
