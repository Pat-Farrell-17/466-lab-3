from parsing import parseData
import math, sys

def euclidianDistance(pointA, pointB, attributes):
	distances = [(pointA[attribute] - pointB[attribute]) ** 2 for attribute in attributes[:-1]]
	return math.sqrt(sum(distances))

def addNeighbor(neighbors, distanceToAdd, neighborToAdd):
	neighbors.pop()
	if distanceToAdd > neighbors[len(neighbors) - 1][0]:
		neighbors.append((distanceToAdd, neighborToAdd))
		return distanceToAdd
	for index, (distance, neighbor) in enumerate(neighbors):
		if distanceToAdd < distance:
			neighbors.insert(index, (distanceToAdd, neighborToAdd))
			return neighbors[len(neighbors) - 1][0]

def knn(data, attributes, k):
	predictions = []

	for toClassifyIndex, pointToClassify in enumerate(data):
		nearestNeighbors = [(sys.maxsize, None)] * k
		maxNeighbor = sys.maxsize
		neighborsAdded = 0
		for index, dataPoint in enumerate(data):
			print(nearestNeighbors)
			if index != toClassifyIndex:
				distance = euclidianDistance(pointToClassify, dataPoint, attributes)
				if distance < maxNeighbor or neighborsAdded < 5:
					print('adding neighbor')
					maxNeighbor = addNeighbor(nearestNeighbors, distance, dataPoint)
					neighborsAdded += 1
		classifications = [neighbor['Class'] for _, neighbor in nearestNeighbors]
		predictions.append(max(set(classifications), key=classifications.count))
	return predictions

def main():
	data, attributes = parseData(sys.argv[1])
	predictions = knn(data, attributes, int(sys.argv[2]))

	correctPredictions = 0
	for index, prediction in enumerate(predictions):
		if data[index]['Class'] == prediction:
			correctPredictions += 1
	
	print(f'Correct Predictions: {correctPredictions}')

if __name__ == '__main__':
	main()