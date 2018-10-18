import random
import sys
import csvParser
import decisionTree as dt
import classify
from lxml import etree
from TreeNode import Node
import itertools

def sliceData(data, k):
    numEntries = len(data)
    lenSlice = int(numEntries / k)
    dataSlices = []
    for i in range(k):
        slice = random.sample(data, lenSlice)
        dataSlices.append(slice)

    return dataSlices

def calcClassifErrors(data, classif):
    tp, tn, fp, fn = 0, 0, 0, 0
    for cl in classif:
        dP = cl[0]
        c = cl[1]
        if dP['Category'] == "Obama" and c == "Obama":
            tp += 1
        elif dP['Category'] == "Obama" and c == "McCain":
            fn += 1
        elif dP['Category'] == "McCain" and c == "Obama":
            fp += 1
        elif dP['Category'] == "McCain" and c == "McCain":
            tn += 1

    return (tp, tn, fp, fn)

def main():
    tp, tn, fp, fn = 0, 0, 0, 0

    if not len(sys.argv) >= 3:
        print("\t\tMissing arguments\n\tProper Call :\tpython validation.py <CSVFile> k-fold [<restrictions>]")
        return

    trainingSet = sys.argv[1]
    k = int(sys.argv[2])

    data = csvParser.parse(trainingSet)
    if k == -1:
        k = len(data) - 1
    elif k == 0:
        print("")
    """ slice data into training and testing subsets """
    dSlices = sliceData(data, k)
    attributes = list(data[0].keys())

    if len(sys.argv) == 4:
    	restrFile = sys.argv[3]
    	with open(restrFile, 'r') as file:
    		restr = file.read().split(',')

    	attributes = restrictAttrib(attributes[:-1], restr[1:])

    """ perform cross validation """
    kFoldResults = []
    print("\n\nRunning {}-fold cross validation on {} ...".format(k, trainingSet))
    for i in range(k):
        root = Node('Root', None)
        trainingSet = dSlices[0:i] + dSlices[i+1:]
        trainingSet = list(itertools.chain.from_iterable(trainingSet))
        testSet = dSlices[i]

        dt.build(trainingSet, attributes, root, 0.01)
        classif = classify.classifyCollection(root, testSet)
        classifErrors = calcClassifErrors(data, classif)
        kFoldResults.append(classifErrors)

    acc = 0
    accs = []
    for r in kFoldResults:
        tp += r[0]
        tn += r[1]
        fp += r[2]
        fn += r[3]
        acc = (r[0] + r[1]) / (r[0] + r[1] + r[2] + r[3])
        accs.append(acc)

    recall = (tp / (tp + fn)) * 100
    prec = (tp / (tp + fp)) * 100
    pf = (fp / (fp + tn)) * 100
    fm = ((2 * prec * recall) / (prec + recall))
    totAcc = ((tp + tn) / (tp + tn + fp + fn)) * 100
    avgAcc = (sum(accs) / len(accs)) * 100

    print("\nAggregate Confusion Matrix:")
    print("\t\t\tClassified Positive\t|\tClassified Negative")
    print("\t===================================================================")
    print("\tActual Positive |\t{}\t\t|\t{}\t".format(tp, fn))
    print("\t===================================================================")
    print("\tActual Negative |\t{}\t\t|\t{}\t".format(fp, tn))
    print("\n\tAggregate Performance Measures")
    print("Recall\t\t:\t{} %".format(recall))
    print("Precision\t:\t{} %".format(prec))
    print("pf\t\t:\t{} ".format(pf))
    print("f-measure\t:\t{} ".format(fm))
    print("\nOverall Accuracy:\t{} %".format(totAcc))
    print("Average Accuracy:\t{} %".format(avgAcc))

if __name__ == '__main__':
	main()
