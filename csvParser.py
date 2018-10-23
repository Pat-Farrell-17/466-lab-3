import json, sys, os

def parse(filename):
	dataPoints = []
	with open(filename, 'r') as file:
		lines = file.read().strip().split('\n')
		category = lines[2]
		variables = lines[0].split(',')[1:]
		
		for line in lines[3:]:
			row = line.split(',')
			dict = {}
			for index, variableName in enumerate(variables):
				if variableName == category:
					dict['Category'] = row[index + 1]
				else:
					dict[variableName] = row[index + 1]
			dataPoints.append(dict)
	return dataPoints

def main():
	print(json.dumps(parse(sys.argv[1]), indent=2))

if __name__ == '__main__':
	main()
