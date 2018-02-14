import numpy as np
import matplotlib.pyplot as chart
import math
from scipy.integrate import ode

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
	m, M, L, g, eta, l1, l2, gamma = params

	x1, x2, x3, x4 = X

	f1 = m*L*(x4**2)*math.sin(x3) - m*g*math.sin(2*x3)/2
	g1 = M + m*((math.sin(x3))**2)
	g2 = (M + m*((math.sin(x3))**2))/math.cos(x3)
	d1 = (g*math.sin(x3))/L

	s1 = x2 + l1*(x1 - 20)
	s2 = x4 + l2*(x3 - math.pi)

	S = s2 + gamma*s1

	v_eq = -d1 - l2*x4 - gamma*l1*x2
	v_sw = -eta*np.tanh(S)

	v = (1/((gamma/g1) - 1/g2))*(v_eq + v_sw)

	x1dot = x2
	x2dot = v/g1
	x3dot = x4
	x4dot = d1 - v/g2
	
	return [x1dot, x2dot, x3dot, x4dot]

def solve(params):
	
	t0 = 0
	X0 = [0, 0, math.pi, 0]
	t1 = 20
	dt = 0.001
	
	r = ode(model).set_integrator('dopri5', nsteps = 10000, method='bdf')
	r.set_initial_value(X0, t0).set_f_params(params)

	Y = np.zeros((t1/dt + 1, 5))
	t =[0]
	i = 0

	while r.successful() and r.t < t1:
	
		r.integrate(r.t + dt)
		x1, x2, x3, x4 = r.y
		m, M, L, g, eta, l1, l2, gamma = params
		e_theta = x3*180.0/math.pi - 180
		e_x = x1 - 20
		
		s1 = x2 + l1*(x1 - 20)
		s2 = x4 + l2*(x3 - math.pi)

		S = s2 + gamma*s1
#		v_eq = -d1 - l2*x4 - gamma*l1*x2
#		v_sw = -eta*np.tanh(S)
#		v = (1/((gamma/g1) - 1/g2))*(v_eq + v_sw)
 		
		Y[i] = [e_theta, e_x, s1, s2, S]
		t.append(r.t)
		i = i + 1
	
	print(np.size(Y, 0))
	print(len(t))
	chart.plot(t, Y[:,0], label='error_theta')
	chart.plot(t, Y[:,1], label='error_x')
	chart.legend(loc='upper right')
	chart.grid()
	chart.show()
	
	labels = ['s_x', 's_theta', 'S']
	
	for i in range(3):
		chart.plot(t, Y[:,i+2], label=labels[i])
	chart.legend(loc='upper right')	
	chart.grid()
	chart.show()
################################################################################
if __name__ == '__main__':

	#params    m,   M, L,  g, eta, l1,  l2, gamma
	params = [0.02, 2, 1, 9.8, 10, 0.01, 2, 30]	
	solve(params)
