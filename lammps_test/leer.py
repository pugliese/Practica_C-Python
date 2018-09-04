import numpy as np
import matplotlib.pylab as plt
import sys

if (len(sys.argv)==0):
  print("Error: Falta nombre del archivo")
else:
  if (sys.argv[1]=='a'):
    filename = sys.argv[2]
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

  if (sys.argv[1]=='t'):
    n = 0
    if (len(sys.argv)==4):
      n = int(sys.argv[3])
    data = np.loadtxt(sys.argv[2], delimiter = ' ')
    plt.figure(1)
    plt.grid()
    T = data[n:, 0]
    E = data[n:, 1]
    plt.plot(T, '.--')
    plt.ylabel('Temperatura')
    plt.figure(2)
    plt.grid()
    plt.plot(E, '.--')
    plt.ylabel('Energia')
    plt.figure(3)
    plt.grid()
    plt.xlabel('Temperatura')
    plt.ylabel('Energia')
    plt.plot(T, E, 'b.')
    m, b = np.polyfit(T, E, 1)
    plt.plot(np.sort(T), np.sort(T)*m+b, "r-")
    print(m, b)
    plt.show()
