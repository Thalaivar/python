import fuzzy_tools as fuzz
from scipy.integrate import ode
import numpy as np
import matplotlib.pyplot as plt
import math

def main():
    e_univ = np.linspace(-2.57, 2.57, 1000)
    e_fuzzy_set_1 = [-1.285, 0.5, 'l_inf']
    e_fuzzy_set_2 = [0, 0.5, 'none']
    e_fuzzy_set_3 = [1.285, 0.5, 'r_inf']

    e_dot_univ = np.linspace(-4.15, 4.15, 1000)
    e_dot_fuzzy_set_1 = [-1.57, 0.5, 'l_inf']
    e_dot_fuzzy_set_2 = [0, 0.5, 'none']
    e_dot_fuzzy_set_3 = [1.57, 0.5, 'r_inf']

    i_univ = np.linspace(-30, 30, 1000)
    i_fuzzy_set_1 = [-15, 0.25, 'none']
    i_fuzzy_set_2 = [0, 0.25, 'none']
    i_fuzzy_set_3 = [15, 0.25, 'none']

    e_fuzz_set = [e_fuzzy_set_1, e_fuzzy_set_2, e_fuzzy_set_3]
    e_dot_fuzz_set = [e_dot_fuzzy_set_1, e_dot_fuzzy_set_2, e_dot_fuzzy_set_3]
    i_fuzz_set = [i_fuzzy_set_1, i_fuzzy_set_2, i_fuzzy_set_3]

    names = ["N", "Z", "P"]

    e_memship = np.zeros((3,), dtype = object)
    e_dot_memship = np.zeros((3,), dtype = object)
    i_memship = np.zeros((3,), dtype = object)
    for i in range(len(e_fuzz_set)):
        e_memship[i] = fuzz.membership('gauss', e_fuzz_set[i], e_univ, names[i])
        e_dot_memship[i] = fuzz.membership('gauss', e_dot_fuzz_set[i], e_dot_univ, names[i])
        i_memship[i] = fuzz.membership('gauss', i_fuzz_set[i], i_univ, names[i])

    params = [e_memship, e_dot_memship, i_memship]
    x0 = [1.57, 0]
    t0 = 0
    t1 = 10
    dt = 0.001
    state = np.zeros((10001,2))
    i = 0
    t= []
    r = ode(model).set_integrator('vode').set_f_params(params).set_initial_value(x0, t0)
    while r.successful() and r.t < t1:
        r.integrate(r.t + dt)
        state[i] = r.y
        t.append(r.t)
        i += 1

    plt.plot(t, state[:,0])
    plt.show()
def rule_set(x, y):

    # 0 - N
    # 1 - Z
    # 2 - P
    z = [0, 0, 0]
    z[0] = x[2]*y[2]
    z[0] += x[2]*y[1]
    z[1] = x[2]*y[0]
    z[0] += x[1]*y[2]
    z[1] += x[1]*y[1]
    z[2] = x[1]*y[0]
    z[1] += x[0]*y[2]
    z[2] += x[0]*y[1]
    z[2] += x[0]*y[0]

    return z

def model(t, X, params):
    x1, x2 = X
    e_memship, e_dot_memship, i_memship = params

    r = (math.pi/2) + math.sin(math.pi*t)
    rdot = math.pi*math.cos(math.pi*t)
    e = x1 - r
    edot = x2 - rdot

    for i in range(len(e_memship)):
        fuzz.fuzzify(e, e_memship[i])
        fuzz.fuzzify(edot, e_dot_memship[i])
    e_fuzz = []
    e_dot_fuzz = []
    for i in range(len(e_memship)):
        e_fuzz.append(e_memship[i].fuzz_val)
        e_dot_fuzz.append(e_dot_memship[i].fuzz_val)

    i_fuzz = rule_set(e_fuzz, e_dot_fuzz)

    i = fuzz.defuzzify(i_fuzz, i_memship, 'CAD')

    x1dot = x2
    x2dot = -64*math.sin(x1) -5*x2 + 4*i

    return [x1dot, x2dot]

if __name__ == '__main__':
    main()
