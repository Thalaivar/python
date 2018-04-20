import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

NL = 0
NS = 1
Z  = 2
PS = 3
PL = 4

def fuzzify(x, mfx_set, univ):
    y = []
    for a in mfx_set:
        y.append(fuzz.interp_membership(univ, a, x))

    return y

def defuzzify(fuzz, vals):

def model(t, X, params):
    e, edot = X
    e_univ, edot_univ, rule_univ, e_mfx, edot_mfx, rule_mfx = params

    e_fuzz = fuzzify(e, e_mfx, e_univ)
    edot_fuzz = fuzzify(edot, edot_mfx, edot_univ)

    rule = get_rule_premise(e_fuzz, edot_fuzz)

    v = defuzzify(rule_mfx, rule)

    xdot = edot
    xddot = 9.81*sin(1.2*v)

def get_rule_premise(e_fuzz, edot_fuzz):
    rule = np.zeros((25,))
    i = 0
    for x in e_fuzz:
        for y in edot_fuzz:
            rule[i] = x*y
            i += 1

    return rule

def make_singelton_mfx(univ, params):
    y = []
    for x in univ:
        if x < params or x > params:
            y.append(0)
        elif x == params:
            y.append(1)

    return y

def main(params, univ):
    e_univ, edot_univ = univ
    e_params, edot_params, rule_params = params

    # generate the mfx
    e_mfx = []
    edot_mfx = []
    rule_mfx = []

    for i in range(len(e_params)):
        e_mfx.append(fuzz.trimf(e_univ, e_params[i]))
    for i in range(len(edot_params)):
        edot_mfx.append(fuzz.trimf(edot_univ, edot_params[i]))
    for i in range(len(rule_params)):
        rule_mfx.append(make_singelton_mfx(rule_univ, rule_params[i]))

if __name__ == '__main__':
    e_univ = np.linspace(-0.5, 0.5, 5)
    edot_univ = np.linspace(-4, 4, 5)
    rule_univ = np.linspace(-10, 10, 5)
    e_params = np.array([[-0.5, -0.5, -0.25],
                         [-0.5, -0.25, -0.0],
                         [-0.25, 0.0, 0.25],
                         [0.0, 0.25, 0.5],
                         [0.25, 0.5, 0.5]])
    edot_params = np.array([[-4, -4, -2],
                         [-4, -2, -0],
                         [-2, 0, 2],
                         [0, 2, 4],
                         [2, 4, 4]])
    rule_params = np.array([-10, -5, 0, 5, 10])

    univ = [e_univ, edot_univ, rule_univ]
    params = [e_params, edot_params, rule_params]

    main(params, univ)
