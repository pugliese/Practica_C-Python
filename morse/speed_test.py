import numpy as np
import matplotlib.pylab as plt
import sys

# O0 = np.array([217, 311, 306, 315, 233])
# O1 = np.array([147, 159, 157, 173, 146])
# O2 = np.array([276, 315, 283, 299, 279])/2
# O3 = np.array([184, 131, 131, 130, 183])/2
# Ofast = np.array([268, 78, 78, 78, 267])/4

O0 = np.array([8.328338, 8.325681, 8.324565, 8.323766, 8.310368])
O1 = np.array([6.182029, 2.320479, 2.438701, 2.357373, 6.895068])
O2 = np.array([5.680205, 1.917866, 1.921345, 0.827395, 6.237666])
O3 = np.array([5.750089, 1.207084, 1.91325, 11.863415, 6.352175])
Ofast = np.array([3.080330, 1.026707, 1.021079, 4.18008, 6.26369])

flags = ["O0","O1","O2","O3","Ofast"]

data = np.array([O0,O1,O2,O3,Ofast])

if (sys.argv[1]=="f"):
    for i in range(0,5):
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
        plt.bar(range(1,6),data[i,:])
plt.show()
