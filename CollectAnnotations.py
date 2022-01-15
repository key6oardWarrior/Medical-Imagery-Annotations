from os.path import isdir
from sys import argv

class CollectAnnotations:
	def __init__(self):
		from staticPy.Singleton import Singleton
		from sys import exit

		if len(argv) < 2:
			raise ValueError("Zero command line arguments were passed, but expected at least 1")

		if "-h" in argv:
			print("command line args: -s (optional) [folder to save data to]")
			exit(0)

		if "-s" in argv:
			filePath = argv.index("-s") + 1

			if isdir(argv[filePath]) == False:
				raise ValueError(f"{self.argv[filePath]} is not a valid dir")

			self.__resources = Singleton.getInstance(argv[filePath])
		else:
			self.__resources = Singleton.getInstance()

		index = 0
		isContinue = False
		# check each file to ensure it exists
		for filePath in argv[1:]:
			if filePath == "-s":
				isContinue = True
				continue

			if isContinue:
				isContinue = False
				continue

			from os.path import exists
			while exists(filePath) == False:
				del argv[index]

				ans = input(f"File path {filePath} does not exist do you want to replace it? Y/n ")
				if ans.lower().strip() == "y":
					ans = input("Enter new file location: ")
				else:
					if len(argv) < 2:
						raise ValueError("Zero command line arguments were passed, but expected at least 1")
					break

				filePath = ans
				argv[index] = ans
			index += 1

	def __createFolder(self):
		while(isdir(f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}images{self.__resources.folderCnt}")):
			self.__resources.folderCnt += 1

	def start(self) -> None:
		self.__createFolder()
		from os import mkdir
		mkdir(f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}images{self.__resources.folderCnt}")
		mkdir(f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}filtered{self.__resources.folderCnt}")
		mkdir(f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}boundingBoxes{self.__resources.folderCnt}")
		
		from getData.GetData import GetData
		from getData.FindUnion import FindUnion
		from threading import Thread
		isContinue = False
		for i in argv[1:]:
			if i == "-s":
				isContinue = True
				continue

			if isContinue:
				isContinue = False
				continue

			getData = GetData(self.__resources, i)
			getData.downloadImages()
			print("\nDone Downloading Images\n")
			getData.getResponces()

			union = FindUnion(self.__resources, i)
			unionThread = Thread(target=union.findUnion, args=())
			unionThread.start()

			self.__resources.folderCnt += 1

setup = CollectAnnotations()
setup.start()