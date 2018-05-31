import numpy as np
import matplotlib.pylab as plt
import sys

# Nstat = 1000, Npart = 216
O0 = [ 0.00166503,0.00184625,0.00184201,0.00194386,0.00185273,0.00268227,0.00195591,0.00171437]
O1 = [ 0.00087411,0.00092488,0.00097287,0.00093948,0.00091262,0.00161048,0.00121704,0.00085452]
O2 = [ 0.00077495,0.00083048,0.00083692,0.00086108,0.00085047,0.0016602,0.001263,0.00087256]
O3 = [ 0.00076989,0.00098125,0.00077068,0.00076879,0.000774,0.00160516,0.00110644,0.00073144]
Ofast = [ 0.00053532,0.00057642,0.00057766,0.00054639,0.00056943,0.00091884,0.0007127, 0.00061924]

O0 = np.array(O0)
O1 = np.array(O1)
O2 = np.array(O2)
O3 = np.array(O3)
Ofast = np.array(Ofast)

flags = ["O0","O1","O2","O3","Ofast"]

data = np.array([O0,O1,O2,O3,Ofast])

if (sys.argv[1]=="f"):
    for i in range(0,8):
        plt.figure(i+1)
        plt.title("Implementacion "+str(i+1))
        plt.xlabel("Flag")
        plt.ylabel("Tiempo [s]")
        plt.bar(flags,data[:,i])
if (sys.argv[1]=="i"):
    for i in range(0,5):
        plt.figure(i+1)
        plt.title("-"+flags[i])
        plt.xlabel("Implementacion")
        plt.ylabel("Tiempo [s]")
        plt.bar(range(1,9),data[i,:])
plt.show()
