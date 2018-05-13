import sys
import numpy as np
import matplotlib.pylab as plt
sys.path.insert(0, '../../pexmd/pexmd/box')
sys.path.insert(1, '../../pexmd/pexmd/integrator')
sys.path.insert(2, '../../pexmd/pexmd/interaction')
sys.path.insert(3, '../../pexmd/pexmd/neighbour')
sys.path.insert(4, '../../pexmd/pexmd/particles')

import Particles
import Integrator
import Interaction
import Box
import Neighbour
#import pexmd

# Inicializo parametros

# Particulas
part = Particles.PointParticles(8)
pos = np.array([.5,.5,.5]) + np.array([[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]])
part.x = pos
part.mass = np.zeros((8,1),dtype=np.float32)+1
# Caja
bx = Box.Box([0,0,0],[2,2,2])
# Interaccion
LJ = Interaction.LennardJones(1.2, 1, 0.2)
# Integrador
verlet = Integrator.VelVerlet(0.01)
# Vecinos
vecinos = Neighbour.Neighbour()
pares = vecinos.build_list(part.x,"None")

def energia_cinetica(v):
    return 0.5*sum(sum(v**2))

# Termalizamos
N = 2000
Epot = np.zeros((N,1))
Ecin = np.zeros((N,1))
part.f, Epot[0] = LJ.forces(part.x,part.v)
for i in range(0,N):
    part.x, part.v = verlet.first_step(part.x, part.v, part.f)
    bx.wrap_boundary(part.x,part.v)
    part.f, Epot[i] = LJ.forces(part.x,part.v)
    part.x, part.v = verlet.last_step(part.x, part.v, part.f)
    bx.wrap_boundary(part.x,part.v)
    Ecin[i] = energia_cinetica(part.v)
    part.f, Epot[i] = LJ.forces(part.x,part.v)

part.f, Epot[N-1] = LJ.forces(part.x,part.v)

print(part.f)

plt.plot(Epot,"-b")
plt.plot(Ecin, "-r")
plt.plot(Ecin+Epot, "-g")
plt.show()
