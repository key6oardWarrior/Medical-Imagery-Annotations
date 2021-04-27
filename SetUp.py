import os
import threading

import pandas as pd

from getData.FindUnion import FindUnion
from getData.GetData import GetData

from staticPy.Singleton import Singleton
from staticPy.ClusterData import ClusterData

class Setup:
	__resources = Singleton.getInstance(ClusterData())

	def __init__(self):
		pass

	def __wantNewFile(self, msg, i):
		'''
		# If user does not want to replace file return false

		@param <class 'str'> message to user\n
		@param <class 'int'> index of file in question\n
		@return <class 'bool'> true if user wants a new file
		'''
		print(msg)

		if input("Do you want use a different file Y/N: ").upper() == "N":
			del self.__files[i]
			return False
		return True

	def __checkFiles(self):
		self.__files = input("Enter each file path seprated by a white space: ").split(" ")

		i = 0
		while i < len(self.__files): # check to see if each file is valid
			if os.path.exists(self.__files[i]) == False:
				if self.__wantNewFile(f"\nThe file path {self.__files[i]} does not exist", i):
					self.__files[i] = input("Enter name of new file: ")

			elif os.stat(self.__files[i]).st_size <= 5:
				if self.__wantNewFile(f"\nThe file {self.__files[i]} is empty", i):
					self.__files[i] = input("Enter name of new file: ")
			else:
				i += 1

	def __setFolderCnt(self):
		while os.path.isdir(f"{self.__resources.PATH}\\images{self.__resources.folderCnt}"):
			self.__resources.folderCnt += 1

	def start(self):
		self.__setFolderCnt()
		os.system(f"mkdir {self.__resources.PATH}\\images{self.__resources.folderCnt}")
		os.system(f"mkdir {self.__resources.PATH}\\filtered{self.__resources.folderCnt}")
		os.system(f"mkdir {self.__resources.PATH}\\boundingBoxes{self.__resources.folderCnt}")

		setup.__checkFiles()

		for i in self.__files:
			fileData = pd.read_csv(i)
			getData = GetData(self.__resources, fileData)

			downloadImagesThread = threading.Thread(target=getData.downloadImages, args=())
			conceptIDsThread = threading.Thread(target=getData.getResponces, args=())

			print("\nDownloading Images\n")
			conceptIDsThread.start()
			downloadImagesThread.start()

			union = FindUnion(self.__resources, fileData, downloadImagesThread)
			union.findUnion()

			conceptIDsThread.join()
			self.__resources.folderCnt += 1

setup = Setup()
setup.start()