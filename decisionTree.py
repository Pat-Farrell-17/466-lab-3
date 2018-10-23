from TreeNode import Node
import csvParser, collections, math, sys
from itertools import groupby
from operator import itemgetter

def categoryCounts(data):
	categories = [dict['Category'] for dict in data]
	return dict(collections.Counter(categories))

def mostFrequentCategory(data):
	dict = categoryCounts(data)
	return max(dict.keys(), key=lambda key: dict[key])

def entropy(data):
	n = len(data)
	return -sum(count / n * math.log2(count / n) for count in categoryCounts(data).values())

def isUniform(list):
	return len(set(list)) <= 1

def groupByAttribute(data, attribute):
	attributeDict = {}
	for row in data:
		if row[attribute] not in attributeDict:
			attributeDict[row[attribute]] = []
		attributeDict[row[attribute]].append(row)
	return attributeDict

def selectSplittingAttribute(data, attributes, threshold):
	currentEntropy = entropy(data)
	bestAttribute = None
	maxGain = -1
	for attribute in attributes:
		if attribute == 'Category':
			continue
		attributeDict = groupByAttribute(data, attribute)
		entropyAfterSplit = sum(len(group) / len(data) * entropy(group) for group in attributeDict.values())
		informationGain = currentEntropy - entropyAfterSplit
		if informationGain > maxGain:
			maxGain = informationGain
			bestAttribute = attribute
	return bestAttribute if maxGain > threshold else None


# C4.5 Decision Tree Algorithm
def build(data, attributes, tree, threshold):
	if isUniform(dict['Category'] for dict in data):
		tree.setName(data[0]['Category'])
	elif len(attributes) == 0:
		tree.setName(mostFrequentCategory(data))
	else:
		bestAttribute = selectSplittingAttribute(data, attributes, threshold)
		if not bestAttribute:
			tree.setName(mostFrequentCategory(data))
		else:
			tree.setName(bestAttribute)
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
	data = csvParser.parse(sys.argv[1])
	attributes = list(data[0].keys())
	root = Node('Root', None)
	build(data, attributes, root, 0.01)
	print(root.name)
	for child in root.children:
		print(child.name)


if __name__ == '__main__':
	main()