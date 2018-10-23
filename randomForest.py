import sys, random, collections
from parsing import parseData
from classify import classifyPointNum, classifyPointCat
from dTreeNumeric import build as buildTree
from TreeNode import Node

NUM_FOLDS = 10
THRESHOLD = 0.03
OUTPUT_FILE = 'results.txt'

def selectRandomData(data, attributes, numAttributes, numDataPoints):
	randomDataPoints = []

	randomAttributes = list(attributes)
	random.shuffle(randomAttributes)
	randomAttributes = randomAttributes[:numAttributes]

	for i in range(numDataPoints):
		randomDataPoints.append(random.choice(data))

	return randomDataPoints, randomAttributes

def splitList(lst, n):
    return [lst[i::n] for i in range(n)]

def getTrainingSet(dataFolds, holdoutSetIndex):
	trainingSet = []
	for index, dataFold in enumerate(dataFolds):
		if index != holdoutSetIndex:
			trainingSet += dataFold

	return trainingSet

def tenFoldCrossValidation(data, attributes, numAttributes, numDataPoints, numTrees):
	dataCopy = list(data)
	random.shuffle(dataCopy)
	dataFolds = splitList(dataCopy, NUM_FOLDS)
	predictions = []

	with open(OUTPUT_FILE, 'w') as outputFile:
		totalUncategorized = 0
		for holdoutSetIndex, dataFold in enumerate(dataFolds):
			trainingSet = getTrainingSet(dataFolds, holdoutSetIndex)
			classifs, uncategorizedPoints = randomForest(trainingSet, attributes, numAttributes, numDataPoints, numTrees, dataFolds[holdoutSetIndex])
			totalUncategorized += uncategorizedPoints
			for index, classif in classifs:
				outputFile.write(f'id:{index}, class:{classif}\n')
				predictions.append((index, classif))

	return predictions, totalUncategorized


def randomForest(data, attributes, numAttributes, numDataPoints, numTrees, holdoutSet):
	trees = []
	uncategorizedPoints = 0
	for _ in range(numTrees):
		randomData, randomAttributes = selectRandomData(data, attributes, numAttributes, numDataPoints)
		currentTree = Node('Root', None)
		buildTree(randomData, randomAttributes, currentTree, THRESHOLD)
		trees.append(currentTree)

	bestClassifs = []
	for index, dataPoint in enumerate(holdoutSet):
		classifs = [classifyPointCat(tree, dataPoint) for tree in trees]
		classifs = list(filter(lambda x: x is not None, classifs))
		if len(classifs) == 0:
			uncategorizedPoints += 1
			continue
		mostFreqClassif = max(classifs, key=classifs.count)
		bestClassifs.append((dataPoint['id'], mostFreqClassif))

	return bestClassifs, uncategorizedPoints

def getAccuracy(data, predictions, totalUncategorized):
	correctPredictions = 0
	for index, prediction in predictions:
		if prediction == data[index]['Class']:
			correctPredictions += 1
	print(f'Uncategorized Points: {totalUncategorized}')
	return correctPredictions / (len(data) - totalUncategorized)


def main():
	data, attributes = parseData(sys.argv[1])
	predictions, totalUncategorized = tenFoldCrossValidation(data, attributes, *(int(num) for num in sys.argv[2:5]))
	accuracy = getAccuracy(data, predictions, totalUncategorized)
	print(f'Accuracy of algorithm: {accuracy}')

if __name__ == '__main__':
	main()