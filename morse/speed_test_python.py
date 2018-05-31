import itertools as it
import numpy as np
import matplotlib.pylab as plt
import sys
from datetime import datetime
import ctypes as ct

speed = ct.CDLL('./speed_test.so')
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

def particulas(Npart):
    x = np.zeros((Npart,3))
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
    return prom,var

def comp(Niter,Npart,Nstat=1,fs=range(1,9)):
    prom = np.zeros(len(fs))
    x = particulas(Npart)
    xp = x.ctypes.data_as(ct.c_voidp)
    pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
    pairsp = pairs.ctypes.data_as(ct.c_voidp)
    dummy_forces = x.copy()
    dummy_forcesp = (dummy_forces).ctypes.data_as(ct.c_voidp)
    for j in range(len(fs)):
        f = lambda : eval("speed.forces"+str(fs[j]))(xp,pairsp,len(pairs),1,1,1,100,dummy_forcesp)
        print("forces"+str(fs[j]))
        for i in range(Nstat):
            t0 = datetime.now()
            for k in range(Niter):
                f()
            t1 = datetime.now()
            prom[j] += (t1-t0).total_seconds()/Nstat
    return prom

def graf_barras(T):
    #plt.title("Niter="+str(Niter)+" | Npart="+str(Npart)+" | Nstat="+str(Nstat))
    plt.xlabel("Implementacion")
    plt.ylabel("Tiempo [s]")
    plt.bar(range(1,len(T)+1),T)
    plt.show()

if (1<len(sys.argv)):
    Niter = int(sys.argv[1])
    Npart = int(sys.argv[2])
    Nstat = 1
    if(len(sys.argv)==4):
        Nstat = int(sys.argv[3])
    T = comp(Niter,Npart,Nstat)
    print(T)
    plt.title("Niter="+str(Niter)+" | Npart="+str(Npart)+" | Nstat="+str(Nstat))
    plt.xlabel("Implementacion")
    plt.ylabel("Tiempo [s]")
    plt.bar(range(1,9),T)
    plt.show()
