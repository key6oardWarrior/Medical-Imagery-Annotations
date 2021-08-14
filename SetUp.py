import os
import sys
import threading

import pandas as pd

from getData.FindUnion import FindUnion
from getData.GetData import GetData

from staticPy.Singleton import Singleton

class Setup:
	__resources = Singleton.getInstance()

	def __init__(self):
		while os.path.isdir(f"{self.__resources.PATH}\\images{self.__resources.folderCnt}"):
			self.__resources.folderCnt += 1

	def __wantNewFile(self, msg: str, i: int) -> bool:
		'''
		If user does not want to replace file return false

		# Params:
		msg - message to user\n
		i - index of file in question

		# Returns:
		true if user wants a new file
		'''
		print(msg)

		if input("Do you want use a different file Y/N: ").upper() == "N":
			del self.__files[i]
			
			if len(self.__files) == 0:
				sys.exit(0)
			
			return False
		return True

	def __checkFiles(self) -> None:
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

	def start(self) -> None:
		os.mkdir(f"{self.__resources.PATH}\\images{self.__resources.folderCnt}")
		os.mkdir(f"{self.__resources.PATH}\\filtered{self.__resources.folderCnt}")
		os.mkdir(f"{self.__resources.PATH}\\boundingBoxes{self.__resources.folderCnt}")

		self.__checkFiles()

		for i in self.__files:
			getData = GetData(self.__resources, i)

			downloadImagesThread = threading.Thread(target=getData.downloadImages, args=(), daemon=True)
			conceptIDsThread = threading.Thread(target=getData.getResponces, args=(), daemon=True)

			print("\nDownloading Images\n")
			conceptIDsThread.start()
			downloadImagesThread.start()

			union = FindUnion(self.__resources, i, downloadImagesThread)
			union.findUnion()

			conceptIDsThread.join()
			self.__resources.folderCnt += 1

setup = Setup()
setup.start()