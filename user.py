
import sys, time, os, subprocess

lines = []
with open(sys.argv[1], "r") as inp:
    for line in inp:
        lines.append(line)

m_size = int(lines[0])
w_size = int(lines[1])

m_preflists = []
for i in range(m_size):
    split_gt = lines[i + 2][:-1].split(" > ")

    curr = 1
    preflist = []
    for outer_split in split_gt:
        split_eq = outer_split.split(" = ")
        for inner_split in split_eq:
            preflist.append((int(inner_split), curr))
            curr += len(split_eq)

    m_preflists.append(preflist)

w_preflists = []
for i in range(w_size):
    split_gt = lines[i + 2 + m_size][:-1].split(" > ")

    curr = 1
    preflist = []
    for outer_split in split_gt:
        split_eq = outer_split.split(" = ")
        for inner_split in split_eq:
            preflist.append((int(inner_split), curr))
        curr += len(split_eq)

    w_preflists.append(preflist)

with open("input.lp", "w") as out:
    out.write("man(1..{}).\n".format(m_size))
    out.write("woman(1..{}).\n".format(w_size))
    out.write("\n")
    for i in range(m_size):
        for elem, val in m_preflists[i]:
            out.write("mrank({:3d}, {:3d}, {:3d}).\n".format(i + 1, elem, val))
    out.write("\n")
    for i in range(w_size):
        for elem, val in w_preflists[i]:
            out.write("wrank({:3d}, {:3d}, {:3d}).\n".format(i + 1, elem, val))

if len(sys.argv) == 2:
    optimize = "noopt"
    command = "../../clingo/clingo --stats input.lp ../codes/smpti.lp 1"
elif sys.argv[2] == "sexeq":
    optimize = "sexeq"
    command = "../../clingo/clingo --stats input.lp ../codes/smpti.lp ../codes/sexequal.lp 0"
elif sys.argv[2] == "egal":
    optimize = "egal"
    command = "../../clingo/clingo --stats input.lp ../codes/smpti.lp ../codes/egalitarian.lp 0"
elif sys.argv[2] == "minreg":
    optimize = "minreg"
    command = "../../clingo/clingo --stats input.lp ../codes/smpti.lp ../codes/minregret.lp 0"
elif sys.argv[2] == "maxcar":
    optimize = "maxcar"
    command = "../../clingo/clingo --stats input.lp ../codes/smpti.lp ../codes/maxcardinality.lp 0"

start = time.time()
process = subprocess.run(command, shell = True, stdout = subprocess.PIPE)
output = process.stdout.decode('utf-8')
end = time.time()

resultfile = "result.txt"
with open(resultfile, "w") as out:
    out.write(output)

if optimize != "noopt":
    lines = output.split('\n')
    for i, line in enumerate(lines):
        if line == "OPTIMUM FOUND":
            match=lines[i-2].split()
            optval = lines[i - 1].split()[-1]
            print("time: {:09.2f} seconds\noptimization: {}".format(end - start, optval))
            break
else:
    lines = output.split('\n')
    for i, line in enumerate(lines):
        if line == "SATISFIABLE":
            match=lines[i-1].split()
            print("time: {:09.2f} seconds".format(end - start))
            break

out.close()
print(' '*2+"M"+' '*3+"W")
for m in match:
    if(m[0:5]=="marry"):
        print('{0:3d} {1:3d}'.format(int(m[-4]), int(m[-2])))
