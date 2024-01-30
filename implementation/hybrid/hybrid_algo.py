#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from scipy.cluster.hierarchy import dendrogram, ward
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity
from pylab import rcParams
rcParams['figure.figsize'] = 50, 20
import nltk
from nltk.corpus import stopwords
import re
import time
start=time.time()
nltk.download('stopwords')
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings; warnings.simplefilter('ignore')
from sklearn.cluster import KMeans
import scipy.sparse as sp
from typing import List


# Functions to clean skills data and make a vocabulary for skills vectorization

def text_scrubber(values):
    result = []
    for string in values:
        # Handle NaN values
        if pd.isna(string):
            result.append(np.nan)
        else:
            temp = re.sub('(\(.*\))', '', string)
            temp = re.sub('&#39;|\x92', '\'', temp)
            temp = re.sub(' &amp; |&amp;|\x95|:|;|&|\.|/| and ', ',', temp)
            result.append(temp)
    return result

def tokenizer(df):   
    # Custom stop words that come up very often but don't say much about the job title.
    stops = ['manager', 'nice' 'responsibilities', 'used', 'skills', 'duties', 'work', 'worked', 'daily', 'next','magic','world','interview',
             'services', 'job', 'good','using', '.com', 'end', 'prepare', 'prepared', 'lead', 'requirements','#39','see below','yes'] + list(stopwords.words('english'))
    values, ids, resume_ids = [],[],[]
    count = 0
    for idx, row in df.iterrows():
        
        # Split on commas
        array = row['skills']
        array=str(array)
        array=array.lower().split(',')
        for x in array:
            # make sure the value is not empty or all numeric values or in the stop words list
            if x != '' and not x.lstrip().rstrip() in stops and not x.lstrip().rstrip().isdigit():
                # make sure single character results are the letter 'C' (programming language)
                if len(x) > 1 or x == 'C':
                    # drop stuff > 4 gram
                    if len(x.split(' ')) <= 4:
                        # update lists
                        
                        values.append(x.lstrip().rstrip())
                        ids.append(count)
                        count+=1
    
    # New dataframe with updated values.
    result_df = pd.DataFrame()
    
    result_df['skills'] = values
    return result_df

# Define a function to clean the text in each job description
def clean_text(text):
    cleaned_text = text.replace("&nbsp;", " ").replace("\x92", " ").replace("\x95", " ").replace('&amp;', " ") \
        .replace('*', " ").replace(".", " ").replace("co&#39;s", "").replace("\xae&quot;", "") \
        .replace("&#39;s", "").replace("&quot;", "").replace("?", "").replace("&#39;s", "") \
        .replace("@", "").replace("\x96", "")
    return cleaned_text


def give_suggestions(resume_text):
    matches=dict()
    # Vectorize user's skills and job descriptions
    desc = pd.DataFrame(vec.transform([resume_text]).todense())
    desc.columns = vec.get_feature_names_out()
    skillz = pd.DataFrame(vec2.transform([resume_text]).todense())
    skillz.columns = vec2.get_feature_names_out()
    mat = pd.concat([skillz, desc], axis=1)
    # Tranform feature matrix with pca
    user_comps = pd.DataFrame(pca.transform(mat))

    # Predict cluster for user and print cluster number
    cluster = lr.predict(user_comps)[0]
    print ('CLUSTER NUMBER', cluster, '\n\n')

    # Calculate cosine similarity
    cos_sim = pd.DataFrame(cosine_similarity(user_comps,comps[comps.index==cluster]))

    # Get job titles from df to associate cosine similarity scores with jobs
    samp_for_cluster = df[df['cluster_no']==cluster]
    cos_sim = cos_sim.T.set_index(samp_for_cluster['jobtitle'])
    cos_sim.columns = ['score']
    
    # Print the top ten suggested jobs for the user's cluster
    top_cos_sim = cos_sim.sort_values('score', ascending=False)[:10]
    print ('Top ten suggested for your cluster', '\n', top_cos_sim, '\n\n')
    
    # print('Accuracy',)

    # Print the top five suggested jobs for each cluster
    mat = mat.T
    for i in range(8):
        cos_sim = pd.DataFrame(cosine_similarity(user_comps,comps[comps.index==i]))
        samp_for_cluster = df[df['cluster_no']==i]
        cos_sim = cos_sim.T.set_index(samp_for_cluster.index)
        cos_sim.columns = ['score']
        top_5 = cos_sim.sort_values('score', ascending=False)[:5]

        # Merge top_5 with sample2 to get skills and description
        merged_top_5 = top_5.merge(df, how='left', left_index=True, right_index=True)
        print ('---------Top five suggested in cluster', i,  '---------\n', top_5, '\n\n')
        # Vectorize to find skills needed for each job title
       
        for job in merged_top_5.index:
            job_skills = pd.DataFrame(vec2.transform([merged_top_5.loc[job]['jobdescription'] + merged_top_5.loc[job]['skills']]).todense())
            job_skills.columns = vec2.get_feature_names_out()
            job_skills = job_skills.T
            job_skills.columns = ['score']
            job_skills = job_skills[job_skills['score'] != 0].sort_values('score', ascending=False)
            mat.columns = ['score']
            mat = mat[mat['score'] != 0]
            needed_skills = []
            scorey = []
            for i in job_skills.index:
                if i not in mat.index:    
                    needed_skills.append(i)
                    scorey.append(job_skills.loc[i][0])
            top_skills = pd.DataFrame(list(zip(needed_skills, scorey)), columns=['Skills', 'Importance'])
            print('To become a/an', job,',', '\n', 'these are the top ten skills you need:', '\n')
            print(top_skills[:5], '\n')
    return top_cos_sim

