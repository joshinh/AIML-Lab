import util
import numpy as np
import sys
import random

PRINT = True

###### DON'T CHANGE THE SEEDS ##########
random.seed(42)
np.random.seed(42)

def small_classify(y):
    classifier, data = y
    return classifier.classify(data)

class AdaBoostClassifier:
    """
    AdaBoost classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    
    """

    def __init__( self, legalLabels, max_iterations, weak_classifier, boosting_iterations):
        self.legalLabels = legalLabels
        self.boosting_iterations = boosting_iterations
        self.classifiers = [weak_classifier(legalLabels, max_iterations) for _ in range(self.boosting_iterations)]
        self.alphas = [0]*self.boosting_iterations

    def train( self, trainingData, trainingLabels):
        """
        The training loop trains weak learners with weights sequentially. 
        The self.classifiers are updated in each iteration and also the self.alphas 
        """
        
        self.features = trainingData[0].keys()
        "*** YOUR CODE HERE ***"
        sample_weights = [1.0/len(trainingData)] * len(trainingData)
        for i in range(self.boosting_iterations):
        	error = 0.0
           	self.classifiers[i].train(trainingData, trainingLabels, sample_weights)
        	predictions = self.classifiers[i].classify(trainingData)
        	for j in range(len(trainingLabels)):
        		if trainingLabels[j] != predictions[j]:
        			error += sample_weights[j]
        	for j in range(len(trainingLabels)):
        		if trainingLabels[j] == predictions[j]:
        			sample_weights[j] = (sample_weights[j] * error/(1-error))
        	total = sum(sample_weights)
        	#print(total)
        	sample_weights = [sample_weights[j]/total for j in range(len(trainingData))]
        	self.alphas[i] = float(np.log((1-error) / error)) 
        	
        	


        #util.raiseNotDefined()

    def classify( self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label. This is done by taking a polling over the weak classifiers already trained.
        See the assignment description for details.

        Recall that a datum is a util.counter.

        The function should return a list of labels where each label should be one of legaLabels.
        """

        "*** YOUR CODE HERE ***"
        poll_list = [0] * len(data)
        for i in range(self.boosting_iterations):
            curr_output = self.classifiers[i].classify(data)
            poll_list = [poll_list[j] + (curr_output[j]  * self.alphas[i]) for j in range(len(data))]
        final_prediction = []
        for i in range(len(data)):
            if poll_list[i] >= 0:
                final_prediction.append(1)
            else:
                final_prediction.append(-1)

        return final_prediction
        #util.raiseNotDefined()