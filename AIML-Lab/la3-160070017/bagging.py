import util
import numpy as np
import sys
import random

PRINT = True

###### DON'T CHANGE THE SEEDS ##########
random.seed(42)
np.random.seed(42)

class BaggingClassifier:
    """
    Bagging classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    
    """

    def __init__( self, legalLabels, max_iterations, weak_classifier, ratio, num_classifiers):

        self.ratio = ratio
        self.num_classifiers = num_classifiers
        self.classifiers = [weak_classifier(legalLabels, max_iterations) for _ in range(self.num_classifiers)]

    def train( self, trainingData, trainingLabels):
        """
        The training loop samples from the data "num_classifiers" time. Size of each sample is
        specified by "ratio". So len(sample)/len(trainingData) should equal ratio. 
        """

        self.features = trainingData[0].keys()
        "*** YOUR CODE HERE ***"
        paired_data = []
        for i in range(len(trainingData)):
            paired_data.append((trainingData[i],trainingLabels[i]))
        for i in range(self.num_classifiers):
            new_pairs = util.nSample([1.0/len(trainingData)] * len(trainingData), paired_data, int(self.ratio * len(trainingData)))
            new_data, new_labels = zip(*new_pairs)
            self.classifiers[i].train(new_data,new_labels)

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
        for i in range(self.num_classifiers):
            curr_output = self.classifiers[i].classify(data)
            poll_list = [poll_list[j] + curr_output[j] for j in range(len(data))]
        final_prediction = []
        for i in range(len(data)):
            if poll_list[i] > 0:
                final_prediction.append(1)
            else:
                final_prediction.append(-1)

        return final_prediction

        #util.raiseNotDefined()
