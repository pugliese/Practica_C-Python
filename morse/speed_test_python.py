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

dt1 = datetime.now()
dt2 = datetime.now()
dt3 = datetime.now()
dt4 = datetime.now()
dt5 = datetime.now()

Niter =  100
Npart =  1000
if (1 < len(sys.argv)):
    Niter = int(sys.argv[1])
    if (2 < len(sys.argv)):
        Npart = int(sys.argv[2])

def tiempo_iter(fs,Niter,Npart,Nstat=1):
    x = np.zeros((Npart,3))
    n3 = np.ceil(Npart**(1/3))
    i = 0
    for p in it.product(range(n3),range(n3),range(n3)):
        if Npart <= i:
            break
        x[i,:] = np.array(p)*5.0/n3
        i += 1
    xp = x.ctypes.data_as(ct.c_voidp)
    pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
    pairsp = pairs.ctypes.data_as(ct.c_voidp)
    dummy_forces = x.copy()
    dummy_forcesp = (dummy_forces).ctypes.data_as(ct.c_voidp)
    prom = np.zeros(len(Niter))
    var = np.zeros(len(Niter))
    f = lambda : eval("speed.forces"+str(fs))(xp,pairsp,len(pairs),1,1,1,10,dummy_forcesp)
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
        x = np.zeros((Npart[n],3))
        n3 = int(np.ceil(Npart[n]**(1/3)))
        print(n3)
        i = 0
        for p in it.product(range(n3),range(n3),range(n3)):
            if Npart[n] <= i:
                break
            x[i,:] = np.array(p)*5.0/n3
            i += 1
        xp = x.ctypes.data_as(ct.c_voidp)
        pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
        pairsp = pairs.ctypes.data_as(ct.c_voidp)
        dummy_forces = x.copy()
        dummy_forcesp = (dummy_forces).ctypes.data_as(ct.c_voidp)
        f = lambda : eval("speed.forces"+str(fs))(xp,pairsp,len(pairs),1,1,1,10,dummy_forcesp)
        for i in range(Nstat):
            t0 = datetime.now()
            for j in range(Niter):
                f()
            t1 = datetime.now()
            prom[n] += (t1-t0).total_seconds()/Nstat
            var[n] += (t1-t0).total_seconds()**2/Nstat
    var -= prom*prom
    return prom,var
