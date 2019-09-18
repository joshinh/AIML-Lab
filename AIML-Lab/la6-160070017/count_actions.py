import sys

pathfile = sys.argv[1]
p = float(sys.argv[2])

f = open(pathfile, "r")
for x in f:
	x = x.rstrip()
	print(p,len(x.split(" ")))

f.close()