Toolkit for fuzzy logic implementation
=======================================

__Version:__ 1.1.1

Support:
--------

1. Membership functions (type)
    * Triangular
    * Singleton
    * Gaussian

2. Defuzzification (method)
    * Centre average defuzzification

Guide:
------

`membership(type, params, univ, name)`:

- the main class that holds info about a particular membership function, 
the different types of membership functions supported are listen in __Support__
for each membership function type, there is an expected parameter vector that
must be supplied:

- each class holds the following data:
   1. `membership.type`     - type of membership function
   2. `membership.univ`     - universe of definition membership function
   3. `membership.params`   - parameters defining the membership function
   4. `membership.fuzz_val` - fuzzified value of a partiuclar variable related to the membership function
   5. `membership.memship_arr` - the array used to plot the membership function
   6. `membership.name`     - the name of the memebrship function
      
| membership | parameter form | description |
| :--------: | :------------: | :---------: |
| trimf      | [a, b, c]      | a, b, c represent the left, center and right points of the triangle |
| singleton  | [a]            | a represents the location of the singleton |
| gaussian   | [a, b, c]      | a, b represent the centre and spread, c is a keyword argument |

`make_memship(membership)`:

- __Input:__ membership class instance
- __Operation:__ accesses the `membership.memship_arr` array by filling it with the y-values of the membership
- __Use:__ for plotting membership functions

`fuzzify(x, membership)`:
- __Input:__ variable to be fuzzified, membership class instance of fuzzy set membership
- __Returns:__ fuzzy value of variable corresponding to that membership

