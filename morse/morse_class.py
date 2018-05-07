import numpy as np
import itertools as it
import ctypes as ct

mor = ct.CDLL('./morse_pot.so')
morseforces_c = mor.forces
morseforces_c.argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
morseforces_c.restype = ct.c_float

class Morse():
  """
  Morse potential
  """
  def __init__(self, rcut, alpha, D, req, shift_style='None'):
    self.alpha = alpha
    self.D = D
    self.req = req
    super().__init__(rcut, shift_style)

  def forces(self, x, v, pairs=None):
    """
    Calculate Morse force
    """
    energ = 0
    forces = np.zeros_like(x, dtype=np.float32)
    if pairs is None:
      pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
    xp = x.ctypes.data_as(ct.c_voidp)
    pairsp = pairs.ctypes.data_as(ct.c_voidp)
    forcesp = forces.ctypes.data_as(ct.c_voidp)
    energ = morseforces_c(xp, pairsp, len(pairs), self.alpha, self.D, self.req, self.rcut, forcesp)
    return forces, energ

  def pair_force(self, s1, s2):
    d = np.linalg.norm(s1-s2)
    if d > self.rcut:
      return np.zeros_like(s1)
    mf = -2*self.D*self.alpha*(1-np.exp(-self.alpha*(d-self.req)))*np.exp(-self.alpha*(d-self.req))*(s1-s2)/d
    if self.shift_style == 'None':
      return mf
    elif self.shift_style == 'Displace':
      return mf

  def pair_energ(self, s1, s2):
    vcut = self.D*(1-np.exp(-self.alpha*(self.rcut-self.req)))**2
    d = np.linalg.norm(s1-s2)      # Distance
    if d >= self.rcut:
      return 0
    mf = self.D*(1-np.exp(-self.alpha*(d-self.req)))**2
    if self.shift_style == 'None':
      return mf
    elif self.shift_style == 'Displace':
      return mf - vcut
