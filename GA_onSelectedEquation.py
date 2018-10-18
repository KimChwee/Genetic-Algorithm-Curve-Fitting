"""
1-time setup:
If you are using Spyder via Anaconda
    Go to Tools --> Preferences
    Click on iPython Console, select "Graphics" tab on the right
    Under the "Graphic Backend" section, change the option to "QT" or "QT5"
If you are using Python IDLE, no setup required

Change the path and filename of your data file as required under __init__ method

### Genetic Algorithm CA [Sep-2018]

### Given a set of data, is there a formula behind it that matches closely and can be used for prediction?
### Neural Network can come close to the predict but the formula cannot be extracted after training
### Genetic Algorithm on the other hand, the formula can be extracted after trainning and applied for prediction!
    
# Team : Avengers
# Student Name      Student ID     User Id (for email)
# Goh Hui Kiang      A0178382U      E0267693
# Chin Weng Khin     A0178203J      E0267514
# Lim Kim Chwee      A0178196M      E0267507

Learning log:
    learn to plot graph
    learn to read data from file
    learn to plot graph using data from file
    learn to display animated graph
    learn to use trackbar
    design & code chromsome
    research on an appropriate mutation function for this problem
    re-learn polynomial & sin functions
    learn to refresh the graph after every N evolution
    research on a good crossover logic for this problem
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from math import *
from scipy.interpolate import spline
import time

# Object Oriented Programming and Genetic Algorithm are born to be the perfect match
class DNA(object):
# All one-time initialization + hyper parameter is here
    def __init__(self, ax):
        self.line, = ax.plot([], [], '-')
        self.evo = 0            # Evolution counter
        self.nPop = 100         # Population Size
        self.nLen = 7           # Chromosome length i.e. no. of coefficient
        self.nKeep = 0.2        # Survival rate 20%
        self.learn_rate = 0.1   # Learning rate for mutation used
        self.rPop = self.population(self.nPop)
        self.nMutate = 0.4      #Mutation probability
        self.nBreed = 0.2       #Breed 20% of population
        print('New Population created of size:', len(self.rPop))
        self.ax = ax
        """ # Concept: Generic formula are added here
        # Program will genetically evolve using these formula to find the best fit curve
        # User can modify the formula here as required for their business case
        # In future when more Maths are discovered, simply add them here """
        f = []
        """ # <<< For reference >>>
        # Depending on business scenario, change the formula as required
        # Add them if need and the program will evolve accordingly.
        # Note: GA is computationally expensive even for today's technology
        #y = exp(aX)*sin(bx) + c    #exponential sin wave
        #y = aX^2 + bX + C    #generic polynomial equation
        #y = (aX^2 + bX + c)sin(dX^2 + eX + f) + g    #generic formula for complex curve
        # <<< End of reference >>> """

###    <<<   y = (aX^2 + bX + c)sin(dX^2 + eX + f) + g   >>> Generic formula for complex curve
        #f.append('sin(w[0]*x**2) + w[1]*x**2 + w[2]*x + w[3]')
        #f.append('(w[0]*x**2 + w[1]*x + w[2])*sin(w[3]*x**2 + w[4]*x + w[5]) + w[6]*x**2 + w[7]*x + w[8]')
        f.append('(w[0]*x**2 + w[1]*x + w[2])*sin(w[3]*x**2 + w[4]*x + w[5]) + w[6]')
        
        self.formula = f
###    <<< Change your file path, file name as required, end your path with \\ >>>
        #fPath = 'C:\\Data\\'
        fPath = ''

        fname = 'GA-Order1Data-007.csv'   
        
        actualY = np.loadtxt(fPath + fname, delimiter=',', unpack=True)
        self.x = np.linspace(0, 10, len(actualY))
        # normalize the data before proceeding
        minY = min(actualY)
        maxY = max(actualY) - minY
        for count, newY in enumerate(actualY):
            actualY[count] = ((newY - minY)/maxY)*1   #you can scale your plot as required
        # end of normalization 
        self.actualY = actualY
        self.ax.set_ylim(min(actualY), max(actualY))
        self.ax.plot(self.x, actualY, 'x')
        #initialize a temp file for recording learning curve
        fLearnCurve = open("learningCurve.txt", 'w')
        fLearnCurve.close()
        
    def init(self):
        self.line.set_data([], [])
        return self.line,

    #Create a member of the population
    def individual(self, dec=1):
        return [ random.randint(-1*10**dec, 1*10**dec)/(10**dec) for p in range(self.nLen) ]
    
    # Creates a population consisting of nPop # of chromesome of length nLen
    def population(self, zPop):
        return [ self.individual() for x in range(zPop) ]

    def fitness(self, chromsome):
        predict = self.evaluate(chromsome)
        return np.sqrt(((predict - self.actualY) ** 2).mean())

    #Method Evaluate is to calculate entire Y values [array]
    def evaluate(self, w):
        f = []
        for x in self.x:
            p = 0
            for g in self.formula:
                p += eval(g)
            f.append(p)
        return f

    # simply convert derived formula into text for display
    def getFormula(self, w):
        ###    <<<   y = (aX^2 + bX + c)sin(dX^2 + eX + f) + g   >>>
        print('Evo#', self.evo, ' Best so far:', '(', w[0], 'X^2 +', w[1], 'X +', w[2], ')sin(', w[3], 'X^2 +', w[4], 'X +', w[5], ') +', w[6])

        """ Future enhancement, change the display to be more generic according to self.formula[] """
        #f = ''
        #This part is required when we have multiple formula in future
        #for q in self.formula:
        #    f += q

        #replace coefficient with the actual values
        #for cnt in range(len(w)):
        #    f.replace('w[' + str(cnt) + ']', str(w[cnt]))
        #print(w)
        #return f

        """ <<<<   Genetic Algorthim   >>>>
        #    Mutation, Survival of fittest, crossover etc GA logic will be contained here
        #    (Quite CPU intensive)
        #    This function will be repeatedly called until user close the pop up graph
        #
        #    Soul of GA:
        #        GA does not look for the BEST answer, it will always has the Best so far solution
        #        and will keep evolving better and better
        """
    def mutate(self, child):
        m_child = child
        for index in range(len(child)):
            if random.uniform(0, 1) <= self.nMutate:
                m_child[index] = self.individual()[index]
        return m_child
    
    def __call__(self, i):
        # This way the plot can continuously run and we just keep
        # watching new realizations of the process
        graded = []
        # Add fitness column and call the new array: Graded
        for chromsome in self.rPop:
            graded.append([self.fitness(chromsome), chromsome[:]])
        graded.sort()               #sort individual by fittness
        bestGrade = graded[0][1]    #1st row will always be the best fit
        #fLearnCurve.append(graded[0][0])   #Record fittness history to plot learning curve
        # plot best fit on graph
        y = self.evaluate(bestGrade)
        x_smooth = np.linspace(self.x.min(), self.x.max(), 200)
        y_smooth = spline(self.x, y, x_smooth)
        self.line.set_data(x_smooth, y_smooth)
        p , q = list(zip(*graded))   #extract the sorted population
