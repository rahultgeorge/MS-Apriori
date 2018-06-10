from __future__ import division
import operator
from itertools import combinations


def scanTransactions(itemSet):
    file = open("input.txt", "r")
    for line in file:
        if line.count(',') > 0:
            temp = set(map(int, line.replace(' ', '').replace('{', '').replace('}', '').replace('\n', '').split(',')))
        else:
            singleElement = int(line.replace(' ', '').replace('{', '').replace('}', '').replace('\n', ''))
            temp = set()
            temp.add(singleElement)
        if itemSet <= temp:
            candidateCount[i] = candidateCount[i] + 1

        # tailCount


def tailCount(itemSet):
    tailSet = itemSet [1 : len(itemSet)]
    count = 0
    for transaction in transactionsList:
        if set(tailSet) <= transaction:
            count = count + 1;
    return count;


# cannot have
def cannot_Have():
    if cannotHave:
        for f in F:
            for cannotSet in cannotHave:
                itemIndex = 0
                max = len(f)
                while itemIndex < max:
                    if cannotSet <= set(f[itemIndex]):
                        if F.index(f) > 1:
                            del FCount[F.index(f)][itemIndex]
                        f.remove(f[itemIndex])
                        max = len(f)
                    else:
                        itemIndex = itemIndex + 1;

                    # must have


def must_Have():
    if mustHave:
        for f in F:
            itemIndex = 0
            max = len(f)
            while itemIndex < max:
                if set(f[itemIndex]).isdisjoint(mustHave):
                    if F.index(f) > 1:
                        del FCount[F.index(f)][itemIndex]
                    f.remove(f[itemIndex])
                    max = len(f)
                else:
                    itemIndex = itemIndex + 1;


# Making the initial pass


def init_Pass():
    global L
    L = []
    for i in range(len(M)):
        if ((itemCount.get(M[i]) / noOfTransactions) >= MIS.get(M[i])):
            L.append(M[i])
            break;
    for j in range(i + 1, len(M)):
        if ((itemCount.get(M[j]) / noOfTransactions) >= MIS.get(M[i])):
            L.append(M[j])


# Generating candidates for Level 2 which works differently as compared to other levels
def level2CandidateGeneration():
    candidateKeys=[]   #List to hold 2-items itemsets
    for i in range (0,len(L)):
        if (itemCount.get(L[i]) / noOfTransactions) >= MIS[L[i]]:
            for h in range( i + 1, len(L)):
                if (itemCount.get(L[h]) / noOfTransactions) >= MIS[L[i]] and abs((itemCount.get(L[h]) / noOfTransactions) - (itemCount.get(L[i]) / noOfTransactions)) <= sdc:
                    candidateKeys.append(set())
                    candidateKeys[len(candidateKeys)-1].add(L[i])
		    candidateKeys[len(candidateKeys)-1].add(L[h])
            return candidateKeys


# MS Candidate Keys Generation
def MSCandidateGeneration(k):
    candidate_keys = []
    max = len(F[k - 1])
    unionList = []
    elementPos = 0
    for i in range(0, max):
        for j in range(0, max):
            while elementPos < k - 1 and F[k - 1][i][elementPos] == F[k - 1][j][elementPos]:
                elementPos = elementPos + 1
            if (elementPos == k - 2):
                if F[k - 1][i][elementPos] < F[k - 1][j][elementPos] and (abs(
                        (itemCount.get(F[k - 1][i][elementPos]) / noOfTransactions) - (
                                itemCount.get(F[k - 1][j][elementPos]) / noOfTransactions)) <= sdc):
                    unionList = [element for element in F[k - 1][i]];
                    unionList.append(F[k - 1][j][elementPos]);
                    candidate_keys.append(set(unionList));
                    # subsets of unionList
                    for subset in list(combinations(unionList, k - 1)):
                        subset = set(subset)
                        if unionList[0] in subset or MIS.get(unionList[0]) == MIS.get(unionList[1]):
                            for f in F[k - 1]:
                                if subset > set(f):
                                    candidate_keys.remove(set(unionList));
                                    break;
            elementPos = 0
    return candidate_keys;


# Create F1 from L
def genF1():
    for j in range(len(L)):
        if itemCount.get(L[j]) / noOfTransactions >= MIS.get(L[j]):
            F[1].append([])
            F[1][len(F[1]) - 1].append(L[j])


