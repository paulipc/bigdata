from time import time
import numpy
from pyspark import SparkContext, SparkConf

# declare spark context
conf = SparkConf().setAppName("test").setMaster("local")
sc = SparkContext(conf=conf)

bands = 13  # split input matrices into this number of row/column bands

N = (1000/bands)*bands  # set matrix size arount 1000, dividible evenly by 'bands'
band_size = N/bands
A = numpy.random.rand(N,N)  # random matrix size about 1000x1000
B = numpy.random.rand(N,N)  # random matrix size about 1000x1000

rows_A = numpy.array_split(A, bands, axis=0) # split rows to bands
columns_B = numpy.array_split(B, bands, axis=1) # split columns to bands

rows_A_ix = [(idx, row) for idx,row in enumerate(rows_A)] # add index to each block to rows and columns
columns_B_ix = [(idx, col) for idx,col in enumerate(columns_B)]
C_true = numpy.dot(A, B) # calculate without parallellization to verify the result at the end

t = time()

rowsRDD = sc.parallelize(rows_A_ix) # parallellizies splitted rows
colsRDD = sc.parallelize(columns_B_ix) # parallellizies splitted columns

pairs = rowsRDD.cartesian(colsRDD)
D = pairs.collect()
O = numpy.empty((N,N))

for el in D:
    xind = el[0][0]*band_size # this is index where we need to put this element
    yind = el[1][0]*band_size # this is index where we need to put this element
    el1 = el[0][1] # get row matrix
    el2 = el[1][1] # get column matrix
    O[xind:xind+band_size, yind:yind+band_size] = numpy.dot(el1, el2)

#print "Parallel: %.2fsec" % (time()-t)
print "Result is correct: ", numpy.allclose(O, C_true)
