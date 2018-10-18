import parsing, collections, math, sys
import copy
from TreeNode import Node
from operator import itemgetter
from lxml import etree

# ================= Helper Functions ==========================================

# Returns a set of all the unique values of attribute in data set D
def getVals(D, attribute):
    return set([d[attribute] for d in D])

def categoryCounts(data):
    categories = [dict['Class'] for dict in data]
    return dict(collections.Counter(categories))

def mostFrequentCategory(data):
    dict = categoryCounts(data)
    return max(dict.keys(), key=lambda key: dict[key])

def entropy(data):
	n = len(data)
	return -sum(cnt / n * math.log2(cnt / n) for
        cnt in categoryCounts(data).values())

def isUniform(list):
    return len(set(list)) <= 1

# TODO implement
def isContinuous(attribute):
    return None

# Restricts the attribute list to use for C4.5 based on optional commandline
# argument file
def restrictAttrib(att, restr):
	attributes = copy.deepcopy(att)
	attR = []
	for i, r in enumerate(restr):
		if int(r) < 1:
			attributes[i] = "-"
	for j, attribute in enumerate(attributes):
		if not attribute == "-":
			attR.append(attribute)
	return attR

# Calculates the entropy of splitting D on attr with splitVal as
# the split point
def entropyBinSplit(D, attr, splitVal):

    Dsplit = splitOnVal(D, attr, splitVal)
    # Set of all data points d in D s.t. d[attr] <= splitVal
    Dlt = Dsplit[0]
    # Rest of D (all d in D s.t. d[attr] > splitVal)
    Dgt = Dsplit[1]

    # Calculate the entropy of the split and return it
    return - ( (len(Dlt) / len(D)) * entropy(Dlt) -
                ( (len(Dgt) / len(D)) * entropy(Dgt)))

# Splits D into two sets (X, Y)
# where X is every data point d in D s.t. d[attr] <= splitVal
# and Y is the rest of D (every d in D s.t. d[attr] > splitVal)
def splitOnVal(D, attr, splitVal):
    lt, gt = [], []
    for d in D:
        if float(d[attr]) <= splitVal:
            lt.append(d)
        else:
            gt.append(d)
    return (lt, gt)

# ================= End Helper Functions ======================================

#       Modified selection method to use numeric data
# Input:    A - List of attributes
#           D - Set of data
#           threshold - information gain threshold to use
# Ouput:    Attribute in A with the highest information gain
def selectSpittingAttributeN(A, D, threshold):
    # Calculate current entropy of the dataset and init variables
    initEntropy = entropy(D)
    gain, entropy = {}, {}
    maxGain = 0
    best = ""

    for attr in A:
        # Ignore class labels for splitting purposes
        if attr == 'Class':
            continue

        # If the attribute is continuous, find the entropy of the
        # best value to do a binary split on
        if True:
            toSplit = findBestSplit(attr, D)
            entropy[attr] = entropyBinSplit(D, attr, toSplit)
        else:
            entropy[attr] = entropy(D)

        infoGain = initEntropy - entropy[attr]
        # Keep track of highest info gain and the corresponding split
        # attribute
        if infoGain > maxGain:
            maxGain = infoGain
            best = attr

        gain[attr] = initEntropy - entropy[attr]

    return best if gain[best] > threshold else None

# Finds the value of attr that will give the highest information gain
# when split on
def findBestSplit(attr, D):
    # Initialize variables
    initEntropy = entropy(D)
    attrVals = getVals(D, attr)
    counts = dict((val, 0) for val in attrVals)
    gain = copy.deepcopy(counts)
    maxGain, bestSplit = 0, 0.0

    # Count total # of occurences of each value of attr in D and store
    # them in the counts dict where each key:value pair is
    #           (attribute value : # occurences)
    for dataPnt in D:
        counts[dataPnt[attr]] += 1

    # Calculate the information gain for splitting on each value
    for val in counts.keys():
        entropySplit = entropyBinSplit(D, attr, val)
        infoGain = initEntropy - entropySplit

        # Keep track of the highest info gain and the corresponding
        # split value
        if infoGain > maxGain:
            bestSplit = val
            maxGain = infoGain
        #print("Info gain for splitting on {}\t:\t{}".format(val, infoGain))
        gain[val] = initEntropy - entropySplit

    return (bestSplit, maxGain)


def main():

    # This is all just testing bs
    d = parsing.parseIris("E:\Documents\CSC466\Lab 3\\466-lab-3.git\\trunk\iris.data")
    attributes = list(d[0].keys())
    print(attributes)
    print("Length of dataset: {}".format(len(d)))
    """for dP in d:
    	print(dP)
    """
    toSplit = selectSpittingAttributeN(attributes, d, 0.01)
    print(toSplit)



if __name__ == '__main__':
	main()
