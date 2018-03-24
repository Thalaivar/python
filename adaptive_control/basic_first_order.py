import matplotlib.pyplot as plt
from scipy.integrate import ode
import numpy as np
from numpy import sin

gamma = 2

def model(t, X):
    y, ym, ar_cap, ay_cap = X
    r = 4

    e = y - ym
    u = ar_cap*r + ay_cap*y

    ydot = y + 3*u
    ymdot = -4*ym +4*r
    ar_cap_dot = -gamma*e*r
    ay_cap_dot = -gamma*e*y

    return [ydot, ymdot, ar_cap_dot, ay_cap_dot]

def main():

    X0 = [0, 0, 0, 0]
    t0 = 0
    t1 = 6
    dt = 0.01

    r = ode(model).set_integrator('vode', method='bdf')
    r.set_initial_value(X0, t0)

    x = np.zeros((601, 4))
    t = []
    i = 0

    while r.successful() and r.t < t1:
        r.integrate(r.t + dt)
        x[i] = r.y
        t.append(r.t)
        i += 1

    return x, t

if __name__ == '__main__':
    x, t = main()

    y = np.reshape(x[:,0], (601,))
    ym = np.reshape(x[:,1], (601,))
    ar_cap = np.reshape(x[:,2], (601,))
    ay_cap = np.reshape(x[:,3], (601,))
    ar_ideal = (4/3)*np.ones((601,))
    ay_ideal = -(5/3)*np.ones((601,))

    plt.subplot(211)
    plt.plot(t , y, 'r', t, ym, 'k')
    plt.ylabel('tracking performance')
    plt.grid()

    plt.subplot(212)
    plt.plot(t, ar_cap, 'b', t, ay_cap, 'k', t, ar_ideal, t, ay_ideal)
    plt.ylabel('parameter estimation')
    plt.grid()

    plt.show()
