# A-Priori, finding popular candidates
######################################################################################
# FIRST PASS
######################################################################################

# bitarray cannot store integers so need to use dict
singles_count = {} # singles count
bucket = {} # buckets can contain many tuples
bucket_count = {} # count how many items in each bucket
C_k = [] # this is a tuple got from baskets
k = 2
number_of_buckets = 1000000
with open("data.txt", 'r') as f:
    for l in f:
        line = l[:-1]
        if line == "":  # reset k-tuple for new basket
            C_k = [] # make tuple empty for next tuple
            continue

        C_k.append(line)
        # add single items and counts to sd dict
        if len(C_k) == k:

            hashi = abs(hash(C_k[0])) % number_of_buckets
            hashj = abs(hash(C_k[1])) % number_of_buckets

            if hashi in singles_count:
                singles_count[hashi] += 1
            else:
                singles_count[hashi] = 1

            if hashj in singles_count:
                singles_count[hashj] += 1
            else:
                singles_count[hashj] = 1
            C_k = C_k[1:]

######################################################################################
# BETWEEN PASSES
######################################################################################

# make a bitvector
s = 1269 # treshold should be quite high i.e. 1% of number of baskets
s = 10
from bitarray import bitarray
gBitarray = bitarray(number_of_buckets) # here we'll but all items that are above support level
gBitarray.setall(0)

# change dict to bitarray
for singles_hash, scount in singles_count.iteritems():
    if scount >= s:
        gBitarray[singles_hash] = 1

# since we have now frequent buckets we can use only those as input for next pass

######################################################################################
# SECOND PASS
######################################################################################

# Read file second time

pop = {}
i = 0
C_k = []
with open("data.txt", 'r') as f:
    for l in f:
        line = l[:-1]

        if line == "":  # reset k-tuple for new basket
            C_k = []
            continue

        C_k.append(line)  # add new item from basket, return k-tuple
        if len(C_k) == k:
            ihash = abs(hash(C_k[0])) % number_of_buckets
            jhash = abs(hash(C_k[1])) % number_of_buckets
            if gBitarray[ihash] and gBitarray[jhash]:
                i += 1
                if tuple(C_k) in pop:
                    pop[tuple(C_k)] += 1
                else:
                    pop[tuple(C_k)] = 1
                #print '('+C_k[0]+','+C_k[1]+')'
            #yield C_k
            C_k = C_k[1:]

# select only frequent pairs from all candidates, with support at least 's'
s = 10  # support threshold
L2 = {}
for ck,n in pop.iteritems():
    if n >= s:
        L2[ck] = n
print '%d pairs of items with >%d occurances' % (len(L2), s)

print "Done"
