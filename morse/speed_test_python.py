import itertools as it
import numpy as np
import matplotlib.pylab as plt
import sys
from datetime import datetime
import ctypes as ct

speed = ct.CDLL('./forces.so')
(speed.forces1).argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
(speed.forces1).restype = ct.c_float
(speed.forces2).argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
(speed.forces2).restype = ct.c_float
(speed.forces3).argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
(speed.forces3).restype = ct.c_float
(speed.forces4).argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
(speed.forces4).restype = ct.c_float
(speed.forces5).argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
(speed.forces5).restype = ct.c_float
(speed.forces6).argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
(speed.forces6).restype = ct.c_float
(speed.forces7).argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
(speed.forces7).restype = ct.c_float
(speed.forces8).argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
(speed.forces8).restype = ct.c_float
(speed.forces9).argtypes = [ct.c_voidp, ct.c_voidp, ct.c_longlong, ct.c_float,
                       ct.c_float, ct.c_float, ct.c_float, ct.c_voidp]
(speed.forces9).restype = ct.c_float

def particulas(Npart):
    x = np.zeros((Npart,3), dtype=np.float32)
    n3 = int(np.ceil(Npart**(1.0/3)))
    i = 0
    for p in it.product(range(n3),range(n3),range(n3)):
        if Npart <= i:
            break
        x[i,:] = np.array(p)*5.0/n3
        i += 1
    return x



def tiempo_iter(fs,Niter,Npart,Nstat=1):
    x = particulas(Npart)
    xp = x.ctypes.data_as(ct.c_voidp)
    pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
    pairsp = pairs.ctypes.data_as(ct.c_voidp)
    dummy_forces = x.copy()
    dummy_forcesp = (dummy_forces).ctypes.data_as(ct.c_voidp)
    prom = np.zeros(len(Niter))
    var = np.zeros(len(Niter))
    f = lambda : eval("speed.forces"+str(fs))(xp,pairsp,len(pairs),1,1,1,100,dummy_forcesp)
    for n in range(len(Niter)):
        print(Niter[n])
        for i in range(Nstat):
            t0 = datetime.now()
            for j in range(Niter[n]):
                f()
            t1 = datetime.now()
            prom[n] += (t1-t0).total_seconds()/Nstat
            var[n] += (t1-t0).total_seconds()**2/Nstat
    var -= prom*prom
    return prom, var


def tiempo_part(fs,Niter,Npart,Nstat=1):
    prom = np.zeros(len(Npart))
    var = np.zeros(len(Npart))
    for n in range(len(Npart)):
        print(Npart[n])
        x = particulas(Npart[n])
        xp = x.ctypes.data_as(ct.c_voidp)
        pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
        pairsp = pairs.ctypes.data_as(ct.c_voidp)
        dummy_forces = x.copy()
        dummy_forcesp = (dummy_forces).ctypes.data_as(ct.c_voidp)
        f = lambda : eval("speed.forces"+str(fs))(xp,pairsp,len(pairs),1,1,1,100,dummy_forcesp)
        for i in range(Nstat):
            t0 = datetime.now()
            for j in range(Niter):
                f()
            t1 = datetime.now()
            prom[n] += (t1-t0).total_seconds()/Nstat
            var[n] += (t1-t0).total_seconds()**2/Nstat
    var -= prom*prom
    return prom,np.sqrt(var)

def comp(Niter,Npart,Nstat=1,fs=range(1,9)):
    prom = np.zeros(len(fs))
    sigma = np.zeros(len(fs))
    x = particulas(Npart)
    xp = x.ctypes.data_as(ct.c_voidp)
    pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
    pairsp = pairs.ctypes.data_as(ct.c_voidp)
    dummy_forces = x.copy()
    dummy_forcesp = (dummy_forces).ctypes.data_as(ct.c_voidp)
    for j in range(len(fs)):
        f = lambda : eval("speed.forces"+str(fs[j]))(xp,pairsp,len(pairs),1,1,1,100,dummy_forcesp)
        #print("forces"+str(fs[j]))
        for i in range(Nstat):
            t0 = datetime.now()
            for k in range(Niter):
                f()
            t1 = datetime.now()
            prom[j] += (t1-t0).total_seconds()/Nstat
            sigma[j] += (t1-t0).total_seconds()**2/Nstat
    sigma -= prom*prom
    sigma = np.sqrt(sigma)
    return prom,sigma

def valor(j,Npart):
    x = particulas(Npart)
    xp = x.ctypes.data_as(ct.c_voidp)
    pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
    pairsp = pairs.ctypes.data_as(ct.c_voidp)
    dummy_forces = x.copy()
    dummy_forcesp = (dummy_forces).ctypes.data_as(ct.c_voidp)
    energia = eval("speed.forces"+str(j))(xp,pairsp,len(pairs),1,1,1,100,dummy_forcesp)
    return energia, dummy_forces



def graf_barras(T):
    #plt.title("Niter="+str(Niter)+" | Npart="+str(Npart)+" | Nstat="+str(Nstat))
    plt.xlabel("Implementacion")
    plt.ylabel("Tiempo [s]")
    plt.bar(range(1,len(T)+1),T)
    plt.show()

nargs = len(sys.argv)
if (1<nargs):
    if sys.argv[1]=="c":
        Niter = int(sys.argv[2])
        Npart = int(sys.argv[3])
        Nstat = int(sys.argv[4])
        filename = sys.argv[5]
        fs = range(1,9)
        if(nargs>6):
            fs = []
            for i in range(6,nargs):
                fs.append(int(sys.argv[i]))
        formato = "%f"
        for i in range(len(fs)-1):
            formato = formato + ", %f"
        formato += "\n"
        file = open(filename, 'a')
        T,T_std = comp(Niter,Npart,Nstat,fs)
        file.write(formato %tuple(T))
        file.write(formato %tuple(T_std))
        file.close()
    if sys.argv[1]=="e":
        Niter = []
        Npart_bas = int(sys.argv[2])
        Npart_it = int(sys.argv[3])
        Nstat = int(sys.argv[4])
        filename = sys.argv[5]
        for i in range(6, nargs):
            Niter.append(int(sys.argv[i]))
        file = open(filename, 'a')
        file.write("%d, %d, %d" %(Npart_bas, Nstat, Niter[0]))
        for i in range(1,len(Niter)):
            file.write(", %d" %Niter[i])
        file.write("\n")
        formato = "%f"
        for i in range(Npart_it):
            formato = formato + ", %f"
        formato += "\n"
        Npart = Npart_bas**np.array(range(Npart_it+1))
        for n in Niter:
            T,T_std = tiempo_part(1,n,Npart,Nstat)
            file.write(formato %tuple(T))
            file.write(formato %tuple(T_std))
        file.close()
    if sys.argv[1]=="i":
        Npart = int(sys.argv[2])
        filename = sys.argv[3]
        file = open(filename, 'a')
        #file.write("%d, %d, %d" %(Npart_bas, Nstat, Niter[0]))
        formato = "%f"
        for i in range(3*Npart):
            formato = formato + ", %f"
        formato += "\n"
        for j in range(1,10):
            E,F = valor(j,Npart)
            data = np.reshape(F,(1,3*Npart))
            data = np.append(data[0],[E])
            file.write(formato %tuple(data))
        file.close()
