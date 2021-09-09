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
	
	def __find(self, START: int, STOP: int, DIRECTION: str="left") -> None:
		'''
		Find all the data points within a range of indexes

		# Params:
		START - what index in the Dataframe to start at\n
		STOP - what index to stop at in the Dataframe
		DIRECTION - left, width, heigth, or top
		'''
		SIZE = len(DIRECTION) + 2
		for ii in self.__directionData.loc[START: STOP, "Answer.annotation_data"]:
			index = ii.index(DIRECTION) + SIZE
			self.__dir.append(int(ii[index: ii.index(",", index)]))

	def findUnion(self) -> None:
		'''
		Find the union between all the data points.
		'''
		self.__dir = []
		ogLocation = ""
		cnt, prevCnt = 0, 0

		for image in self.__imageLocations["Input.image_url"]:
			if ogLocation == "": # find all data points that need to be collected
				ogLocation = image

			elif ogLocation != image: # collect only the needed data points
				ogLocation = image

				self.__find(prevCnt, cnt)
				self.__directions["Left"].append(self.__compare())

				self.__find(prevCnt, cnt, "top")
				self.__directions["Top"].append(self.__compare())

				self.__find(prevCnt, cnt, "width")
				self.__directions["Width"].append(self.__compare())

				self.__find(prevCnt, cnt, "height")
				self.__directions["Height"].append(self.__compare())
				prevCnt = cnt

		print("Done collecting data\n")
		self.__crop()