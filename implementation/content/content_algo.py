#!/usr/bin/env python
# coding: utf-8

import numpy as np 
import pandas as pd 

import matplotlib.pyplot as plt
import os
import nltk
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json
from os import listdir
import glob
from scipy import spatial
import spacy

def cosine_similarity(arr1,arr2):
    ans=1- spatial.distance.cosine(arr1,arr2)
    if(np.isnan(ans)):
        return 0
    else:
        return ans
class job_postings:    
    def __init__(self,link):
        self.df2=pd.read_csv(link)
        self.training_range=int(len(self.df2.loc[:,'uniq_id']))
    def check_threshold(self, threshold,ele):
        if(ele[0]!=threshold[0][0] and abs(ele[1]-threshold[0][1])<0.03):
            return True
        else:
            return False   
    def match_profile(self,input_path,user_id,flag=0): #(content)
        #Match a given user_id with all jobs in the database
        
        df=pd.read_csv(input_path+"domain_user_profile.csv",index_col='Respondent')
        #print("test1")
        #print(df.columns)
        matches=dict()
        if(flag==0):
            if(user_id in df.index):
                userdomain=df.loc[user_id,:]
                #print("test2")
                #print(userdomain)
                #If user_id exists, retrieve the user profile from input_path
                df=pd.read_csv(input_path+"languages_profile_user.csv",index_col='Respondent')
                userlanguages=df.loc[user_id,:]

                df=pd.read_csv(input_path+"frameworks_profile_user.csv",index_col='Respondent')
                userframeworks=df.loc[user_id,:]

                df=pd.read_csv(input_path+"platforms_profile_user.csv",index_col='Respondent')
                userplatforms=df.loc[user_id,:]

                df=pd.read_csv(input_path+"databases_profile_user.csv",index_col='Respondent')
                userdatabases=df.loc[user_id,:]

                userdomain=np.asarray(userdomain.fillna(0))
                userlanguages=np.asarray(userlanguages.fillna(0))
                userframeworks=np.asarray(userframeworks.fillna(0))
                userplatforms=np.asarray(userplatforms.fillna(0))
                userdatabases=np.asarray(userdatabases.fillna(0))
                #print("test3")
                #print(userdomain)
            else:
                print("error! user id not in Dataset")
            #If it doesn't,take user profile as input
        else:

            print("New user!Enter details..")
            name=input("Enter full name")
            skills=input("Enter skills(comma separated). These are programming languages, frameworks,platforms or databases you have experience with").split(",")
            domains=''
            flag=1
            while(1):
                print("Enter domain(s) of interest separated by commas(Names are case sensitive). Should be one of the following:")
                for i in df.columns:
                    print(i,end=",")
                domains=input().split(",")
                for domain in domains:
                    if(domain not in df.columns):
                        flag=0
                        break
                if(flag==1):
                    break
                else:
                    print("Please enter valid domain")
            #domains=list(map(lambda x:x.lower(),domains))
            skills=list(map(lambda x:x.lower(),skills))                

            userdomain=pd.DataFrame(columns=df.columns)
            dictionary=dict()
            for domain in domains:
                dictionary[domain]=1.0
            userdomain=userdomain.append(dictionary,ignore_index=True)
            

            df=pd.read_csv(input_path+"languages_profile_user.csv",index_col='Respondent')
            userlanguages=pd.DataFrame(columns=df.columns)
            dictionary=dict()
            for skill in skills:
                if(skill in df.columns):
                    dictionary[skill]=1.0
            userlanguages=userlanguages.append(dictionary,ignore_index=True)

            df=pd.read_csv(input_path+"frameworks_profile_user.csv",index_col='Respondent')
            userframeworks=pd.DataFrame(columns=df.columns)
            dictionary=dict()
            for skill in skills:
                if(skill in df.columns):
                    dictionary[skill]=1.0
            userframeworks=userframeworks.append(dictionary,ignore_index=True)

            df=pd.read_csv(input_path+"platforms_profile_user.csv",index_col='Respondent')
            userplatforms=pd.DataFrame(columns=df.columns)                
            dictionary=dict()
            for skill in skills:
                if(skill in df.columns):
                    dictionary[skill]=1.0
            userplatforms=userplatforms.append(dictionary,ignore_index=True)

            df=pd.read_csv(input_path+"databases_profile_user.csv",index_col='Respondent')
            userdatabases=pd.DataFrame(columns=df.columns)               
            dictionary=dict()
            for skill in skills:
                if(skill in df.columns):
                    dictionary[skill]=1.0
            userdatabases=userdatabases.append(dictionary,ignore_index=True)
            #print(userdomain)
            userdomain=np.asarray(userdomain.iloc[0,:].fillna(0))
            userlanguages=np.asarray(userlanguages.iloc[0,:].fillna(0))
            userframeworks=np.asarray(userframeworks.iloc[0,:].fillna(0))
            userplatforms=np.asarray(userplatforms.iloc[0,:].fillna(0))
            userdatabases=np.asarray(userdatabases.iloc[0,:].fillna(0))
                
        jobdomain=pd.read_csv(input_path+"domain_job_profile.csv",index_col='uniq_id')
        joblanguages=pd.read_csv(input_path+'languages_profile_job.csv',index_col='uniq_id')
        jobframeworks=pd.read_csv(input_path+'frameworks_profile_job.csv',index_col='uniq_id')
        jobplatforms=pd.read_csv(input_path+'platforms_profile_job.csv',index_col='uniq_id')
        jobdatabases=pd.read_csv(input_path+'databases_profile_job.csv',index_col='uniq_id')
        #print(len(jobdomain.index),len(joblanguages.index))
        
        
        for i in jobdomain.index:
            #print(i)
            domain=jobdomain.loc[i,:].fillna(0)
            language=joblanguages.loc[i,:].fillna(0)
            framework=jobframeworks.loc[i,:].fillna(0)
            platform=jobplatforms.loc[i,:].fillna(0)
            database=jobdatabases.loc[i,:].fillna(0)
            job_id=str(i)
            domain=np.asarray(domain)
            language=np.asarray(language)
            framework=np.asarray(framework)
            platform=np.asarray(platform)
            database=np.asarray(database)
            #print(len(domain),len(userdomain))
            score=(0.7*cosine_similarity(domain,userdomain))+(0.3*(cosine_similarity(language,userlanguages)+cosine_similarity(framework,userframeworks)+cosine_similarity(platform,userplatforms)+cosine_similarity(database,userdatabases)))
            matches[job_id]=score
            score=(0.7*cosine_similarity(domain,userdomain))+(0.3*(cosine_similarity(language,userlanguages)+cosine_similarity(framework,userframeworks)+cosine_similarity(platform,userplatforms)+cosine_similarity(database,userdatabases)))
            #Initializing job profiles for later access
            self.job_domain=domain
            self.job_language=language
            self.job_framework=framework
            self.job_platform=platform
            self.job_database=database
            
            self.user_domain=userdomain
            self.user_language=userlanguages
            self.user_framework=userframeworks
            self.user_platform=userplatforms
            self.user_database=userdatabases
        matches=sorted(matches.items(),key=lambda x:x[1],reverse=True)
        #print("test4")
        #print(userdomain)
        recommendations=matches[:10]
        print("recommendations are")

        rows=pd.DataFrame(columns=self.df2.columns)
        count=0
        for i in recommendations:
            row=self.df2[self.df2['uniq_id']==i[0]]
            rows = pd.concat([rows, row], ignore_index=True)
            count=count+1
        return rows

#creates top 10 recommendations for each user
import os
obj = job_postings("../data/dice_com-job_us_sample.csv")

df_user = pd.read_csv("../data/survey_results_public.csv")
df_job = pd.read_csv("../data/dice_com-job_us_sample.csv")
output_csv_path = "../data/recommend_content_algo.csv"
recommendations_1000=pd.DataFrame(columns=df_job.columns)

# Check if the output file already exists
write_header = not os.path.exists(output_csv_path)

for ele in df_user.loc[:, 'Respondent'].tolist()[:10]:
    rows = obj.match_profile("../data/", ele)
    rows['Respondent'] = ele
    #recommendations_1000 = pd.concat([recommendations_1000, rows.head(1)], ignore_index=True)
    #print("recommendations_1000", recommendations_1000)

    # Reorder columns with 'Respondent' as the first column
    rows = rows[['Respondent'] + [col for col in rows.columns if col != 'Respondent']]
    
    # Append rows to the CSV file without writing the header after the first time
    rows.to_csv(output_csv_path, mode='a', index=False, header=write_header)
    
    # Set write_header to False after writing the header for the first time
    write_header = False

#recommendations_1000.to_csv("../data/collaborative_filt/recommendations3.csv")

