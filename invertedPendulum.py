import matplotlib.pyplot as chart
import math
import numpy as np
from scipy.integrate import odeint

#define constants
M = 1.5
m = 0.75
l = 1
g = 9.8
gamma = 6
eta = 1.2

#define the dynamics of the system
def f(X, t):
	x1, x2 = X
	
	u = (M*l)/math.sin(x1*math.pi/180)*((g/l)*math.cos(x1*math.pi/180) + gamma*(x1 - 20) - eta*np.sign(x2 + gamma*(x1 - 20)))
	x1dot = x2
	x2dot = u*math.sin(x1)/(M*l) - (g/l)*math.cos(x1)
	
	return [x1dot, x2dot]

#initial conditions
X0 = [90, 0]

t = np.linspace(0, 100)

#solver
X = odeint(f, X0, t)


chart.plot(t, X[0:])
chart.grid()
chart.show()
