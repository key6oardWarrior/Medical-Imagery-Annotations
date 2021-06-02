import os
import pandas as pd
import cv2

class ClusterData:
	'''
	# Each concept ID is used as a key in __cluster
	# Values will be each cropped image location
	'''
	__cluster = {}
	__images = []

	def __init__(self, RESOURCES):
		self.__resources = RESOURCES

	def __groupImages(self):
		'''
		# Group images that have the same concept id in the same folder

		Since the code for other algorithms have already been created it is
		easier to just must the image than rewrite the code to put images in
		the right place.
		'''
		PATH = f"{self.__resources.PATH}\\images{self.__resources.folderCnt}\\simular\\"
		imageIndex = 0

		# create dir. the dir name will be the concept id
		os.system(f"mkdir {PATH}")

		for i in self.__images:
			cv2.imwrite(f"{PATH}\\{imageIndex}.jpg", i)
			imageIndex += 1

	def put(self, KEY):
		'''
		# Put KEY in the dict if the key does not already exists
		# this will ensure that a key's value is never overridden

		@param <class 'str'> the key to be put in dict
		'''
		if (KEY in self.__cluster.keys()) == False:
			self.__cluster[KEY] = []

	def appendValue(self, KEY, VALUE, IMAGE):
		'''
		# Append VALUE to __cluster[KEY]

		@param <class 'str'> the key to an array that VALUE will be appended to\n
		@param <class 'str'> value that will get appened to __cluster[KEY]
		@param <class 'numpy.ndarray'>
		'''
		if KEY in self.__cluster.keys():
			self.__cluster[KEY].append(VALUE)
			self.__images.append(IMAGE)

	def makeCSV(self):
		'''
		# Save the cluster data in a file

		@param <class '__main__.Singleton'>
		'''
		self.__KEYS = list(self.__cluster.keys())
		longestArr = 0

		for i in self.__KEYS:
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