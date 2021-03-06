from bitarray import bitarray
import time
import requests
import json
from collections import defaultdict  # available in Python 2.5 and newer
import operator
import os
import binascii
import numpy

starttime=time.time() # this is starting time, we want to run this for selected time in sec.

# d = defaultdict(float) # counts for topics
# treshold = 1/2 # this is a treshold when topic is dropped from counting. Must be less than 1
# c = float(1)/1000000000 # this is a constant

r = requests.get('http://stream.meetup.com/2/rsvps', stream=True)

# create Bloom filter with single hash function
N = 1000000
largePrime = 1003162753
B = bitarray(N)
B.setall(0)

# 1,013,527
# 1,003,162,753
r1 = numpy.random.randint(N)
r2 = numpy.random.randint(N)


#
# do this for 24h, test with less time.
#
for raw_rsvp in r.iter_lines():
    timediff = int(time.time()-starttime)    
    if raw_rsvp:
        rsvp = json.loads(raw_rsvp)
        list_topics = rsvp[u'group'][u'group_topics']
        person = rsvp[u'member'][u'member_name']
        person =  u' '.join((person)).encode('utf-8').strip()
        # add person to bloom filter
        binperson = binascii.crc32(person)
        hash_i = ((binperson*r1 + r2) % largePrime) % N
        B[hash_i] = 1

    if timediff >= 20: # 86400 sec on 24h
        print ("sekuntia meni ", timediff)
        break

#
# check if person exists in bloom filter bin array
#

r = requests.get('http://stream.meetup.com/2/rsvps', stream=True)
starttime=time.time() # start the next day
count = 0
for raw_rsvp in r.iter_lines():
    timediff = int(time.time()-starttime)    
    if raw_rsvp:
        rsvp = json.loads(raw_rsvp)
        list_topics = rsvp[u'group'][u'group_topics']
        person = rsvp[u'member'][u'member_name']
        person = u' '.join((person)).encode('utf-8').strip()
        # check if username is existing in bitarray
        binperson = binascii.crc32(person)
        hash_i = ((binperson*r1 + r2) % largePrime) % N
        if B[hash_i] == 1:
            count += 1


    if timediff >= 20: # 86400 sec on 24h
        print ("sekuntia meni ", timediff)
        break

print ('repetitive users', count)
