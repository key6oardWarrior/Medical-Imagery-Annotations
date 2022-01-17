class Singleton(object):
	'''
	Create only one instance of shared resources. This will also prevent a
	race condition from occurring.
	'''
	__KEY = object()
	__instance = None
	slash = ""
	folderCnt = 0

	def __init__(self, KEY: object, PATH):
		'''
		# This constructor is private. Use Singleton.getInstance(PATH)
		'''
		assert(KEY == Singleton.__KEY), \
			"Singleton objects must be created using Singleton.getInstance(PATH)"

		from sys import platform
		if platform == "win32":
			self.slash = "\\"
		else:
			self.slash = "/"

		from os import getcwd
		if PATH == None:
			self.PATH = getcwd()
		else:
			self.PATH = PATH

		RESULTS = f"{self.PATH}{self.slash}results"

		from os.path import isdir
		from os import mkdir
		if isdir(RESULTS) == False:
			mkdir(RESULTS)

	@classmethod
	def getInstance(cls, PATH: str=None):
		'''
		# Returns:
		The only instance of Singleton that will ever exist.
		'''
		if cls.__instance == None:
			cls.__instance = Singleton(cls.__KEY, PATH)

			from staticPy.ClusterData import ClusterData
			cls.dataCluster = ClusterData(cls.__instance)

		return cls.__instance