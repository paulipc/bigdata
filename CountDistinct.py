import time
import os
import requests
import json
import binascii
import numpy

def count_trail_zeroes(d):
    """Count the number of leading and trailing zeroes in an integer."""
    b = "{:064b}".format(d)
    try:
        return 63 - b.rindex("1")
    except ValueError:  # "stubsting not found" error - did not find any '1' in the string
        return 64

starttime=time.time()

# read online data stream of RSVPs,
# extract city and name of sender,
# count approximate number of different cities/names
# (and their exact number by naive algorithm for comparison)
# note: this code runs forever - until you manually stop it

largePrime = 1003162753
r1 = numpy.random.randint(largePrime)
r2 = numpy.random.randint(largePrime)

R_persons = 0
R_cities = 0
u_persons = set()  # sets to store exact number of already seen different persons/cities
u_cities = set()

r = requests.get('http://stream.meetup.com/2/rsvps', stream=True)
for raw_rsvp in r.iter_lines():
    timediff = int(time.time()-starttime)
    if raw_rsvp:
        rsvp = json.loads(raw_rsvp)
        person =rsvp[u'member'][u'member_name']
        #city = rsvp[u'group'][u'group_city']
        hash_person = (binascii.crc32(person.encode('utf-8'))*r1 + r2) % largePrime 
        #hash_city = (binascii.crc32(city.encode('utf-8'))*r1 + r2) % largePrime 
        u_persons.add(hash_person)
        #u_cities.add(hash_city)
        R_persons = max(R_persons, count_trail_zeroes(hash_person))
        #R_cities = max([R_cities, count_trail_zeroes(hash_city)])
        #print "%d unique persons (%d true),  %d unique cities (%d true)" % (2**R_persons, len(u_persons), 2**R_cities, len(u_cities))
    if timediff >= 120: # 86400 sec on 24h
        print ("sekuntia meni ", timediff)
        print ("%d unique persons" % (2**R_persons))
        break
