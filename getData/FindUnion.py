from numpy.lib.function_base import delete
from numpy import where, append, sum, amax

class FindUnion:
	'''
	Find the union between all the user data given. Then use the data
	to crop an image
	'''
	__IMAGE_L = "Image Location"

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

		from pandas import read_csv
		self.__directionData = read_csv(fileLocation, error_bad_lines=False)
		self.__imageLocations = read_csv(f"{self.__PATH}filtered{self.__resources.folderCnt}{self.__resources.slash}filteredResults.csv", error_bad_lines=False)

	def crop(self) -> None:
		'''
		Crop each image based on the directional values
		found in left, top, width, and height
		'''
		PATH = f"{self.__PATH}images{self.__resources.folderCnt}{self.__resources.slash}"

		print("\n")
		from os import mkdir
		mkdir(f"{PATH}croppedImages")
		print("\nCroping images now\n")

		cnt = 0
		from PIL import Image
		for ii in self.__imageLocations[self.__IMAGE_L]:
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
			
			if((top == -1) and (height == -1) and (left == -1) and (width == -1)):
				pass
			elif((top == -1) or (height == -1)):
				cropped = image.crop((width, image.height, left, image.height))
			elif((left == -1) or (width == -1)):
				cropped = image.crop((image.width, top, image.width, height))
			elif((left != width) and (top != height)):
				cropped = image.crop((width, top, left, height))
				cropped.save(f"{PATH}croppedImages{self.__resources.slash}{cnt}.jpg")

			cnt += 1

		print("Cropping complete")

	def __compare(self) -> int:
		'''
		Find the avg of each value, then check to ensure that the value is
		within a threshold and if it is store it in a list.

		# Returns:
		The largest in self.__dir that is >= LOWER_BOUND and <= UPPER_BOUND
		'''
		AVG = sum(self.__dir) / self.__dir.size
		LOWER_BOUND = AVG * 0.6
		UPPER_BOUND = AVG / 0.6

		self.__dir = delete(self.__dir, where(self.__dir < LOWER_BOUND))
		self.__dir = delete(self.__dir, where(self.__dir > UPPER_BOUND))

		return amax(self.__dir) if self.__dir.size > 0 else -1
	
	def __find(self, DIRECTION: str="left") -> int:
		'''
		Find all the data points within a range of indexes

		# Params:
		DIRECTION - left, width, heigth, or top
		'''
		from numpy import array
		self.__dir = array([])
		SIZE = len(DIRECTION) + 2
		SEARCH = self.__directionData["Input.image_url"].iloc[self.__start]
		SAME_URLS = where(self.__directionData["Input.image_url"].iloc[self.__start:] == SEARCH)
		END = self.__start + SAME_URLS[0].size + 1

		for croppingData in self.__directionData["Answer.annotation_data"].iloc[self.__start: END]:
			index = croppingData.index(DIRECTION) + SIZE
			self.__dir = append(self.__dir, int(croppingData[index: croppingData.index(",", index)]))

		return END

	def findUnion(self) -> None:
		'''
		Find the union between all the data points.
		'''
		self.__start = 0

		'''
		if the range soluition does not work uncomment below
		'''
		ii = 0
		while ii < len(self.__imageLocations[self.__IMAGE_L]):
			self.__find()
			self.__directions["Left"].append(self.__compare())

			self.__find("top")
			self.__directions["Top"].append(self.__compare())

			self.__find("width")
			self.__directions["Width"].append(self.__compare())

			self.__start = self.__find("height")
			self.__directions["Height"].append(self.__compare())

			ii += 1

		print("\nDone collecting data\n")