import os
import sys
from staticPy.ClusterData import *

class Singleton(object):
	'''
	Create only one instance of shared resources. This will also prevent a
	race condition from occurring.
	'''
	__createKey = object()
	__instance = None
	slash = ""
	folderCnt = 0

	def __init__(self, createKey, PATH):
		'''
		# This constructor is private. Use Singleton.getInstance()
		'''
		assert(createKey == Singleton.__createKey), \
			"Singleton objects must be created using Singleton.getInstance(PATH)"

		if sys.platform == "win32":
			self.slash = "\\"
		else:
			self.slash = "/"

		if PATH == "":
			self.PATH = os.getcwd()
		else:
			self.PATH = PATH

		RESULTS = f"{self.PATH}{self.slash}results"

		if os.path.isdir(RESULTS) == False:
			os.mkdir(RESULTS)

	@classmethod
	def getInstance(cls, PATH=""):
		'''
		@return <class '__main__.Singleton'> the only instance of Singleton
		that will ever exist
		'''

		if cls.__instance == None:
			cls.__instance = Singleton(cls.__createKey, PATH)

		cls.dataCluster = ClusterData(cls.__instance)

		return cls.__instance