def _single_list_similarity(predicted: list, feature_df: pd.DataFrame, u: int) -> float:
    # exception predicted list empty
    if not(predicted):
        raise Exception('Predicted list is empty, index: {0}'.format(u))

    #get features for all recommended items
    feature_df_reset = feature_df.set_index('jobtitle')
    #recs_content = feature_df_reset.concat[predicted]
    recs_content = feature_df.iloc[predicted]
    recs_content = recs_content.dropna()
    recs_content = sp.csr_matrix(recs_content.values)

    #calculate similarity scores for all items in list
    similarity = cosine_similarity(X=recs_content, dense_output=False)

    #get indicies for upper right triangle w/o diagonal
    upper_right = np.triu_indices(similarity.shape[0], k=1)

    #calculate average similarity score of all recommended items in list
    ils_single_user = np.mean(similarity[upper_right])
    return ils_single_user

def intra_list_similarity(predicted: List[list], feature_df: pd.DataFrame) -> float:
    feature_df = feature_df.fillna(0)
    Users = range(len(predicted))
    print(predicted)
    ils = [_single_list_similarity(predicted[u], feature_df, u) for u in Users]
    return np.mean(ils)

#Cleaning the data
df = pd.read_csv("../../data/dice_com-job_us_sample.csv",encoding='cp850')

df['skills'] = text_scrubber(df['skills'])
test_df = tokenizer(df)

vocab = test_df['skills'].unique()
print(vocab)

# Apply the clean_text function to each element in the 'jobdescription' column
df['jobdescription'] = df['jobdescription'].apply(clean_text)

mine = ['manager', 'amp', 'nbsp', 'responsibilities', 'used', 'skills', 'duties', 'work', 'worked', 'daily','services', 'job', 'using', 'com', 'end', 'prepare', 'prepared', 'lead', 'requirements','summary','Job Role','Position']

vec = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), token_pattern='[a-zA-z]{3,50}', max_df=0.2, min_df=2, max_features=10000, stop_words=list(text.ENGLISH_STOP_WORDS.union(list(mine))), decode_error='ignore', vocabulary=None, binary=False)
df['skills']=df['skills']+df['jobdescription']+df['jobtitle']
description_matrix2 = vec.fit_transform(df['skills'].values.astype('U'))
description_matrix2 = pd.DataFrame(description_matrix2.todense())
description_matrix2.columns = vec.get_feature_names_out()

print(df['jobdescription'])

vec2 = TfidfVectorizer(vocabulary=vocab, decode_error='ignore')
df['skills']=df['skills']+df['jobdescription']+df['jobtitle']
skills_matrix2 = vec2.fit_transform(df['skills'].values.astype('U'))
skills_matrix2 = pd.DataFrame(skills_matrix2.todense())
skills_matrix2.columns = vec2.get_feature_names_out()

jobtitle_matrix = pd.concat([skills_matrix2, description_matrix2], axis=1)
jobtitle_matrix

# Run PCA to reduce number of features

pca = PCA(n_components=1000, random_state=42)
comps = pca.fit_transform(jobtitle_matrix)

# Put the components into a dataframe

comps = pd.DataFrame(comps)

# Cluster job titles based on components derived from feature matrix

cltr = AgglomerativeClustering(n_clusters=8)
cltr.fit(comps)

