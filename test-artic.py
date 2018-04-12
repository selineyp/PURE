import itertools
import numpy as np
import time, os, subprocess
import subprocessmethodrun

percentages = [25, 50, 100]
inputsizes = [10, 20, 30]
ties = [0, 10]
stddev = 10
resultsf  = open("results.txt", "w")


for m_input, w_input in itertools.product(inputsizes, inputsizes):
    for m_percent, w_percent in itertools.product(percentages, percentages):
        for m_ties, w_ties in itertools.product(ties, ties):
            fileprefix = "m-{}-w-{}--m-{}pc-w-{}pc--m-{}pc-w-{}pc".format(m_input, w_input, m_percent, w_percent, m_ties, w_ties)

            #### skip if the file already exists 

            if os.path.isfile("files/{}--input.lp".format(fileprefix)): continue

            #### determine length of preference lists

            m_dist = np.full(m_input, w_input) if m_percent == 100 else ((stddev / 100) * np.random.randn(m_input) + (m_percent / 100)) * w_input
            w_dist = np.full(w_input, m_input) if w_percent == 100 else ((stddev / 100) * np.random.randn(w_input) + (w_percent / 100)) * m_input
            m_rounded = [int(round(x)) for x in m_dist]
            w_rounded = [int(round(x)) for x in w_dist]
            for x in m_rounded:
                if x > w_input: x = w_input
                elif x < 0: x = 0
                else: continue
            for x in w_rounded:
                if x > m_input: x = m_input
                elif x < 0: x = 0
                else: continue

            #### create preference lists

            m_preflists = []
            for i in range(m_input):
                w_shuffled = np.arange(1, w_input+1)
                np.random.shuffle(w_shuffled)
                m_preflist = [[None, x] for x in w_shuffled][: m_rounded[i]]

                last = 1
                for j, pref in enumerate(m_preflist):
                    rnd = np.random.random_sample()
                    if rnd >= (m_ties / 100):
                        pref[0] = j + 1
                        last = j + 1
                    else:
                        pref[0] = last
                m_preflists.append(m_preflist)
            w_preflists = []
            for i in range(w_input):
                m_shuffled = np.arange(1, m_input+1)
                np.random.shuffle(m_shuffled)
                w_preflist = [[None, x] for x in m_shuffled][: w_rounded[i]]

                last = 1
                for j, pref in enumerate(w_preflist):
                    rnd = np.random.random_sample()
                    if rnd >= (m_ties / 100):
                        pref[0] = j + 1
                        last = j + 1
                    else:
                        pref[0] = last
                w_preflists.append(w_preflist)

            #### write input to the file

            inputfilename = "files/{}--input.lp".format(fileprefix)
            with open(inputfilename, "w") as out:
                m_mean = sum([len(m_preflist) for m_preflist in m_preflists]) / (m_input * w_input)
                w_mean = sum([len(w_preflist) for w_preflist in w_preflists]) / (m_input * w_input)
                resultsf.write("file:  {:80s}  man: {:.2f}   woman: {:.2f}".format(inputfilename, m_mean, w_mean))
                out.write("man(")
                k=""
                for i in range(m_input):
                    k+="m"+str(i+1)+";"
                out.write(k[:len(k)-1]+").\n")
                out.write("woman(")
                k=""
                for i in range(w_input):
                    k+="w"+str(i+1)+";"
                out.write(k[:len(k)-1]+").\n")
                for i in range(m_input):
                    for j in range(len(m_preflists[i])):
                        out.write("mpref(m"+str(i+1))
                        out.write(",w"+str(m_preflists[i][j][1]))
                        out.write(","+str(m_preflists[i][j][0])+").\n")
                # for comparison
                # out.write(out.write("mrank(m{:3d}, s, {:3d}).\n".format(i + 1, len(m_preflists[i]) + 1)))
                # for test
                    if np.random.random_sample() >= (m_ties / 100):
                        out.write("mpref(m"+str(i+1))
                        out.write(",s,"+str(len(m_preflists[i]) + 1))
                        out.write(").\n")
                    else:
                        if(len(m_preflists[i])!=0):
                            out.write("mpref(w"+str(i+1))
                            out.write(",s,"+str(m_preflists[i][-1][0]))
                            out.write(").\n")
                for i in range(w_input):
                    for j in range(len(w_preflists[i])):
                        out.write("wpref(w"+str(i+1))
                        out.write(",m"+str(w_preflists[i][j][1]))
                        out.write(","+str(w_preflists[i][j][0])+").\n")
                # for comparison
                # out.write(out.write("wrank(w{:3d}, s, {:3d}).\n".format(i + 1, len(w_preflists[i]) + 1)))
                # for test
                    if np.random.random_sample() >= (w_ties / 100):
                        out.write("wpref(w"+str(i+1))
                        out.write(",s,"+str(len(w_preflists[i]) + 1))
                        out.write(").\n")
                    else:
                        if(len(w_preflists[i])!=0):
                            out.write("wpref(w"+str(i+1))
                            out.write(",s,"+str(w_preflists[i][-1][0]))
                            out.write(").\n")



                '''for i in range(m_input):
                    rand=2
                    if(len(m_preflists[i])>2):
                        rand=np.random.randint(3*(len(m_preflists[i])/4),len(m_preflists[i])+1)
                    for j in range(len(m_preflists[i])):
                        out.write("mpref({:3d},w".format(i+1))
                        out.write(str(m_preflists[i][j][1]))
                        out.write(",{:3d}).\n".format(m_preflists[i][j][0]))
                    out.write("mpref({:3d}, s,{:3d}).\n".format(i+1,len(m_preflists[i])+1))

                for i in range(w_input):
                    rand=2
                    if(len(w_preflists[i])>2):
                        rand=np.random.randint(3*(len(w_preflists[i])/4),len(w_preflists[i])+1)
                    for j in range(len(w_preflists[i])):
                        out.write("wpref({:3d},w".format(i+1))
                        out.write(str(w_preflists[i][j][1]))
                        out.write(",{:3d}).\n".format(w_preflists[i][j][0]))
                    out.write("wpref({:3d},s,{:3d}).\n".format(i+1,len(w_preflists[i])+1))'''

            #### no optimization

            resultfilename = inputfilename[:-8] + "result.txt"

            start = time.time()
            command = "clingo/clingo --stats {} codes/smpti-artic.lp 1".format(inputfilename)
            retcode, stdout, stderr = subprocessmethodrun.run(command, shell = True, stdout = subprocess.PIPE)
            output = stdout.decode('utf-8')
            end = time.time()

            with open(resultfilename, "w") as out:
                out.write(output)
                resultsf.write("file:  {:80s}  time: {:09.2f} seconds".format(resultfilename, end - start))

            #### sex equal smpti

            resultfilename = inputfilename[:-8] + "result-sexequal.txt"

            start = time.time()
            command = "clingo/clingo --stats {} codes/smpti-artic.lp codes/sexequal.lp 0".format(inputfilename)
            retcode, stdout, stderr = subprocessmethodrun.run(command, shell = True, stdout = subprocess.PIPE)
            output = stdout.decode('utf-8')
            end = time.time()

            with open(resultfilename, "w") as out:
                out.write(output)
                resultsf.write("file:  {:80s}  time: {:09.2f} seconds".format(resultfilename, end - start))

            #### egalitarian smpti

            resultfilename = inputfilename[:-8] + "result-egalitarian.txt"

            start = time.time()
            command = "clingo/clingo --stats {} codes/smpti-artic.lp codes/egalitarian.lp 0".format(inputfilename)
            retcode, stdout, stderr = subprocessmethodrun.run(command, shell = True, stdout = subprocess.PIPE)
            output = stdout.decode('utf-8')
            end = time.time()

            with open(resultfilename, "w") as out:
                out.write(output)
                resultsf.write("file:  {:80s}  time: {:09.2f} seconds".format(resultfilename, end - start))

            #### minimum regret smpti

            resultfilename = inputfilename[:-8] + "result-minregret.txt"

            start = time.time()
            command = "clingo/clingo --stats {} codes/smpti-artic.lp codes/minregret.lp 0".format(inputfilename)
            retcode, stdout, stderr = subprocessmethodrun.run(command, shell = True, stdout = subprocess.PIPE)
            output = stdout.decode('utf-8')
            end = time.time()

            with open(resultfilename, "w") as out:
                out.write(output)
                resultsf.write("file:  {:80s}  time: {:09.2f} seconds".format(resultfilename, end - start))

            #### maximum cardinality smpti

            resultfilename = inputfilename[:-8] + "result-maxcardinality.txt"

            start = time.time()
            command = "clingo/clingo --stats {} codes/smpti-artic.lp codes/maxcardinality.lp 0".format(inputfilename)
            retcode, stdout, stderr = subprocessmethodrun.run(command, shell = True, stdout = subprocess.PIPE)
            output = stdout.decode('utf-8')
            end = time.time()

            with open(resultfilename, "w") as out:
                out.write(output)
                resultsf.write("file:  {:80s}  time: {:09.2f} seconds".format(resultfilename, end - start))

            resultsf.write("")
resultsf.close()
out.close()
