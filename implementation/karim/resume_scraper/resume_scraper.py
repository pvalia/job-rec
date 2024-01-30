import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import ngrams
from pathlib import Path
import uuid
#language worth with , database worked with , platform worked with, franework worked with, domain -> devType

class scrape_resume:
    def __init__(self,mediatype:str="csv",survey_results_flag:bool=False):
        """
            mediatype: whether resume data is in csv,pdf, or word 
        """
        self.media=mediatype
        self.survey=survey_results_flag
        self.resume_path=Path(r"C:\Users\karim\OneDrive\Desktop\capstone\resume_scraper\survey_results_public.csv")
       
    def start(self):


        databases_profile_resume_df=pd.DataFrame(columns=["uid","amazon dynamodb","amazon rds/aurora","amazon redshift","apache hbase","apache hive","aster data","cassandra","elasticsearch", "filemaker pro","firebird","google bigquery",
        "google cloud storage","greenplum","hsqldb","ibm db2","informix","mariadb", "memcached","memsql","microsoft access","microsoft azure (tables, cosmosdb, sql, etc)","microsoft azure"
        "mongodb","msql","mysql","neo4j","netezza","oracle","panorama","postgresql","redis","sap hana","sql server","sqlite","teradata","timesten","unidata","universe","vertica"])
        domain_resume_profile_df=pd.DataFrame(columns=["uid","back end","c-suite executive","cloud computing","data Scientist","data or business analyst","business analyst","data analyst","database administrator(dba)","database administrator"
                 ,"designer","devops","academic researcher","educator","embedded applications","embedded devices developer","engineering manager","enterprise application","front end"
                 ,"full stack","game developer","Information Security","Mobile developer","Network engineer","product manager","Qa","Test developer","Sales professional","software developer","java developer"
                 ,"sudent","system administrator","web developer"])
        frameworks_profile_resume=pd.DataFrame(columns=["uid",".net core","agile","angular","asp.net mvc","aura","aurelia","bottle","cakephp","cassandra","catalyst","cloudera","codeigniter","cordova","couchdb","cuba",
                                "django","dojo","dropwizard","durandal","elm","ember.js","express","flask","flatiron","flex","flink","google web toolkit","grails","hadoop","halcyon","hive","hpcc",
                                "jsf","koa","laravel","lift","lithium","map reduce","mason","meteor","moustache","ninja","nitro","node.js","pentaho","phoenix","play","polymer","pyramid",
                                "rapidminer","react","revel","riot.js","ruby on rails","rum","simplex","sinatra","solar","spark","spring","storm","struts","symfony","tapestry","tensorflow","pytorch"
                                ,"tornado","vaadin","vanilla","vert.x","vue.js","web2py","wicket","xamarin","yarn","yii","zend","zope"])
        languages_profile_resume=pd.DataFrame(columns=["uid",".net","abap","abc","actionscript","ada","ajax","apex","apl","applescript","arc","arduino","asp","assembly","atlas","automator","avenue","awk","bash","bc","bourne shell","bro"
                            ,"c","c shell","c#","c++","caml","ceylon","cfml","ch","clarion","clean","clojure","cobol","cobra","coffeescript","coldfusion","css","ct","d","dart"
                            ,"dcl","pascal","e","ecl","ec","ecmascript","egl","elixir","erlang","f#","falcon","felix","forth","fortran","fortress","go","gosu","groovy","hack","haskell",
                            "html","icon","idl","inform","informix-4gl","io","java","jade","javascript","jscript","julia","korn shell","kotlin","labview","ladder logic","lingo","lisp"
                            ,"logo","lotusscript","lpc","lua","lustre","magic","mantis","mathematica","matlab","mercury","ml","monkry","moo","mumps",
                            "objective-c","ocaml","occam","ooc","opa","opencl","perl","php","pilot","sql","postscript","powerscript","powershell","puppet","python","q","r","rexx","ruby","ruby on rails"
                            ,"rust","s","s-plus","sas","scala","scilab","sed","self","shell","signal","simula","simulink","smalltalk","smarty","spark","spss","sqr","swift","tacl","tcl","tom","transact-sql"
                            ,"typescript","vb.net","vba","vbscript","verilog","vhdl","visual basic 6","xen","xquery","xslt"])
        platforms_profile_resume=pd.DataFrame(columns=["uid","amazon echo","android","apple watch","apple tv","arduino","aws","azure","drupal","esp8266","firebase","gaming console","google cloud platform","heroku","google home","ibm cloud","watson"
                            ,"ios","linux","mac os","mainframe","predix","raspberry pi","salesforce","serverless","sharepoint","windows desktop","windows server","windows phone","wordpress"])
        match self.media:
            case "csv":
                df_resume_data=pd.read_csv(self.resume_path)
                df_resume_data["Respondent"]=df_resume_data["Respondent"].apply(lambda x : uuid.uuid4().hex)
                df_resume_data.rename(columns={"Respondent": "uid"},inplace=True)
                df_resume_data = df_resume_data.fillna("NA")
                print(df_resume_data.head())
                
                databases_profile_resume_df=self.extract_databases(databases_profile_resume_df,survey_csv=df_resume_data)
                databases_profile_resume_df.to_csv("./resume_scraper/databases_resume.csv")
                frameworks_profile_resume=self.extract_frameworks(frameworks_profile_resume,survey_csv=df_resume_data)
                frameworks_profile_resume.to_csv("./resume_scraper/frameworks_profile_resume.csv")
                languages_profile_resume=self.extract_languages(languages_profile_resume,survey_csv=df_resume_data)
                languages_profile_resume.to_csv("./resume_scraper/languages_profile_resume.csv")
                platforms_profile_resume=self.extract_platform(platforms_profile_resume,survey_csv=df_resume_data)
                platforms_profile_resume.to_csv("./resume_scraper/platforms_profile_resume.csv")
                domain_resume_profile_df=self.extract_domains(domain_resume_profile_df,survey_csv=df_resume_data)
                domain_resume_profile_df.to_csv("./resume_scraper/domain_resume_profile.csv")
            case "pdf":
                pass
            case _ : 
                raise Exception("media type not supported")


        
       
        
        
        


    def set_path(self,path:str="./"):
        self.resume_path=Path(path)


    def extract_skills(self,df):
        
            
            list_of_databases=["amazon dynamodb","amazon rds/aurora","amazon redshift","apache hbase","apache hive","aster data","cassandra","elasticsearch", "filemaker pro","firebird","google bigquery",
            "google cloud storage","greenplum","hsqldb","ibm db2","informix","mariadb", "memcached","memsql","microsoft access","microsoft azure (tables, cosmosdb, sql, etc)","microsoft azure"
            "mongodb","msql","mysql","neo4j","netezza","oracle","panorama","postgresql","redis","sap hana","sql server","sqlite","teradata","timesten","unidata","universe","vertica"]           
            list_of_domains=["back end","c-suite executive","cloud computing","data Scientist","data or business analyst","business analyst","data analyst","database administrator(dba)","database administrator"
                 ,"designer","devops","academic researcher","educator","embedded applications","embedded devices developer","engineering manager","enterprise application","front end"
                 ,"full stack","game developer","Information Security","Mobile developer","Network engineer","product manager","Qa","Test developer","Sales professional","software developer","java developer"
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
            "mongodb","msql","mysql","neo4j","netezza","oracle","panorama","postgresql","redis","sap hana","sql server","sqlite","teradata","timesten","unidata","universe","vertica","back end","c-suite executive","cloud computing","data Scientist","data or business analyst","business analyst","data analyst","database administrator(dba)","database administrator"
                 ,"designer","devops","academic researcher","educator","embedded applications","embedded devices developer","engineering manager","enterprise application","front end"
                 ,"full stack","game developer","Information Security","Mobile developer","Network engineer","product manager","Qa","Test developer","Sales professional","software developer","java developer"
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
    

    def extract_databases(self,df,uid=None,job_info_skills=None,survey_csv=None):
        list_of_databases=["amazon dynamodb","amazon rds/aurora","amazon redshift","apache hbase","apache hive","aster data","cassandra","elasticsearch", "filemaker pro","firebird","google bigquery",
            "google cloud storage","greenplum","hsqldb","ibm db2","informix","mariadb", "memcached","memsql","microsoft access","microsoft azure","microsoft azure"
            "mongodb","msql","mysql","neo4j","netezza","oracle","panorama","postgresql","redis","sap hana","sql server","sqlite","teradata","timesten","unidata","universe","vertica"]
       
        if self.survey:
            row=0
            for uid,skills in zip(survey_csv['uid'].values,survey_csv['DatabaseWorkedWith'].values):
                row+=1
                if row == 1000:
                    break
                skills_found={}
                skills_found['uid']=uid
                print(skills.split(";"))
                if skills != "NA":
                    for skill in skills.split(";"):
                        skill=skill.lower()
                        if skill in list_of_databases:
                            print(skill)
                            
                            skills_found[skill]=1  
                                     
                df.loc[len(df)]=skills_found



        else:
            skills_found={}
            if uid not in df['uid'].values:
                skills_found['uid']=uid
                for db_skill in job_info_skills:
                    if db_skill in list_of_databases:
                        skills_found[db_skill]=1
                df.loc[len(df)]=skills_found

        return df
                

    def extract_domains(self,df,uid=None,job_info_skills=None,survey_csv=None):
        list_of_domains=["back end","c-suite executive","cloud computing","data Scientist","data or business analyst","business analyst","data analyst","database administrator(dba)","database administrator"
                 ,"designer","devops","academic researcher","educator","embedded applications","embedded devices developer","engineering manager","enterprise application","front end"
                 ,"full stack","game developer","Information Security","Mobile developer","Network engineer","product manager","Qa","Test developer","Sales professional","software developer","java developer"
                 ,"sudent","system administrator","web developer"]
        

        
        row=0
        if self.survey:
            for uid,skills in zip(survey_csv['uid'].values,survey_csv['DevType'].values):
                row+=1
                if row == 1000:
                    break
                skills_found={}
                skills_found['uid']=uid
                print(skills.split(";"))
                if skills != "NA":
                    for skill in skills.split(";"):
                        skill=skill.lower()
                        if skill in list_of_domains:
                            print(skill)
                            
                            skills_found[skill]=1  
                                     
                df.loc[len(df)]=skills_found
                

        else:
            domains_found={}
            if uid not in df.values:
                domains_found['uid']=uid
                for db_skill in job_info_skills:
                    if db_skill in list_of_domains:
                        domains_found[db_skill]=1
                
                df.loc[len(df)]=domains_found

        return df

    def extract_languages(self,df,uid=None,job_info_skills=None,survey_csv=None):
        list_of_languages=[".net","abap","abc","actionscript","ada","ajax","apex","apl","applescript","arc","arduino","asp","assembly","atlas","automator","avenue","awk","bash","bc","bourne shell","bro"
                                    ,"c","c shell","c#","c++","caml","ceylon","cfml","ch","clarion","clean","clojure","cobol","cobra","coffeescript","coldfusion","css","ct","d","dart"
                                    ,"dcl","pascal","e","ecl","ec","ecmascript","egl","elixir","erlang","f#","falcon","felix","forth","fortran","fortress","go","gosu","groovy","hack","haskell",
                                    "html","icon","idl","inform","informix-4gl","io","java","jade","javascript","jscript","julia","korn shell","kotlin","labview","ladder logic","lingo","lisp"
                                    ,"logo","lotusscript","lpc","lua","lustre","magic","mantis","mathematica","matlab","mercury","ml","monkry","moo","mumps",
                                    "objective-c","ocaml","occam","ooc","opa","opencl","perl","php","pilot","sql","postscript","powerscript","powershell","puppet","python","q","r","rexx","ruby","ruby on rails"
                                    ,"rust","s","s-plus","sas","scala","scilab","sed","self","shell","signal","simula","simulink","smalltalk","smarty","spark","spss","sqr","swift","tacl","tcl","tom","transact-sql"
                                    ,"typescript","vb.net","vba","vbscript","verilog","vhdl","visual basic 6","xen","xquery","xslt","bash/shell"]
        

        
        row=0
        if self.survey:
            for uid,skills in zip(survey_csv['uid'].values,survey_csv['LanguageWorkedWith'].values):
                row+=1
                if row == 1000:
                    break
                skills_found={}
                skills_found['uid']=uid
                print(skills.split(";"))
                if skills != "NA":
                    for skill in skills.split(";"):
                        skill=skill.lower()
                        if skill in list_of_languages:
                            print(skill)
                            
                            skills_found[skill]=1  
                                     
                df.loc[len(df)]=skills_found
        else:
            language_found={}
            if uid not in df.values:
                language_found['uid']=uid
                for db_skill in job_info_skills:
                    
                    if db_skill in list_of_languages:
                        language_found[db_skill]=1
                df.loc[len(df)]=language_found

        return df



    def extract_platform(self,df,uid=None,job_info_skills=None,survey_csv=None):
        list_of_platforms=["amazon echo","android","apple watch","apple tv","arduino","aws","azure","drupal","esp8266","firebase","gaming console","google cloud platform","heroku","google home","ibm cloud","watson"
                                    ,"ios","linux","mac os","mainframe","predix","raspberry pi","salesforce","serverless","sharepoint","windows desktop","windows server","windows phone","wordpress"]
        

        row=0
        if self.survey:
            for uid,skills in zip(survey_csv['uid'].values,survey_csv['PlatformWorkedWith'].values):
                row+=1
                if row == 1000:
                    break
                skills_found={}
                skills_found['uid']=uid
                print(skills.split(";"))
                if skills != "NA":
                    for skill in skills.split(";"):
                        skill=skill.lower()
                        if skill in list_of_platforms:
                            print(skill)
                            
                            skills_found[skill]=1  
                                     
                df.loc[len(df)]=skills_found
        else:
            platforms_found={}
            if uid not in df.values:
                platforms_found['uid']=uid
                for db_skill in job_info_skills:
                    if db_skill in list_of_platforms:
                        platforms_found[db_skill]=1
                df.loc[len(df)]=platforms_found

        return df

    def extract_frameworks(self,df,uid=None,job_info_skills=None,survey_csv=None):
        list_of_frameworks=[".net core","agile","angular","asp.net mvc","aura","aurelia","bottle","cakephp","cassandra","catalyst","cloudera","codeigniter","cordova","couchdb","cuba",
                                "django","dojo","dropwizard","durandal","elm","ember.js","express","flask","flatiron","flex","flink","google web toolkit","grails","hadoop","halcyon","hive","hpcc",
                                "jsf","koa","laravel","lift","lithium","map reduce","mason","meteor","moustache","ninja","nitro","node.js","pentaho","phoenix","play","polymer","pyramid",
                                "rapidminer","react","revel","riot.js","ruby on rails","rum","simplex","sinatra","solar","spark","spring","storm","struts","symfony","tapestry","tensorflow","pytorch"
                                ,"tornado","vaadin","vanilla","vert.x","vue.js","web2py","wicket","xamarin","yarn","yii","zend","zope"]
        
        

        row = 0
        if self.survey:

            for uid,skills in zip(survey_csv['uid'].values,survey_csv['FrameworkWorkedWith'].values):
                row+=1
                if row == 1000:
                    break
                skills_found={}
                skills_found['uid']=uid
                print(skills.split(";"))
                if skills != "NA":
                    for skill in skills.split(";"):
                        skill=skill.lower()
                        if skill in list_of_frameworks:
                            print(skill)
                            
                            skills_found[skill]=1  
                                     
                df.loc[len(df)]=skills_found
        else:    
            frameworks_found={}
            if uid not in df.values:
                frameworks_found['uid']=uid
                for db_skill in job_info_skills:
                    if db_skill in list_of_frameworks:
                        frameworks_found[db_skill]=1
                df.loc[len(df)]=frameworks_found

        return df
    
    def set_new_media(self,mediatype:str):
        self.media=mediatype

    def set_survey_flag(self,flag:bool):
        self.survey=flag


if __name__ == "__main__":

    extract_resume=scrape_resume(survey_results_flag=True)
    extract_resume.start()