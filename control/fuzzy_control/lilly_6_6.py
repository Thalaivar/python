import fuzzy_tools as fuzz
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import ode
import math

A1 = np.array([[ 0.0,  1],
               [-2, -2]])
A2 = np.array([[ 0.0,  1],
               [-1, -2]])
A3 = np.array([[ 0.0,  1],
               [-3, -2]])
A4 = np.array([[ 1.0,  1],
               [-2, -2]])
A5 = np.array([[ 0.0,  1],
               [-2, -1]])
A6 = np.array([[ 0.0,  1],
               [-1, -2]])
A7 = np.array([[ 0.0,  1],
               [-2, -2]])
A8 = np.array([[-1.0, -1],
               [ 1,  0]])
A9 = np.array([[ 0.0,  1],
               [ 2, -2]])
B1 = np.array([[0.0],
               [2]])
B2 = np.array([[2.0],
               [2]])
B3 = np.array([[-2.0],
               [2]])
B4 = np.array([[0.0],
               [-2]])
B5 = np.array([[0.0],
               [1]])
B6 = np.array([[1.0],
               [1]])
B7 = np.array([[-1.0],
               [1]])
B8 = np.array([[0.0],
               [-1]])
B9 = np.array([[0],
               [1]])
A_i = [A1, A2, A3, A4, A5, A6, A7, A8, A9]
B_i = [B1, B2, B3, B4, B5, B6, B7, B8, B9]

def main():
    x1_univ = np.linspace(-1000, 1000, 10000)
    x1_fuzz_set_1 = [-1, -1, 0]
    x1_fuzz_set_2 = [-1, 0 , 1]
    x1_fuzz_set_3 = [0, 1, 1]
    x2_univ = np.linspace(-1000, 1000, 10000)
    x2_fuzz_set_1 = [-1, -1, 0]
    x2_fuzz_set_2 = [-1, 0 , 1]
    x2_fuzz_set_3 = [0, 1, 1]
    names = ["left", "center", "right"]
    x1_fuzz_set = [x1_fuzz_set_1, x1_fuzz_set_2, x1_fuzz_set_3]
    x2_fuzz_set = [x2_fuzz_set_1, x2_fuzz_set_2, x2_fuzz_set_3]
    x1_fuzz_mem = []
    x2_fuzz_mem = []
    for i in range(len(x1_fuzz_set)):
        x1_fuzz_mem.append(fuzz.membership('trimf', x1_fuzz_set[i], x1_univ, names[i]))
        x2_fuzz_mem.append(fuzz.membership('trimf', x2_fuzz_set[i], x2_univ, names[i]))
    params = [x1_fuzz_mem, x2_fuzz_mem]
    x0 = [0, 0]
    t0 = 0
    t1 = 8
    dt = 0.001
    r = ode(model).set_integrator('vode').set_f_params(params).set_initial_value(x0, t0)
    state = np.zeros((8000, 2))
    t = []
    i = 0
    while r.successful() and r.t < t1:
        r.integrate(r.t + dt)
        state[i] = r.y
        t.append(r.t)
        i += 1
    plt.plot(t, state[:,0], t, state[:,1])
    plt.show()

def get_fuzzy_basis(fuzz_set_1, fuzz_set_2):
    a = len(fuzz_set_1)*len(fuzz_set_2)
    z = np.zeros((a,))
    k = 0
    for i in range(len(fuzz_set_1)):
        for j in range(len(fuzz_set_2)):
            z[k] = fuzz_set_1[i]*fuzz_set_2[j]
            k += 1
    premise_sum = np.sum(z)
    z = z/premise_sum
    return z

def model(t, X, params):
    x1, x2 = X
    x1_fuzz_mem, x2_fuzz_mem = params
    x1_fuzz = []
    x2_fuzz = []
    u = 3*math.sin(math.pi*t)

    for i in range(len(x1_fuzz_mem)):
        fuzz.fuzzify(x1, x1_fuzz_mem[i])
        fuzz.fuzzify(x2, x2_fuzz_mem[i])
    for i in range(len(x1_fuzz_mem)):
        x1_fuzz.append(x1_fuzz_mem[i].fuzz_val)
        x2_fuzz.append(x2_fuzz_mem[i].fuzz_val)
    fuzz_basis = get_fuzzy_basis(x1_fuzz, x2_fuzz)

    A = np.zeros_like(A1)
    B = np.zeros_like(B1)
    i = 0

    for x in fuzz_basis:
        A += A_i[i]*x
        B += B_i[i]*x
        i += 1

    x1dot = A[0,0]*x1 + A[0,1]*x2 + B[0,0]*u
    x2dot = A[1,0]*x1 + A[1,1]*x2 + B[1,0]*u
    return [x1dot, x2dot]

if __name__ == '__main__':
    main()
