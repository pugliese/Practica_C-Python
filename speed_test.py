import numpy as np
import matplotlib.pylab as plt
import sys


filename = sys.argv[2]
file = open(filename,"r")
fs = file.readline()
fs = fs[2:len(fs)-1]
fs = fs.split(" ")
Os = file.readline()
Os = Os[2:len(Os)-1]
Os = Os.split(" ")
Npart = int(file.readline()[1:])
data = np.loadtxt(filename,delimiter=",")*2/(Npart*(Npart+1))
file.close()

if (sys.argv[1]=="f"):
    for i in range(len(fs)):
        plt.figure(i+1)
        plt.title("Implementacion "+str(i+1))
        plt.xlabel("Flag")
        plt.ylabel("Tiempo por par [s]")
        print(range(len(Os)),data[:,i])
        plt.bar(range(len(Os)),data[:,i])
        plt.grid()
        plt.xticks(range(len(Os)), Os)
if (sys.argv[1]=="i"):
    for i in range(len(Os)):
        plt.figure(i+1)
        plt.title("-"+Os[i])
        plt.xlabel("Implementacion")
        plt.ylabel("Tiempo por par [s]")
        plt.bar(range(len(fs)),data[i,:])
        plt.grid()
        plt.xticks(range(len(fs)), fs)
if (sys.argv[1]=="j"):
    N = (len(fs)+1)*len(Os)
    X = range(N)
    Y = []
    labels = []
    for i in range(len(Os)):
        labels.append("O"+Os[i]+":")
        Y.append(0)
        for j in range(len(fs)):
            Y.append(data[i,j])
            labels.append(fs[j])
    plt.bar(X,Y)
    plt.axis([0,N,0,np.max(np.max(data))*1.05])
    plt.xticks(X,labels)
    plt.grid()
    plt.ylabel("Tiempo por par [s]")
plt.show()
