import sys
import numpy as np
import matplotlib.pylab as plt
import itertools as it
from datetime import datetime
sys.path.insert(0, '../../pexmd/pexmd/box')
sys.path.insert(1, '../../pexmd/pexmd/integrator')
#sys.path.insert(2, '../../pexmd/pexmd/interaction')
sys.path.insert(3, '../../pexmd/pexmd/neighbour')
sys.path.insert(4, '../../pexmd/pexmd/particles')

import Particles
import Integrator
import morse
import thermostat
import Box
import Neighbour

def particulas(Npart,L):
  x = np.zeros((Npart,3), dtype=np.float32)
  n3 = int(np.ceil(Npart**(1.0/3)))
  i = 0
  for p in it.product(range(n3),range(n3),range(n3)):
    if Npart <= i:
      break
    x[i, :] = np.array(p)*L/n3
    i += 1
  return x

def energia_cinetica(v):
  return 0.5*sum(sum(v**2))


if (sys.argv[1]=="e"):
  # Inicializo parametros
  # Caja
  L = 2
  bx = Box.Box([0, 0, 0], [L, L, L], "Fixed")
  # Particulas
  Npart = sys.argv[2]
  N = sys.argv[3]
  part = Particles.PointParticles(Npart)
  pos = particulas(Npart,L)
  part.x = pos
  part.mass = np.zeros((Npart,1), dtype=np.float32) + 1
  # Interaccion
  morse = morse.Morse(1.1, 1, 0.2, 0.25)
  # Integrador
  verlet = Integrator.VelVerlet(0.01)
  # Vecinos
  vecinos = Neighbour.Neighbour()
  pares = vecinos.build_list(part.x, "None")

  # Termalizamos
  Epot = np.zeros(N)
  Ecin = np.zeros(N)
  part.f, Epot[0] = morse.forces(part.x,part.v)
  for i in range(N):
    part.x, part.v = verlet.first_step(part.x, part.v, part.f)
    bx.wrap_boundary(part.x,part.v)
    part.f, Epot[i] = morse.forces(part.x,part.v, pares)
    part.x, part.v = verlet.last_step(part.x, part.v, part.f)
    Ecin[i] = energia_cinetica(part.v)
    part.f, Epot[i] = morse.forces(part.x,part.v, pares)

    part.f, Epot[N-1] = morse.forces(part.x,part.v, pares)

    print(part.f)

    plt.plot(Epot,"-b")
    plt.plot(Ecin, "-r")
    plt.plot(Ecin+Epot, "-g")
    plt.show()

if (sys.argv[1]=="t"):
	# Inicializo parametros
	# Temperaturas
  To = float(sys.argv[2])
  T_step = float(sys.argv[3])
  N_temp = int(sys.argv[4])
  Npart = int(sys.argv[5])
  N_samp = int(sys.argv[6])
  # Caja
  L = 6.3496
  bx = Box.Box([0, 0, 0], [L, L, L], "Fixed")
  # Particulas
  part = Particles.PointParticles(Npart)
  pos = particulas(Npart,L)
  part.x = pos
  part.v = np.random.normal(0,np.sqrt(To*1.5),(Npart,3))
  part.mass = np.zeros((Npart,1), dtype=np.float32) + 1
  # Interaccion
  morse = morse.Morse(2.5, 1.0, 0.5, 1.0)
  # Integrador
  verlet = Integrator.VelVerlet(0.005)
  # Vecinos
  vecinos = Neighbour.Neighbour()
  pares = vecinos.build_list(part.x, part.t)
  # Termostato
  therm = thermostat.Andersen(To, 0.05, 1)

  Nportemp = int(N_samp*0.8/N_temp)
  Nterm = N_samp - Nportemp*N_temp
  t0 = datetime.now()
  dataFile= open("data.txt", "w")
  for i in range(Nterm):
    part.x, part.v = verlet.first_step(part.x, part.v, part.f)
    bx.wrap_boundary(part.x, part.v)
    part.f, Epot = morse.forces(part.x, part.v, pares)
    part.x, part.v = verlet.last_step(part.x, part.v, part.f)
    part.v = therm.step(part.v, part.mass)
    Ecin = energia_cinetica(part.v)
    dataFile.write("%f %f\n" %(2*Ecin/(3*Npart), Ecin+Epot))
  print("Terminada termalizacion: %d" %Nterm)
  for i in range(N_temp):
    therm.temperature = To - i * T_step
    print(i)
    for j in range(Nportemp):
      part.x, part.v = verlet.first_step(part.x, part.v, part.f)
      bx.wrap_boundary(part.x, part.v)
      part.f, Epot = morse.forces(part.x, part.v, pares)
      part.x, part.v = verlet.last_step(part.x, part.v, part.f)
      part.v = therm.step(part.v, part.mass)
      Ecin = energia_cinetica(part.v)
      dataFile.write("%f %f\n" %(2*Ecin/(3*Npart), Ecin+Epot))
  dataFile.close()
  t1 = datetime.now()
  print((t1-t0).total_seconds())

