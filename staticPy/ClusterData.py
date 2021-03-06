from staticPy.Singleton import Singleton

class ClusterData:
	'''
	Each concept ID is used as a key in __cluster
	Values will be each cropped image location
	'''
	__cluster = {}

	def __init__(self):
		self.__resources = Singleton.getInstance()
		self.__PATH = f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}"

	def __groupImages(self) -> None:
		'''
		Group images that have the same concept id in the same folder
		'''
		PATH = f"{self.__PATH}images{self.__resources.folderCnt}{self.__resources.slash}simular"

		# create dir the dir name will be the concept id
		from os.path import isdir, join
		from os import mkdir
		if isdir(PATH) == False:
			mkdir(PATH)

		from shutil import copy2
		for key, value in self.__cluster.items():
			FILE = join(PATH, key)

			if isdir(FILE) == False:
				mkdir(FILE)

			for i in value:
				if i == "N/A":
					continue

				copy2(i, FILE)

		print("Clustering complete")

	def put(self, KEY: str, VALUE: str) -> None:
		'''
		Put KEY in the dict if the key does not already exists
		else append the value to the KEY's list.

		# Params:
		KEY - concept id that will be used as a key in __cluster
		'''
		if (KEY in self.__cluster.keys()) == False:
			self.__cluster[KEY] = [VALUE]
		else:
			self.__cluster[KEY].append(VALUE)

	def makeCluster(self) -> None:
		'''
		Cluster all data then save it in a comma delimited csv file
		and group all images that are simular
		'''
		print("Clustering data")
		KEYS = list(self.__cluster.keys())
		longestArr = 0

		for i in KEYS:
			# remove keys with empty values
			if not self.__cluster[i]:
				del self.__cluster[i]

			# determin longestArr
			elif len(self.__cluster[i]) > longestArr:
				longestArr = len(self.__cluster[i])

		if longestArr > 0:
			# make all values in dict same length
			for i in self.__cluster.keys():
				appendAmount = longestArr - len(self.__cluster[i])

				if appendAmount > 0:
					self.__cluster[i].extend(["N/A"]*appendAmount)

		from pandas import DataFrame
		DataFrame(self.__cluster).to_csv(f"{self.__PATH}filtered{self.__resources.folderCnt}{self.__resources.slash}clusteredData.csv", sep=",", errors="replace")
		self.__groupImages()