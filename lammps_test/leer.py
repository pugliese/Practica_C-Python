import numpy as np
import matplotlib.pylab as plt
import sys

def histograma_piola(data, x_lab, titulo, indice):
    plt.figure(indice)
    plt.grid()
    plt.hist(data, 30)
    plt.xlabel(x_lab)
    plt.ylabel("Ocurrencias")
    plt.title(titulo)
    m = np.mean(data)
    s = np.std(data)
    plt.axvline(x=m, color="k")
    plt.axvline(x=m+s, color="r")
    plt.axvline(x=m-s, color="r")
    orden = np.floor(np.log(s)/np.log(10))
    m /= 10**orden
    s /= 10**orden
    plt.legend([r'$\mu$=%.1fE%d'%(m, orden) + '\n' + r'$\sigma$=%1.1fE%d'%(s,orden)])

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

  if (sys.argv[1]=='t2'):
    n_skip = 0
    dataFile = open(sys.argv[2])
    line = dataFile.readline()
    params = line.split(" ")
    Npart, L, Nterm, Nportemp = int(params[1]), float(params[2]), int(params[3]), int(params[4])
    line = dataFile.readline()
    params = line.split(" ")
    T = np.array([float(params[i]) for i in range(1,len(params))])
    if (len(sys.argv)==4):
      n_skip = int(sys.argv[3])
    data = np.loadtxt(sys.argv[2], delimiter = ' ')
    plt.grid()
    E = data[Nterm:, 1]
    mean_E = [np.mean(E[i*Nportemp+n_skip:(i+1)*Nportemp]) for i in range(len(T))]
    var_E = [np.std(E[i*Nportemp+n_skip:(i+1)*Nportemp]) for i in range(len(T))]
    plt.errorbar(T, mean_E, var_E, fmt="b.")
    m, b = np.polyfit(T, mean_E, 1)
    plt.plot(np.sort(T), np.sort(T)*m+b, "r-")
    plt.axis([0,11,-30000,-18000])
    print(m, b)
    plt.show()

  if (sys.argv[1]=='h'):
    n_skip = 0
    dataFile = open(sys.argv[2])
    line = dataFile.readline()
    params = line.split(" ")
    Npart, L, Nterm, Nportemp = int(params[1]), float(params[2]), int(params[3]), int(params[4])
    line = dataFile.readline()
    params = line.split(" ")
    T = np.array([float(params[i]) for i in range(1,len(params))])
    if (len(sys.argv)==4):
      n_skip = int(sys.argv[3])
    data = np.loadtxt(sys.argv[2], delimiter = ' ')
    T2 = data[Nterm:, 0]
    E = data[Nterm:, 1]
    E_sep = [np.array(E[i*Nportemp+n_skip:(i+1)*Nportemp]) for i in range(len(T))]
    T_sep = [np.array(T2[i*Nportemp+n_skip:(i+1)*Nportemp]) for i in range(len(T))]
    med = len(T)//2
    histograma_piola(E_sep[0], "Energia", "T="+str(T[0]), 1)
    histograma_piola(E_sep[med], "Energia", "T="+str(T[med]), 2)
    histograma_piola(E_sep[-1], "Energia", "T="+str(T[-1]), 3)
    histograma_piola(T_sep[0], "2Ecin/3N", "T="+str(T[0]), 4)
    histograma_piola(T_sep[med], "2Ecin/3N", "T="+str(T[med]), 5)
    histograma_piola(T_sep[-1], "2Ecin/3N", "T="+str(T[-1]), 6)
    """
    plt.figure(1)
    plt.grid()
    plt.hist(E_sep[0], 30)
    plt.xlabel("Energía")
    plt.ylabel("Ocurrencias")
    plt.title("T="+str(T[0]))
    plt.figure(2)
    plt.grid()
    plt.hist(E_sep[-1], 30)
    plt.xlabel("Energía")
    plt.ylabel("Ocurrencias")
    plt.title("T="+str(T[-1]))
    plt.figure(3)
    plt.grid()
    plt.hist(E_sep[len(T)//2], 30)
    plt.xlabel("Energía")
    plt.ylabel("Ocurrencias")
    plt.title("T="+str(T[len(T)//2]))
    plt.figure(4)
    plt.grid()
    plt.hist(T_sep[0], 30)
    plt.xlabel("2Ecin/3N")
    plt.ylabel("Ocurrencias")
    plt.title("T="+str(T[0]))
    plt.figure(5)
    plt.grid()
    plt.hist(T_sep[-1], 30)
    plt.xlabel("2Ecin/3N")
    plt.ylabel("Ocurrencias")
    plt.title("T="+str(T[-1]))
    plt.figure(6)
    plt.grid()
    plt.hist(T_sep[len(T)//2], 30)
    plt.xlabel("2Ecin/3N")
    plt.ylabel("Ocurrencias")
    plt.title("T="+str(T[len(T)//2]))
    """
    plt.show()
