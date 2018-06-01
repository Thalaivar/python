import fuzzy_tools as fuzz
import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin
import random

# no. of iterations
n_steps = 200

# no. of rules
n_rules = 5

lam1 = 0.001
lam2 = 0.001
lam3 = 0.001

# universe
x = np.linspace(0, 6, 1000)

# function to estimate
g = x - cos(1.5*x) + sin(0.4*x)

# training data pairs
x_train = np.random.rand(n_steps,)*6.0

# to get output data point
def get_y(data_point_x):
    return data_point_x - cos(1.5*data_point_x) + sin(0.4*data_point_x)

# to update the fuzzy sets with lates paramter value
def update_fuzzy_sets(memship, c, sig):
    for i in range(len(memship)):
        memship[i].params = [c[i, 0], sig[i, 0], "none"]

    return memship

def get_rule_premise(x, memship):
    rule_premise = np.zeros((n_rules, 1))
    for i in range(len(memship)):
        fuzz.fuzzify(x, memship[i])
        rule_premise[i, 0] = memship[i].fuzz_val
    return rule_premise

def fuzzy_grad_des(data_point_x, f, b, c, sig, premise):
    e = f - get_y(data_point_x)
    basis_func = premise/np.sum(premise)
    b_next = np.zeros_like(b)
    c_next = np.zeros_like(c)
    sig_next = np.zeros_like(sig)

    for i in range(n_rules):
        # update output singleton positions
        b_next[i,0] = b[i,0] - lam1*e*basis_func[i,0]

        # update input fuzzy set centres
        c_next[i,0] = c[i,0] - lam2*e*premise[i,0]*((data_point_x - c[i,0])/(sig[i,0]**2))*((b[i,0] - f)/np.sum(premise))

        # update input fuzzy set spreads
        sig_next[i,0] = sig[i,0] - lam3*e*((b[i,0] - f)/np.sum(premise))*premise[i,0]*(((data_point_x - c[i,0])**2)/(sig[i,0])**3)

    return [b_next, c_next, sig_next]

def simulate(memship, b_0, c_0, sig_0):
    for i in range(n_steps):
        data_point_x = x_train[i]

        # initial step
        if i == 0:
            # get estimate of function
            premise = get_rule_premise(data_point_x, memship)
            f = np.dot(np.transpose(b_0), premise)
            # get updated params
            b_next, c_next, sig_next = fuzzy_grad_des(data_point_x, f, b_0, c_0, sig_0, premise)
            memship = update_fuzzy_sets(memship, c_next, sig_next)

        else:
            # get estimate of function
            premise = get_rule_premise(data_point_x, memship)
            f = np.dot(np.transpose(b_next), premise)
            # get updated params
            b_next, c_next, sig_next = fuzzy_grad_des(data_point_x, f, b_next, c_next, sig_next, premise)
            memship = update_fuzzy_sets(memship, c_next, sig_next)

    return [b_next, c_next, sig_next]

def compare(b, c, sig, memship):
    fuzz_basis = np.zeros((len(x) ,n_rules))
    memship = update_fuzzy_sets(memship, c, sig)
    temp = np.zeros((n_rules,))
    for i in range(len(x)):
        for j in range(n_rules):
            fuzz.fuzzify(x[i], memship[j])
            temp[j] = memship[j].fuzz_val
        fuzz_basis[i] = temp/np.sum(temp)

    g_cap = np.zeros_like(x)
    for i in range(len(x)):
        g_cap[i] = b[0]*fuzz_basis[i,0] + b[1]*fuzz_basis[i,1] + b[2]*fuzz_basis[i,2] + b[3]*fuzz_basis[i,3] + b[4]*fuzz_basis[i,4]

    plt.plot(x, g, x, g_cap)
    plt.show()

def main():
  # create fuzzy system
    # initial fuzzy set parameters
    b_0 = np.random.rand(5, 1)*15.0
    c_0 = np.random.rand(5, 1)*6.0
    sig_0 = np.random.rand(5, 1)*2.0

    # create fuzzy sets
    memship = []
    for i in range(len(b_0)):
        p = [c_0[i, 0], sig_0[i, 0], "none"]
        memship.append(fuzz.membership("gauss", p, x, "none"))

    b, c, sig = simulate(memship, b_0, c_0, sig_0)
    memship = update_fuzzy_sets(memship, c, sig)
    b, c, sig = simulate(memship, b, c, sig)
    memship = update_fuzzy_sets(memship, c, sig)
    b, c, sig = simulate(memship, b, c, sig)
    memship = update_fuzzy_sets(memship, c, sig)
    b, c, sig = simulate(memship, b, c, sig)
    memship = update_fuzzy_sets(memship, c, sig)
    b, c, sig = simulate(memship, b, c, sig)
    memship = update_fuzzy_sets(memship, c, sig)
    b, c, sig = simulate(memship, b, c, sig)
    memship = update_fuzzy_sets(memship, c, sig)
    
    compare(b, c, sig, memship)

if __name__ == '__main__':
    main()
