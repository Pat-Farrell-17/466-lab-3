import parsing, collections, math, sys, copy
from TreeNode import Node
from operator import itemgetter
from lxml import etree

# ================= Helper Functions ==========================================

# Returns a set of all the unique values of attribute in data set D
def getVals(D, attribute):
    return set([d[attribute] for d in D])

def categoryCounts(data):
    categories = [d['Class'] for d in data]
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

def getDecision(className):
    irisClasses = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
    shroomClasses = ["e", "p"]
    letterClasses = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
        "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "X", "Y", "Z"]
    if className in irisClasses:
    	return irisClasses.index(className) + 1
    elif className in shroomClasses:
    	return shroomClasses.index(className) + 1
    elif className in letterClasses:
        return letterClasses.index(className) + 1
    else:
    	return -1

def outputXML(root):
	num = 1;
	rootNode = etree.Element("node", var="{}".format(root.name))
	for child in root.children:
		edge = etree.Element("edge", var="{}".format(child.label), num ="{}".format(num))
		num+=1
		rootNode.append(edge)
		if child.children:
			childNode = outputXML(child)
		else:
			childNode = etree.Element("decision", choice="{}".format(child.name), end="{}".format(getDecision(child.name)))
		edge.append(childNode)

	return rootNode

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

# Takes a list of dictionaries as data and an attribute
# and returns a dictionary where each key is a value in
# the domain of attribute and the values are all data
# points that have that value in them
def groupByAttribute(data, attribute):
	attributeDict = {}
	for row in data:
		if row[attribute] not in attributeDict:
			attributeDict[row[attribute]] = []
		attributeDict[row[attribute]].append(row)
	return attributeDict

# Calculates the entropy of splitting D on attr with splitVal as
# the split point
def entropyBinSplit(D, attr, splitVal):

    Dsplit = splitOnVal(D, attr, splitVal)
    # Set of all data points d in D s.t. d[attr] <= splitVal
    Dlt = Dsplit[0]
    # Rest of D (all d in D s.t. d[attr] > splitVal)
    Dgt = Dsplit[1]

    # Calculate the entropy of the split and return it
    return ( (len(Dlt) / len(D)) * entropy(Dlt) ) + ( (len(Dgt) / len(D)) * entropy(Dgt))

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

#       Modified selection method to use numeric data
# Input:    A - List of attributes
#           D - Set of data
#           threshold - information gain threshold to use
# Ouput:    Attribute in A with the highest information gain
def selectSplittingAttributeN(attribs, data, threshold):
    # Calculate current entropy of the dataset and init variables
    initEntropy = entropy(data)
    gain, entrpy = {}, {}
    maxGain, toSplit = 0, 0
    bestVal = -1
    best = "nothin"
    gain[best] = 0
    for attr in attribs:
        # Ignore class labels for splitting purposes
        if attr == 'Class':
            continue
        # If the attribute is continuous, find the entropy of the
        # best value to do a binary split on
        if isinstance(data[0][attr], float):
            toSplit = findBestSplit(attr, data)
            entrpy[attr] = entropyBinSplit(data, attr, toSplit)
        else:
            attributeDict = groupByAttribute(data, attr)
            entropyAfterSplit = sum(len(group) / len(data) * entropy(group) for
                group in attributeDict.values())
            entrpy[attr] = entropyAfterSplit

        infoGain = initEntropy - entrpy[attr]
        #print("Info gain of {}\t\t:\t{}".format(attr, infoGain))
        # Keep track of highest info gain and the corresponding split
        # attribute and val
        if infoGain > maxGain:
            maxGain = infoGain
            best = attr
            bestVal = toSplit

        gain[attr] = initEntropy - entrpy[attr]
    return (best, bestVal) if gain[best] > threshold else None

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
        #print("Info gain for splitting {} on {}\t:\t{}".format(attr, val, infoGain))
        gain[val] = initEntropy - entropySplit

    return bestSplit

# ================= End Helper Functions ======================================

# C4.5 Decision Tree Algorithm
def build(data, attributes, tree, threshold):

    if isUniform(d['Class'] for d in data):    # All class labels are the same
    	tree.setName(data[0]['Class'])
    elif len(attributes) == 0:                 # No more attributes
    	tree.setName(mostFrequentCategory(data))
    else:
        bestAttribute = selectSplittingAttributeN(attributes, data, threshold)
        if not bestAttribute:                  # No best attribute to split on
        	tree.setName(mostFrequentCategory(data))
        else:
            valToSplit = bestAttribute[1]   # -1 if attribute is categorical
            bestAttribute = bestAttribute[0]

            tree.setName(bestAttribute)
            if valToSplit > 0: # attribute is continuous
                # Split data on valToSplit
                splits = splitOnVal(data, bestAttribute, valToSplit)

                # Recursive call on data <= split val
                nodeLT = Node(None, "<= {}".format(valToSplit))
                tree.addChild(nodeLT)
                build(splits[0], attributes, nodeLT, threshold)

                # Recursive call on data > split val
                nodeGT = Node(None, "> {}".format(valToSplit))
                tree.addChild(nodeGT)
                build(splits[1], attributes, nodeGT, threshold)

            else:               # attribute is categorical
                attributeDict = groupByAttribute(data, bestAttribute)
                for attributeName in attributeDict.keys():
                    newData = attributeDict[attributeName]

                    if len(newData) > 0:
                        newAttributes = list(attributes)
                        newAttributes.remove(bestAttribute)

                        childNode = Node(None, attributeName)
                        tree.addChild(childNode)
                        build(newData, newAttributes, childNode, threshold)


def main():
    """
    if not len(sys.argv) >= 2:
        print("\t\tMissing arguments\n\tProper Call :\tpython C45.py <CSVFile> [<Restrictions>]")
        return

    dataFile = sys.argv[1]

    d = parsing.parseData(dataFile)
    data = d[0]
    attributes = d[1]

    if len(sys.argv) == 3:
        restrFile = sys.argv[2]
        with open(restrFile, 'r') as file:
            restr = file.read().split(',')

        attributes = restrictAttrib(attributes[:-1], restr[1:])

    """
    # This is all just print testing bs
    shrooms=r"E:\Documents\CSC466\Lab 3\466-lab-3.git\trunk\agaricus-lepiota.data.csv"
    iris = r"E:\Documents\CSC466\Lab 3\466-lab-3.git\trunk\iris.data"
    letters=r"E:\Documents\CSC466\Lab 3\466-lab-3.git\trunk\letter-recognition.data.csv"
    data, attributes = parsing.parseData(letters)

    print(attributes)
    print("Number of records : {}\nWith  {}  different attributes"
        .format(len(data), len(attributes)))
    #s = selectSplittingAttributeN(attributes, data, 0.01)
    #en = entropyBinSplit(data, s[0], s[1])
    #print(en)

    root = Node('Root', None)
    build(data, attributes, root, 0.3)
    xmlOutput = etree.tostring(outputXML(root), pretty_print=True, encoding='unicode')
    print(xmlOutput)




if __name__ == '__main__':
	main()
