import ctypes as C
import sys
import numpy as np
math = C.CDLL('./mylib.so')

def add_float_py(a,b):
    math.add_float.restype = C.c_float
    return math.add_float(C.c_float(a), C.c_float(b))

def add_int_py(a,b):
    return math.add_int(C.c_int(a), C.c_int(b))

def add_float_ref_py(a, b):
    a_c = C.c_float(a)
    b_c = C.c_float(b)
    res_c = C.c_float()
    math.add_float_ref(C.byref(a_c), C.byref(b_c), C.byref(res_c))
    return res_c.value

def add_int_ref_py(a,b):
    a_c = C.c_int(a)
    b_c = C.c_int(b)
    res_c = C.c_int()
    math.add_int_ref(C.byref(a_c), C.byref(b_c), C.byref(res_c))
    return res_c.value


print add_float_py(3.0,4)
print add_int_py(3,4)
one = int(sys.argv[1]);
two = int(sys.argv[2]);
print add_float_ref_py(float(one),float(two))
print add_int_ref_py(one,two)

def add_int_array_py(a,b):
    intp = C.POINTER(C.c_int)
    n = len(a)
    assert(n==len(b))
    in1 = np.array(a,dtype = C.c_int)
    in2 = np.array(b,dtype = C.c_int)
    out = np.zeros(n,dtype = C.c_int)
    math.add_int_array(in1.ctypes.data_as(intp),in2.ctypes.data_as(intp),out.ctypes.data_as(intp),C.c_int(n))
    return out

def dot_product_py(a,b):
    floatp = C.POINTER(C.c_float)
    n = len(a)
    assert(n==len(b))
    in1 = np.array(a,dtype = C.c_float)
    in2 = np.array(b,dtype = C.c_float)
    math.dot_product.restype = C.c_float
    return math.dot_product(in1.ctypes.data_as(floatp),in2.ctypes.data_as(floatp),C.c_int(n))



print add_int_array_py([1,2,3],[3,2,1])
print dot_product_py([2.0,10.0],[3.0,1.0])
