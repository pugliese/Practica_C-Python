import numpy as np
import matplotlib.pylab as plt
import sys


filename = sys.argv[2]
file = open(filename,"r")

if (sys.argv[1]=="j"):
    fs = file.readline()
    fs = fs[2:len(fs)-1]
    fs = fs.split(" ")
    Os = file.readline()
    Os = Os[2:len(Os)-1]
    Os = Os.split(" ")
    Npart = int(file.readline()[1:])
    data = np.loadtxt(filename,delimiter=",")*2/(Npart*(Npart-1))
    file.close()
    N = (len(fs)+1)*len(Os)
    X = range(N)
    Y = []
    Yerr = []
    labels = []
    for i in range(len(Os)):
        labels.append("O"+Os[i]+":")
        Y.append(0)
        Yerr.append(0)
        for j in range(len(fs)):
            Y.append(data[2*i,j])
            Yerr.append(data[2*i+1,j])
            labels.append(fs[j])
    plt.bar(X,Y,yerr = Yerr)
    plt.axis([0,N,0,np.max(np.max(data))*1.05])
    plt.xticks(X,labels)
    plt.grid()
    plt.ylabel("Tiempo por par [s]")
if (sys.argv[1]=="e"):
    params = file.readline()
    params = params.split(", ")
    Npart_bas = int(params[0])
    Nstat = int(params[1])
    Niter = []
    for i in range(2, len(params)):
        Niter.append(int(params[i]))
    data = np.loadtxt(filename,delimiter=",",skiprows=1)
    Npart_it = len(data[0,:])
    Npart = Npart_bas**np.array(range(Npart_it))
    leyenda = []
    fig = plt.figure()
    ax = plt.axes()
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Cantidad de particulas")
    ax.set_ylabel("Tiempo por iteracion [s]")
    formatos = [".", "c", "^", "s", "v", "*"]
    for i in range(len(Niter)):
        n = Niter[i]
        plt.errorbar(Npart, data[2*i,:]/n, yerr=data[2*i+1,:]/n, fmt=formatos[i]+"-")
        leyenda.append(r'$N_{iter} = $' + str(n))
    plt.legend(leyenda)
    plt.title(r'$N_{stat} = $'+str(Nstat))
    plt.grid()
    file.close()
if (sys.argv[1]=="i"):
    Os = file.readline()
    Os = Os.split(", ")
    data = np.loadtxt(filename,delimiter=",",skiprows=1)
    Npart = (len(data[0,:])-1)/3
    nfs = len(data[:,0])/3
    distintos = []
    for j in range(nfs):
        for i in range(3):
            if(np.prod(data[j+i*nfs,:]==data[j,:])==False):
                distintos.append([i,j])
    print distintos
plt.show()
