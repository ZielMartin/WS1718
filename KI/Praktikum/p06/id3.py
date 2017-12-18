import math

shouldPrint = True


def H(S):
    global shouldPrint
    sum = 0
    for p in S:
        if shouldPrint:
            # print(p, " * log2(", p, ") + ", end="")
            pass
        try:
            sum += p * math.log2(p)
        except ValueError:
            pass
    #print("0", end="")
    sum *= -1
    #print(sum)
    return sum

def Values(A):
    allValues = []
    for value in A:
        if value not in allValues:
            allValues.append(value)
    return allValues

def Sublist(list, indices):
    l = []
    for i in indices:
        l.append(list[i])
    return l

def R(SA):
    A = SA[len(SA)-1]
    ratios = {}
    for colNr in range(len(SA)-1):
        sum = 0

        for v in Values(SA[colNr]):

            for v2 in Values(A):
                if((colNr, v2) not in ratios.keys()):
                    ratios[(colNr, v2)] = []
                indices = [i for i, x in enumerate(A) if x == v2]
                # print(indices)
                listOfClass = Sublist(SA[colNr], indices)
                print("v: ", v, " list: ", listOfClass)
                shitCount = listOfClass.count(v)
                r = shitCount / len(listOfClass)
                ratios[(colNr, v2)].append(r)
            # print(SA[colNr].count(v), " / ", len(SA[colNr]))
            print(ratios)
            #print(ratios)

            # sum += SA[colNr].count(v) / len(SA[colNr]) * H(ratios[(colNr, v2)])
            # print(")")
        print("SUM: ", sum)


myTable = [0 for x in range(4)]

myTable[0] = [True, False, True, True, True, False, False]
myTable[1] = [True, False, True, False, True, True, False]
myTable[2] = ['A', 'M', 'B', 'A', 'M', 'B', 'A']
myTable[3] = [True, True, False, False, True, True, False]

R(myTable)
