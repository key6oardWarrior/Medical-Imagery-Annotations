import wget
import pandas as pd

class GetData:
	'''
	# Get and format all user data from CSV_FILE
	'''

	def __init__(self, RESOURCES, FILE_DATA):
		'''
		@param <class '__main__.Singleton'>\n
		@param <class 'dict'>
		'''
		self.__resources = RESOURCES
		self.__FILE_DATA = FILE_DATA

	def __getIDs(self):
		'''
		set self.allIDs to a numpy array and use ":" as a dilimmiter
		the append each dillimmited peice of data to self.ids
		'''
		self.__ids = []
		biggest = 0

		for i in range(len(self.__allIDs)):
			index = self.__allIDs[i].index(":")
			localID = (self.__allIDs[i])[: index]

			self.__ids.append(localID)
			self.__resources.dataCluster.put(localID)

	def getResponces(self):
		'''
		# Put all user responces in self.__FILE_DATA (<class 'dict'>), so they can
		# be put in a comma delimited csv file.
		'''

		conceptIDs = {
			"Concept IDs": [],
			"Answer.annotation_data": []
		}
		boundingBoxes = { "Bouding Boxes": [] }
		KEYWORD = "Answer.Keyword"
		KEYWORD1 = "Answer.annotation_data"

		for i in self.__FILE_DATA[KEYWORD]:
			try:
				self.__allIDs = i.split("|")
			except AttributeError:
				self.__ids.append("N/A")
			except: # just incase of edge cases
				self.__ids.append("N/A")
			else:
				self.__getIDs()
			conceptIDs["Concept IDs"].append(self.__ids)
			self.__resources.ids.append(self.__ids)

		for i in self.__FILE_DATA[KEYWORD1]:
			allData = i[2: len(i)-2].split(",")

			inputKeyword = (allData[4].split(":"))[1]
			conceptIDs[KEYWORD1].append(inputKeyword)
			boundingBoxes["Bouding Boxes"].append(allData[:4])

		pd.DataFrame(conceptIDs).to_csv(f"{self.__resources.PATH}\\filtered{self.__resources.folderCnt}\\filteredConceptIDs.csv", sep=",")
		pd.DataFrame(boundingBoxes).to_csv(f"{self.__resources.PATH}\\boundingBoxes{self.__resources.folderCnt}\\boundingBoxes.csv", sep=",")

	def downloadImages(self):
		userData = {}
		IMAGE_FILE = f"{self.__resources.PATH}\\images{self.__resources.folderCnt}\\"
		KEYWORD = "Input.image_url"
		KEYWORD1 = "Answer.Keyword"
		prev = ""
		isKey = True
		cnt = 0

		for i in self.__FILE_DATA[KEYWORD]:
			if type(i) != str:
				continue

			if i == prev:
				continue

			path = f"{IMAGE_FILE}{cnt}.jpg"

			if isKey:
				userData[KEYWORD] = []
				userData[KEYWORD1] = []
				isKey = False

			try: # if server does not respond error is not fatal
				userData[KEYWORD].append(wget.download(i, path))
			except:
				print(f"\nImage {i} could not be downloaded")
				userData[KEYWORD].append(f"Image {i} could not be downloaded")
				userData[KEYWORD1].append(f"Image {i} could not be downloaded")
			else:
				userData[KEYWORD1].append(self.__FILE_DATA[KEYWORD1][cnt])
			finally:
				cnt += 1
				prev = i

		imagesDataFrame = pd.DataFrame(userData)
		imagesDataFrame.to_csv(f"{self.__resources.PATH}\\filtered{self.__resources.folderCnt}\\filteredResults.csv", sep=",")