import fuzzy_tools as fuzz
import numpy as np
import matplotlib.pyplot as plt
import math
from numpy import tanh, sin, cos
from scipy.integrate import ode

# model parameters
b = 0.0000313
d = 0.00000075
Ixx = 0.0075
Iyy = Ixx
Izz = 0.013
l = 0.23

# literals
n_inputs = 6
n_angles = 3
n_sets = 5
n_rules = 25

# angle error to desired rate
ang_to_rat_phi = 1.0
ang_to_rat_theta = 1.0
ang_to_rat_psi = 1.0

# smc parameters
phi_lam = 1.0
theta_lam = 1.0
psi_lam = 1.0
phi_k = 1.0
theta_k = 1.0
psi_k = 1.0
phi_eta = 1.0
theta_eta = 1.0
psi_eta = 1.0

# adaptation rates
adap_gain_phi = 1.0
adap_gain_theta = 1.0
adap_gain_psi = 1.0

# global variables to calculate sdot
s_prev = np.zeros((n_angles,))

# setup fuzzy sets
def setup_fuzz_sys():
    # define universes of input variables
    e_phi_univ   = np.linspace(-math.pi/2.0, math.pi/2.0, 1000)
    e_theta_univ = np.linspace(-math.pi/2.0, math.pi/2.0, 1000)
    e_psi_univ   = np.linspace(-math.pi, math.pi, 1000)
    de_phi_univ   = np.linspace(-1.74, 1.74, 1000)
    de_theta_univ = np.linspace(-1.74, 1.74, 1000)
    de_psi_univ   = np.linspace(-1.74, 1.74, 1000)

    e_univ = [e_phi_univ, e_theta_univ, e_psi_univ]
    de_univ = [de_phi_univ, de_theta_univ, de_psi_univ]

    # define centres for each input
    e_phi_c   = np.array([-0.785, -0.3925, 0, 0.3925, 0.785])
    e_theta_c = np.array([-0.785, -0.3925, 0, 0.3925, 0.785])
    e_psi_c   = np.array([-math.pi/2, -0.785, 0 , 0.785, math.pi/2])
    de_phi_c   = np.array([-0.872, -0.436, 0, 0.436, 0.785])
    de_theta_c = np.array([-0.872, -0.436, 0, 0.436, 0.785])
    de_psi_c   = np.array([-0.872, -0.436, 0, 0.436, 0.785])

    e_c = [e_phi_c, e_theta_c, e_psi_c]
    de_c = [de_phi_c, de_theta_c, de_psi_c]

    # define spreads
    sig = 0.184

    # make memberships
    e_membership = []
    de_membership = []
    for i in range(n_angles):
        temp1 = []
        temp2 = []

        # get parameters for input
        c = e_c[i]
        dc = de_c[i]
        for j in range(n_sets):
            # make parameter vectors for sets
            p1 = [c[j], sig, "none"]
            p2 = [dc[j], sig, "none"]
            temp1.append(fuzz.membership("gauss", p1, e_univ[i], "none"))
            temp2.append(fuzz.membership("gauss", p2, de_univ[i], "none"))

        e_membership.append(temp1)
        de_membership.append(temp2)

    return [e_membership, de_membership]

# for one angle, and therefor for one control input
def get_fuzz_basis(e, e_mem, de, de_mem):
    temp = np.zeros((n_rules, 1))

    # get fuzzy membership values fo reach membership func
    for i in range(n_sets):
        fuzz.fuzzify(e, e_mem[i])
        fuzz.fuzzify(de, de_mem[i])

    # get rule premise values
    k = 0
    for i in range(n_sets):
        for j in range(n_sets):
            temp[k,0] = e_mem[i].fuzz_val*de_mem[j].fuzz_val
            k += 1

    # get basis funcs
    temp = temp/(np.sum(temp))
    return temp

def model(t, X, params):
    phi, dphi, theta, dtheta, psi, dpsi, b_phi, b_theta, b_psi = X
    e_mem, de_mem, step_size = params
    b = np.array([b_phi, b_theta, b_psi])

    e, de = get_err(phi, dphi, theta, dtheta, psi, dpsi)

    # get basis funcs
    eps = np.zeros_like(e)
    for i in range(n_angles):
        eps[i] = get_fuzz_basis(e[i], e_mem[i], de[i], de_mem[i])

    # get estimates of control outputs
    u = np.zeros_like(eps)
    for i in range(n_angles):
        u[i] = np.dot(np.transpose(eps[i]), b[i])

    # get sliding surfaces
    s = get_s(e, de)

    # get s_dot
    sdot = (s - s_prev)/step_size
    s_prev = s

    x1dot = dphi
    x2dot = a1*dtheta*dpsi + b1*u[0]
    x3dot = dtheta
    x4dot = a2*dpsi*dphi + b2*u[1]
    x5dot = dpsi
    x6dot = a3*dphi*dtheta + b3*u[2]
    b_phi_dot = -0.5*adap_gain_phi*eps[0]*(sdot[0] + phi_k*s[0] + phi_eta*tanh(s[0]))
    b_theta_dot = -0.5*adap_gain_theta*eps[1]*(sdot[1] + theta_k*s[1] + theta_eta*tanh(s[1]))
    b_psi_dot = -0.5*adap_gain_psi*eps[2]*(sdot[2] + psi_k*s[2] + psi_eta*tanh(s[2]))

    return [x1dot, x2dot, x3dot, x4dot, x5dot, x6dot, b_phi_dot, b_theta_dot, b_psi_dot]

def get_s(e, de):
    s = np.zeros((n_angles,))
    params = np.array([phi_lam, theta_lam, psi_lam])
    for i in range(n_angles):
        s[i] = de[i] + params[i]*e[i]

    return s

def get_err(phi, dphi, theta, dtheta, psi, dpsi):
    # stationary desired values
    e_phi = phi - 0.1744
    e_theta = theta + 0.2616
    e_psi = psi
    e = np.array([e_phi, e_theta, e_psi])

    # get desired rates by passing through P controller
    dphi_d = ang_to_rat_phi*e_phi
    dtheta_d = ang_to_rat_theta*e_theta
    dpsi_d = ang_to_rat_psi*e_psi

    # get angle rate errors
    de_phi = dphi - dphi_d
    de_theta = dtheta - dtheta_d
    de_psi = dpsi - dpsi_d
    de = np.array([de_phi, de_theta, de_psi])

    return [e, de]

def main():
    e_mem, de_mem = setup_fuzz_sys()

    # initial condition
    b_phi_0 = np.zeros((n_rules, 1))
    b_theta_0 = np.zeros((n_rules, 1))
    b_psi_0 = np.zeros((n_rules, 1))
    X0 = [0, 0, 0, 0, 0, 0, b_phi_0, b_theta_0, b_psi_0]
    t0 = 0
    # integrator parameters
    dt = 0.001
    t1 = 20
    params = [e_mem, de_mem, dt]

    x = np.zeros((20001, 6))
    t = []
    r = ode(model).set_integrator('vode').set_initial_value(X0, t0).set_f_params(params)
    i = 0
    while r.successful() and r.t < t1:
        r.integrate(r.t + dt)
        x[i] = r.y
        t.append(r.t)
        i += 1

if __name__ == '__main__':
    main()
