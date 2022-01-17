from sys import argv, platform, exit
from os.path import exists
from os import mkdir
from pandas import read_csv, DataFrame

if len(argv) < 2:
	raise ValueError("Expected at least one command line argument to be passed, but got 0")

slash = ""
if platform == "win32":
	slash = "\\"
else:
	slash = "/"

if "-h" in argv:
	print("[file path] -s (optional): where to save file, -h (optional): help, -l (required): last index that was read from. This can be 0, -c (optional): the number of indexes to be read (exclusive). If argument is not passed 101 is assumed")
	exit(0)

if exists(argv[1]) == False:
	raise ValueError(f"File {argv[1]} does not exists")

path = ""
if "-s" in argv:
	INDEX = argv.index("-s") + 1
	path = f"{argv[INDEX]}{slash}"
else:
	try:
		mkdir("Batches")
	except FileExistsError:
		pass
	
	path = f"Batches{slash}"

if "-l" in argv:
	START = int(argv[argv.index("-l") + 1])
else:
	raise ValueError("Expected to find -l in command line arguments")

if "-c" in argv:
	INDEX = argv.index("-c") + 1
	STOP = int(argv[INDEX]) + START

	if STOP < START:
		raise ValueError("-c argumet must be > -l argumet")
else:
	STOP = 101 + START

BATCH = read_csv(argv[1], on_bad_lines='skip')[START: STOP]

cnt = 0
while(exists(f"{path}{slash}batch{cnt}.csv")):
	cnt += 1

DataFrame(BATCH).to_csv(f"{path}{slash}batch{cnt}.csv", sep=",", errors="replace")

# clean csv
batch = open(f"{path}{slash}batch{cnt}.csv", 'r').read()
cleanBatch = open(f"{path}{slash}batch{cnt}.csv", 'w')

for line in batch:
	encodedStr = line.encode("ascii", "ignore")
	cleanBatch.write(encodedStr.decode())

cleanBatch.close()