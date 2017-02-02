import numpy
from numpy import meshgrid
from math import exp
from copy import copy

def ripple(w1, w2, damp, n = 1):
    for _ in xrange(n):
        w2 *= -2
        w2[1:-1,1:-1] += w1[0:-2, 1: -1]
        w2[1:-1,1:-1] += w1[2:  , 1: -1]
        w2[1:-1,1:-1] += w1[1:-1, 0: -2]
        w2[1:-1,1:-1] += w1[1:-1, 2:   ]
        w2 *= .5 * (1. - 1./damp)
        w1, w2 = w2, w1

def refract(x, y, w, rindex, depth = 10):
    sx = x[0,1] - x[0,0]
    sy = y[1,0] - y[0,0]

    dw_dx = (w[2: ,1:-1] - w[:-2,1:-1]) / sx * .5
    dw_dy = (w[1:-1,2: ] - w[1:-1,:-2]) / sy * .5

    xang = numpy.arctan(dw_dx)
    xrefract = numpy.arcsin(sin(xang) / rindex)
    dx = numpy.tan(xrefract) * dw_dx * depth

    yang = numpy.arctan(dw_dy)
    yrefract = numpy.arcsin(sin(yang) / rindex)
    dy = numpy.tan(yrefract) * dw_dy * depth

    dx *= numpy.sign(dw_dx)
    dy *= numpy.sign(dw_dy)

    xmin = x[0,0]
    xmax = x[0,-1]
    x[1:-1,1:-1] += dx
    x[:,:] = numpy.where(x < xmin, xmin, x)
    x[:,:] = numpy.where(x > xmax, xmax, x)

    ymin = y[0,0]
    ymax = y[-1,0]
    y[1:-1,1:-1] += dy
    y[:,:] = numpy.where(y < ymin, ymin, y)
    y[:,:] = numpy.where(y > ymax, ymax, y)
x,y = 33,200    
x,y = meshgrid(x,y)
w = 10 * exp(- (x*x + y*y))
w1 = copy(w) #w.copy()
x1,y1 = meshgrid(numpy.r_[0:len(x):1.0], numpy.r_[0:len(y):1.0])
ripple(w, w1, 16) # w1 will be modified
refract(x1, y1, w1, rindex=2, depth=10) # x1 and y1 will be modified
numpy.around(x1, out=x1) # but you will get better results with interpolate
numpy.around(y1, out=y1) # 