import random
import math
import numpy as np

"""
Neural network class:

TODO List:
    Add biases into each neuron before sent into activation function [X]
    Add back prop [X]
    Play around with mutating learning rate [X]
"""

class neuralNetwork:
    #2 layer neural network, 10 neurons per layer
    #Initilized with the number of inputs to be expecting and the number of outputs to be expecting
    def __init__(self, inp, out):
        self.inp = inp
        self.out = out
        #masses are the multipliers of each neuron layer
        self.masses = []
        self.biases = []
        #weights are the multiplied and summed inputs along each layer
        self.primers = []
        self.weights = [] #Activation of each neuron
        #Learning rate in this case is the highest percentage a mass can change during mutation
        #This will remain constant through families
        self.learningRate = 0.2
        self.delta = []
        """
    Masses are to be initilized as such:

        M_x_y_z where,
        x = the neuron layer you are in
        y = the neuron number you are going to
        z = the neuron number you are coming from

    Masses are going to filled randomly with numbers between -1 and 1 2 to start
    No biases are added between layers
    No sigmoid functions
    just a bare bone neural network.
        """
        self.fillBiases()
        for x in range(3):
            self.fillMasses(x)

    def fillMasses(self, layer):
        #Fills the masses array with random values between -1 and 1.
        #Place Holder/Starter for optimization
        if layer == 0:
            comeFrom = self.inp
            goTo = 3
        elif layer == 1:
            comeFrom = goTo = 3
        else:
            comeFrom = 3
            goTo = self.out
        massGoTo = []
        for y in range(goTo):
            massCome = []
            for z in range(comeFrom):
                massCome.append(random.uniform(-1,1))
            massGoTo.append(massCome)
        self.masses.append(massGoTo)

    def fillBiases(self):
        for layers in range(2):
            biases = []
            for bias in range(3):
                biases.append(random.uniform(-1,1))
            self.biases.append(biases)
        biases = []
        for i in range(self.out):
            biases.append(random.uniform(-1,1))
        self.biases.append(biases)

    def run(self, inpArr):
        #Sums product of weights and masses through the Neural Network
        self.weights = []
        self.primers = []
        self.weights.append(inpArr)
        for x in range(len(self.masses)):
            weight = []
            primer = []
            for my, by in zip(self.masses[x], self.biases[x]):
                total = by
                for mz, wy in zip(my, self.weights[x]):
                    total += (mz*wy)
                primer.append(total)
                weight.append(self.sigmoid(total))
            self.primers.append(primer)
            self.weights.append(weight)
            
    def sigmoid(self, x):
        return (1/(1+ np.exp(-1*x)))

    def sigmoidPrime(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def costDerivative(self, outA, desired):
        return (outA - desired)

    def getCost(self, desiredArr):
        cost = []
        total = 0
        for y, yPrime in zip(desiredArr, self.getOutput()):
            cost.append(0.5*(y - yPrime)**2)
        for c in cost:
            total += c
        return total
            

    def getOutput(self):
        return self.weights[-1]

    def toString(self):
        print('\nPrimers')
        print(self.primers)
        print('\nweights')
        print(self.weights)
        print('\nBiases')
        print(self.biases)
        print('\n')

    """
    Now are the Optimization Functions.
    First is mutation which is mainly used int he evolutionary arena.

    Second is BackPropagation which is used when controlling the fighters
    This is so they learn from your actions.
"""

    def mutate(self):
        #Create a child for the Neural Network and bump masses around 
        child = neuralNetwork(self.inp, self.out)
        child.masses = self.masses
        child.learningRate = self.learningRate
        child.biases = self.biases
        
        #for each mass, bump it up or down determined by the learning rate
        #TODO, play around with mutating the learning Rate
        for mx in range(len(child.masses)):
            for my in range(len(child.masses[mx])):
                for mz in range(len(child.masses[mx][my])):
                    mutationRate = random.uniform(-1* child.learningRate, child.learningRate)
                    child.masses[mx][my][mz] += mutationRate

        
        for bx in range(len(child.biases)):
            for by in range(len(child.biases[bx])):
                mutationRate = random.uniform(-1* child.learningRate, child.learningRate)
                child.biases[bx][by] += mutationRate

        return child

    def getMassTotal(self, layer, goTo):
        massTotal = 0
        for m in self.masses[layer - 1][goTo]:
            massTotal += m
        return massTotal


    def getError(self, error, x, comeFrom):
        errorTotal = 0
        massT = np.transpose(self.masses[-x + 1])
        massTotal = 0
        for goTo in range(len(error[-x + 1])):
            massTotal = 0
            #for each neuron connected to the one we're looking at:
            #calc massTotal connected to that neuron
            for z in range(len(self.masses[-x + 1][goTo])):
                massTotal += self.masses[-x + 1][goTo][z]

            #then add error proportional to the mass percentage by the error
            errorTotal += ((massT[comeFrom][goTo] * error[-x+1][z]) / float(massTotal))
            
        return errorTotal

    def backprop(self, desiredArr):
        #uses the desired output array to apply gradient descent to the masses and biases
        error = []
        for x in range(len(self.biases)):
            errorx = []
            for y in range(len(self.biases[x])):
                errorx.append(0)
            error.append(errorx)

        #find error for the first layer
        for y in range(len(error[-1])):
            error[-1][y] = desiredArr[y] - self.weights[-1][y]

        #Find error for all the other layers
        for x in range(2, len(error) + 1):
            for y in range(len(error)):
                error[-x][y] = self.getError(error, x, y)

        #Update all masses
        for x in range(len(self.masses)):
            for y in range(len(self.masses[x])):
                for z in range(len(self.masses[x][y])):
                    self.masses[x][y][z] += error[x][z] * self.learningRate / self.getMassTotal(y, z)
        #Update all Biases
            self.biases[x][y] += error[x][y] * self.learningRate

        return #End of Backprop()

myNN = neuralNetwork(2, 4)
myNN.run([0.5,0.33333])
print('Cost, Output')
print(myNN.getCost([0.25, 0.5, 0.75, 1.0]), myNN.getOutput())

for i in range(10000):
    myNN.run([0.5, 0.33333])    
    myNN.backprop([0.25, 0.5, 0.75, 1.0])
    
print('Cost, Output')
print( myNN.getCost([0.25,0.5,0.75, 1.0]), myNN.getOutput())
