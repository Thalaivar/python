import fuzzy_tools as fuzz
import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt
from numpy.linalg import inv

# universe for real function
x1 = np.linspace(-1, 1, 100)
x2 = np.linspace(-1, 1, 100)

# real function
g = sin(x1)*((cos(x2))**2)

# data points for estimation
x1_cap = np.zeros((11,))
x2_cap = np.zeros((11,))
x_cap = np.zeros((121,2))
k = 0
for i in range(11):
    j = (2*i/10)
    x1_cap[i] = -1.0 + j
    x2_cap[i] = -1.0 + j
for i in range(len(x1_cap)):
    for j in range(len(x2_cap)):
        x_cap[k] = np.array([x1_cap[i], x2_cap[j]])
        k += 1
g_cap = np.zeros_like(x1_cap)
for i in range(len(x1_cap)):
    g_cap[i] = sin(x1_cap[i])*((cos(x2_cap[i]))**2)

# fuzzy sets
centres = [-1.0, -0.5, 0, 0.5, 1]
spread = 0.2123
option = 'none'
params = []
names = 'none'
memship_1 = []
memship_2 = []
for x in centres:
    params.append([x, spread, option])
for x in params:
    memship_1.append(fuzz.membership('gauss', x, x1, names))
    memship_2.append(fuzz.membership('gauss', x, x2, names))

# fuzzified value set
fuzz_val_set_1 = np.zeros((len(x1_cap),len(memship_1)))
fuzz_val_set_2 = np.zeros((len(x2_cap),len(memship_2)))
temp = np.zeros((len(memship_1),))
for i in range(len(x1_cap)):
    for j in range(len(memship_1)):
        fuzz.fuzzify(x1_cap[i], memship_1[j])
        temp[j] = memship_1[j].fuzz_val
    fuzz_val_set_1[i] = temp
for i in range(len(x2_cap)):
    for j in range(len(memship_2)):
        fuzz.fuzzify(x2_cap[i], memship_2[j])
        temp[j] = memship_2[j].fuzz_val
    fuzz_val_set_2[i] = temp

# get rule premise values
fuzz_rule_premise = np.zeros((len(x1_cap), len(memship_1)*len(memship_2)))
temp = np.zeros((len(memship_1)*len(memship_2), ))
l = 0
for i in range(len(x1_cap)):
    for j in range(len(memship_1)):
        for k in range(len(memship_2)):
            temp[l] = fuzz_val_set_1[i, j]*fuzz_val_set_2[i, k]
            l += 1
    fuzz_rule_premise[i] = temp
    l = 0

# get fuzzy basis function values
fuzz_basis = np.zeros_like(fuzz_rule_premise)
for i in range(len(x1_cap)):
    a1 = np.sum(fuzz_rule_premise[i])
    fuzz_basis[i] = (fuzz_rule_premise[i])/a1

# LSE
phi = fuzz_basis
phi_t = np.transpose(phi)
phi_t_phi = np.dot(phi_t, phi)
phi_t_phi_inv = inv(phi_t_phi)
Y = g_cap.reshape((len(x1_cap), 1))
theta_cap = np.dot(phi_t_phi_inv, (np.dot(phi_t, Y)))
