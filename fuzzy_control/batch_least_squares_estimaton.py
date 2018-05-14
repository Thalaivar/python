import numpy as np
import matplotlib.pyplot as plt
from numpy import sin, log
import math
from numpy.linalg import inv

no_of_estimates = []
estimated_f = []
for i in range(3):
    no_of_estimates.append(i+5)
x_1 = np.linspace(1, 2, 1000)
f_1 = 3*sin(x_1**3) - 4*log(x_1) + 5*(x_1**2)
for i in range(len(no_of_estimates)):
    x = np.linspace(1, 2, no_of_estimates[i])
    f = 3*sin(x**3) - 4*log(x) + 5*(x**2)
    Y = np.reshape(f, (no_of_estimates[i],1))
    phi = np.zeros((no_of_estimates[i], 3))

    for j in range(no_of_estimates[i]):
        phi[j,0] = math.sin(x[j]**3)
        phi[j,1] = math.log(x[j])
        phi[j,2] = x[j]**2

    phi_t = np.transpose(phi)
    phi_t_phi_inv = inv(np.dot(phi_t, phi))

    theta_estimate = np.dot(phi_t_phi_inv, np.dot(phi_t, Y))

    f_estimate = theta_estimate[0,0]*sin(x**3) + theta_estimate[1,0]*log(x) + theta_estimate[2,0]*(x**2)
    estimated_f.append(f_estimate)

    plt.plot(x_1, f_1, x, f_estimate)
plt.show()
