import os
from staticPy.ClusterData import ClusterData

class Singleton(object):
	'''
	Create only one instance of shared resources. This will also prevent a
	race condition from occurring.
	'''
	__createKey = object()
	__instance = None
	folderCnt = 0
	ids = []

	def __init__(self, createKey):
		'''
		# This constructor is private. Use Singleton.getInstance()
		'''
		assert(createKey == Singleton.__createKey), \
			"Singleton objects must be created using Singleton.getInstance()"
		
		FILE_PATH = os.path.dirname(__file__)
		INDEX = FILE_PATH.rindex("\\")
		self.PATH = f"{FILE_PATH[:INDEX]}\\results"

		if os.path.isdir(self.PATH) == False:
			os.mkdir(self.PATH)

	@classmethod
	def getInstance(cls, isTest=None) -> Singleton:
		'''
		@return <class '__main__.Singleton'> the only instance of Singleton
		that will ever exist
		'''

		if cls.__instance == None:
			cls.__instance = Singleton(cls.__createKey)

		cls.dataCluster = ClusterData(cls.__instance)

		return cls.__instance