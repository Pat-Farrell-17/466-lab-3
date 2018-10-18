import decisionTree as dt
import xmltodict
import csvParser
import random
import sys
import copy
from TreeNode import Node

def classL():
    c = random.randint(0,1)
    if c == 1:
        return "Obama"
    else:
        return "McCain"

# Takes a decision tree and a data point to classify and returns
# the predicted class label
def classifyPoint(tree, dataPoint):
    while tree.children:
        category = tree.name
        for child in tree.children:
            if dataPoint[category] == child.label:
                tree = child
        if not dataPoint[category] == tree.label: # no good branch
            return classL()

    return tree.name

# Takes a decision tree and a collection of data to classify and returns
# a list of tuples where each tuple is of the form:
#               (dataPoint (dict), classLabel (string))
def classifyCollection(tree, data):
    classification = []

    for dataPoint in data:
        classLbl = classifyPoint(tree, dataPoint)
        pointClassif = (dataPoint, classLbl)
        classification.append(pointClassif)

    return classification

def isTrainingSet(data):
    return ('Category' in data[1].keys())

def removeClassLabels(data):
    dc = copy.deepcopy(data)
    for d in dc:
        d.pop("Category")
    return dc

def accuracy(numRecords, numErrors):
    acc = (numRecords - numErrors) / numRecords * 100
    if acc < 0:
        acc = 0
    return acc

def errors(numRecords, numErrors):
    p_err = (numErrors / numRecords) * 100
    if p_err < 0:
        p_err = 0
    return p_err

def buildTree(filename):
    root = Node('Root', None)
    print("building tree...")
    with open(filename, 'r') as xmlFile:
        xml = xmlFile.read()
        d = xmltodict.parse(xml)

    print(d)
    print("\n\n")
    while d:
        for key, val in d.items():
            print("KEY: {}\nVAL: {}".format(key, val))
            d = val
            print("\n\nNEW D: {}".format(d))

def main():
    if not len(sys.argv) == 3:
        print("\t\tMissing arguments\n\tProper Call :\tpython classify.py <CSVFile> <XMLFile>")
        return

    dataFile = sys.argv[1]
    dTreeFile = sys.argv[2]

    data = csvParser.parse(dataFile)
    dataB = csvParser.parse("tree01-100-words.csv")
    attributes = list(data[0].keys())

    root = Node('Root', None)
    dt.build(dataB, attributes, root, 0.01)

    if (isTrainingSet(data)):
        print("\n\tTraining set detected as input, ignoring actual classes " + "during classification")

        actualClasses = []
        for dataPoint in data:
            actualClasses.append(dataPoint['Category'])
        dataC = removeClassLabels(data)

    else:
        dataC = data

    classes = classifyCollection(root, dataC)

    print("Print mode : [V]erbose [S]hort\t",end="")
    printMode = input()
    while not printMode.lower() == "v" and not printMode.lower() == "s":
        print("entered: |{}|".format(printMode))
        print("Please enter V for verbose printing or S for a shorter output")
        printMode = input()

    if printMode.lower() == "v":
        for classif in classes:
            print("\nDatapoint :")
            for key, val in classif[0].items():
                print("\t{} : {}".format(key, val))
            print("\tClassification for datapoint\t:\t{}".format(classif[1]))
    else:
        for i, classif in enumerate(classes):
            print("\tClassification for datapoint #{}\t:\t{}".format(i+1, classif[1]))

    if (isTrainingSet(data)):
        numErr = 0
        tot = 0
        print("\nErrors:\n====================================================")
        for i, classif in enumerate(classes):
            if not classif[1] == actualClasses[i]:
                print("Record {} classified as {}\tactual class {}".format(i, actualClasses[i], classif[1]))
                numErr += 1
            tot = i + 1
        print("\nTotal records classified:\t\t{}".format(tot))
        print("# records correctly classified:\t\t{}".format(tot - numErr))
        print("# records incorrectly classified:\t{}".format(numErr))
        print("Accuracy:\t\t\t\t{}%".format(accuracy(tot, numErr)))
        print("Error rate:\t\t\t\t{}%".format(errors(tot, numErr)))




if __name__ == '__main__':
	main()
