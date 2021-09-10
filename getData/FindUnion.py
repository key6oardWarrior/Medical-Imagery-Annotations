import os
import pandas as pd
from PIL import Image

class FindUnion:
	'''
	Find the union between all the user data given. Then use the data
	to crop an image
	'''
	def __init__(self, RESOURCES, fileLocation: str):
		'''
		Get all the cropping values given from user.

		# Params:
		RESOURCES - Singleton pattern\n
		fileLocation - the location of the directional data
		'''
		self.__resources = RESOURCES
		self.__PATH = f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}"
		self.__directions = {
			"Left": [],
			"Width": [],
			"Height": [],
			"Top": []
		}

		self.__directionData = pd.read_csv(fileLocation)
		self.__imageLocations = pd.read_csv(f"{self.__PATH}filtered{self.__resources.folderCnt}{self.__resources.slash}filteredResults.csv")

	def __crop(self) -> None:
		'''
		Crop each image based on the directional values
		found in left, top, width, and height
		'''
		PATH = f"{self.__PATH}images{self.__resources.folderCnt}{self.__resources.slash}"

		print("\n")
		os.mkdir(f"{PATH}croppedImages")
		print("\nCroping images now\n")

		cnt = 0
		for ii in self.__imageLocations["Input.image_url"]:
			# crop image
			image = Image.open(ii)
			top = self.__directions["Top"][cnt]
			height = self.__directions["Height"][cnt]
			left = self.__directions["Left"][cnt]
			width = self.__directions["Width"][cnt]

			if((top < 0) or (left < 0) or (width < 0) or (height < 0)):
				cnt += 1
				continue

			if height < top:
				temp = height
				height = top
				top = temp

			if left < width:
				temp = left
				left = width
				width = temp

			if left == width:
				left += 1

			if top == height:
				height += 1

			cropped = image.crop((width, top, left, height))
			cropped.save(f"{PATH}croppedImages{self.__resources.slash}{cnt}.jpg")

			cnt += 1

		print("Cropping complete")

	def __compare(self) -> int:
		'''
		Find the avg of each value, then check to ensure that the value is
		within a threshold and if it is store it in a list.

		# Returns:
		The largest in self.__dir that is >= SMALL_AVG and >= BIG_AVG
		'''
		total = 0
		localDir = []

		for num in self.__dir:
			total += num

		AVG = total / len(self.__dir)
		SMALL_AVG = AVG * 0.6
		BIG_AVG = AVG / 0.6

		for num in self.__dir:
			if((num >= SMALL_AVG) and (num <= BIG_AVG)):
				localDir.append(num)

		self.__dir = []

		return max(localDir) if len(localDir) > 0 else -1
	
	def __find(self, DIRECTION: str="left") -> None:
		'''
		Find all the data points within a range of indexes

		# Params:
		DIRECTION - left, width, heigth, or top
		'''
		SIZE = len(DIRECTION) + 2
		for ii in self.__directionData["Answer.annotation_data"]:
			index = ii.index(DIRECTION) + SIZE
			self.__dir.append(int(ii[index: ii.index(",", index)]))
	
	def getData(self) -> None:
		self.__find()
		self.__directions["Left"].append(self.__compare())

		self.__find("top")
		self.__directions["Top"].append(self.__compare())

		self.__find("width")
		self.__directions["Width"].append(self.__compare())

		self.__find("height")
		self.__directions["Height"].append(self.__compare())

	def findUnion(self) -> None:
		'''
		Find the union between all the data points.
		'''
		self.__dir = []
		ogLocation = ""

		'''
		if the range soluition does not work uncomment below
		'''
		for ii in self.__imageLocations["Input.image_url"]:
			if ogLocation == "": # find all data points that need to be collected
				ogLocation = ii

			elif ogLocation != ii: # collect only the needed data points
				ogLocation = ii

				self.getData()

		# No idea why, but this code always does not get the last few result,
		# so it is getting hard coded
		SIZE = len(self.__imageLocations["Input.image_url"])
		DIFF = len(self.__directions["Top"]) - SIZE

		if DIFF < 0:
			for imageL in range(DIFF, 0, 1):
				self.getData()

		print("\nDone collecting data\n")
		self.__crop()