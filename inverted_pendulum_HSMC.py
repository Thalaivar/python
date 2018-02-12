import numpy as np
import matplotlib.pyplot as chart
import math
from scipy.integrate import ode

# params_0 = Cc
# params_1 = m
# params_2 = M
# params_3 = L
# params_4 = Cp
# params_5 = g


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


def model(t, X, params):
	
	x1, x2, x3, x4 = X
	
	Cc, m, M, L, Cp, g, l1, l2, gamma, eta = params

	f1 = Cc*x2 - (Cp*x4 + m*g*L*math.sin(x3))*math.cos(x3)/L - m*L*(x4**2)*math.sin(x3)
	g1 = M + m*((math.sin(x3))**2)
	f2 = Cc*x2 - m*L*(x4**2)*math.sin(x3) - Cp*x4*(m+M)/(m*L*math.cos(x3)) - (m*g*L*math.sin(x3)*(m+M))/(m*L*math.cos(x3))
	g2 = -(m+M)*L*(M+m*((math.sin(x3))**2))

	s1 = x2 + l1*x1
	s2 = x4 + l2*x3

	S = s2 + gamma*s1

	u_eq = ((f2/g2) - l2*x4 - gamma*l1*x2 + gamma*(f1/g1))/((1/g2) + (gamma/g1))
	u_sw = -eta*S*np.tanh(S)/((1/g2) + (gamma/g1))

	u = u_eq + u_sw

	x1dot = x2
	x2dot = (u - f1)/g1
	x3dot = x4
	x4dot = (u - f2)/g2

	return [x1dot, x2dot, x3dot, x4dot]

def solve(params):
	
	t0 = 0
	X0 = [0, 0, math.pi/2, 0]
	t1 = 100
	dt = 0.01
	
	r = ode(model).set_integrator('dopri5', nsteps = 1000, method='bdf').set_initial_value(X0, t0).set_f_params(params)

	Y = np.zeros((10001,4))
	t =[]
	i = 0

	while r.successful() and r.t < t1:
		r.integrate(r.t + dt)
		Y[i] = r.y
		t.append(r.t)
	
	print Y

################################################################################
if __name__ == '__main__':
	
	params = [0.09, 0.2, 1, 1, 0.05, 9.8, 6, 6, 7, 10]
	
	solve(params)
