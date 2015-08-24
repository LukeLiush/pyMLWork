__author__ = 'kaggle'
#Filename: dt_tree.py
from math import log
import operator

def createTree(dataset, labels):
    classList = [examples[-1] for examples in dataset] # get the label classes
    if classList.count(classList[0]) == len(classList):
        # pick the first element if the count of the occurances of the first element == length of the classes,
        # then we can stop and return the classList[0] that tells me the value of the class.
        return classList[0]
    if len(dataset[0]) == 1:
        # if we only have used up all the attributes, but we still end up that we could not clear up classify the data
        # we take votes
        return majorityCnt(classList) # return the value of the class
    bestFeat = chooseBestFeatureToSplit(dataset)
    bestFeatLabel = labels[bestFeat]

    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataset]
    uniqueValues = set(featValues)
    for value in uniqueValues:
        subLabels = labels[:] # make a copy of the labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataset, bestFeat, value), subLabels)
    return myTree

def majorityCnt(classList):
    '''
    :param classList: the class list
    :return: the class label that has the highest count
    '''
    classCount = {} # class ditionary
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def chooseBestFeatureToSplit(dataset):
    numFeatures = len(dataset[0]) - 1
    baseEntropy = calcShannonEnt(dataset)
    bestInfoGain = 0.0
    bestFeature = -1 # initialize bestFeature with unknown i.e. -1

    # for each feature value
    for i in range(numFeatures):
        featList = [examples[i] for examples in dataset]
        uniqueValues = set(featList)
        newEntropy = 0.0
        for v in uniqueValues:
            subDataset = splitDataSet(dataset, i, v)
            prob = float(len(subDataset)) / len(dataset)
            newEntropy += prob * calcShannonEnt(subDataset)
        infoGain = baseEntropy - newEntropy
        print infoGain, i
        if bestInfoGain < infoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def calcShannonEnt(dataset):
    numRows = len(dataset) # number of dataset/entries
    labelCounts = {} # dictionary [label, count]
    for featVect in dataset: # find out how many examples there out for each label class
        currentLabel = featVect[-1] # the decision label
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0
    for key in labelCounts:
        prob = float(labelCounts[key])/numRows
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def splitDataSet(dataset, axis, val):
    retDataset = [] # returned newly split dataset
    for featVec in dataset:
        if featVec[axis] == val:
            reducedFeatVect = featVec[:axis]
            reducedFeatVect.extend(featVec[axis+1:])
            retDataset.append(reducedFeatVect)
    return retDataset

def createDataSet():
    dataSet = [[1, 1, 'Yes'],
               [1, 1, 'Yes'],
               [1, 0, 'No'],
               [0, 1, 'No'],
               [0, 1, 'No']
               ]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def main():
    a, b = createDataSet()
    chooseBestFeatureToSplit(a)

if __name__ == '__main__':
    main()

