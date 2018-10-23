from parsing import parseData
import time
import math, sys

def euclidianDistance(pointA, pointB, attributes):
	distances = [(pointA[attribute] - pointB[attribute]) ** 2 for attribute in attributes[:-1]]
	return math.sqrt(sum(distances))

def categoricalDistance(pointA, pointB, attributes):
	matches = sum(1 for attribute in attributes[:-1] if pointA[attribute] == pointB[attribute])
	numAttributes = len(attributes) - 1
	return (numAttributes - matches) / numAttributes

def addNeighbor(neighbors, distanceToAdd, neighborToAdd):
	neighbors.pop()
	if distanceToAdd >= neighbors[len(neighbors) - 1][0]:
		neighbors.append((distanceToAdd, neighborToAdd))
		return distanceToAdd
	for index, (distance, neighbor) in enumerate(neighbors):
		if distanceToAdd < distance:
			neighbors.insert(index, (distanceToAdd, neighborToAdd))
			return neighbors[len(neighbors) - 1][0]

def knn(data, attributes, k, getDistance):
	predictions = []

	for toClassifyIndex, pointToClassify in enumerate(data):
		nearestNeighbors = [(sys.maxsize, None)] * k
		maxNeighbor = sys.maxsize
		for index, dataPoint in enumerate(data):
			if index != toClassifyIndex:
				distance = getDistance(pointToClassify, dataPoint, attributes)
				if distance < maxNeighbor:
					maxNeighbor = addNeighbor(nearestNeighbors, distance, dataPoint)
		classifications = [neighbor['Class'] for _, neighbor in nearestNeighbors]
		predictions.append(max(set(classifications), key=classifications.count))
	return predictions

def main():
	data, attributes = parseData(sys.argv[1])
	distanceFunction = euclidianDistance if sys.argv[3] == 'numeric' else categoricalDistance
	start = time.time()
	predictions = knn(data, attributes, int(sys.argv[2]), distanceFunction)
	print(f'Running Time: {time.time() - start}')

	correctPredictions = 0
	for index, prediction in enumerate(predictions):
		if data[index]['Class'] == prediction:
			correctPredictions += 1
	
	print(f'Accuracy: {correctPredictions / len(data)}')

if __name__ == '__main__':
	main()