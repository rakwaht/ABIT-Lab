#! /usr/bin/python
#
# Rank pages based on incoming links

import numpy
import numpy.linalg

#user with probability d follow the links, with probability 0.1 it moves randomly
d= .9

# N = number of pages (depends on E matrix)
N = 4

#matrix for edges
E = numpy.matrix (
    [
       [0, 1, 0, 1],
       [0, 0, 1, 0],
       [0, 1, 1, 0],
       [0, 0, 0, 1],
    ],
    dtype = float
)

#L is stocastic version of matrix e
L = numpy.matrix (E)
for r in L:
	r /= r.sum()

#modify L with user choise
L = d * L + (1-d)/N * numpy.ones ((4, 4))

#traspose L
Lt = L.T
#print Lt

#calculate vector p
w, v = numpy.linalg.eig(Lt)
p = numpy.real(v[:,2])
p /= p.sum()

#vector of probability at time 0
pt = numpy.matrix([1,0,0,0], dtype=float).T

#calculate probability pt at time i
for i in range (10):
	pt = Lt * pt
	print pt.T







