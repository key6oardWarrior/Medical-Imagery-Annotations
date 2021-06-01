import os
import pandas as pd

class ClusterData:
	'''
	# Each concept ID is used as a key in __cluster
	# Values will be each cropped image location
	'''
	__cluster = {}

	def __init__(self):
		pass

	def put(self, key):
		'''
		# Put key in the dict if the key does not already exists
		# this will ensure that a key's value is never overridden

		@param <class 'str'> the key to be put in dict
		'''
		if (key in self.__cluster.keys()) == False:
			self.__cluster[key] = []

	def appendValue(self, key, value):
		'''
		# Append value to __cluster[key]

		@param <class 'str'> the key to an array that value will be appended to\n
		@param <class 'str'> value that will get appened to __cluster[key]
		'''
		if key in self.__cluster.keys():
			self.__cluster[key].append(value)

	def makeCSV(self, RESOURCES):
		'''
		# Save the cluster data in a file

		@param <class '__main__.Singleton'>
		'''
		keys = list(self.__cluster.keys())
		longestArr = 0

		for i in range(len(keys)):
			if not self.__cluster[keys[i]]:
				del self.__cluster[keys[i]] # remove keys with empty values
			else: # determin longestArr
				if len(self.__cluster[keys[i]]) > longestArr:
					longestArr = len(self.__cluster[keys[i]])

		for i in self.__cluster.keys(): # make all values in dict same length
			appendAmount = longestArr - len(self.__cluster[i])
			if appendAmount > 0:
				self.__cluster[i].extend(["N/A"]*appendAmount)

		pd.DataFrame(self.__cluster).to_csv(f"{RESOURCES.PATH}\\filtered{RESOURCES.folderCnt}\\clusteredData.csv", sep=",")