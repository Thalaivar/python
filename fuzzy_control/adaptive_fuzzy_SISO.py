import fuzzy_tools as fuzz
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
import math

def make_fuzzy_sets():
    # define universe of e
    e_univ = np.linspace(-3, 3, 1000)

    # centres and spreads
    c = [-1.5, 0, 1.5]
    sig = 0.484

    # make the fuzzy sets
    names = ["F1", "F2", "F3"]
    memship = []
    for i in range(len(c)):
        p = [c[i], sig, "none"]
        memship.append(fuzz.membership("gauss", p, e_univ, names[i]))

    return memship

def model(t, X, params):
    e = X
    lam, gam, memship = params

    phi = get_fuzzy_basis(e, memship)
    phi_t = np.transpose(phi)

    new_theta = lam*gam*e*phi_t

    u = np.dot(phi_t, new_theta)

    x_dot = ((1 - math.exp(-x))/(1 + math.exp(-x))) + u
    return x_dot

def get_fuzzy_basis(x, memship):
    fuzz_basis = np.zeros((len(memship,)))
    for i in range(len(memship)):
        fuzz.fuzzify(x, memship[i])
        temp[i] = memship[i].fuzz_val
        temp = temp.reshape((5,1))
    return fuzz_basis

def simulate(memship):
    x0 = [0, 0, 0, 0]
    t0 = 0
    dt = 0.01
    t1 = 10

    params = [1.2, 1.2, memship]
    r = ode(model).set_integrator("vode")
    r.set_initial_value(x0, t0).set_f_params(params)

    y = np.zeros((1001,))
    t = []
    i = 0

    while r.successful() and r.t < t1:
        r.integrate(r.t + dt)
        y[i] = r.y
        t.append(r.t)
        i += 1

    return [y, t]

def main():
    memship = make_fuzzy_sets()

    y, t = simulate(memship)

if __name__ == '__main__':
    main()
