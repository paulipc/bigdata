#
# This is part of "big data service"- project made for Arcada Big Data Analytics course
# It takes in firewall log and predicts network traffic with KNN 
# Input needs to be in subdirectory ./inputs and outputs in ./outputs
# Training and predicting will be in separate functions. In development phase all code is in one file.
# Code is developed with jupyter notebook, since this way it is very easy to test and see output.
#
# There are several steps and I am working now on the first one.
# For first step data needs to be prepared with several transformations to required format.
# 10.2.2017
#

import numpy as np
import pandas as pd
import csv
from sklearn.neighbors import KNeighborsRegressor

# read file into dataframe
df = pd.read_csv('./inputs/F1_All_Traffic.csv')

# need to read whatever file in the directory and then delete them
# requirement for "service"

# filter all 'Denied' lines
df2 = df[df.msg != 'Denied']

# split 'info_5' field information into substrings
# expand dataframe with 0,1,2 columns
# where 1 = sent, 2 = received
#df2=df['info_5'].str.split(";",expand=True)
df3 = pd.concat([df2, df2['info_5'].str.split(";",expand=True)], axis=1, join_axes=[df2.index])

# create new field for sent and received data
# move traffic information to 'sent' and 'received' fields
# correct datatypes
df3['received'] = pd.to_numeric(df3[2].str.replace('rcvd_bytes=',''))
df3['sent'] = pd.to_numeric(df3[1].str.replace('sent_bytes=',''))
df3['date'] = pd.to_datetime(df3['update_time'])

# select needed fields only to new dataframe
df4 = df3[['date','sent','received']]

####
# this makes dataframe to sum data traffic to 15 min. periods
###
# set update time to index
df4 = df4.set_index(['date'])
# resample, sum rolling and mean gives us needed information
df5 = df4.resample('15T').sum().fillna(0).rolling(window=15, min_periods=1).mean()

df5.to_csv('./outputs/output.csv') # temporary output for testing

# This is current state of work and now output needs to be transformed to one timeline matrix and one data traffic vector 
# for KNN.
# Comments below describes work to be done.

#
# KNeighbors Regressor
#

# convert dataframe to suitable input to Regressor

# split data, if it is in right format, if not then need to reformat

# train, predict - these should be in separate .py -files (project requirement)

# test accuracy, optimize parameters

# provide data that can be plotted easily to ./outputs directory
# as well as accuracy to separate file
# clean up and then all is done to point 1.
