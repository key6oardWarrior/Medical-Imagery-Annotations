import os
import cv2

class FindUnion:
	'''
	# Find the union between all the user data given. Then use the data
	# to crop an image
	'''
	def __init__(self, RESOURCES, FILE_DATA, THREAD):
		'''
		# Get all the cropping values given from user.

		@param <class <class '__main__.Singleton'>\n
		@param <class 'pandas.core.frame.DataFrame'> file data dataframe\n
		@param <class 'threading.Thread'> downloading images thread
		'''
		self.__resources = RESOURCES
		self.__THREAD = THREAD

		self.__orignalCroppingValues = {}
		KEYWORD = "Answer.annotation_data"
		IMAGE = "Image"
		cnt = 0

		for i in FILE_DATA[KEYWORD]:
			self.__getCropHelper(i)
			self.__orignalCroppingValues[cnt] = self.__tempValues
			cnt += 1

	def __getCropHelper(self, DATA):
		'''
		# Find numbers in self.FILE_DATA[KEYWORD][DATA] and add each number to a list.

		@param <class 'str'>
		'''
		self.__tempValues = []
		temp = ""

		for i in range(len(DATA)-1):
			if DATA[i].isnumeric():
				temp += DATA[i]

			if((temp != "") and (DATA[i+1].isnumeric() == False)):
				try:
					self.__tempValues.append(int(temp.replace(" ", "")))
				except ValueError:
					pass
				except: # just incase of edge case
					pass
				finally:
					temp = ""

	def __crop(self):
		'''
		# Crop each image based on the directional values
		# found in left, top, width, and height
		'''
		left = []
		top = []
		PATH = f"{self.__resources.PATH}\\images{self.__resources.folderCnt}\\"
		KEYWORD = "Input.image_url"
		cnt = 0

		print("\n")
		os.system(f"mkdir {PATH}croppedImages\\")

		self.__THREAD.join()
		print("\nCroping images now\n")

		for i in range(len(self.__newLeft)):
			if type(self.__newLeft[i]) != int:
				continue
			if type(self.__newTop[i]) != int:
				continue

			image = cv2.imread(f"{PATH}{i}.jpg")
			left = (self.__newLeft[i]) if self.__newLeft[i] > 0 else 1
			top = (self.__newTop[i]) if self.__newTop[i] > 0 else 1

			try:
				cropped = image[top: len(image[0]), left: len(image[0])]
			except TypeError:
				pass
			except: # just incase of edge case
				pass
			else:
				cv2.imwrite(f"{PATH}croppedImages\\{i}.jpg", cropped)
				# cv2.imshow(f"{PATH}{i}.jpg", image) # to veiw the og image
				# cv2.imshow(f"{PATH}croppedImages\\{i}.jpg", cropped) # to view cropped image
				# print(image.shape) # og image size
				# print(cropped.shape) # new image size
				# cv2.waitKey(0) # uncomment to view images
				for j in self.__resources.ids[i]:
					self.__resources.dataCluster.appendValue(j, f"{PATH}croppedImages\\{i}.jpg")

	def __helper(self, VALUE, VALUE1):
		'''
		# Determin which value is bigger and if the smaller value is
		# within the threshold of the bigger value. If the
		# smaller value is not within the threshold, then return
		# "No union found" else return the smaller value.

		@param <class 'int'>\n
		@param <class 'int'>\n
		@return <class 'str'> or <class 'int'>
		'''
		THRESHOLD = 0.60

		if VALUE > VALUE1:
			if((VALUE1 >= (VALUE * THRESHOLD)) and (VALUE1 <= VALUE)):
				return VALUE1
			return False

		if((VALUE >= (VALUE1 * THRESHOLD)) and (VALUE <= VALUE1)):
			return VALUE
		return False

	def __getDirectionData(self, DIRECTION=0, isLast=False):
		'''
		# get data for a given direction

		DIRECTION = 0 = left\n
		DIRECTION = 1 = top\n
		DIRECTION = 2 = width\n
		DIRECTION = 3 = height

		@param <class 'int'>\n
		@param <class 'bool>\n
		@return <class 'list'>
		'''
		data = []

		for i in self.__croppingValues.keys():
			value = self.__croppingValues[i][DIRECTION]
			temp = (i - 1) if isLast else (i + 1)
			value1 = self.__croppingValues1[temp][DIRECTION]

			data.append(self.__helper(value, value1))

		return data

	def __reduceDimension(self, INDEX, DIRECTION=0):
		'''
		# Take each left, top, width, height multi-dimensional list and
		# reduce them to a 1D list

		@param <class 'int'>\n
		@param <class 'int'>\n
		@return <class 'int'> or <class 'str'>
		'''
		direction = []

		if DIRECTION == 0:
			direction = self.__left
		elif DIRECTION == 1:
			direction = self.__top
		elif DIRECTION == 2:
			direction = self.__width
		else:
			direction = self.__height

		lowest = direction[0][INDEX]

		for i in range(1, len(direction)):
			if((type(lowest) == bool) or (type(direction[i][INDEX]) == int)):
				lowest = direction[i][INDEX]
		return lowest

	def __setValues(self, isFirst=True):
		'''
		@param <class 'bool'>
		'''
		if isFirst:
			for i in range(self.__start, self.__end, self.__USERS_SURVEYED):
				self.__croppingValues.update({i: self.__orignalCroppingValues[i]})
		else:
			for i in range(self.__start, self.__end, self.__USERS_SURVEYED):
				self.__croppingValues1.update({i: self.__orignalCroppingValues[i]})

	def findUnion(self):
		self.__left = []
		self.__top = []
		self.__width = []
		self.__height = []
		NUM_OF_QUESTIONS = 13 # 25

		# META DATA CONSTANT
		self.__USERS_SURVEYED = len(self.__orignalCroppingValues.keys()) // NUM_OF_QUESTIONS

		'''
		this allows each user's responces to be compared to each
		other and then find the union
		'''
		stop = 0
		isEven = True
		if self.__USERS_SURVEYED % 2 == 0:
			stop = int(self.__USERS_SURVEYED / 2)
		else:
			stop = int((self.__USERS_SURVEYED+1) / 2)
			isEven = False

		for cnt in range(stop):
			self.__croppingValues = {}
			self.__start = (self.__start + 1) if cnt != 0 else 0
			self.__end = (self.__end + 1) if cnt != 0 else NUM_OF_QUESTIONS*self.__USERS_SURVEYED

			self.__setValues()

			if((isEven) or (cnt < (stop - 1))):
				self.__croppingValues1 = {}
				self.__start += 1
				self.__end += 1

				self.__setValues(False)

				self.__left.append(self.__getDirectionData())
				self.__top.append(self.__getDirectionData(1))
				self.__width.append(self.__getDirectionData(2))
				self.__height.append(self.__getDirectionData(3))
			else:
				self.__left.append(self.__getDirectionData(isLast=True))
				self.__top.append(self.__getDirectionData(1, True))
				self.__width.append(self.__getDirectionData(2, True))
				self.__height.append(self.__getDirectionData(3, True))

		if self.__USERS_SURVEYED > 2:
			self.__newLeft = []
			self.__newTop = []
			self.__newWidth = []
			self.__newHeight = []

			for i in range(len(self.__left[0])):
				self.__newLeft.append(self.__reduceDimension(i))
				self.__newTop.append(self.__reduceDimension(i, 1))
				self.__newWidth.append(self.__reduceDimension(i, 2))
				self.__newHeight.append(self.__reduceDimension(i, 3))
		else:
			self.__newLeft = self.__left[0]
			self.__newTop = self.__top[0]
			self.__newWidth = self.__width[0]
			self.__newHeight = self.__height[0]

		print("Done collecting data\n")
		self.__crop()
		self.__resources.dataCluster.makeCSV(self.__resources)