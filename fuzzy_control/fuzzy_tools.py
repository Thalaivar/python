import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
import math

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
    
