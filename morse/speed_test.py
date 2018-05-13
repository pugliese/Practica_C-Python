import numpy as np
import matplotlib.pylab as plt
import sys

O0 = np.array([217, 311, 306, 315, 233])
O1 = np.array([147, 159, 157, 173, 146])
O2 = np.array([276, 315, 283, 299, 279])/2
O3 = np.array([184, 131, 131, 130, 183])/2
Ofast = np.array([268, 78, 78, 78, 267])/4

flags = ["O0","O1","O2","O3","Ofast"]

data = np.array([O0,O1,O2,O3,Ofast])

if (sys.argv[1]=="f"):
    for i in range(0,5):
        plt.figure(i+1)
        plt.title("Implementacion "+str(i+1))
        plt.xlabel("Flag")
        plt.ylabel("Tiempo cada 1E9 iteraciones [s]")
        plt.bar(flags,data[:,i])
if (sys.argv[1]=="i"):
    for i in range(0,5):
        plt.figure(i+1)
        plt.title("-"+flags[i])
        plt.xlabel("Implementacion")
        plt.ylabel("Tiempo cada 1E9 iteraciones [s]")
        plt.bar(range(1,6),data[i,:])
plt.show()
