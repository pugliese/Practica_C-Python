import numpy as np
import matplotlib.pylab as plt
import sys


filename = sys.argv[2]
file = open(filename,"r")
Os = file.readline()
fs = file.readline()
data = np.loadtxt(filename)

if (sys.argv[1]=="f"):
    for i in range(0,8):
        plt.figure(i+1)
        plt.title("Implementacion "+str(i+1))
        plt.xlabel("Flag")
        plt.ylabel("Tiempo [s]")
        plt.bar(Os,data[:,i])
if (sys.argv[1]=="i"):
    for i in range(0,5):
        plt.figure(i+1)
        plt.title("-"+flags[i])
        plt.xlabel("Implementacion")
        plt.ylabel("Tiempo [s]")
        plt.bar(fs,data[i,:])
plt.show()
