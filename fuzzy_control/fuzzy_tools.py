import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode

# membership function class
class membership():
    def __init__(self, type, params, univ, name):
        self.type = type
        self.params = params
        self.univ = univ
        self.name = name
        self.check_params()

    def check_params(self):
        params = self.params
        type = self.type
        univ = self.univ

        if type == 'trimf':
            if len(params) != 3:
                print("Check params for trimf: not proper no. of params")

            else:
                a, b ,c = params
                if a < np.amin(univ) or c > np.amax(univ):
                    print("Check params for trimf: not in univ")

                if a > b or a > c or b > c:
                    print("Check params for trimf: not in correct order")

        if type == 'singleton':
            if len(params) != 1:
                print("Check params for singleton: not proper of no. params")

            else:
                a = params
                if a < np.amin(univ) or a > np.amax(univ):
                    print("Check params for singleton: not in univ")


# plot the array returned by make_memship
def plot_memship(memship, univ):
    for i in range(len(memship)):
            plt.plot(univ, memship[i])
    plt.show()

# returns an array to use for plotting
def make_memship(membership):
    type = membership.type
    params = membership.params
    univ = membership.univ

    if type == 'trimf':
        if len(params) == 3:
            a, b, c = params
            y = np.zeros_like(univ)
            i = 0
            for x in univ:
                if a == b:
                    if x <= a:
                        y[i] = 1
                    if x >= b and x <= c:
                        y[i] = (1/(b - c))*(x - c)

                elif x >= a and x <= b:
                    y[i] = (1/(b - a))*(x - a)

                if b == c:
                    if x >= b:
                        y[i] = 1
                    if x >= a and x <= b:
                        y[i] = (1/(b - a))*(x - a)

                elif x >= b and x <= c:
                    y[i] = (1/(b - c))*(x - c)

                if x == b:
                    y[i] = 1
                i += 1

    if type == 'singleton':
        a = params
        y = np.zeros_like(univ)
        i = 0
        for x in univ:
            if x == a:
                y[i] = 1.0
            else:
                y[i] = 0.0
            i +=1

    return y

# returns fuzzy membership of x
def fuzzify(x, membership):
    params = membership.params
    type = membership.type
    univ = membership.univ
    y = 0

    # make sure x is in the universe
    if x < np.amin(univ) or x > np.amax(univ):
        print("value to be fuzzified not in the universe")
        return None

    elif type == 'trimf':
        a, b, c = params

        if a == b:
            if x <= a:
                y = 1
            if x >= b and x <= c:
                y = (1/(b - c))*(x - c)

        elif x >= a and x <= b:
            y = (1/(b - a))*(x - a)

        if b == c:
            if x >= b:
                y = 1
            if x >= a and x <= b:
                y = (1/(b - a))*(x - a)

        elif x >= b and x <= c:
            y = (1/(b - c))*(x - c)

        if x == b:
            y = 1

    elif type == 'singleton':
        a = params[0]

        if x == a:
            y == 1.0
        else:
            y = 0.0

    return y



# returns crisp value of a fuzzy memship
def defuzzify(fuzz_val ,memship, method):
    y = 0
    z = 0
    if method == "CAD":
        for i in range(len(memship)):
            if memship[i].type == 'singleton':
                a = memship[i].params[0]
                y += a*fuzz_val[i]
                z += fuzz_val[i]
        return y/z


