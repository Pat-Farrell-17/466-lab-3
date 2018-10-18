import parsing, collections, math, sys
import copy
from TreeNode import Node
from operator import itemgetter
from lxml import etree

#       Modified selection method to use numeric data
# Input:    A - List of attributes
#           D - Set of data
#           threshold - information gain threshold to use
# Ouput:    Attribute in A with the highest information gain
def selectSpittingAttributeN(A, D, threshold):
    # Calculate current entropy of the dataset
    initEntropy = entropy(D)
    infoGain, entropy = {}, {}

    for attr in A:
        # Ignore class labels for splitting purposes
        if attr == 'Class':
            continue

        if isContinuous(attr):
            toSplit = findBestSplit(attr, D)
            entropy[attr] = entropyBinSplit(D, attr, toSplit)
        else:
            entropy[attr] = entropy(D)

        infoGain[attr] = initEntropy - entrop[attr]

    best = max(infoGain)    # Need the ATTRIBUTE, not the info gain itself
    return best if infoGain[best] > threshold else None

# Finds the value of attr that will give the highest information gain
# when split on
def findBestSplit(attr, D):
    initEntropy = entropy(D)
    attrVals = getVals(D, attr)
    counts = dict((val, 0) for val in attrVals)
    gain = copy.deepcopy(counts)
    maxGain, bestSplit = 0, 0.0

    # Count total # of occurences of each value of attr in D
    for dataPnt in D:
        counts[dataPnt[attr]] += 1

    # Calculate the information gain for splitting on each value
    for val in counts.keys():
        entropySplit = entropyBinSplit(D, attr, val)
        infoGain = initEntropy - entropySplit

        if infoGain > maxGain:
            bestSplit = val
            maxGain = infoGain
        print("Info gain for splitting on {}\t:\t{}".format(val, infoGain))
        gain[val] = initEntropy - entropySplit

    return (bestSplit, maxGain)

# Returns a set of all the unique values of attribute in data set D
def getVals(D, attribute):
    return set([d[attribute] for d in D])

def categoryCounts(data):
    categories = [dict['Class'] for dict in data]
    return dict(collections.Counter(categories))

def entropy(data):
	n = len(data)
	return -sum(count / n * math.log2(count / n) for count in categoryCounts(data).values())

# Returns the entropy of splitting D on attr with splitVal as
# the split point.
def entropyBinSplit(D, attr, splitVal):

    Dsplit = splitOnVal(D, attr, splitVal)
    # Set of all data points d in D s.t. d[attr] <= splitVal
    Dlt = Dsplit[0]
    # Rest of D (all d in D s.t. d[attr] > splitVal)
    Dgt = Dsplit[1]

    # Calculate the entropy of the split and return it
    return - ( (len(Dlt) / len(D)) * entropy(Dlt) -
                ( (len(Dgt) / len(D)) * entropy(Dgt)))

# Splits D into two sets (X, y)
# where X is every d in D s.t. d[attr] <= splitVal
# and Y is the rest of D (every d in D s.t. d[attr] > splitVal)
def splitOnVal(D, attr, splitVal):
    lt, gt = [], []
    for d in D:
        if float(d[attr]) <= splitVal:
            lt.append(d)
        else:
            gt.append(d)
    return (lt, gt)

# TODO
def isContinuous(attribute):
    return None

def main():

    d = parsing.parseIris("E:\Documents\CSC466\Lab 3\iris.data")
    print("Length of dataset: {}".format(len(d)))
    """for dP in d:
    	print(dP)
    """
    split = splitOnVal(d, 'Sepal Width', 3.0)
    cnts = findBestSplit('Sepal Width', d)
    print(cnts)

    #print(entropyBinSplit(d, 'Sepal Length', 5.0 ))
    #print("LT : {}\tGT : {}".format(len(split[0]), len(split[1])))
    #for i in range(10):
    #    print("===============================")
    #    print(split[0][i])
    #    print(split[1][i])

if __name__ == '__main__':
	main()
