from os import read
from pandas import read_csv
from pandas import DataFrame
from numpy import array
from sys import argv
from sys import platform
from os.path import dirname

SIZE = len(argv)
if SIZE < 2:
	raise ValueError("Expected only one command line argument to be passed, but got", SIZE)

slash = ""
if platform == "win32":
	slash = "\\"
else:
	slash = "/"

path = ""
if "-s" in argv:
	index = argv.index("-s") + 1
	path = argv[index]

BATCH = read_csv(argv[1])
CNT = 100

if BATCH % CNT != 0:
	raise ValueError("Batch file does not have enought results to create 100 batch files")

batchFiles = array(BATCH.iloc[::CNT])

cnt = 0
for ii in batchFiles:
	if path != "":
		ii.to_csv(f"{path}{cnt}.csv")
	else:
		ii.to_csv(f"{cnt}.csv")
	cnt += 1

print("")