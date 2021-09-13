from os import read
from os.path import exists
from pandas import read_csv
from pandas import DataFrame
from numpy import array
from sys import argv
from sys import platform
from os.path import dirname

SIZE = len(argv)
if SIZE < 2:
	raise ValueError("Expected only one command line argument to be passed, but got", SIZE)

del SIZE

slash = ""
if platform == "win32":
	slash = "\\"
else:
	slash = "/"

path = ""
if "-s" in argv:
	index = argv.index("-s") + 1
	path = argv[index]

if exists(argv[1]) == False:
	raise ValueError(f"File {argv[1]} does not exists")

BATCH = read_csv(argv[1], error_bad_lines=False)
CNT = 100

batchFiles = array(BATCH.iloc[::CNT])
keywordCnt = 1
batchDF = {
	"image_url": [],
	"caption": []
}

cnt = 0
for ii in batchFiles:
	batchDF["image_url"].append(ii[0])
	batchDF["caption"].append(ii[1])

	for jj in ii[2:]:
		batchDF[f"Keyword{keywordCnt}"] = jj
		keywordCnt += 1

	keywordCnt = 1
	if path == "":
		DataFrame(batchDF).to_csv(f"{cnt}.csv")
	else:
		DataFrame(batchDF).to_csv(f"{path}{cnt}.csv")
	cnt += 1

print("")