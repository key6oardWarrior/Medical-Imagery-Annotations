from tokenize import Single
from pandas import read_csv
from pandas import DataFrame
from staticPy.Singleton import Singleton

class GetData:
	'''
	Get and format all user data from FILE_DATA
	'''
	def __init__(self, FILE_DATA: str):
		'''
		# Params:
		RESOURCES - Singleton pattern\n
		FILE_DATA - Data to be added from the batch file
		'''
		self.__resources = Singleton.getInstance()
		self.__FILE_DATA = read_csv(FILE_DATA, on_bad_lines='skip')
		self.__PATH = f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}"

	def __createCluster(self) -> None:
		'''
		Get each concept ID and put them into the cluster
		'''
		index = 0

		for cids in self.__URLs["Answer.Keyword"]:
			if type(cids) == float: # if the cell is empty
				pass
			elif cids.find("|") > -1:
				for cid in cids.split("|"): # get all ids
					if cid.find(":") > -1: # put id in cluster
						self.__resources.dataCluster.put(cid.split(":")[0],
							self.__URLs["Image Location"][index])
			else: # if only 1 id
				if cid.find(":") > -1:
					self.__resources.dataCluster.put(cid.split(":")[0],
						self.__URLs["Image Location"][index])
			index += 1

	def getResponces(self) -> None:
		'''
		Put all user responces in self.__FILE_DATA, so they can be put in a
		comma delimited csv file.
		'''
		from threading import Thread
		clusterThread = Thread(target=self.__createCluster)
		clusterThread.start()

		KEYWORD = "Answer.Keyword"
		ANSWER = "Answer.annotation_data"
		CONCEPT = "Concept IDs"
		BOX = "Bouding Boxes"
		self.__conceptIDs = {
			CONCEPT: [],
			ANSWER: []
		}
		boundingBoxes = { BOX: [] }

		for ii in self.__FILE_DATA[KEYWORD]:
			if type(ii) == float: # if the cell is empty
				self.__conceptIDs[CONCEPT].append(["N/A"])
			elif ii.find("|") != -1: # get all IDs
				self.__conceptIDs[CONCEPT].append(ii.split("|"))
			elif ii.find(":") != -1: # if there is only one value in cell
				self.__conceptIDs[CONCEPT].append([ii])
			else:
				self.__conceptIDs[CONCEPT].append(["N/A"])

		# get the annotation data
		for ii in self.__FILE_DATA[ANSWER]:
			LABEL = ii.find("label")
			endLabel = ii.find("}", LABEL)

			if LABEL > -1:
				self.__conceptIDs[ANSWER].append(ii[LABEL + 8: endLabel])
				boundingBoxes[BOX].append(ii[: LABEL])
			else:
				self.__conceptIDs[ANSWER].append("N/A")
				boundingBoxes[BOX].append("N/A")

		clusterThread.join()
		DataFrame(self.__conceptIDs).to_csv(f"{self.__PATH}filtered{self.__resources.folderCnt}{self.__resources.slash}filteredConceptIDs.csv", sep=",", errors="replace")
		DataFrame(boundingBoxes).to_csv(f"{self.__PATH}boundingBoxes{self.__resources.folderCnt}{self.__resources.slash}boundingBoxes.csv", sep=",", errors="replace")
		print("\nDone collecting data\n")
		self.__resources.dataCluster.makeCluster()

	def downloadImages(self) -> None:
		URL = "Input.image_url"
		Image_L = "Image Location"
		KEYWORD = "Answer.Keyword"
		userData = {
			Image_L: [],
			KEYWORD: []
		}
		IMAGE_FILE = f"{self.__PATH}images{self.__resources.folderCnt}{self.__resources.slash}"
		prev = ""
		cnt = 0

		from wget import download
		from os.path import exists
		for i in self.__FILE_DATA[URL]:
			if type(i) != str:
				continue

			if i == prev:
				continue

			path = f"{IMAGE_FILE}{cnt}.jpg"

			try: # if server does not respond the error is not fatal
				userData[Image_L].append(download(i, path))
			except:
				# Log errors
				errorFile = f"{self.__PATH}errors{self.__resources.folderCnt}{self.__resources.slash}errors.txt"
				if exists(errorFile):
					open(errorFile, 'a').write(f"{i}\n")
				else:
					open(errorFile, 'w').write("URLs that did not work:\n")
			else:
				userData[KEYWORD].append(self.__FILE_DATA[KEYWORD][cnt])
			finally:
				cnt += 1
				prev = i

		self.__URLs = DataFrame(userData)
		DataFrame(userData).to_csv(f"{self.__PATH}filtered{self.__resources.folderCnt}{self.__resources.slash}filteredResults.csv", sep=",", errors="replace")