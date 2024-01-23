#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import random
from numpy import array

dfuser=pd.read_csv("./data/collaborative_filt/userskills.csv")
dfuser = dfuser.loc[:,~dfuser.columns.duplicated()]
dfuser=dfuser.fillna(0)
dfuser.shape
dfuser.head()

#remove rows with less than 5 skills
dfuser=dfuser.dropna(thresh=5)
dfuser.shape
m = np.int32(max(dfuser["Respondent"])).item()
print(m)
print(type(m))

#Build  a dictionary of respondent id's as keys  and thier skills as values
temp=[0]*m
vector=np.array(temp)
count=1
star=time.time()
d=dict()
for row in dfuser.iterrows():
        index,data=row
        l=list()
        #l=[data.values[0],list(data.values[1:])]
        s = np.int32(data.values[0]).item()
        d[s]=np.array(list(data.values[1:]))
        #print(type(data))
end=time.time()
print(d[1])
print(end-star)

#Build the user user similarity matrix based on thier skill vectors

sim=list()
s=time.time()
for i in range(5000):
        l=list()
        l=[0]*5000
        sim.append(l)
e=time.time()
print(e-s)

count1=1
count2=1
t=time.time()
for key, value in d.items():
        if(key<5000):
            print(key)
            b=(np.linalg.norm(value))
            for key2,value2 in d.items():
                if(key2<5000):
                    #print(key2)
                    a=np.dot(d[key],d[key2])
                    ans=a/(np.linalg.norm(value2)*b)
                    sim[key][key2]=ans
                    #count2+=1
            #count1+=1
e=time.time()
print("total time for building similarity matrix ")

print(e-s)
print(sim[1][:10])

print((max(sim[1][2:])))
print(sim[1].index(max(sim[1][2:])))

dfjob=pd.read_csv("./data/collaborative_filt/colabdata.csv")

#Recommend user 3 a job based on another user who has almost the same skill as him.
print("Respondent 3 is working in ")
print(dfjob.loc[dfjob.Respondent==3]["company"].values)

m1=max(sim[3][:3])
m2=max(sim[3][4:])
ma=max(m1,m2)
suser=sim[3].index(ma)
#print(suser) #user 3265 is very similar to user 3 and hence we can recommend user 3265 job to user 3.
print("Respondent ",suser,"is working in")
print(dfjob.loc[dfjob.Respondent==suser]["company"].values)

dfcont=pd.read_csv("./data/recommend_content_algo.csv")
sim=list()
s=time.time()
for i in range(200):
        l=list()
        l=[0]*200
        sim.append(l)
e=time.time()
print(e-s)
t=time.time()
print("Building the similarity matrix....\n")
for key, value in d.items():
        if(key<200):
            #print(key)
            b=(np.linalg.norm(value))
            for key2,value2 in d.items():
                if(key2<200):
                    #print(key2)
                    a=np.dot(d[key],d[key2])
                    ans=a/(np.linalg.norm(value2)*b)
                    sim[key][key2]=ans
                    #count2+=1
            #count1+=1
e=time.time()

print("Respondent 3 was recommended jobs from content based filtering in \n")
print(dfcont.loc[dfcont.Respondent==3]["company"].values)
print("Respondent 3 was recommended job titles from content based filtering ")
print(dfcont.loc[dfcont.Respondent==3]["jobtitle"].values)
print("\n")
m1=max(sim[3][:3])
m2=max(sim[3][4:])
ma=max(m1,m2)

suser=sim[3].index(ma)

print("Respondent ",suser,"was most similiar to respondent 3\n")
print("Based on respondent ",suser," the jobs recommended to 3 are ")
print(dfcont.loc[dfcont.Respondent==suser]["company"].values)
print("The recommended job titles are ")
print(dfcont.loc[dfcont.Respondent==suser]["jobtitle"].values)

