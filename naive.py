import numpy as np
# adding temp file because run into memory error with pairs.append(i,j)

# hash table for singles, hash function, hashing and de-hashing
singles = {}

def s2h(x):
    k = 5000
    h = abs(hash(x)) % k
    if x in singles:
        print 'error, existing string'
    singles[h] = x
    return h

def readdata(k, fname="data.txt"):
    f2 = open("temp.txt","w")
    pairs = []
    items = []
    hline = ''
    f = open(fname, 'r')
    for l in f:
        line = l[:-1]
        if line == "":  # new basket
            if len(items) > 1:
                # here counting to matrix
                A = np.zeros((len(set(items)), len(set(items))), dtype=np.int16)  # memory n(matrix(n,n))
                # making items to set and dict to get index for matrix
                d = dict.fromkeys(set(items))  # memory n(distinct items)
                i = 0
                for k, v in d.iteritems():
                    d[k] = i
                    i += 1
                for i in items:
                    for j in items:
                        if d[i] < d[j]:
                            A[d[i]][d[j]] += 1

                n = len(items)
                n1 = n * (n - 1) / 2
                n2 = 1
                pair = []
                # here printing counts out of matrix
                d2 = dict((y, x) for x, y in d.iteritems())  # switch dict around to get str based on index
                len_items = len(set(items))
                items = []
                # After counting tuples to matrix these can be written to file to save memory
                # Just douple loop i and j to length of set(items) and output based on dict the right string
                for i in range(1, len_items ):
                    for j in range(1, len_items ):
                        if i < j:
                            for k in range(1, A[i][j] + 1):  # print as many tuples as there is count in A
                                f2.write('(' + str(d2[i]) + ',' + str(d2[j]) + ')\n')
            else:
                items = []
                continue
            continue
        else:
            hline = s2h(line)
            items.append(hline)
    f2.close()
    f.close()

# generate all candidate pairs with their counts (Naive approach)

readdata(k=2)
C2 = {}
f = open("temp.txt", "r")
for C_k in f:

    key = C_k[:-1]
    if key in C2:
        C2[key] += 1
    else:
        C2[key] = 1
f.close()

# select only frequent pairs from all candidates, with support at least 's'
s = 10  # support threshold
L2 = {}
for ck,n in C2.iteritems():
    if n >= s:
        L2[ck] = n
print '%d pairs of items with >%d occurances' % (len(L2), s)
