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

	Nportemp = int(N_samp*0.8/N_temp)
	Nterm = N_samp - Nportemp*N_temp

	t0 = datetime.now()
	file = open("data.txt","w")
	for i in range(Nterm):
		part.x, part.v = verlet.first_step(part.x, part.v, part.f)
		bx.wrap_boundary(part.x, part.v)
		part.f, Epot = morse.forces(part.x, part.v, pares)
		part.x, part.v = verlet.last_step(part.x, part.v, part.f)
		Ecin = energia_cinetica(part.v)
		# if ((i+1)%500 == 0):
		# 	print(i+1)
		file.write("%f %f\n" %(Ecin/(3*Npart), Ecin+Epot))
	print("Terminada termalizacion: %d" %Nterm)
	for i in range(N_temp):
		factor2 = 1 - T_step/(To - i * T_step)
		part.v = part.v * np.sqrt(factor2)
		print(i)
		for j in range(Nportemp):
			part.x, part.v = verlet.first_step(part.x, part.v, part.f)
			bx.wrap_boundary(part.x, part.v)
			part.f, Epot = morse.forces(part.x, part.v, pares)
			part.x, part.v = verlet.last_step(part.x, part.v, part.f)
			Ecin = energia_cinetica(part.v)
			file.write("%f %f\n" %(Ecin/(3*Npart), Ecin+Epot))
	file.close()
	t1 = datetime.now()
	print((t1-t0).total_seconds())

	# # Termalización inicial
	# N = 1000
	# part.f, Epot = morse.forces(part.x, part.v)
	# for i in range(N):
	#   part.x, part.v = verlet.first_step(part.x, part.v, part.f)
	#   bx.wrap_boundary(part.x, part.v)
	#   part.f, Epot = morse.forces(part.x, part.v)
	#   part.x, part.v = verlet.last_step(part.x, part.v, part.f)
	# print("Terminada termalizacion")
	#
	# # Muestreo
	# Etot = np.zeros(N_temp)
	# T = np.zeros(N_temp)
	# for i in range(N_temp):
	# 	print(i)
	# 	# Termalización intermedia
	# 	for j in range(int(N/50)):
	# 		part.x, part.v = verlet.first_step(part.x, part.v, part.f)
	# 		bx.wrap_boundary(part.x, part.v)
	# 		part.f, Epot = morse.forces(part.x, part.v)
	# 		part.x, part.v = verlet.last_step(part.x, part.v, part.f)
	# 	# Calculo de temperatura
	# 	Ecin = np.zeros(N_samp)
	# 	for j in range(N_samp):
	# 		part.x, part.v = verlet.first_step(part.x, part.v, part.f)
	# 		bx.wrap_boundary(part.x, part.v)
	# 		part.f, Epot = morse.forces(part.x, part.v)
	# 		part.x, part.v = verlet.last_step(part.x, part.v, part.f)
	# 		Ecin[j] = energia_cinetica(part.v)
	# 		Etot[i] += Ecin[j] + Epot
	# 	T[i] = np.mean(Ecin) / (3 * Npart)
	# 	factor2 = 1 - T_step/(To - i * T_step)
	# 	part.v = part.v * np.sqrt(factor2)
	# Etot = Etot / N_samp
	# file = open("data.txt","w")
	# for i in range(N_temp):
	# 	file.write("%f %f\n" %(T[i], Etot[i]))
