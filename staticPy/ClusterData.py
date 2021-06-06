import os
import shutil
import pandas as pd

class ClusterData:
	'''
	# Each concept ID is used as a key in __cluster
	# Values will be each cropped image location
	'''
	__cluster = {}

	def __init__(self, RESOURCES):
		'''
		@param <class <class '__main__.Singleton'>
		'''
		self.__resources = RESOURCES

	def __groupImages(self):
		'''
		# Group images that have the same concept id in the same folder
		'''
		PATH = f"{self.__resources.PATH}\\images{self.__resources.folderCnt}\\simular"

		# create dir the dir name will be the concept id
		if os.path.isdir(PATH) == False:
			os.mkdir(PATH)

		for key, value in self.__cluster.items():
			FILE = os.path.join(PATH, key)

			if os.path.isdir(FILE) == False:
				os.mkdir(FILE)

			for i in value:
				if i == "N/A":
					continue

				shutil.copy2(i, FILE)
		
		print("Clustering complete")

	def put(self, KEY):
		'''
		# Put KEY in the dict if the key does not already exists
		# this will ensure that a key's value is never overridden

		@param <class 'str'> the KEY is a concept id
		'''
		if (KEY in self.__cluster.keys()) == False:
			self.__cluster[KEY] = []

	def appendValue(self, KEY, VALUE):
		'''
		# Append VALUE to __cluster[KEY]

		@param <class 'str'> the key to an array that VALUE will be appended to\n
		@param <class 'str'> value that will get appened to __cluster[KEY]\n
		'''
		if KEY in self.__cluster.keys():
			self.__cluster[KEY].append(VALUE)
	
	def makeCluster(self):
		'''
		# Cluster all data then save it in a comma delimited csv file
		# and group all images that are simular

		@param <class '__main__.Singleton'>
		'''
		print("Clustering data")
		KEYS = list(self.__cluster.keys())
		longestArr = 0

		for i in KEYS:
			if not self.__cluster[i]:
				del self.__cluster[i] # remove keys with empty values

			elif len(self.__cluster[i]) > longestArr: # determin longestArr
				longestArr = len(self.__cluster[i])

		if longestArr > 0:
			for i in self.__cluster.keys(): # make all values in dict same length
				appendAmount = longestArr - len(self.__cluster[i])

				if appendAmount > 0:
					self.__cluster[i].extend(["N/A"]*appendAmount)

		pd.DataFrame(self.__cluster).to_csv(f"{self.__resources.PATH}\\filtered{self.__resources.folderCnt}\\clusteredData.csv", sep=",")
		self.__groupImages()