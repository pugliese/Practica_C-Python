#include morse_pot.h

float forces(float *x, long int* pairs, long int npairs, float alpha,float D, float req, float rcut, float *force){
  float energy = 0;
  float energy_cut = (1-exp(-alpha*(rcut-req)));
  energy_cut = D*energy_cut*energy_cut;

  for(int l=0;l<npairs;l++){
    float delta_r[3];
    int i = npairs[2*l];
    int j = npairs[2*l+1];

    for(int k=0;k<3;k++){
      delta_r[3] = x[3*i+k]-x[3*j+k];
    }

    float r = 0;
    for(int k=0;k<3;k++){
      r = r + delta_r*delta_r;
    }
    r = sqrt(r);

    if (r<rcut){
      float mexp = exp(-alpha*(r-req));
      float m_force = -2*alpha*D*(1-mexp)*mexp/r;
      for(int k=0;k<3;k++){
        force[3*i+k] = force[3*i+k] + m_force*delta_r[k];
        force[3*j+k] = force[3*j+k] - m_force*delta_r[k];
      }
      energy = energy + D*(1-2*mexp+mexp*mexp) - energy_cut;
    }
  }

  return energy;

}
