import fuzzy_tools as fuzz
import numpy as np

p1 = [-1, 0.5]
p2 = [0, 0.5]
p3 = [1, 0.5]
p = [p1, p2, p3]
univ = np.linspace(-3, 3, 1000)
a = []
for x in p:
	a.append(fuzz.membership('gauss', x, univ, 'test'))
for x in a:
	fuzz.make_memship(x)

fuzz.plot_memship(a)
