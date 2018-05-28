import numpy as np
import matplotlib.pyplot as plt
import fuzzy_tools as fuzz
from numpy.linalg import inv
from numpy import sin, cos
import random

# original function
def data_point_y(data_point_x):
    return data_point_x - cos(1.5*data_point_x) + sin(0.4*data_point_x)

# universe
x = np.linspace(0, 6, 100)

# no of iterations
n_points = 200

# fuzzy sets
p1 = [0, 1.184, "none"]
p2 = [2, 1.184, "none"]
p3 = [4, 1.184, "none"]
p4 = [6, 1.184, "none"]
params = [p1, p2, p3, p4]
input_fuzz_set = []
for z in params:
    input_fuzz_set.append(fuzz.membership("gauss", z, x, "none"))

# to get parameter estimate
def get_estimate(data_point_x, prev_lam, prev_theta):
    # getting fuzzified value
    fuzz_val = []
    for mem in input_fuzz_set:
        fuzz.fuzzify(data_point_x, mem)
        fuzz_val.append(mem.fuzz_val)

    # premise values
    premise_val = np.zeros((len(fuzz_val),))
    for i in range(len(fuzz_val)):
        premise_val[i] = fuzz_val[i]

    # implied fuzzy set membership equals the premise values as we are usign singleton sets
    # for output

    # fuzzy basis functions
    fuzz_basis = premise_val/np.sum(premise_val)

    # new phi vector
    phi = fuzz_basis
    phi_t = np.transpose(phi)

    # RLS update
    new_y = data_point_y(data_point_x)
    gamma = (np.dot(prev_lam, phi))/(1 + np.dot(phi_t, np.dot(prev_lam, phi)))
    R_x_R_identity = np.zeros_like(np.dot(phi_t, phi))
    new_lam = np.dot((R_x_R_identity - np.dot(gamma, phi_t)), prev_lam)
    new_theta = np.dot((R_x_R_identity - np.dot(gamma, phi_t)), prev_theta) + np.dot(new_lam, new_y*phi)

    return new_theta, new_lam

# initial estimate
def get_inital_estimate(data_point_x):
    # getting fuzzified value
    fuzz_val = []
    for mem in input_fuzz_set:
        fuzz.fuzzify(data_point_x, mem)
        fuzz_val.append(mem.fuzz_val)

    # premise values
    premise_val = np.zeros((len(fuzz_val),))
    for i in range(len(fuzz_val)):
        premise_val[i] = fuzz_val[i]

    # implied fuzzy set membership equals the premise values as we are usign singleton sets
    # for output

    # fuzzy basis functions
    fuzz_basis = premise_val/np.sum(premise_val)

    # new phi vector
    phi = fuzz_basis
    phi_t = np.transpose(phi)

    # getting RLS update variables
    lam = 1.0/np.dot(phi_t, phi)
    theta = np.dot(lam, phi_t*data_point_y(data_point_x))

    return theta, lam

# simulation
def main():
    data_point_x = random.random()*6.0
    first_theta, first_lam = get_inital_estimate(data_point_x)

    for i in range(n_points):
        data_point_x = random.random()*6.0
        if i == 0:
            prev_theta, prev_lam = get_estimate(data_point_x, first_lam, first_theta)
        else:
            prev_theta, prev_lam = get_estimate(data_point_x, prev_lam, prev_theta)

    final_theta = prev_theta

    # comparison
    new_func = np.zeros_like(x)
    b = final_theta
    fuzz_basis_2 = np.zeros((len(x), len(input_fuzz_set)))
    temp = np.zeros((4,))
    for i in range(len(x)):
        for j in range(len(input_fuzz_set)):
            fuzz.fuzzify(x[i], input_fuzz_set[j])
            temp[j] = input_fuzz_set[j].fuzz_val
        fuzz_basis_2[i] = temp/np.sum(temp)
    g_cap = np.zeros_like(x)
    for i in range(len(x)):
        g_cap[i] = b[0]*fuzz_basis_2[i,0] + b[1]*fuzz_basis_2[i,1] + b[2]*fuzz_basis_2[i,2] + b[3]*fuzz_basis_2[i,3]
    g = x - cos(1.5*x) + sin(0.4*x)
    plt.plot(x, g, x, g_cap)
    plt.show()



if __name__ == '__main__':
    main()
