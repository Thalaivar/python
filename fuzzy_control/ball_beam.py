import fuzzy_tools as fuzz
import numpy as np
from scipy.integrate import ode
import math
import matplotlib.pyplot as plt

def ball_beam_rule_set(x, y):
    z = np.zeros((5,))
    z1 = 0

    # 0 - NL
    # 1 - NS
    # 2- Z
    # 3- PS
    # 4- PL

    # get firing of rule for output being NL
    for i in range(len(x)):
        z1 += x[0]*y[0]
        z1 += x[0]*y[1]
        z1 += x[0]*y[2]
        z1 += x[1]*y[0]
        z1 += x[1]*y[1]
        z1 += x[2]*y[0]
    z[0] = z1
    z1 = 0

    # get firing of rule for output being NS
    for i in range(len(x)):
        z1 += x[0]*y[3]
        z1 += x[1]*y[2]
        z1 += x[2]*y[1]
        z1 += x[3]*y[0]
    z[1] = z1
    z1 = 0

    # get firing of rule for output being Z
    for i in range(len(x)):
        z1 += x[0]*y[4]
        z1 += x[1]*y[3]
        z1 += x[2]*y[2]
        z1 += x[3]*y[1]
        z1 += x[4]*y[0]
    z[2] = z1
    z1 = 0

    # get firing of rule for output being PS
    for i in range(len(x)):
        z1 += x[1]*y[4]
        z1 += x[2]*y[3]
        z1 += x[3]*y[2]
        z1 += x[4]*y[1]
    z[3] = z1
    z1 = 0

    # get firing of rule of output being PL
    for i in range(len(x)):
        z1 += x[2]*y[4]
        z1 += x[3]*y[3]
        z1 += x[3]*y[4]
        z1 += x[4]*y[2]
        z1 += x[4]*y[3]
        z1 += x[4]*y[4]
    z[4] = z1
    z1 = 0

    return z

def model(t, X, params):
    x1, x2 = X
    e = -x1
    edot = -x2
    e_mem, edot_mem, v_mem = params

    e_fuzz_mem = []
    edot_fuzz_mem = []

    for i in range(len(e_mem)):
        e_fuzz_mem.append(fuzz.fuzzify(e, e_mem[i]))
        edot_fuzz_mem.append(fuzz.fuzzify(edot, edot_mem[i]))

    rule_out = ball_beam_rule_set(e_fuzz_mem, edot_fuzz_mem)

    v = fuzz.defuzzify(rule_out, v_mem, 'CAD')

    x1dot = x2
    x2dot = 9.81*math.sin(0.2*v)

    return [x1dot, x2dot]

def main():
    e_mem = []
    edot_mem = []
    v_mem = []

    e_fuzz_set_1 = [-0.5, -0.5, -0.25]
    e_fuzz_set_2 = [-0.5, -0.25, 0]
    e_fuzz_set_3 = [-0.25, 0.0, 0.25]
    e_fuzz_set_4 = [-0.25, 0.0, 0.25]
    e_fuzz_set_5 = [0.25, 0.5, 0.5]
    e_univ = np.linspace(-1.5, 1.5, 30)

    edot_fuzz_set_1 = [-4, -4, -2]
    edot_fuzz_set_2 = [-4, -2, 0]
    edot_fuzz_set_3 = [-2, 0, 2]
    edot_fuzz_set_4 = [0, 2, 4]
    edot_fuzz_set_5 = [2, 4, 4]
    edot_univ = np.linspace(-5, 5, 10)

    v_fuzz_set_1 = [-10.0]
    v_fuzz_set_2 = [-5.0]
    v_fuzz_set_3 = [0.0]
    v_fuzz_set_4 = [5.0]
    v_fuzz_set_5 = [10.0]
    v_univ = np.linspace(-10, 10, 100)

    e_fuzz_set = [e_fuzz_set_1, e_fuzz_set_2, e_fuzz_set_3, e_fuzz_set_4, e_fuzz_set_5]
    edot_fuzz_set = [edot_fuzz_set_1, edot_fuzz_set_2, edot_fuzz_set_3, edot_fuzz_set_4, edot_fuzz_set_5]
    v_fuzz_set = [v_fuzz_set_1, v_fuzz_set_2, v_fuzz_set_3, v_fuzz_set_4, v_fuzz_set_5]
    names = ['NL', 'NS', 'Z', 'PS', 'PL']
    for i in range(len(edot_fuzz_set)):
        e_mem.append(fuzz.membership('trimf', e_fuzz_set[i], e_univ, names[i]))
        edot_mem.append(fuzz.membership('trimf', edot_fuzz_set[i], edot_univ, names[i]))
        v_mem.append(fuzz.membership('singleton', v_fuzz_set[i], v_univ, names[i]))

    params = [e_mem, edot_mem, v_mem]

    x0 = [-0.12, 1.0]
    t0 = 0
    t1 = 10
    dt = 0.01
    r = ode(model).set_integrator('vode').set_initial_value(x0, t0).set_f_params(params)
    state = np.zeros((1001,2))
    t = []
    i = 0
    while r.successful() and r.t < t1:
        r.integrate(r.t + dt)
        state[i] = r.y
        t.append(r.t)
        i += 1

    plt.plot(t, state[:,0])
    plt.show()

if __name__ == '__main__':
    main()
