import matplotlib.pyplot as chart
import numpy as np
from scipy.integrate import ode
from scipy.integrate import odeint
import math

##### define lambda and eta #####
gamma = 10
eta = 0.3
m_cap = 7
c_cap = 3

##### gets time-dependant model params #####
def getParams(t, X):
	x1, x2 = X

	m = 3 + 1.5*math.sin(abs(x2)*t)
	c = 1.2 + 0.2*math.sin(abs(x2)*t)

	return [m, c]

##### gets desired trajectory#####
def getDesiredTraj(t):
	if t >= 0 and t < 2:
		xd_ddot = 2
		xd_dot = 2*t
		xd = t**2
	
	elif t >= 2 and t < 4:
		xd_ddot = 0
		xd_dot = 4
		xd = 4*(t - 2) + 4

	elif t >= 4 and t <= 6.01:
		xd_ddot = -2
		xd_dot = -2*(t - 4) + 4
		xd = -((t - 4)**2) + 4*(t - 4) + 12
	
	return [xd, xd_dot, xd_ddot]

##### define sliding surface #####
def getSlidingSurface(t, X):
	x1, x2 = X
	
	x_d = getDesiredTraj(t)
	s = x2 - x_d[1] + gamma*(x1 - x_d[0])
	
	return s

##### define signum function #####
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x

##### define model #####
def model(t, X):
	x1, x2 = X
	
	m, c = getParams(t, X)
	s = getSlidingSurface(t, X)
	
	x_d = getDesiredTraj(t)
	u = -m_cap*abs(x_d[2] - gamma*(x2 - x_d[1])) - c_cap*(x2**2) - eta*sign(s)

	x1dot = x2
	x2dot = (u - c*abs(x2)*x2)/m

	return [x1dot, x2dot]

##### solver ####
def simulateSMC():
	X0 = [0, 0]
	t0 = 0
	t1 = 6
	dt = 0.01

	solver = ode(model).set_integrator('dopri5', nsteps= 1000000, method = 'bdf').set_initial_value(X0, t0)
	
	data = np.ones((601, 2))
	i = 0

	while solver.successful() and solver.t < t1:
		solver.integrate(solver.t + dt)
		print(solver.t)	
		X = solver.y
		x_d = getDesiredTraj(solver.t)
		s = getSlidingSurface(solver.t, X)

		u = -m_cap*abs(x_d[2] - gamma*(X[1] - x_d[1])) - c_cap*(X[1]**2) - eta*sign(s)
		error = X[0] - x_d[0]
		
		data[i] = [u, error]
		i = i + 1
	
	return data

data = simulateSMC()

figure = chart.figure()

fig1 = figure.add_subplot(2, 1, 1)
fig1.plot(data[:,0])
fig2 = figure.add_subplot(2, 1, 2)
fig2.plot(data[:,1])
fig1.grid()
fig2.grid()
chart.show()

