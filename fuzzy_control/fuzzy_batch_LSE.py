import fuzzy_tools as fuzz
import numpy as np
import matplotlib.pyplot as plt
from numpy import sin, cos, log
from numpy.linalg import inv

# universe
x = np.linspace(0, 6, 100)

# real thing
g = x - cos(1.5*x) + sin(0.4*x)

# datapoints for getting estimated g(x)
x_estimate = [0, 1, 2, 3, 4, 5, 6]
g_estimate = [-1.0, 1.3187, 3.7073, 4.1428, 4.0394, 5.5627, 7.5866]

# fuzzy sets
p1 = [0, 1.184, 'none']
p2 = [2, 1.184, 'none']
p3 = [4, 1.184, 'none']
p4 = [6, 1.184, 'none']
params = [p1, p2, p3, p4]
memship = []
names = 'none'
for z in params:
    memship.append(fuzz.membership('gauss', z, x, 'none'))

# premise memship and fuzzy basis
fuzz_val_set = np.zeros((len(x_estimate), len(memship)))
temp = np.zeros((len(memship),))
for i in range(len(x_estimate)):
    for j in range(len(memship)):
        fuzz.fuzzify(x_estimate[i], memship[j])
        temp[j] = memship[j].fuzz_val
    fuzz_val_set[i] = temp

# LSE
phi = np.zeros_like(fuzz_val_set)
for i in range(len(x_estimate)):
    a1 = np.sum(fuzz_val_set[i])
    b1 = (fuzz_val_set[i])/a1
    phi[i] = b1
phi_t = np.transpose(phi)
phi_t_phi = np.dot(phi_t, phi)
phi_t_phi_inv = inv(phi_t_phi)
Y = np.array(g_estimate).reshape((len(g_estimate),1))
theta_cap = np.dot(phi_t_phi_inv, (np.dot(phi_t, Y)))

# getting estimated function
b = theta_cap
fuzz_val_set_2 = np.zeros((len(x), len(memship)))
temp = np.zeros((len(memship),))
for i in range(len(x)):
    for j in range(len(memship)):
        fuzz.fuzzify(x[i], memship[j])
        temp[j] = memship[j].fuzz_val
    fuzz_val_set_2[i] = temp
fuzz_basis = np.zeros_like(fuzz_val_set_2)
for i in range(len(x)):
    a1 = np.sum(fuzz_val_set_2[i])
    b1 = (fuzz_val_set_2[i])/a1
    fuzz_basis[i] = b1
g_cap = np.zeros((len(x),))
for i in range(len(x)):
    g_cap[i] = b[0]*fuzz_basis[i,0] + b[1]*fuzz_basis[i,1] + b[2]*fuzz_basis[i,2] + b[3]*fuzz_basis[i,3]

# plotting g and g_cap
plt.plot(x, g, x, g_cap, 'r--')
plt.show()