#
        while(True):
            try:
                fLearnCurve = open("learningCurve.txt", 'a')
                break
            except:
                time.sleep(0.1)
        fLearnCurve = open("learningCurve.txt", 'a')
        fLearnCurve.write(str(graded[0][0]) + '\n')
        fLearnCurve.close()
#

        """     <<< Start of Survival of the fittest & Crossover logic  >>>
        #       <<< Top N% fittest individuals stay  >>>
        #       <<< N% of existing population is used to breed next generation >>>
        #       For every new child you decide if it will result from crossover by random probability.
        #       If yes, then you select two parents, eg. through roulette wheel selection or tournament selection.
        #       The two parents make a child, then you mutate it with mutation probability and add it to the next generation.
        #       If no, then you select only one "parent" clone it, mutate it with probability and add it to the next population.
        """
        keep = int(self.nPop * self.nKeep)   #no. of population to retain
 
        
        """ Using roulette selection, the chance of getting stuck in local optimal is very high
        since the top fittest might have similar base formula. Tournament selection is better for this application """
        breed = int(self.nBreed * self.nPop)
        newGen = []
        for breeding in range(breed):
            t = [random.randint(0, self.nPop-1), random.randint(0, self.nPop-1)]   #randomly pick 2 individuals to breed
            child = self.rPop[t[0]][0:4] + self.rPop[t[1]][4:]    #first half of parent #1 merge with 2nd half of parent #2 to breed child
            newGen.append(self.rPop[t[0]])
            newGen.append(self.rPop[t[1]])
            newGen.append(self.mutate(child))
        #testing only
        #newGen.append([0, -0.4, 0.8, 0.4, -4.8, -8.2, 8])
        newGraded = []
        for chromsome in newGen:
            newGraded.append([self.fitness(chromsome), chromsome[:]])
        newGraded.sort()

        c, d = list(zip(*newGraded))   #extract the sorted population
        # Keep the top N individuals, replace the rest with new individuals
        self.rPop = list(q)[0:keep]
        self.rPop += list(q)[0:breed]
        self.rPop += self.population(self.nPop - keep - breed)
#       <<< End of Survival of the fittness & Crossover logic   >>>

        self.evo += 1
        if self.evo % 20 == 0:     #display result at every 20 evolution
            #print('Evo#', self.evo, ' Best so far:', self.getFormula(bestGrade))
            print('RMSE:', graded[0][0])
            self.getFormula(bestGrade)
        return self.line,

def move_plotWindow(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)
        
# Plot learning curve [live!]
def animate(i):
    graph_data = open('learningCurve.txt', 'r').read()
    lines = graph_data.split('\n')
    
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            ys.append(float(line))
    xs = np.linspace(0, len(ys), len(ys))
    ax2.clear()
    ax2.set_title('Learning Curve')
    ax2.plot(xs, ys)

#<<< main >>>

random.seed(5)    #for re-production of result during demo
fig, ax = plt.subplots()
ax.set_title('Main')
move_plotWindow(fig, 0, 100)    # Set Main window on the left
ud = DNA(ax)
#Main Animation Plot
anim = FuncAnimation(fig, ud, frames=np.arange(100), init_func=ud.init, interval=20, blit=True)

#Accuracy plot
fig2 = plt.figure()
move_plotWindow(fig2, 700, 100)     # Set Accuracy plot window on the right
ax2 = fig2.add_subplot(1,1,1)

ani = FuncAnimation(fig2, animate, interval=1000)
plt.show()
