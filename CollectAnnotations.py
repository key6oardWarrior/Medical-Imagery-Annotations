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
		
		self.__stop = len(sys.argv)

		if "-o" in sys.argv:
			self.__stop = sys.argv.index("-o")

			if "-o" != sys.argv[-2]:
				if "-o" != sys.argv[-4]:
					raise ValueError("argument \"-o\" not in correct index")
				else:
					if sys.argv[-3].isnumeric() == False:
						raise ValueError(f"-o {sys.argv[-3]} argument is not numeric")
			else:
				if sys.argv[-1].isnumeric() == False:
					raise ValueError(f"-o argument {sys.argv[-1]} is not numeric")

		if "-s" in sys.argv:
			if self.__stop == len(sys.argv):
				self.__stop = sys.argv.index("-s")
			if "-s" == self.argv[-2]:
				self.__resources = Singleton.getInstance(self.argv[-1])
			else:
				raise ValueError("argument \"-s\" is not in correct index")
			
			if os.path.isdir(self.argv[-1]) == False:
				raise ValueError(f"{self.argv[-1]} is not a valid dir")
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
