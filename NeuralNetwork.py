import random
import math

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
        for x in range(3):
            self.fillMasses(x)

    def fillMasses(self, layer):
        #Fills the masses array with random values between -1 and 1.
        #Place Holder/Starter for optimization
        if layer == 0:
            comeFrom = self.inp
            goTo = 10
        elif layer == 1:
            comeFrom = goTo = 10
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

    def run(self, inpArr):
        #Sums product of weights and masses through the Neural Network

        self.weights.append(inpArr)
        for mx, wx in zip(self.masses, self.weights):
            weight = []
            for my in mx:
                total = 0
                for mz, wy in zip(my, wx):
                    total += (mz*wy)
                weight.append(self.sigmoid(total))
            self.weights.append(weight)
            
    def sigmoid(self, x):
        return round((1/(1+ math.exp(-1*round(x,4)))), 4)

    def getOutput(self):
        return self.weights[3]

    def mutate(self):
        #Create a child for the Neural Network and bump masses around 
        child = neuralNetwork(self.inp, self.out)
        child.masses = self.masses
        child.learningRate = self.learningRate
        
        #for each mass, bump it up or down determined by the learning rate
        #TODO, play around with mutating the learning Rate
        for mx in range(len(child.masses)):
            for my in range(len(child.masses[mx])):
                for mz in range(len(child.masses[mx][my])):
                    mutationRate = random.uniform(-1* child.learningRate, child.learningRate)
                    child.masses[mx][my][mz] += mutationRate

        return child
