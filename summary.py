import glob, os
os.chdir("files")
res=open("results.txt","w")
previous=""
for file in glob.glob("*.txt"):
    print(file)
    print(' '*5)
    f = open(file, "r")
    for line in f:
        if previous != "":
            if line[0:4] == "Time":
                print(line)
                res.write("\n")
        previous = line

res.close()
f.close()
