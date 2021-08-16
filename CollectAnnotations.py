import os
import sys
import threading
import pandas as pd

from getData.GetData import *
from getData.FindUnion import *
from staticPy.Singleton import *

class CollectAnnotations:
	def __init__(self):
		if len(sys.argv) < 2:
			raise ValueError("Zero command line arguments were passed, but expected at least 1")
		
		if "-h" in sys.argv:
			print("command line args: -o [number of questions given to EACH user] -p [folder to save data]")
			sys.exit(0)

		if "-o" in sys.argv:
			num = sys.argv.index("-o") + 1

			if sys.argv[num].isnumeric() == False:
				raise ValueError(f"-o {sys.argv[num]} argument is not numeric")

		if "-s" in sys.argv:
			filePath = sys.argv.index("-s") + 1

			if os.path.isdir(self.argv[filePath]) == False:
				raise ValueError(f"{self.argv[filePath]} is not a valid dir")

			self.__resources = Singleton.getInstance(self.argv[filePath])
		else:
			self.__resources = Singleton.getInstance()

		index = 0
		# check each file to ensure it exists
		for filePath in sys.argv[1: self.__stop]:
			while os.path.exists(filePath) == False:
				del sys.argv[index]

				ans = input(f"File path {filePath} does not exist do you want to replace it? Y/n ")
				if ans.lower().strip() == "y":
					ans = input("Enter new file location: ")
				else:
					if len(sys.argv) < 2:
						raise ValueError("Zero command line arguments were passed, but expected at least 1")
					break

				filePath = ans
				sys.argv[index] = ans
			index += 1
	
	def __createFolder(self):
		while(os.path.isdir(f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}images{self.__resources.folderCnt}")):
			self.__resources.folderCnt += 1

	def start(self) -> None:
		self.__createFolder()
		os.mkdir(f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}images{self.__resources.folderCnt}")
		os.mkdir(f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}filtered{self.__resources.folderCnt}")
		os.mkdir(f"{self.__resources.PATH}{self.__resources.slash}results{self.__resources.slash}boundingBoxes{self.__resources.folderCnt}")

		for i in sys.argv[1: self.__stop]:
			getData = GetData(self.__resources, i)

			downloadImagesThread = threading.Thread(
				target=getData.downloadImages, args=(), daemon=True)
			conceptIDsThread = threading.Thread(target=getData.getResponces,
				args=(), daemon=True)

			print("\nDownloading Images\n")
			conceptIDsThread.start()
			downloadImagesThread.start()
			union = None

			if "-o" == sys.argv[-2]:
				union = FindUnion(self.__resources, i, downloadImagesThread,
					int(sys.argv[-1]))
			else:
				union = FindUnion(self.__resources, i, downloadImagesThread)
			union.findUnion()

			conceptIDsThread.join()
			self.__resources.folderCnt += 1

setup = CollectAnnotations()
setup.start()
