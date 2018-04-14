import operator
filename="results-article.txt"
f=open(filename,"r")
lines = f.readlines()
filenames= []
pairs= {}
i=1
while(i<len(lines)-2):
    filenames.append(lines[i-1])
    i+=4
k=0
while(k<len(lines)-3):
    pairs.update({lines[k]:lines[k+2]})
    k+=4
sorted_f=sorted(pairs.items())
for key,value in sorted_f:
    print(key)
    print(value)
