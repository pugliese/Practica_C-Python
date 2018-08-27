import numpy as np
import itertools as it
import ctypes as ct

class Interaction(object):
  """
  Base Interaction class.
  """
  def __init__(self):
    pass

  def forces(self, x, v, pairs=None):
    """
    Main loop calculation.
    NOTE: This is highly experimental and slow.
    It is just meant to be a proof of concept for the main loop, but
    has to change *dramatically*, even in arity, when we want to add
    lists of neighbors, parallelization and so on.
    """
    return np.zeros_like(x), 0.0

class ShortRange(Interaction):
  """
  Base short-range class
  """
  def __init__(self, rcut, shift_style='None'):
    """
    Base short-range class
    Parameters
    ----------
    rcut : float
        The cut radius parameter
    shift_style: {'None', 'Displace', 'Splines'}
        Shift style when approaching rcut
    .. note:: 'Splines' not implemented yet
    """
    self.rcut = rcut
    self.shift_style = shift_style
    super().__init__()

  def forces(self, x, v, pairs=None):
    """
    Calculate Lennard-Jones force
    """
    energ = 0
    forces = np.zeros_like(x)
    if pairs is None:
      pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
    for i, j in pairs:
      f = self.pair_force(x[i], x[j])
      energ += self.pair_energ(x[i], x[j])
      forces[i] += f
      forces[j] -= f
    return forces, energ

  def pair_force(self, s1, s2):
    return np.array([0, 0, 0], dtype=np.float32)

  def pair_energ(self, s1, s2):
    return 0.0

mor = ct.CDLL('./morse_pot.so')

morseforces_c = mor.forces
morseforces_c.argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
morseforces_c.restype = ct.c_float

morsepairforce_c = mor.pair_force
morsepairforce_c.argtypes = [ct.c_float, ct.c_float, ct.c_float, ct.c_float]
morsepairforce_c.restype = ct.c_float

morsepairenergy_c = mor.pair_energ
morsepairenergy_c.argtypes = [ct.c_float, ct.c_float, ct.c_float, ct.c_float, ct.c_float]
morsepairenergy_c.restype = ct.c_float

class Morse(ShortRange):
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
    mf = morsepairforce_c(d, self.req, self.D, self.alpha)*(s1-s2)/d
    if self.shift_style == 'None':
      return mf
    elif self.shift_style == 'Displace':
      return mf

  def pair_energ(self, s1, s2):
    d = np.linalg.norm(s1-s2)      # Distance
    if d >= self.rcut:
      return 0
    if self.shift_style == 'None':
      vcut = 0
    elif self.shift_style == 'Displace':
      vcut = morsepairenergy_c(self.rcut, 0, self.req, self.D, self.alpha)
    me = morsepairenergy_c(d, vcut, self.req, self.D, self.alpha)
    return me
