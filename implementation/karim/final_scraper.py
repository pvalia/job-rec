from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import ngrams
import time
from bs4 import BeautifulSoup
import pprint
import pickle
import re
import pandas as pd
import uuid
import json
class scrapejob:
    #TODO: 
    #1-parse skills using 1-gram,2-gram,3-gram -DONE
    #2-parse experience
    #3-separate jobs with zero matches of skills for later debug
    #4-upload job data
    def __init__(self,website:str):
        """
            website(string): indeed or glassdoor
        """
        
        self.jobs_to_upload=[]
        self.jobs_to_check=[]
        opt= Options()
        opt.add_argument("--disable-popup-blocking")
        opt.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(opt)
        self.indeed=False
        self.gdoor=False
        if website == "indeed":
            self.indeed=True
            self.link="https://ca.indeed.com/"
        elif website == "glassdoor":
            self.gdoor=True
            pass
        else:
            raise Exception("website must be indeed or glassdoor")



    def connect(self):
        self.driver.get(self.link)
        self.driver.maximize_window()
        time.sleep(5)

    def search_job(self,job_name:str):
        """
            job_name(str): jobs to look up
        """
            
        if(self.indeed):
            element = self.driver.find_element(By.ID,"text-input-what") # find search box
            element.clear()
            element.send_keys(job_name)
            element.send_keys(Keys.RETURN)
            time.sleep(3)
            self.driver.find_element("xpath","//a[@class='css-145oca5 emf9s7v0']").click() #set to find newest job posts
            time.sleep(3)
            while(True):
                try:
                    
                    e=self.driver.find_elements("xpath", "//button[@class='css-yi9ndv e8ju0x51']") # close the pop up
                    time.sleep(3)
                        
                    if(len(e)!=0):     
                        e[0].click()

                        time.sleep(3)
                        
                        break
                    else:
                        pass
                except:
                    pass
        time.sleep(3)


    def scrape_job_data(self,limit:int=20):
        """
            collects job postings until limit is met.
            limit(int)= number of job posts to collect
        """
        databases_profile_job_df=pd.DataFrame(columns=["uid","amazon dynamodb","amazon rds/aurora","amazon redshift","apache hbase","apache hive","aster data","cassandra","elasticsearch", "filemaker pro","firebird","google bigquery",
        "google cloud storage","greenplum","hsqldb","ibm db2","informix","mariadb", "memcached","memsql","microsoft access","microsoft azure (tables, cosmosdb, sql, etc)","microsoft azure"
        "mongodb","msql","mysql","neo4j","netezza","oracle","panorama","postgresql","redis","sap hana","sql server","sqlite","teradata","timesten","unidata","universe","vertica"])
        domain_job_profile_df=pd.DataFrame(columns=["uid","Back End","C-suite executive","Cloud Computing","Data Scientist","Data or business analyst","business analyst","data analyst","Database Administrator(DBA)","Database Administrator"
                 ,"designer","Devops","academic researcher","educator","Embedded applications","embedded devices developer","Engineering manager","Enterprise application","Front End"
                 ,"Full stack","Game developer","Information Security","Mobile Developer","Network Engineer","product manager","QA","Test developer","Sales professional","software developer","java developer"
                 ,"sudent","system administrator","web developer"])
        frameworks_profile_job=pd.DataFrame(columns=["uid",".net core","agile","angular","asp.net mvc","aura","aurelia","bottle","cakephp","cassandra","catalyst","cloudera","codeigniter","cordova","couchdb","cuba",
                                "django","dojo","dropwizard","durandal","elm","ember.js","express","flask","flatiron","flex","flink","google web toolkit","grails","hadoop","halcyon","hive","hpcc",
                                "jsf","koa","laravel","lift","lithium","map reduce","mason","meteor","moustache","ninja","nitro","node.js","pentaho","phoenix","play","polymer","pyramid",
                                "rapidminer","react","revel","riot.js","ruby on rails","rum","simplex","sinatra","solar","spark","spring","storm","struts","symfony","tapestry","tensorflow","pytorch"
                                ,"tornado","vaadin","vanilla","vert.x","vue.js","web2py","wicket","xamarin","yarn","yii","zend","zope"])
        languages_profile_job=pd.DataFrame(columns=["uid",".net","abap","abc","actionscript","ada","ajax","apex","apl","applescript","arc","arduino","asp","assembly","atlas","automator","avenue","awk","bash","bc","bourne shell","bro"
                            ,"c","c shell","c#","c++","caml","ceylon","cfml","ch","clarion","clean","clojure","cobol","cobra","coffeescript","coldfusion","css","ct","d","dart"
                            ,"dcl","pascal","e","ecl","ec","ecmascript","egl","elixir","erlang","f#","falcon","felix","forth","fortran","fortress","go","gosu","groovy","hack","haskell",
                            "html","icon","idl","inform","informix-4gl","io","java","jade","javascript","jscript","julia","korn shell","kotlin","labview","ladder logic","lingo","lisp"
                            ,"logo","lotusscript","lpc","lua","lustre","magic","mantis","mathematica","matlab","mercury","ml","monkry","moo","mumps",
                            "objective-c","ocaml","occam","ooc","opa","opencl","perl","php","pilot","sql","postscript","powerscript","powershell","puppet","python","q","r","rexx","ruby","ruby on rails"
                            ,"rust","s","s-plus","sas","scala","scilab","sed","self","shell","signal","simula","simulink","smalltalk","smarty","spark","spss","sqr","swift","tacl","tcl","tom","transact-sql"
                            ,"typescript","vb.net","vba","vbscript","verilog","vhdl","visual basic 6","xen","xquery","xslt"])
        platforms_profile_job=pd.DataFrame(columns=["uid","amazon echo","android","apple watch","apple tv","arduino","aws","azure","drupal","esp8266","firebase","gaming console","google cloud platform","heroku","google home","ibm cloud","watson"
                            ,"ios","linux","mac os","mainframe","predix","raspberry pi","salesforce","serverless","sharepoint","windows desktop","windows server","windows phone","wordpress"])
        while(True):
            

            #finds number of jobs in each page
            time.sleep(3)
            jobs = self.driver.find_elements("xpath","//li[@class='css-5lfssm eu4oa1w0']")
            #num_of_jobs= range(0,len(jobs))
            #for index,job in zip(num_of_jobs,jobs):


            for job in jobs:
                current_job_data={}
                try:
                    
                    job.click()
                    time.sleep(10)
                except:
                    continue
                doc=BeautifulSoup(self.driver.page_source,"html.parser")
                temp_position=doc.find("h2",class_="jobsearch-JobInfoHeader-title css-161nklr e1tiznh50") # title full stack , embedded, backend ....
                position=temp_position.get_text().replace(" - job post","")
                job_type_tracker= doc.find_all("div",class_="css-fhkva6 eu4oa1w0") # tracks the job type info
                job_type_info=doc.find_all("div",class_="css-tvvxwd ecydgvn1")  # finds pay info , job type: full time , part time , contract , shift/schedule: night shift , full time
                #finding position title
                current_job_data["uid"]=uuid.uuid4().hex
                current_job_data["company"]=doc.find("span",class_="css-1x7z1ps eu4oa1w0").get_text()
                if position is None:
                    continue
                else:
                    current_job_data["title"]=position
                
                for info,tracker in zip(job_type_info,job_type_tracker):

                    if "from" in info.get_text().lower() and tracker.get_text().lower()=="pay":
                        current_job_data[tracker.get_text().lower()]=info.get_text().lower().replace("from ","") 
                    else:
                        current_job_data[tracker.get_text().lower()]=info.get_text().lower()
                description=doc.find("div",class_="jobsearch-jobDescriptionText jobsearch-JobComponent-description css-1x2lix0 eu4oa1w0")
                pp = pprint.PrettyPrinter(indent=4)
                
                time.sleep(3)
                test=description.get_text().replace('\n'," ").lower()
                
                print(test)
                current_job_data["skills"]=self.extract_skills(description.get_text().replace('\n'," ").lower())
                current_job_data["desc"]=description.get_text().replace('\n'," ").lower()
                current_job_data["experience"]=self.parse_experience(description.get_text().replace('\n'," ").lower())
                time.sleep(5)
                pp.pprint(current_job_data) 
                databases_profile_job_df = self.extract_databases(current_job_data['skills'],current_job_data['uid'],databases_profile_job_df)
                domain_job_profile_df = self.extract_domains(current_job_data['skills'],current_job_data['uid'],domain_job_profile_df)
                frameworks_profile_job = self.extract_frameworks(current_job_data['skills'],current_job_data['uid'],frameworks_profile_job)
                languages_profile_job = self.extract_languages(current_job_data['skills'],current_job_data['uid'],languages_profile_job)
                platforms_profile_job = self.extract_platform(current_job_data['skills'],current_job_data['uid'],platforms_profile_job)
                if len(current_job_data["skills"])>=7:
                    #del current_job_data["desc"]
                    self.jobs_to_upload.append(current_job_data) 
                else:
                    self.jobs_to_upload.append(current_job_data) 
                    self.jobs_to_check.append(current_job_data)
            try:

                #next_page=self.driver.find_elements("xpath","//ul[@class='css-1g90gv6 eu4oa1w0']/li[@class='css-227srf eu4oa1w0']/a[@class='css-akkh0a e8ju0x50']")
                

                next_page=self.driver.find_elements("xpath","//ul[@class='css-1g90gv6 eu4oa1w0']/li[@class='css-227srf eu4oa1w0']/a[@aria-label='Next Page']")
                
                if(len(next_page)!=0 and len(self.jobs_to_upload)<=limit):
                    print("clicking")
                    next_page[0].click()
                    time.sleep(3)
                else:

                    self.driver.close()
                    json_object=json.dumps(self.jobs_to_upload,indent=4)
                    with open("jobs_to_upload.json","w") as out:
                        out.write(json_object)

                    databases_profile_job_df.to_csv("./databases_profile_job.csv")
                    domain_job_profile_df.to_csv("./domain_job_profile.csv")
                    frameworks_profile_job.to_csv("./frameworks_profile_job.csv")
                    languages_profile_job.to_csv("./languages_profile_job.csv")
                    platforms_profile_job.to_csv("./platforms_profile_job.csv")
                    """
                    file = open('jobs-to-upload-data.pkl','wb')

                    pickle.dump(self.jobs_to_upload,file)

                    file.close()
                    
                    file = open('jobs-to-check-data.pkl','wb')

                    pickle.dump(self.jobs_to_check,file)

                    file.close()
                    """
                    break
            except:
                self.driver.close()
                file = open('jobs-to-upload-data.pkl','wb')

                pickle.dump(self.jobs_to_upload,file)

                file.close()
                file = open('jobs-to-check-data.pkl','wb')

                pickle.dump(self.jobs_to_check,file)

                file.close()
                break

    
    def extract_skills(self,description:str):
            """
            list_of_skills=["c","c++","python","react","react.js","next.js","reactjs","nextjs","sql","bigquery","relational database","operating systems","javascript","node","soap","rest","unit testing","project management","time management","object oriented programming","oop","databases","database design","web architecture","rest api","angular","java script","spring boot","java","selenium",
                    "cucumber","spring security","jbdc","junit","prostgresql","rdbms","no sql","nosql","apache","kafka","apache nifi","elasticsearch","devops","database design","code reviews","azure databricks"
                    ,"delta lake","azure storage","adf","azure analysis service","obiee","powerbi","power bi","oracle business intelligence suite enterprise edition","siebel"
                    ,"data analysis","data modeling","data mining","siebel eim","siebel eai","siebel business layer objects","siebel web templates","siebel open ui","jquery","communication skills"
                    ,"interpersonal relations","analytical skills","analytical skills","problem solving","ui integration","git","perforce","robot framework","software testing","test automation"
                    ,"linux","shell scripts","windows powershell","batch scripts","relational databases","oracle","sql server","postgresql","bi","olap","atlassian","pmp","cpmg","itil"
                    ,"project management","analytical abilities","problem solving skills","system integration","transact sql","xml modeling","xslt","xpath","xsd","wsdl","rest","soap"
                    ,"apm tools","dynatrace","splunk","jira","confluence","jenkins","bitbucket","github","agile","agile testing","kubernetes","docker","security testing","aws","ec2","vm","s3","blob storage","elastic compute cloud","amazon s3","amazon simple storage service"
                    ,"unit test","integration test","c#","mysql","nosql","mongo db","aws simpledb","azure cosmos","it administration","user provisioning","ux design","ux","ui design","ui","figma"
                    ,"firebase","query language","shell scripting","sun solaris","solaris","unix","html","css","cloudbees","ci/cd","micro services architecture","microservices architecture"
                    ,"swift","swiftui","soap nh","mvvm","model–view–viewmodel","Model view viewmodel","adivising clients","websphere","jboss","tomcat","wildfly","microsoft iis"
                    ,"node.js","node js","redux","graphql","powerdesigner","visual paradigm","jaws","wave","chrome axe","nvda","wc3 validator","apex","visualforce","object-oriented programming"
                    ,"pubsub","sns","sqs","stp","sftp","ms visual studio","ms sql server","supplier relationships","test","maintain"
                ]
            """
            list_of_databases=["amazon dynamodb","amazon rds/aurora","amazon redshift","apache hbase","apache hive","aster data","cassandra","elasticsearch", "filemaker pro","firebird","google bigquery",
            "google cloud storage","greenplum","hsqldb","ibm db2","informix","mariadb", "memcached","memsql","microsoft access","microsoft azure (tables, cosmosdb, sql, etc)","microsoft azure"
            "mongodb","msql","mysql","neo4j","netezza","oracle","panorama","postgresql","redis","sap hana","sql server","sqlite","teradata","timesten","unidata","universe","vertica"]           
            list_of_domains=["Back End","C-suite executive","Cloud Computing","Data Scientist","Data or business analyst","business analyst","data analyst","Database Administrator(DBA)","Database Administrator"
                 ,"designer","Devops","academic researcher","educator","Embedded applications","embedded devices developer","Engineering manager","Enterprise application","Front End"
                 ,"Full stack","Game developer","Information Security","Mobile Developer","Network Engineer","product manager","QA","Test developer","Sales professional","software developer","java developer"
                 ,"sudent","system administrator","web developer"]
            list_of_frameworks=[".net core","agile","angular","asp.net mvc","aura","aurelia","bottle","cakephp","cassandra","catalyst","cloudera","codeigniter","cordova","couchdb","cuba",
                                "django","dojo","dropwizard","durandal","elm","ember.js","express","flask","flatiron","flex","flink","google web toolkit","grails","hadoop","halcyon","hive","hpcc",
                                "jsf","koa","laravel","lift","lithium","map reduce","mason","meteor","moustache","ninja","nitro","node.js","pentaho","phoenix","play","polymer","pyramid",
                                "rapidminer","react","revel","riot.js","ruby on rails","rum","simplex","sinatra","solar","spark","spring","storm","struts","symfony","tapestry","tensorflow","pytorch"
                                ,"tornado","vaadin","vanilla","vert.x","vue.js","web2py","wicket","xamarin","yarn","yii","zend","zope"]
            list_of_languages=[".net","abap","abc","actionscript","ada","ajax","apex","apl","applescript","arc","arduino","asp","assembly","atlas","automator","avenue","awk","bash","bc","bourne shell","bro"
                            ,"c","c shell","c#","c++","caml","ceylon","cfml","ch","clarion","clean","clojure","cobol","cobra","coffeescript","coldfusion","css","ct","d","dart"
                            ,"dcl","pascal","e","ecl","ec","ecmascript","egl","elixir","erlang","f#","falcon","felix","forth","fortran","fortress","go","gosu","groovy","hack","haskell",
                            "html","icon","idl","inform","informix-4gl","io","java","jade","javascript","jscript","julia","korn shell","kotlin","labview","ladder logic","lingo","lisp"
                            ,"logo","lotusscript","lpc","lua","lustre","magic","mantis","mathematica","matlab","mercury","ml","monkry","moo","mumps",
                            "objective-c","ocaml","occam","ooc","opa","opencl","perl","php","pilot","sql","postscript","powerscript","powershell","puppet","python","q","r","rexx","ruby","ruby on rails"
                            ,"rust","s","s-plus","sas","scala","scilab","sed","self","shell","signal","simula","simulink","smalltalk","smarty","spark","spss","sqr","swift","tacl","tcl","tom","transact-sql"
                            ,"typescript","vb.net","vba","vbscript","verilog","vhdl","visual basic 6","xen","xquery","xslt"]
            list_of_platforms=["amazon echo","android","apple watch","apple tv","arduino","aws","azure","drupal","esp8266","firebase","gaming console","google cloud platform","heroku","google home","ibm cloud","watson"
                            ,"ios","linux","mac os","mainframe","predix","raspberry pi","salesforce","serverless","sharepoint","windows desktop","windows server","windows phone","wordpress"]
            list_of_skills=["amazon dynamodb","amazon rds/aurora","amazon redshift","apache hbase","apache hive","aster data","cassandra","elasticsearch", "filemaker pro","firebird","google bigquery",
            "google cloud storage","greenplum","hsqldb","ibm db2","informix","mariadb", "memcached","memsql","microsoft access","microsoft azure (tables, cosmosdb, sql, etc)","microsoft azure"
            "mongodb","msql","mysql","neo4j","netezza","oracle","panorama","postgresql","redis","sap hana","sql server","sqlite","teradata","timesten","unidata","universe","vertica","Back End","C-suite executive","Cloud Computing","Data Scientist","Data or business analyst","business analyst","data analyst","Database Administrator(DBA)","Database Administrator"
                 ,"designer","Devops","academic researcher","educator","Embedded applications","embedded devices developer","Engineering manager","Enterprise application","Front End"
                 ,"Full stack","Game developer","Information Security","Mobile Developer","Network Engineer","product manager","QA","Test developer","Sales professional","software developer","java developer"
                 ,"sudent","system administrator","web developer",".net core","agile","angular","asp.net mvc","aura","aurelia","bottle","cakephp","cassandra","catalyst","cloudera","codeigniter","cordova","couchdb","cuba",
                                "django","dojo","dropwizard","durandal","elm","ember.js","express","flask","flatiron","flex","flink","google web toolkit","grails","hadoop","halcyon","hive","hpcc",
                                "jsf","koa","laravel","lift","lithium","map reduce","mason","meteor","moustache","ninja","nitro","node.js","pentaho","phoenix","play","polymer","pyramid",
                                "rapidminer","react","revel","riot.js","ruby on rails","rum","simplex","sinatra","solar","spark","spring","storm","struts","symfony","tapestry","tensorflow","pytorch"
                                ,"tornado","vaadin","vanilla","vert.x","vue.js","web2py","wicket","xamarin","yarn","yii","zend","zope",".net","abap","abc","actionscript","ada","ajax","apex","apl","applescript","arc","arduino","asp","assembly","atlas","automator","avenue","awk","bash","bc","bourne shell","bro"
                            ,"c","c shell","c#","c++","caml","ceylon","cfml","ch","clarion","clean","clojure","cobol","cobra","coffeescript","coldfusion","css","ct","d","dart"
                            ,"dcl","pascal","e","ecl","ec","ecmascript","egl","elixir","erlang","f#","falcon","felix","forth","fortran","fortress","go","gosu","groovy","hack","haskell",
                            "html","icon","idl","inform","informix-4gl","io","java","jade","javascript","jscript","julia","korn shell","kotlin","labview","ladder logic","lingo","lisp"
                            ,"logo","lotusscript","lpc","lua","lustre","magic","mantis","mathematica","matlab","mercury","ml","monkry","moo","mumps",
                            "objective-c","ocaml","occam","ooc","opa","opencl","perl","php","pilot","sql","postscript","powerscript","powershell","puppet","python","q","r","rexx","ruby","ruby on rails"
                            ,"rust","s","s-plus","sas","scala","scilab","sed","self","shell","signal","simula","simulink","smalltalk","smarty","spark","spss","sqr","swift","tacl","tcl","tom","transact-sql"
                            ,"typescript","vb.net","vba","vbscript","verilog","vhdl","visual basic 6","xen","xquery","xslt","amazon echo","android","apple watch","apple tv","arduino","aws","azure","drupal","esp8266","firebase","gaming console","google cloud platform","heroku","google home","ibm cloud","watson"
                            ,"ios","linux","mac os","mainframe","predix","raspberry pi","salesforce","serverless","sharepoint","windows desktop","windows server","windows phone","wordpress"]
            #deleted skills 
            
            matches=[]
            description=description.replace("/"," ")
            filter_words=self.format_description(description)
            for unigram in word_tokenize(filter_words.lower()):
                if unigram in list_of_skills:
                    matches.append(unigram)

            for bigram in ngrams(word_tokenize(filter_words),2):
                if bigram in list_of_skills:
                    matches.append(bigram)

            for trigram in ngrams(word_tokenize(filter_words),3):
                if trigram in list_of_skills:
                    matches.append(trigram)
            return list(set(matches))
    

    def extract_databases(self,job_info_skills,uid,df):
        list_of_databases=["amazon dynamodb","amazon rds/aurora","amazon redshift","apache hbase","apache hive","aster data","cassandra","elasticsearch", "filemaker pro","firebird","google bigquery",
            "google cloud storage","greenplum","hsqldb","ibm db2","informix","mariadb", "memcached","memsql","microsoft access","microsoft azure (tables, cosmosdb, sql, etc)","microsoft azure"
            "mongodb","msql","mysql","neo4j","netezza","oracle","panorama","postgresql","redis","sap hana","sql server","sqlite","teradata","timesten","unidata","universe","vertica"]
        

        skills_found={}
        if uid not in df.values:
            skills_found['uid']=uid
            for db_skill in job_info_skills:
                if db_skill in list_of_databases:
                    skills_found[db_skill]=1
            df.loc[len(df)]=skills_found

        return df
                

    def extract_domains(self,job_info_skills,uid,df):
        list_of_domains=["Back End","C-suite executive","Cloud Computing","Data Scientist","Data or business analyst","business analyst","data analyst","Database Administrator(DBA)","Database Administrator"
                 ,"designer","Devops","academic researcher","educator","Embedded applications","embedded devices developer","Engineering manager","Enterprise application","Front End"
                 ,"Full stack","Game developer","Information Security","Mobile Developer","Network Engineer","product manager","QA","Test developer","Sales professional","software developer","java developer"
                 ,"sudent","system administrator","web developer"]
        

        domains_found={}
        if uid not in df.values:
            domains_found['uid']=uid
            for db_skill in job_info_skills:
                if db_skill in list_of_domains:
                    domains_found[db_skill]=1
            
            df.loc[len(df)]=domains_found

        return df

    def extract_frameworks(self,job_info_skills,uid,df):
        list_of_languages=[".net","abap","abc","actionscript","ada","ajax","apex","apl","applescript","arc","arduino","asp","assembly","atlas","automator","avenue","awk","bash","bc","bourne shell","bro"
                                    ,"c","c shell","c#","c++","caml","ceylon","cfml","ch","clarion","clean","clojure","cobol","cobra","coffeescript","coldfusion","css","ct","d","dart"
                                    ,"dcl","pascal","e","ecl","ec","ecmascript","egl","elixir","erlang","f#","falcon","felix","forth","fortran","fortress","go","gosu","groovy","hack","haskell",
                                    "html","icon","idl","inform","informix-4gl","io","java","jade","javascript","jscript","julia","korn shell","kotlin","labview","ladder logic","lingo","lisp"
                                    ,"logo","lotusscript","lpc","lua","lustre","magic","mantis","mathematica","matlab","mercury","ml","monkry","moo","mumps",
                                    "objective-c","ocaml","occam","ooc","opa","opencl","perl","php","pilot","sql","postscript","powerscript","powershell","puppet","python","q","r","rexx","ruby","ruby on rails"
                                    ,"rust","s","s-plus","sas","scala","scilab","sed","self","shell","signal","simula","simulink","smalltalk","smarty","spark","spss","sqr","swift","tacl","tcl","tom","transact-sql"
                                    ,"typescript","vb.net","vba","vbscript","verilog","vhdl","visual basic 6","xen","xquery","xslt"]
        

        languages_found={}
        if uid not in df.values:
            languages_found['uid']=uid
            for db_skill in job_info_skills:
                if db_skill in list_of_languages:
                    languages_found[db_skill]=1
            df.loc[len(df)]=languages_found

        return df



    def extract_platform(self,job_info_skills,uid,df):
        list_of_platforms=["amazon echo","android","apple watch","apple tv","arduino","aws","azure","drupal","esp8266","firebase","gaming console","google cloud platform","heroku","google home","ibm cloud","watson"
                                    ,"ios","linux","mac os","mainframe","predix","raspberry pi","salesforce","serverless","sharepoint","windows desktop","windows server","windows phone","wordpress"]
        

        platforms_found={}
        if uid not in df.values:
            platforms_found['uid']=uid
            for db_skill in job_info_skills:
                if db_skill in list_of_platforms:
                    platforms_found[db_skill]=1
            df.loc[len(df)]=platforms_found

        return df

    def extract_languages(self,job_info_skills,uid,df):
        list_of_frameworks=[".net core","agile","angular","asp.net mvc","aura","aurelia","bottle","cakephp","cassandra","catalyst","cloudera","codeigniter","cordova","couchdb","cuba",
                                "django","dojo","dropwizard","durandal","elm","ember.js","express","flask","flatiron","flex","flink","google web toolkit","grails","hadoop","halcyon","hive","hpcc",
                                "jsf","koa","laravel","lift","lithium","map reduce","mason","meteor","moustache","ninja","nitro","node.js","pentaho","phoenix","play","polymer","pyramid",
                                "rapidminer","react","revel","riot.js","ruby on rails","rum","simplex","sinatra","solar","spark","spring","storm","struts","symfony","tapestry","tensorflow","pytorch"
                                ,"tornado","vaadin","vanilla","vert.x","vue.js","web2py","wicket","xamarin","yarn","yii","zend","zope"]
        

        frameworks_found={}
        if uid not in df.values:
            frameworks_found['uid']=uid
            for db_skill in job_info_skills:
                if db_skill in list_of_frameworks:
                    frameworks_found[db_skill]=1
            df.loc[len(df)]=frameworks_found

        return df

    def format_description(self,sentence:str): 
            # Split the sentence into individual words 
            
            stop_words = set(stopwords.words('english')) 
            words = sentence.split() 
                
            # Use a list comprehension to remove stop words 
            filtered_words = [word for word in words if word not in stop_words] 
                
            # Join the filtered words back into a sentence 
            return ' '.join(filtered_words)


    def parse_experience(self,description:str):
        
        years_of_experience="0"
        for sent in sent_tokenize(description):
            if "experience" in sent:
                if(len(re.findall("[0-9]|[0-9][0-9]",sent))>0):
                    experience= [int(yr) for yr in re.findall("[0-9]|[0-9][0-9]",sent) ]
                    years_of_experience= f"{min(experience)} - {max(experience)} years"

                break
                


        return years_of_experience

if __name__ =="__main__":
    #link="https://ca.indeed.com/"
    look_for_job=scrapejob("indeed") 
    look_for_job.connect()
    look_for_job.search_job("software engineer")
    look_for_job.scrape_job_data()