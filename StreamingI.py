# coding: utf-8

import math
import random
from collections import deque
from os import listdir
from os.path import isfile, join

# setup, change this
error_rate = 0.05  # error multiplier in range (0, 0.5]


def readdata(k, fname):
    """
    for input file generates k-tuples
    :param k:
    :param fname:
    :return:
    """
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


def generate_random_stream():
    """
    Reads malware training files one by one and sends itmem to stream
    :return:
    """
    mypath = './dataset/malware-training/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        for item in readdata(k=3, fname=mypath + file):
            yield item

N = 10000  # size of sliding window

r = math.ceil(1/error_rate)
r = max(r, 2)

queues = []
if N == 0:
    max_index = -1
else:
    max_index = int(math.ceil(math.log(N)/math.log(2)))

queues = [deque() for _ in range(max_index + 1)]

timestamp = 0
oldest_bucket_timestamp = -1  # No bucket so far


# In[5]:

# move sliding window by one new element in a stream, updating bucket structure
def update(element):
    """Update the stream with one element.
    """
    global timestamp
    global oldest_bucket_timestamp
    global queues
    
    timestamp = (timestamp + 1) % (2 * N)

    #check if oldest bucket should be removed
    if (oldest_bucket_timestamp >= 0 and (timestamp - oldest_bucket_timestamp) % (2 * N) >= N):
        # find and remove the oldest bucket we have
        for queue in reversed(queues):
            if len(queue) > 0:
                queue.pop()
                break
        # update oldest bucket timestamp
        oldest_bucket_timestamp = -1
        for queue in reversed(queues):
            if len(queue) > 0:
                oldest_bucket_timestamp = queue[-1]
                break

    # nothing else to do if we get a zero
    if element is False:
        return

    # update buckets if we get a one
    carry_over = timestamp  # index of new/modified bucket
    
    if oldest_bucket_timestamp == -1:
        oldest_bucket_timestamp = timestamp
        
    for queue in queues:
        queue.appendleft(carry_over)
        if len(queue) <= r:  # if we don't go over maximum number of buckets of that size
            break
            
        # remove two buckets if we have too many
        # these two buckets will make one bucket of twice larger size
        last = queue.pop()
        second_last = queue.pop()
        
        # merge last two buckets.
        carry_over = second_last

        # some auxiliary stuff
        if last == oldest_bucket_timestamp:
            oldest_bucket_timestamp = second_last


# process a stream of 2 million random elements, and print buckets
# stream = generate_random_stream(2000000)
# for element in stream:
#      update(element)
# queues

def get_count(k):
    """Returns an estimate of the number of "True" in the last N elements of the stream.
    """
    result = 0
    max_value = 0
    power_of_two = 1
    for queue in queues:
        for element in queue:
            delta = timestamp - element
            if delta < 0:
                delta += 2*N
            if delta <= k:
                max_value = power_of_two
                result += power_of_two
        power_of_two = power_of_two << 1

    result -= math.ceil(max_value/2)
    return int(result)

# add some new data, and print estimates
stream = [i for i in generate_random_stream()]
for element in stream:
     update(element)
        
output = stream[-3825:]

print(len(output))
d = {}
for o in output:
    out = o[0]+'+'+o[1]+'+'+o[2]
    if out in d:
        d[out] += 1
    else:
        d[out] = 1

import operator

maxhash = ''
maxv = 0
toplist = []
i = 0
while(i < 10):
    for k,v in d.items():
        if v > maxv:
            maxv = v
            maxhash = k

    toplist.append((maxhash,maxv))
    del d[maxhash]
    i += 1
    maxv = 0

#print(maxhash, d[maxhash])

#sorted_d = sorted(d.items(), key=operator.itemgetter(1))

print('hello world')
i = 0
for el in toplist:
    print(el[0], el[1])
    i += 1
    if i == 10:
        break

# for o in output:
#     print(o)
#x = get_count(i)
#print ("DGIM estimated sum over last %d elements is %.0f-%.0f (true: %d)" % (i, xmin, xmax, x_true))


# for i in (10, 100, 1000, 10000):
#     x_true = sum(stream[-i:])
#     x = get_count(i)
#     xmax =  math.ceil(x + x*error_rate)
#     xmin = math.floor(x - x*error_rate)
#     print ("DGIM estimated sum over last %d elements is %.0f-%.0f (true: %d)" % (i, xmin, xmax, x_true))