# for the rest of n- frequent itemsets generation
def genF():
    k = 2
    while (F[k - 1]):
        if k == 2:
            C = level2CandidateGeneration()
        else:
            C = MSCandidateGeneration(k)
        candidateCount = [0] * len(C)
        for transaction in transactionsList:
            for i in range(len(C)):
                c = C[i]
                if c <= transaction:
                    candidateCount[i] = candidateCount[i] + 1
        for i in range(len(C)):
            c = C[i]
            if candidateCount[i] / noOfTransactions >= MIS.get((sorted(c, key=MIS.get))[0]):
                F[k].append(sorted(c, key=MIS.get))
                FCount[k].append(candidateCount[i])
        k = k + 1


# SDC MIS (PARAMETER FILE) MIS IS A DICTIONARY and SDC a float
MIS = {}
itemCount = {}
cannotHave = list()
mustHave = set()
file = open("parameter.txt", "r")
for line in file:
    line = line.replace("=", "")
    if line.count("MIS") > 0:
        line = line.replace("MIS(", "")
        line = line.replace(")", "")
        arr = line.split()
        MIS[arr[0]] = float(arr[1])
    elif line.count("SDC") > 0:
        line = line.replace("SDC", "")
        sdc = float(line)
    elif line.count("cannot_be_together:") > 0:
        line = line.replace("cannot_be_together:", "").replace('{', '[').replace('},', '};').replace('}', ']').replace(
            ' ', '').rstrip().split(';')
        for l in line:
            cannotHave.append(set(l.replace("[", "").replace("]", "").rstrip().split(",")));
    elif line.count("must-have:") > 0:
        line = line.replace("must-have:", "").replace(" ", "").rstrip()
        if (line.count("or") > 0):
            mustHave = set(line.split("or"))
        else:
            mustHave = {line}

itemsList = list(MIS.keys())
itemsList.sort()
n = len(itemsList)

for i in range(n):
    itemCount[itemsList[i]] = 0;

# TRANSACTIONS (INPUT FILE) READ AS A LIST OF SETs Each transaction is a set
transactionsList = []
noOfTransactions = 0
file = open("input.txt", "r")
for line in file:
    st = line.replace(' ', '').replace('}', '};').replace('\n', '').split(';')
    st.remove('')
    for s in st:
        if s.count(',') > 0:
            temp = set(
                s.replace(' ', '').replace('\t', '').replace('{', '').replace('}', '').replace('\n', '').split(','))
        else:
            singleElement = s.replace(' ', '').replace('{', '').replace('}', '').replace('\n', '')
            temp = set([singleElement])
        transactionsList.append(temp)
        noOfTransactions = noOfTransactions+1
        for item in itemsList:
            if (item in temp):
                itemCount[item] = itemCount[item] + 1;




# FREQUENT ITEMS LISTS (1 to N)
F = [[] for i in range(1, len(itemsList) + 1)]
candidateCount = []
FCount = [[] for f in F]

# Algorithm Starts here
M = sorted(MIS, key=MIS.get);
init_Pass()
genF1()
genF()

cannot_Have()
must_Have()
outputFile = open("output.txt", "w");
rem = True
for f in F:
    if len(f)!=0:
        rem=False
if rem:
    F=[]
for f in F:
    if f:
        print "Frequent  ", len(f[0]), " itemsets"
        outputFile.write("Frequent  " + str(len(f[0])) + " itemsets" + '\n' + '\n')
        for itemSet in f:
            if F.index(f) == 1:
                print itemCount.get(itemSet[len(itemSet) - 1]), ":", "{"," , ".join(itemSet),"}"
                outputFile.write('\t' + str(itemCount.get(itemSet[len(itemSet) - 1])) + ": { " + ", ".join(itemSet) + ' }\n')
            else:
                print FCount[F.index(f)][f.index(itemSet)], ":", "{"," , ".join(itemSet),"}"
                outputFile.write('\t' + str(FCount[F.index(f)][f.index(itemSet)]) + ": { " + ", ".join(itemSet) + ' }\n')
                print "Tailcount=", tailCount(itemSet)
                outputFile.write("Tailcount=" + str(tailCount(itemSet)) + '\n' + '\n')
        print "Total number of frequent ", len(f[0]),"-itemsets = ", len(f)
        outputFile.write('\t' + "Total " + str(len(f[0])) + "-itemsets = " + str(len(f)) + '\n' + '\n' )

if not F:
    print "No frequent itemsets"
    outputFile.write("No frequent itemsets")
