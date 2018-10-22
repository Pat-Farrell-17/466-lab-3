import c45, math, parsing, copy

# Euclidean distance function for numeric data
def distance(pointA, pointB):
    sum = 0
    for attrib in pointA.keys():
        if isinstance(pointA[attrib], float):
            sum += (pointA[attrib] - pointB[attrib]) ** 2

    return math.sqrt(sum)

# Distance function for categorical data
def matchDistance(pointA, pointB):
    attribs = pointA.keys()
    numMatching = matching(pointA, pointB)
    return (len(attribs) - numMatching) / len(attribs)

# Returns the number of attributes where
# pointA[attribute] = pointB[attribute]
def matching(pointA, pointB):
    matching = 0
    for attrib in pointA.keys():
        if pointA[attrib] == pointB[attrib]:
            matching += 1
    return matching

# Returns the k data entries with the shortest distance measures
# distanceD must be of the form { <dataPoint dict> : distance, ...}
# where distance is a float
def getNearest(k, distanceD):
    distances = copy.deepcopy(distanceD)
    selected = 0
    kNearest = []
    while selected < k:
        # Get key (data point) with the minimum value
        nearest = min(distances, key=lambda j : j[1])


        kNearest.append(nearest)
        distances.remove(nearest)
        selected += 1

    return kNearest

def classifyData(data, k):
    classif = []
    for d in data:
        predicted = knn(data, d, k)
        actual = d['Class']
        classif.append((predicted, actual))
    return classif

def numErrors(classif):
    errors = 0
    for c in classif:
        if not c[0] == c[1]: # Predicted =? actual
            errors+= 1
    return errors

# K-Nearest Neighbors classifier
def knn(data, toClassify, k):
    #print("Classifying \n\t{}".format(toClassify))
    if not k >= 1:                                      # K must be positive
        print("Error : K value must be greater than 0")
        return None

    distances = []

    for d in data:
        if isinstance(list(d.values())[0], float):      # Data is numeric
            dist = distance(d, toClassify)
        else:                                           # Data is categorical
            dist = matchDistance(d, toClassify)
        distances.append((d, dist))

    kNearest = getNearest(k, distances)


    return c45.mostFrequentCategory([d[0] for d in kNearest])


def test_dist(d):
    template = copy.deepcopy(d[0])
    t1 = copy.deepcopy(template)
    for a in t1.keys():
        if a == 'Class':
            continue
        t1[a] = 1.0
    t2 = copy.deepcopy(template)
    for a in t2.keys():
        if a == 'Class':
            continue
        t2[a] = 0.0

    print("\nDistance Testing")

    print("\ttesting distance to the same point . . .\t",end="")
    if (distance(d[0], d[0]) > 0):
        print("FAILED")
    else:
        print("ok")

    print("\ttesting associativity . . .\t\t\t",end="")
    if not distance(d[0], d[1]) == distance(d[1], d[0]):
        print("FAILED")
    else:
        print("ok")

    print("\ttesting distance of 2 . . .\t\t\t",end="")
    if not distance(t1, t2) == 2.0:
        print("FAILED\n\t\tExpected {}\tActual {}".format(2.0, distance(t1, t2)))
    else:
        print("ok")

    print("\ttesting associativity of ^ test. . .\t\t",end="")
    if not distance(t1, t2) == distance(t2, t1):
        print("FAILED")
    else:
        print("ok")

def main():
    shrooms =r"E:\Documents\CSC466\Lab 3\466-lab-3.git\trunk\agaricus-lepiota.data.csv"
    iris = r"E:\Documents\CSC466\Lab 3\466-lab-3.git\trunk\iris.data"

    d = parsing.parseData(iris)
    dataPoints = d[0]
    attributes = d[1]

    classifications = classifyData(dataPoints, 5)
    print(numErrors(classifications))

if __name__ == '__main__':
	main()