if (sys.argv[1]=="t2"):
	# Inicializo parametros
	# Temperaturas
  temperaturas = np.linspace(10,1,19)
  Npart = 512
  N_samp = 100000
  # Caja
  L = 6.3496
  bx = Box.Box([0, 0, 0], [L, L, L], "Fixed")
  # Particulas
  part = Particles.PointParticles(Npart)
  pos = particulas(Npart,L)
  part.x = pos
  part.v = np.random.normal(0,np.sqrt(temperaturas[0]*1.5),(Npart,3))
  part.mass = np.zeros((Npart,1), dtype=np.float32) + 1
  # Interaccion
  morse = morse.Morse(2.5, 1.0, 0.5, 1.0)
  # Integrador
  verlet = Integrator.VelVerlet(0.005)
  # Vecinos
  vecinos = Neighbour.Neighbour()
  pares = vecinos.build_list(part.x, part.t)
  # Termostato
  therm = thermostat.Andersen(temperaturas[0], 0.05, 1)

  N_temp = len(temperaturas)
  Nportemp = int(N_samp*0.8/N_temp)
  Nterm = N_samp - Nportemp*N_temp
  t0 = datetime.now()
  dataFile = open("data.txt", "w")
  dataFile.write('# %d %f %d %d\n' %(Npart, L, Nterm, Nportemp))
  formato = '#'
  for t in temperaturas:
      formato += ' ' + str(t)
  dataFile.write(formato+"\n")
  for i in range(Nterm):
    part.x, part.v = verlet.first_step(part.x, part.v, part.f)
    bx.wrap_boundary(part.x, part.v)
    part.f, Epot = morse.forces(part.x, part.v, pares)
    part.x, part.v = verlet.last_step(part.x, part.v, part.f)
    part.v = therm.step(part.v, part.mass)
    Ecin = energia_cinetica(part.v)
    dataFile.write("%f %f\n" %(2*Ecin/(3*Npart), Ecin+Epot))
  print("Terminada termalizacion: %d" %Nterm)
  for Temp in temperaturas:
    therm.temperature = Temp
    print(Temp)
    for j in range(Nportemp):
      part.x, part.v = verlet.first_step(part.x, part.v, part.f)
      bx.wrap_boundary(part.x, part.v)
      part.f, Epot = morse.forces(part.x, part.v, pares)
      part.x, part.v = verlet.last_step(part.x, part.v, part.f)
      part.v = therm.step(part.v, part.mass)
      Ecin = energia_cinetica(part.v)
      dataFile.write("%f %f\n" %(2*Ecin/(3*Npart), Ecin+Epot))
  dataFile.close()
  t1 = datetime.now()
  print((t1-t0).total_seconds())
