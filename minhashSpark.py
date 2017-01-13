import numpy
import os
import re
import binascii
from time import time

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("minhash")
sc = SparkContext(conf = conf)


# read all files to Spark at once. All the files are collected to one directory to do this.
filesRDD = sc.wholeTextFiles("C:/Users/pauli.sutelainen/Documents/Arcada/iPythonBook/desc/homework2/awd_1990_00")


def getAbstract(x):
    """ Get rid of abstracts in files
    """
    y = ''.join(map(str, x))
    pos = y.find("Abstract    :")
    #print "pos: ", pos
    return y[pos+13:].replace('\n','')

withOutAbstractRDD = filesRDD.map(getAbstract)

def getShingles(line):
    """ Get shingles of texts in files
    """
    k=5
    abstract = ' '.join([line[:-1].strip()])
    abstract = re.sub(' +', ' ', abstract)  # remove double spaces
    # get all k-shingles and return their hash codes
    shingles = set()
    L = len(abstract)
    for i in xrange(L-k+1):
        shingle = abstract[i:i+k]
        crc = binascii.crc32(shingle) & 0xffffffff  # hash the shingle to a 32-bit integer
        shingles.add(crc)
    return shingles

shinglesRDD = withOutAbstractRDD.map(getShingles) # shingles of text files 

# set global parameters to process the whole dataset
bands = 10
rows = 10
nsig = bands*rows  # number of elements in signature, or the number of different random hash functions
maxShingleID = 2**32-1  # record the maximum shingle ID that we assigned
nextPrime = 4294967311  # next prime number after maxShingleID

A = numpy.random.randint(0, nextPrime, size=(nsig,), dtype="int64")
B = numpy.random.randint(0, nextPrime, size=(nsig,), dtype="int64")

def getSignatures(x):
    """ Get signatures out of shingles by hashing shingles
    """
    signature = numpy.ones((nsig,)) * (maxShingleID + 1)
    for ShingleID in x:
        hashCodes = ((A*ShingleID + B) % nextPrime) % maxShingleID
        numpy.minimum(signature, hashCodes, out=signature)
    return signature    

signaturesRDD = shinglesRDD.map(getSignatures)
signatures = signaturesRDD.collect() # now we have signatuers in matrix

def LSH(signatures, bands, rows, Ab, Bb, nextPrime, maxShingleID):
    """Locality Sensitive Hashing
    """
    numItems = signatures.shape[1]
    signBands = numpy.array_split(signatures, bands, axis=0)
    candidates = set()
    for nb in xrange(bands):
        hashTable = {}
        for ni in xrange(numItems):
            item = signBands[nb][:,ni]
            hash = (numpy.dot(Ab[nb,:], item) + Bb[nb]) % nextPrime % maxShingleID
            if hash not in hashTable:
                hashTable[hash] = [ni]
            else:
                hashTable[hash].append(ni)
        for _,items in hashTable.iteritems():
            if len(items) > 1:
                L = len(items)
                for i in range(L-1):
                    for j in range(i+1, L):
                        cand = [items[i], items[j]]
                        numpy.sort(cand)
                        candidates.add(tuple(cand))
    return candidates

# prepare data for LSH
A2 = numpy.random.randint(0, nextPrime/2, size=(bands, rows),  dtype="int64")  # now we need a vector of A parameters for each band
B2 = numpy.random.randint(0, nextPrime/2, size=(bands, ),  dtype="int64")
signatures = numpy.array(signatures).T  # LSH needs a matrix of signatures, not a list of vectors

s = 0.9  # similarity threshold
Nfiles = signatures.shape[1]  # number of different files
t = time()
candidates = LSH(signatures, bands, rows, A2, B2, nextPrime, maxShingleID)
t2 = time() - t
print "finding candidates took %.3f seconds" % t2
print "found %d candidates" % len(candidates)
print "candidate similar pairs of files are:"
for i,j in candidates:
    print fnames[i], fnames[j]
