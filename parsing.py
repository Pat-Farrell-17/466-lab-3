import json, sys, copy

def parseIris(filename):
    dataPoints = []
    dataDict = {}
    attributes = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width', 'Class']
    with open(filename, 'r') as file:
    	for line in file.read().split('\n'):
            if len(line) > 0:
                dataPoints.append(line.split(','))

    dataDict = makeDict(attributes, dataPoints)
    return dataDict

def makeDict(attr, D):
    data = []
    dP = {}
    i = 0

    for dataPoint in D:
        for attribute in attr:
            if attribute == 'Class':
                dP[attribute] = dataPoint[i]
            else:
                dP[attribute] = float(dataPoint[i])
            i+= 1
        data.append(copy.deepcopy(dP))
        i = 0

    return data

def main():

	d = parseIris("E:\Documents\CSC466\Lab 3\iris.data")
	for dP in d:
		print(dP)
	#print(json.dumps(parse(sys.argv[1]), indent=2))

if __name__ == '__main__':
	main()
