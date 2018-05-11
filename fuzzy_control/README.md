Toolkit for fuzzy logic implementation
=======================================

__Version:__ 1.0

Support:
--------

1. Membership functions (type)
    * Triangular
    * Singleton

2. Defuzzification (method)
    * Centre average defuzzification

Guide:
------

`membership(type, params, univ, name)`:

- the main class that holds info about a particular membership function, 
the different types of membership functions supported are listen in __Support__
for each membership function type, there is an expected parameter vector that
must be supplied:
      
| membership | parameter form | description |
| :--------: | :------------: | :---------: |
| trimf      | [a, b, c]      | a, b, c represent the left, center and right points of the triangle |
| singleton  | [a]            | a represents the location of the singleton |

- *name* refers to the linguistic name that is given to the fuzzy membership function, it is of use only when plotting
- *univ* refers to the universe over which the fuzzy membership is defined

`make_memship(membership)`:

- __Input:__ membership class instance
- __Returns:__ array with y-values of membership
- __Use:__ for plotting membership functions

`fuzzify(x, membership)`:
- __Input:__ variable to be fuzzified, membership class instance of fuzzy set membership
- __Returns:__ fuzzy value of variable corresponding to that membership

