import os
import pandas as pd
import cv2

class ClusterData:
	'''
	# Each concept ID is used as a key in __cluster
	# Values will be each cropped image location
	'''
	__cluster = {}
	__images = {}

	def __init__(self, RESOURCES):
		self.__resources = RESOURCES

	def __groupImages(self):
		'''
		# Group images that have the same concept id in the same folder

		Since the code for other algorithms have already been created it is
		easier to just must the image than rewrite the code to put images in
		the right place.
		'''
		PATH = f"{self.__resources.PATH}\\images{self.__resources.folderCnt}\\simular"
		NUM_OF_IMAGES = len(self.__images)

		# create dir. the dir name will be the concept id
		if os.path.isdir(PATH) == False:
			os.mkdir(PATH)

		for key, value in self.__cluster.items():
			FILE = os.path.join(PATH, key.strip())

			if os.path.isdir(FILE) == False:
				os.mkdir(FILE)
			
			for i in value:
				index = i.rfind("\\")

				if index == -1:
					continue
				
				index += 1
				IMAGE = self.__images[int(i[index: -4])]
				
				cv2.imwrite(os.path.join(FILE, f"{i[index:]}"), IMAGE)
		
		print("Clustering complete")

	def put(self, KEY):
		'''
		# Put KEY in the dict if the key does not already exists
		# this will ensure that a key's value is never overridden

		@param <class 'str'> the KEY is a concept id
		'''
		if (KEY in self.__cluster.keys()) == False:
			self.__keys.append(KEY)
			self.__cluster[KEY] = []

	def appendValue(self, KEY, VALUE):
		'''
		# Append VALUE to __cluster[KEY]
		@param <class 'str'> the key to an array that VALUE will be appended to\n
		@param <class 'str'> value that will get appened to __cluster[KEY]
		@param <class 'numpy.ndarray'>
		'''
		if KEY in self.__cluster.keys():
			self.__cluster[KEY].append(VALUE)
	
	def appendImage(self, IMAGE, KEY):
		'''
		# Each image has a number for a name, so each image will be stored at
		# self.__image[KEY]. This will make retriving the image easy because
		# the key will already be known.

		@param <class 'numpy.ndarray'> the image\n
		@param <class 'int'> the index the image will go
		'''
		self.__images[KEY] = IMAGE

	def makeCSV(self):
		'''
		# Save the cluster data in a file

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