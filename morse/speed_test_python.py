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

x = np.random.random((Npart,3))
xp = x.ctypes.data_as(ct.c_voidp)
pairs = np.array(list(it.combinations(range(len(x)), 2)), dtype=np.int64)
print(len(x))
pairsp = pairs.ctypes.data_as(ct.c_voidp)
dummy_forces = x
dummy_forces = (dummy_forces).ctypes.data_as(ct.c_voidp)

t0 = datetime.now()
for i in range(Niter):
    speed.forces1(xp,pairsp,len(pairs),1,1,1,10,dummy_forces)
t1 = datetime.now()
for i in range(Niter):
    speed.forces2(xp,pairsp,len(pairs),1,1,1,10,dummy_forces)
t2 = datetime.now()
for i in range(Niter):
    speed.forces3(xp,pairsp,len(pairs),1,1,1,10,dummy_forces)
t3 = datetime.now()
for i in range(Niter):
    speed.forces4(xp,pairsp,len(pairs),1,1,1,10,dummy_forces)
t4 = datetime.now()
for i in range(Niter):
    speed.forces5(xp,pairsp,len(pairs),1,1,1,10,dummy_forces)
t5 = datetime.now()

def tiempo(T):
    return T.seconds+T.microseconds*1E-6

print((t1-t0).total_seconds(),(t2-t1).total_seconds(),(t3-t2).total_seconds(),(t4-t3).total_seconds(),(t5-t4).total_seconds())
