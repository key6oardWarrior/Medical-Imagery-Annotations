import wget
import pandas as pd

class GetData:
	'''
	Get and format all user data from CSV_FILE
	'''
	def __init__(self, RESOURCES, FILE_DATA: str):
		'''
		# Params:
		RESOURCES - Singleton pattern\n
		FILE_DATA - Data to be added from the batch file
		'''
		self.__resources = RESOURCES
		self.__FILE_DATA = pd.read_csv(FILE_DATA)
		self.__PATH = f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}"

	def __getEachId(self) -> None:
		'''
		Get each concept ID and put them into the cluster
		'''
		for ii in self.__splitCid:
			index = ii.find(":")

			if index > -1:
				self.__resources.dataCluster.put(ii[: index])

	def getResponces(self) -> None:
		'''
		Put all user responces in self.__FILE_DATA (<class 'dict'>), so they can
		be put in a comma delimited csv file.
		'''
		KEYWORD = "Answer.Keyword"
		ANSWER = "Answer.annotation_data"
		CONCEPT = "Concept IDs"
		BOX = "Bouding Boxes"
		conceptIDs = {
			CONCEPT: [],
			ANSWER: []
		}
		boundingBoxes = { BOX: [] }

		for ii in self.__FILE_DATA[KEYWORD]:
			try:
				self.__splitCid = ii.split("|")
			except AttributeError:
				conceptIDs[CONCEPT].append("N/A")
			else:
				conceptIDs[CONCEPT].append(self.__splitCid)
				self.__getEachId()

		for ii in self.__FILE_DATA[ANSWER]:
			label = ii.find("label")
			endLabel = ii.find("}", label)

			if label > -1:
				conceptIDs[ANSWER].append(ii[label + 8: endLabel])
				boundingBoxes[BOX].append(ii[: label])
			else:
				conceptIDs[ANSWER].append("N/A")
				boundingBoxes[BOX].append("N/A")

		pd.DataFrame(conceptIDs).to_csv(f"{self.__PATH}filtered{self.__resources.folderCnt}{self.__resources.slash}filteredConceptIDs.csv", sep=",")
		pd.DataFrame(boundingBoxes).to_csv(f"{self.__PATH}boundingBoxes{self.__resources.folderCnt}{self.__resources.slash}boundingBoxes.csv", sep=",")

	def downloadImages(self) -> None:
		URL = "Input.image_url"
		KEYWORD = "Answer.Keyword"
		userData = {
			URL: [],
			KEYWORD: []
		}
		IMAGE_FILE = f"{self.__PATH}images{self.__resources.folderCnt}{self.__resources.slash}"
		prev = ""
		cnt = 0

		for i in self.__FILE_DATA[URL]:
			if type(i) != str:
				continue

			if i == prev:
				continue

			path = f"{IMAGE_FILE}{cnt}.jpg"

			try: # if server does not respond error is not fatal
				userData[URL].append(wget.download(i, path))
			except:
				print(f"\nImage {i} could not be downloaded")
				userData[URL].append(f"Image {i} could not be downloaded")
				userData[KEYWORD].append(f"Image {i} could not be downloaded")
			else:
				userData[KEYWORD].append(self.__FILE_DATA[KEYWORD][cnt])
			finally:
				cnt += 1
				prev = i

		imagesDataFrame = pd.DataFrame(userData)
		imagesDataFrame.to_csv(f"{self.__PATH}filtered{self.__resources.folderCnt}{self.__resources.slash}filteredResults.csv", sep=",")

	def createCluster(self) -> None:
		'''
		Cluster all images that have the same concept ID
		'''
		return
		for ii in self.__resources.dataCluster.getClusterKeys:
			pass

		self.__resources.dataCluster.makeCluster()