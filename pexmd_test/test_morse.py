import sys
import numpy as np
import matplotlib.pylab as plt
import itertools as it
sys.path.insert(0, '../../pexmd/pexmd/box')
sys.path.insert(1, '../../pexmd/pexmd/integrator')
#sys.path.insert(2, '../../pexmd/pexmd/interaction')
sys.path.insert(3, '../../pexmd/pexmd/neighbour')
sys.path.insert(4, '../../pexmd/pexmd/particles')

import Particles
import Integrator
import morse
import Box
import Neighbour
#import pexmd

def particulas(Npart,L):
	x = np.zeros((Npart,3), dtype=np.float32)
	n3 = int(np.ceil(Npart**(1.0/3)))
	i = 0
	for p in it.product(range(n3),range(n3),range(n3)):
		  if Npart <= i:
		      break
		  x[i,:] = np.array(p)*L/n3
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
	Npart = 64
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
	N = 2000
	Epot = np.zeros(N)
	Ecin = np.zeros(N)
	part.f, Epot[0] = morse.forces(part.x,part.v)
	for i in range(N):
		  part.x, part.v = verlet.first_step(part.x, part.v, part.f)
		  bx.wrap_boundary(part.x,part.v)
		  part.f, Epot[i] = morse.forces(part.x,part.v)
		  part.x, part.v = verlet.last_step(part.x, part.v, part.f)
		  Ecin[i] = energia_cinetica(part.v)
		  part.f, Epot[i] = morse.forces(part.x,part.v)

	part.f, Epot[N-1] = morse.forces(part.x,part.v)

	print(part.f)

	plt.plot(Epot,"-b")
	plt.plot(Ecin, "-r")
	plt.plot(Ecin+Epot, "-g")
	plt.show()
if (sys.argv[1]=="t"):
	# Inicializo parametros
	# Temperaturas
	To = 3
	N_temp = 15
	N_samp = 100
	# Caja
	L = 2
	bx = Box.Box([0, 0, 0], [L, L, L], "Fixed")
	# Particulas
	Npart = 216
	part = Particles.PointParticles(Npart)
	pos = particulas(Npart,L)
	part.x = pos
	part.v = np.random.normal(0,np.sqrt(To),(Npart,3))
	part.mass = np.zeros((Npart,1), dtype=np.float32) + 1
	# Interaccion
	morse = morse.Morse(1, 1, 1, 0.25)
	# Integrador
	verlet = Integrator.VelVerlet(0.01)
	# Vecinos
	vecinos = Neighbour.Neighbour()
	pares = vecinos.build_list(part.x, "None")


	# Termalización inicial
	N = 2000
	part.f, Epot = morse.forces(part.x, part.v)
	for i in range(N):
	  part.x, part.v = verlet.first_step(part.x, part.v, part.f)
	  bx.wrap_boundary(part.x, part.v)
	  part.f, Epot = morse.forces(part.x, part.v)
	  part.x, part.v = verlet.last_step(part.x, part.v, part.f)

	# Muestreo
	Etot = np.zeros(N_temp)
	T = np.zeros(N_temp)
	for i in range(N_temp):
		print(i)
		# Termalización intermedia
		for j in range(int(N/50)):
			part.x, part.v = verlet.first_step(part.x, part.v, part.f)
			bx.wrap_boundary(part.x, part.v)
			part.f, Epot = morse.forces(part.x, part.v)
			part.x, part.v = verlet.last_step(part.x, part.v, part.f)
		# Calculo de temperatura
		Ecin = np.zeros(N_samp)
		for j in range(N_samp):
			part.x, part.v = verlet.first_step(part.x, part.v, part.f)
			bx.wrap_boundary(part.x, part.v)
			part.f, Epot = morse.forces(part.x, part.v)
			part.x, part.v = verlet.last_step(part.x, part.v, part.f)
			Ecin[j] = energia_cinetica(part.v)
			Etot[i] += Ecin[j] + Epot
		T[i] = np.mean(Ecin) / (3 * Npart)
		factor2 = 1 - 0.1/(To - i * 0.1)
		part.v = part.v * np.sqrt(factor2)
	Etot = Etot / N_samp

	plt.plot(T,Etot,"-b")
	plt.show()
