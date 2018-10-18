class Node:
	def __init__(self, name, label):
		self.name = name
		self.label = label
		self.children = []

	def addChild(self, child):
		self.children.append(child)

	def setName(self, name):
		self.name = name

def main():
	root = Node('Ideology', 'Liberal')
	root.addChild(Node('Obama', None))
	print(root.children[0].name)

if __name__ == '__main__':
	main()
	