# Add new column containing cluster number to sample, comps, and feature matrix dataframes

#trying out 8.10.15 num of clucters ------------test more1!!!!!
df['cluster_no'] = cltr.labels_
X = comps
y = df['cluster_no']
X_train, X_test, y_train, y_test = train_test_split(X,y, stratify=y, random_state=42)
lr = LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)
lr.fit(X_train, y_train)
score1=lr.score(X_test, y_test)
print(score1)

cltr1 = AgglomerativeClustering(n_clusters=10)
cltr1.fit(comps)
df['cluster_no'] = cltr1.labels_
X = comps
y = df['cluster_no']
X_train, X_test, y_train, y_test = train_test_split(X,y, stratify=y, random_state=42)
lr = LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)
lr.fit(X_train, y_train)
score2=lr.score(X_test, y_test)
print(score2)

#hierarchical clustering
cltr2 = AgglomerativeClustering(n_clusters=15)
cltr2.fit(comps)
df['cluster_no'] = cltr2.labels_
X = comps
y = df['cluster_no']
X_train, X_test, y_train, y_test = train_test_split(X,y, stratify=y, random_state=42)
lr = LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)
lr.fit(X_train, y_train)
score3=lr.score(X_test, y_test)
print(score3)

#partitional clustering
cltr = KMeans(n_clusters=15)
cltr.fit(comps)
df['cluster_no'] = cltr.labels_
X = comps
y = df['cluster_no']
X_train, X_test, y_train, y_test = train_test_split(X,y, stratify=y, random_state=42)
lr = LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)
lr.fit(X_train, y_train)
score=lr.score(X_test, y_test)
print(score)

cltr3 = AgglomerativeClustering(n_clusters=20)
cltr3.fit(comps)
df['cluster_no'] = cltr3.labels_

X = comps
y = df['cluster_no']

X_train, X_test, y_train, y_test = train_test_split(X,y, stratify=y, random_state=42)
lr = LogisticRegression(C=10, penalty='l2', multi_class='multinomial', solver='sag', max_iter=1000)
lr.fit(X_train, y_train)
score4=lr.score(X_test, y_test)
print(score4)

clusters=[8,10,15,20]
accuracy=[score1,score2,score3,score4]

plt.plot(clusters,accuracy, color='g')
plt.xlabel('No of Clusters')
plt.ylabel('Accuracy')
plt.title('Accuracy')
plt.show()

# Look at clusters

from sklearn.manifold import TSNE

tsne = TSNE()
g = pd.DataFrame(tsne.fit_transform(comps), columns=['one', 'two'])


g['cluster_no'] = cltr3.labels_

import matplotlib.cm as cm

plt.figure(figsize=(10,10))
plt.title('Clusters Using T-SNE Components', fontsize=20)
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.scatter(g['one'], g['two'], c=g['cluster_no'], cmap=cm.jet, alpha=0.5)
plt.show()

#dont need
lr.fit(X, y)

# Assign cluster number to each job title in comps to pull particular cluster out for comparison
comps['cluster_no'] = y.values
comps.set_index('cluster_no', inplace=True)

#resume_text=input("Enter your skills. These are programming languages, frameworks,platforms or databases that you have experience with")
resume_text = '''jesus.brown3255@gmail.com SUMMARY:I am  a passion for using data to make faster and betterdecisions that leads to improved customer experiences and increased productivity. My combination oftechnical and business experience provides a unique skill-set to be able to work cross-functionally toachieve these results.SKILLSTECHNICAL:Java, Python (Pandas, Scikit-Learn, NumPy, Seaborn), Data Analytics , Big Data (AWS, Hadoop, Spark), Tableau,Advanced Microsoft Excel (Power BI, Macros, etc.) ·Student- DataScience·Oct2016 - Learned the skills to become a data professional including Python (Pandas, Numpy, Seaborn, Scikit-Learn), Advanced SQL,  No-SQL (MongoDB), MachineLearning Modeling , Big Data (AWS, Hadoop, Spark)
'''

cos_sim_result=give_suggestions(resume_text)
#only goes up to 7, remove that part


top_10_recommendations=cos_sim_result.sort_values('score', ascending=False)[:10]
top_10_list = top_10_recommendations.reset_index().to_records(index=False).tolist()
first_elements = [item[0] for item in top_10_list]
feature_df = df[['jobtitle','jobdescription']]
print(top_10_recommendations)
print(feature_df)
intra_list_similarity(top_10_recommendations, feature_df)

