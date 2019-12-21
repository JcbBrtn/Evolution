import random
import math
import numpy as np

"""
Neural network class:

TODO List:
    Add biases into each neuron before sent into activation function
    Add back prop
    Play around with mutating learning rate
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
        self.weights = []
        #Learning rate in this case is the highest percentage a mass can change during mutation
        #This will remain constant through families
        self.learningRate = random.random()
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
            comeFrom = 10
            goTo = self.out
        massGoTo = []
        for y in range(goTo):
            massCome = []
            for z in range(comeFrom):
                massCome.append(random.uniform(-10,10))
            massGoTo.append(massCome)
        self.masses.append(massGoTo)

    def fillBiases(self):
        for layers in range(2):
            biases = []
            for bias in range(10):
                biases.append(random.randint(-20, 20))
            self.biases.append(biases)
        biases = []
        for i in range(self.out):
            biases.append(random.randint(-20,20))
        self.biases.append(biases)

    def run(self, inpArr):
        #Sums product of weights and masses through the Neural Network

        self.weights.append(inpArr)
        for mx, wx, bx in zip(self.masses, self.weights, self.biases):
            weight = []
            for my, by in zip(mx, bx):
                total = by
                for mz, wy in zip(my, wx):
                    total += (mz*wy)
                weight.append(self.sigmoid(total))
            self.weights.append(weight)
            
    def sigmoid(self, x):
        return round((1/(1+ np.exp(-1*x))), 4)

    def getOutput(self):
        return self.weights[3]

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
