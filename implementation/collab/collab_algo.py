#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from numpy import array

#--------------------------------finding similar user-------------------------------------------------

dfuser=pd.read_csv("./data/test_data/userskills.csv")
dfuser=dfuser.loc[:,~dfuser.columns.duplicated()]
dfuser=dfuser.fillna(0)
dfuser.shape
dfuser.head()

#remove rows with less than 5 skills
dfuser=dfuser.dropna(thresh=5)
dfuser.shape
#extract max user id's
m = np.int32(max(dfuser["Respondent"])).item()

#Build  a dictionary of respondent id's as keys and thier skills as values
temp=[0]*m
count=1
start=time.time()
d=dict()
for row in dfuser.iterrows():
        index,data=row
        l=list()
        #l=[data.values[0],list(data.values[1:])]
        s = np.int32(data.values[0]).item()
        d[s]=np.array(list(data.values[1:]))
end=time.time()
print(d[1])
print(end-start)

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
print("Building the similarity matrix....\n")
for key, value in d.items():
        if(key<5000):
            b=(np.linalg.norm(value))
            for key2,value2 in d.items():
                if(key2<5000):
                    #computes the dot product of the two skill vectors
                    a=np.dot(d[key],d[key2])
                    #calculates the cosine similarity between these vectors
                    ans=a/(np.linalg.norm(value2)*b)
                    sim[key][key2]=ans
                    #count2+=1
            #count1+=1
e=time.time()
print("total time for building similarity matrix ")

print(e-s)
#prints the first 10 similarity scores for the user with ID 1
print(sim[1][:10])
#finds and prints the highest similarity score for user 1, excluding the similarity with user 0 and themselves (user 1)
print((max(sim[1][2:])))
#prints the index (or user ID) of the most similar user to user 1, again excluding user 0 and user 1 themselves
print(sim[1].index(max(sim[1][2:])))

#file with respondent and their company where they work
dfjob=pd.read_csv("./data/test_data/colabdata.csv")

#Recommend user (Number) a job based on another user who has almost the same skill as him.
print("Respondent X is working in ")
print(dfjob.loc[dfjob.Respondent==3]["company"].values)

#similarity of user 3 and 1,2,3
m1=max(sim[3][:3])
#similarity of user 3 and 4+
m2=max(sim[3][4:])
#finds max similarity between the 2 ranges
ma=max(m1,m2)
#finds user id of max similarity user
suser=sim[3].index(ma)

#user 3265 is very similar to user 3 and hence we can recommend user 3265 job to user 3.
print("Respondent ",suser,"is working in")
print(dfjob.loc[dfjob.Respondent==suser]["company"].values)

#------------------------------finding jobs reccomended to similar user---------------------------------------------------

dfcont=pd.read_csv("./data/test_data/recommend_content_algo.csv")

print("Respondent 3 was recommended jobs from content based filtering in \n")
print(dfcont.loc[dfcont.Respondent==3]["company"].values)
print("Respondent 3 was recommended job titles from content based filtering ")
print(dfcont.loc[dfcont.Respondent==3]["jobtitle"].values)
print("\n")

print("Respondent ",suser,"was most similiar to respondent 3\n")
print("Based on respondent ",suser," the jobs recommended to 3 are ")
print(dfcont.loc[dfcont.Respondent==suser]["company"].values)
print("The recommended job titles are ")
print(dfcont.loc[dfcont.Respondent==suser]["jobtitle"].values)

