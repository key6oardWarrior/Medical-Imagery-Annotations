from sys import argv

if len(argv) < 2:
	raise ValueError("Expected at least one command line argument to be passed, but got 0")

slash = ""
from sys import platform
if platform == "win32":
	slash = "\\"
else:
	slash = "/"

if "-h" in argv:
	print("[file path] -s (optional): where to save file, -h (optional): help, -l (required): last index that was read from. This can be 0, -c (optional): the number of indexes to be read (exclusive). If argument is not passed 100 is assumed")

from os.path import exists
if exists(argv[1]) == False:
	raise ValueError(f"File {argv[1]} does not exists")

path = ""
if "-s" in argv:
	INDEX = argv.index("-s") + 1
	path = f"{argv[INDEX]}{slash}"
else:
	from os import mkdir
	try:
		mkdir("Batches")
	except FileExistsError:
		pass
	
	path = f"Batches{slash}"

if "-l" in argv:
	LAST = int(argv[argv.index("-l") + 1])
else:
	raise ValueError("Expected to find -l in command line arguments")

if "-c" in argv:
	INDEX = argv.index("-c") + 1
	CNT = int(argv[INDEX])

	if CNT < LAST:
		raise ValueError("-c argumet must be > -l argumet")
else:
	CNT = 100

from pandas import read_csv
BATCH = read_csv(argv[1], error_bad_lines=False)[LAST: CNT]

cnt = 0
while(exists(f"{path}{slash}batch{cnt}.csv")):
	cnt += 1

from pandas import DataFrame
DataFrame(BATCH).to_csv(f"{path}{slash}batch{cnt}.csv", sep=",", errors="replace")