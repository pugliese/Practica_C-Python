import numpy as np
import matplotlib.pylab as plt
import sys

if (len(sys.argv)==0):
  print("Error: Falta nombre del archivo")
else:
  filename = sys.argv[1]
  file = open(filename,"r")
  line = file.readline()
  Ecin = []
  while (line!=""):
    Ecin.append(0)
    while (line!="ITEM: ATOMS type x y z vx vy vz \n"):
      line = file.readline()
    line = file.readline()
    while (line!="ITEM: TIMESTEP\n" and line!=""):
      data = line.split(" ")
      Ecin[-1] += float(data[-2])**2 + float(data[-3])**2 + float(data[-4])**2
      line = file.readline()
    Ecin[-1] /= 2
  T = np.array(Ecin)/(3*4000)
  print(T)
  plt.plot(T, ".--")
  plt.show()