def main():
    e_mem = []
    edot_mem = []
    v_mem = []

    e_fuzz_set_1 = [-0.5, -0.5, -0.25]
    e_fuzz_set_2 = [-0.5, -0.25, 0]
    e_fuzz_set_3 = [-0.25, 0.0, 0.25]
    e_fuzz_set_4 = [0.25, 0.0, 0.25]
    e_fuzz_set_5 = [0.25, 0.5, 0.5]
    e_univ = np.linspace(-1.5, 1.5, 30)

    edot_fuzz_set_1 = [-4, -4, -2]
    edot_fuzz_set_2 = [-4, -2, 0]
    edot_fuzz_set_3 = [-2, 0, 2]
    edot_fuzz_set_4 = [0, 2, 4]
    edot_fuzz_set_5 = [2, 4, 4]
    edot_univ = np.linspace(-5, 5, 10)

    v_fuzz_set_1 = [-10.0]
    v_fuzz_set_2 = [-5.0]
    v_fuzz_set_3 = [0.0]
    v_fuzz_set_4 = [5.0]
    v_fuzz_set_5 = [10.0]
    v_univ = np.linspace(-10, 10, 100)

    e_fuzz_set = [e_fuzz_set_1, e_fuzz_set_2, e_fuzz_set_3, e_fuzz_set_4, e_fuzz_set_5]
    edot_fuzz_set = [edot_fuzz_set_1, edot_fuzz_set_2, edot_fuzz_set_3, edot_fuzz_set_4, edot_fuzz_set_5]
    v_fuzz_set = [v_fuzz_set_1, v_fuzz_set_2, v_fuzz_set_3, v_fuzz_set_4, v_fuzz_set_5]
    names = ['NL', 'NS', 'Z', 'PS', 'PL']
    for i in range(len(edot_fuzz_set)):
        e_mem.append(membership('trimf', e_fuzz_set[i], e_univ, names[i]))
        edot_mem.append(membership('trimf', edot_fuzz_set[i], edot_univ, names[i]))
        v_mem.append(membership('singleton', v_fuzz_set[i], v_univ, names[i]))

    r = ode(model).set_integrator('vode').set_integrator

def ball_beam_rule_set(x, y):
    z = []
    z1 = 0

    # 0 - NL
    # 1 - NS
    # 2- Z
    # 3- PS
    # 4- PL

    # get firing of rule for output being NL
    for i in range(len(x)):
        z1 += x[0]*y[0]
        z1 += x[0]*y[1]
        z1 += x[0]*y[2]
        z1 += x[1]*y[0]
        z1 += x[1]*y[1]
        z1 += x[2]*y[0]
    z.append(z1)
    z1 = 0

    # get firing of rule for output being NS
    for i in range(len(x)):
        z1 += x[0]*y[3]
        z1 += x[1]*y[2]
        z1 += x[2]*y[1]
        z1 += x[3]*y[0]
    z.append(z1)
    z1 = 0

    # get firing of rule for output being Z
    for i in range(len(x)):
        z1 += x[0]*y[4]
        z1 += x[1]*y[3]
        z1 += x[2]*y[2]
        z1 += x[3]*y[1]
        z1 += x[4]*y[0]
    z.append(z1)
    z1 = 0

    # get firing of rule for output being PS
    for i in range(len(x)):
        z1 += x[1]*y[4]
        z1 += x[2]*y[3]
        z1 += x[3]*y[2]
        z1 += x[4]*y[1]

    # get firing of rule of output being PL
    for i in range(len(x)):
        z1 += x[2]*y[4]
        z1 += x[3]*y[3]
        z1 += x[3]*y[4]
        z1 += x[4]*y[2]
        z1 += x[4]*y[3]
        z1 += x[4]*y[4]
    z.append(z1)
    z1 = 0

    return z

def model(t, X, params):
    x1, x2 = X
    e = -x1
    edot = -x2
    e_mem, edot_mem, v_mem = params

    e_fuzz_mem = []
    edot_fuzz_mem = []

    for i in range(len(e_mem)):
        e_fuzz_mem.append(fuzzify(e, e_mem[i]))
        edot_fuzz_mem.append(fuzzify(edot, edot_mem[i]))

    rule_out = ball_beam_rule_set(e_fuzz_mem, edot_fuzz_mem)

    v = defuzzify(rule_out, v_mem, 'CAD')

    x1dot = x2
    x2dot = 9.81*sin(0.2*v)

    return [x1dot, x2dot]

if __name__ == '__main__':
    main()
