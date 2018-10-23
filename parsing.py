import json, sys, copy

def parseData(filename):
    dataPoints, attribs, attribTypes = [], [], []

    with open(filename, 'r') as file:
        lines = file.read().strip().split('\n')
        attribs = lines[0].split(',')
        attribTypes = lines[1].split(',')

        if not len(attribs) == len(attribTypes):
            print("\t< Error in data file > # attribs : {}\t# attribTypes : {}"\
                .format(len(attribs), len(attribTypes)))
            print("\tNumber of attributes specified does not match number of " +
                    "attribute types")
            return None

        for index, line in enumerate(lines[2:]):
            row = line.split(',')
            dataDict = {}

            for i, attrib in enumerate(attribs):
                if attribTypes[i] == 'n':
                    dataDict[attrib] = float(row[i])
                else:
                    dataDict[attrib] = row[i]

            dataDict['id'] = index
            dataPoints.append(dataDict)
    return (dataPoints, attribs)

def main():
    shrooms =r"E:\Documents\CSC466\Lab 3\466-lab-3.git\trunk\agaricus-lepiota.data.csv"
    iris = r"E:\Documents\CSC466\Lab 3\466-lab-3.git\trunk\iris.data"

    d = parseData(shrooms)
    for dP in d:
        print(dP)

if __name__ == '__main__':
	main()
