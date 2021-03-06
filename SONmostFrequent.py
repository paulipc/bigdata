def readdata(k, fname="data.txt"):
    C_k = []
    with open(fname, 'r') as f:
        for l in f:
            line = l[:-1]
            
            if line == "":  # reset k-tuple for new basket
                C_k = []
                continue
            
            C_k.append(line)  # add new item from basket, return k-tuple
            if len(C_k) == k:
                yield C_k[:]  # 'C_k[:]' is a copy of 'C_k'
                C_k = C_k[1:]

f = open('uusdata2.txt','w') # input data is transformed to file with "tuples" separated with '+' sign.

for C_k in readdata(k=2):
    f.write(C_k[0] +'+'+C_k[1]+'\n')

f.close()

#
## filter VALUES SMALLER THAN TRESHOLD
#
## in SON this is first MAP and REDUCE
#
def support(line):
     if line[1] >= 10:
         return True
     else:
         return False

lines = sc.textFile("uusdata2.txt") #.map(lambda line: line.split(","))
ccounts = lines.map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)


popular = ccounts.filter(support)
#popular.collect()

#
## in SON this is second MAP and REDUCE
#
linesnew = lines.map(lambda x: (x,0))
joinedpopular = popular.join(linesnew).map(lambda e: (e[0], e[1][0])).map(lambda d: (d[0],1)).reduceByKey(lambda a, b: a + b)

def support(line):
     if line[1] >= 10:
         return True
     else:
         return False

joinedpopular.filter(support).count()
