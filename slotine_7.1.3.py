import math
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as chart

gamma = 20
eta = 0.3

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x

def model(t, X):
    x1 = X[0]
    x2 = X[1]

    #unknown model paramter
    a = abs(math.sin(t)) + 1

    #desired trajectories
    x_d = math.sin(math.pi*t/2)
    x_ddot = (math.pi/2)*math.cos(math.pi*t/2)
    x_dddot = -((math.pi/2)**2)*math.sin(math.pi*t/2)

	#sliding surface
    s = (x2 - x_ddot) + gamma*(x1 - x_d)

	#control input
    u = -2*(x1**2)*abs(math.cos(3*x1))*sign(s) - eta*sign(s) + x_dddot - gamma*(x2 - x_ddot)

	#dynamics
    x1dot = x2
    x2dot = -a*x2*math.cos(3*x1) + u

    Xdot = [x1dot, x2dot]

    error.append(x1 - x_d)
    return Xdot

X0 = [0, 0]
t0 = 0
t1 = 300
dt = 0.1

error = []
t = []

r = ode(model).set_integrator('vode', method = 'bdf')
r.set_initial_value(X0, t0)

#basic check to see if integrator working
while r.successful() and r.t < t1:
    r.integrate(r.t+dt)
	Y.append(r.y)

print(Y)

#chart.plot(error)
#chart.grid()
#chart.show()
