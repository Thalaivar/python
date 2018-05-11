import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
import math

# membership function class
class membership():
    """
        Class to form the membership functions for a given universe:
            * type - singleton, trimf
            * params - the defining parameters of the corresponding type of fuzzy membership
            * univ - the universe on which the fuzzy membership is defined
            * name - the name of the membership
    """
    def __init__(self, type, params, univ, name):
        self.type = type
        self.params = params
        self.univ = univ
        self.name = name
        self.fuzz_val = None
        self.memship_arr = np.zeros_like(univ)
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
                    print(params)

                if a > b or a > c or b > c:
                    print("Check params for trimf: not in correct order")
                    print(params)

        if type == 'singleton':
            if len(params) != 1:
                print("Check params for singleton: not proper of no. params")
                print(params)

            else:
                a = params
                if a < np.amin(univ) or a > np.amax(univ):
                    print("Check params for singleton: not in univ")
                    print(params)

        if type == 'gauss':
            if len(params) != 3:
                print("Check params for gaussian: not proper no. of params")
                print(params)

            else:
                a, b, c = params
                if min(a, b) < np.amin(univ) or max(a, b) > np.amax(univ):
                    print("Check params for gaussian: not in univ")
                    print(params)

# plot the array returned by make_memship
def plot_memship(memship):
    for i in range(len(memship)):
        plt.plot(memship[i].univ, memship[i].memship_arr, label=memship[i].name)
        plt.legend(loc='upper right')
    plt.show()

# returns an array to use for plotting
def make_memship(membership):
    type = membership.type
    params = membership.params
    univ = membership.univ

    if type == 'trimf':
        if len(params) == 3:
            a, b, c = params
            i = 0
            for x in univ:
                if a == b:
                    if x <= a:
                        membership.memship_arr[i] = 1
                    if x >= b and x <= c:
                        membership.memship_arr[i] = (1/(b - c))*(x - c)

                elif x >= a and x <= b:
                    membership.memship_arr[i] = (1/(b - a))*(x - a)

                if b == c:
                    if x >= b:
                        membership.memship_arr[i] = 1
                    if x >= a and x <= b:
                        membership.memship_arr[i] = (1/(b - a))*(x - a)

                elif x >= b and x <= c:
                    membership.memship_arr[i] = (1/(b - c))*(x - c)

                if x == b:
                    membership.memship_arr[i] = 1
                i += 1

    if type == 'singleton':
        a = params
        i = 0
        for x in univ:
            if x == a:
                membership.memship_arr[i] = 1.0
            else:
                membership.memship_arr[i] = 0.0
            i += 1

    if type == 'gauss':
        a, b, c= params
        i = 0
        for x in univ:
            if c == 'l_inf':
                if x <= a:
                    membership.memship_arr[i] = 1.0
                else:
                    membership.memship_arr[i] = math.exp(-0.5*(((x - a)**2)/b))
            elif c == 'r_inf':
                if x >= a:
                    membership.memship_arr[i] = 1.0
                else:
                    membership.memship_arr[i] = math.exp(-0.5*(((x - a)**2)/b))
            else:
                membership.memship_arr[i] = math.exp(-0.5*(((x - a)**2)/b))

            i += 1

# returns fuzzy membership of x
def fuzzify(x, membership):
    params = membership.params
    type = membership.type
    univ = membership.univ
    membership.fuzz_val = 0
    # make sure x is in the universe
    if x < np.amin(univ) or x > np.amax(univ):
        print("value to be fuzzified not in the universe")
        print(x)
        return None

    elif type == 'trimf':
        a, b, c = params
        if a == b:
            if x <= a:
                membership.fuzz_val = 1
            if x >= b and x <= c:
                membership.fuzz_val = (1/(b - c))*(x - c)

        elif x >= a and x <= b:
            membership.fuzz_val = (1/(b - a))*(x - a)

        if b == c:
            if x >= b:
                membership.fuzz_val = 1
            if x >= a and x <= b:
                membership.fuzz_val = (1/(b - a))*(x - a)

        elif x >= b and x <= c:
            membership.fuzz_val = (1/(b - c))*(x - c)

        if x == b:
            membership.fuzz_val = 1

    elif type == 'singleton':
        a = params[0]
        if x == a:
            membership.fuzz_val == 1.0
        else:
            membership.fuzz_val = 0.0

    elif type == 'gauss':
        a, b, c = params
        if c == 'l_inf':
            if x <= a:
                membership.fuzz_val = 1.0
            else:
                membership.fuzz_val = math.exp(-0.5*(((x - a)**2)/b))
        elif c == 'r_inf':
            if x >= a:
                memebership.fuzz_val = 1.0
            else:
                membership.fuzz_val = math.exp(-0.5*(((x - a)**2)/b))
        else:
            membership.fuzz_val = math.exp(-0.5*(((x - a)**2)/b))

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
            if memship[i].type == 'trimf':
                a, b, c = memship[i].params
                if (b - a) == (c - b):
                    y += b*fuzz_val[i]
                    z += fuzz_val[i]
            if memship[i].type == 'gauss':
                a, b, c = memship[i].params
                y += a*fuzz_val[i]
                z += fuzz_val[i]
        return y/z
