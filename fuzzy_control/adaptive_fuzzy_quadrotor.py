import fuzzy_tools as fuzz
import numpy as np
import matplotlib.pyplot as plt

# model parameters
Ixx = 0.006228
Iyy = 0.006225
Izz = 0.01121
l = 0.232


def make_fuzzy_sets():
    # fuzzy system params

    # fuzzy universes for error in angle
    e_phi = np.linspace(-1.57, 1.57, 1000)
    e_theta = e_phi
    e_psi = e_phi

    # fuzzy universes for error in angular velocity
    de_phi = np.linspace(-100, 100, 10000)
    de_theta = de_phi
    de_psi = de_phi

    # centres for gaussian memberships in e universe
    c_e_phi = [-0.785, 0, 0.785]
    c_e_theta = c_e_phi
    c_e_psi = c_e_phi

    # spreads for gaussian memberships in e universe
    sig_e_phi = 0.285
    sig_e_theta = sig_e_phi
    sig_e_psi = sig_e_phi

    # centres for gaussian memberships in e dot universe
    c_de_phi = [-50, 0, 50]
    c_de_theta = c_de_phi
    c_de_psi = c_de_phi

    # spreads for gaussian memberships in e dot universe
    sig_de_phi = 1000
    sig_de_theta = sig_e_phi
    sig_de_psi = sig_e_phi

    c_e = [c_e_phi, c_e_theta, c_e_psi]
    c_de = [c_de_phi, c_de_theta, c_de_psi]
    sig_e = [sig_e_phi, sig_e_theta, sig_e_psi]
    sig_de = [sig_de_phi, sig_de_theta, sig_de_psi]
    e = [e_phi, e_theta, e_psi]
    de = [de_phi, de_theta, de_psi]

    e_memship = []
    de_memship = []

    # make  e fuzzy sets
    for i in range(3):
        temp_memship = []
        c = c_e[i]
        sig = sig_e[i]
        for j in range(len(c)):
            p = [c[j], sig, "none"]
            temp_memship.append(fuzz.membership("gauss", p, e[i], "none"))
        e_memship.append(temp_memship)

    for i in range(3):
        temp_memship = []
        c = c_de[i]
        sig = sig_de[i]
        for j in range(len(c)):
            p = [c[j], sig, "none"]
            temp_memship.append(fuzz.membership("gauss", p, de[i], "none"))
        de_memship.append(temp_memship)

    return [e_memship, de_memship]

def main():
    e_memship, de_memship = make_fuzzy_sets()

    
if __name__ == '__main__':
    main()
