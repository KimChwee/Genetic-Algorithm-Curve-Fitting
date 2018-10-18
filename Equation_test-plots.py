"""
    Change the return formula in function: Evaluate
    And observe how the formula is plotted based on random coefficient

    If you want to see area instead of line, comment out "ax.clear()" under Function: Animate()
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import norm
import numpy as np
from random import *
from math import *

def evaluate(w, i):
    #return w[0] + w[1]*i**2 + w[2]*i
    #return w[0] + w[1]*i**3 + w[2]*i**2 + w[3]*i
    #return w[0]*cos(i*w[1]**w[2])
    #return w[0]*i + w[1]*cos(w[2] + w[3]*i**2)
    #return (w[0]*i**3+w[1]*i**2+w[2]*i)*cos(i)**2
    #return (w[0]*i**2+w[1]*i)*cos(i)**2 + w[2] + w[3]*i**3 + w[4]*i**2 + w[5]*i
    #return (w[0]*i**3+w[1]*i**2+w[2]*i)*cos(i)**2 + w[3] + w[4]*i**3 + w[5]*i**2 + w[6]*i
    #similar as above
    #return (w[0]*i**3+w[1]*i**2+w[2]*i)*cos(i)**2 + w[3] + w[4]*i**3 + w[5]*i**2 + w[6]*i + (w[7]*i**3+w[8]*i**2+w[9]*i)*cos(i)**2
    #return (w[0]*i**2+w[1]*i)*cos(i*w[2]**w[3]) + (w[4]*i**2+w[5]*i)*sin(i*w[6]**w[7])
    #return exp(w[0]*i)*sin(i) + w[1]
    #return w[0]*sin(i) + exp(w[1]*i)
    #return (w[0]*i**2+w[1]*i)*sin(w[2]*i) + w[3]*i**3 + w[4]*i**2 + w[5]*i + w[6]
    return (w[0]*i**2+w[1]*i+w[2])*sin(w[3]*i**2+w[4]*i+w[5])+w[6]

fig, ax = plt.subplots()   # must-have decoration

# function animate will be called endlessly, if you change values of y, the plot will be updated
def animate(i):
    ax.clear()      #comment this line if you want to see area instead of 1 line
    w = []
    w.append(round(uniform(-1, 2), 2))     #random float bwt -1 to 1, 2 decimal places
    w.append(round(uniform(-1, 1), 2))
    w.append(round(uniform(-1, 1), 2))
    w.append(round(uniform(-1, 1), 2))
    w.append(round(uniform(-1, 1), 2))
    w.append(round(uniform(-1, 1), 2))
    w.append(round(uniform(-1, 1), 2))
    w.append(round(uniform(-1, 1), 2))
    w.append(round(uniform(-1, 1), 2))
    w.append(round(uniform(-1, 1), 2))
    x = np.linspace(0, 30, 50)
    #f = [(a*i**2+b*i)*cos(i)**2 + c for i in x]
    actualY = []
    for i in x:
        actualY.append(evaluate(w, i))
    # normalize the data before proceeding
    minY = min(actualY)
    maxY = max(actualY) - minY
    for count, newY in enumerate(actualY):
        try:
            actualY[count] = ((newY - minY)/maxY)*1   #you can scale your plot as required
        except:
            actualY[count] = 0
    #print('Ratio:', ((newY - minY)/maxY)*1)
    # end of normalization
        
    ax.set_ylim([0, 1.5])
    #ax.set_xlim([0, 100])
#    ax.scatter(x, y)
    ax.plot(x, actualY, ':')

# enable animation with refresh rate 1000ms
anim = animation.FuncAnimation(fig, animate, frames=2000, interval=500)
plt.show()
