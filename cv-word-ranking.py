import csv
from inspect import Attribute
from numpy import split
import numpy as np
import spacy
from nltk.corpus import stopwords
import uuid
import os
import json
import pandas as pd
import shutil
nlp = spacy.load('en_core_web_sm')
STOPWORDS = set(stopwords.words('english'))
csvfile = 'cv-content.csv'
SOURCE_DIR = '/home/iresha/Downloads/resume-screening-method/ROWDATA'
Categories = {
'Accounting-Auditing-Finance':['Accounting','Auditing','Finance'],
'Agriculture-Dairy-Environment':['Agriculture','Dairy','Environment'],
'Apparel-Clothing':['Apparel','Clothing'],
'Banking-Insurance':['Banking','Insurance'],
'Civil-Interior-Architecture':['Civil','Interior','Architecture'],
'Corporate Management-Analysts':['Corporate Management','Analysts'],
'Customer Relations-Public Relations':['Customer Relations','Public Relations'],
'Fashion-Beauty':['Fashion','Beauty'],
'Hospital-Nursing-Healthcare':['Hospital','Nursing','Healthcare'],
'Hospitality-Tourism':['Hospitality','Tourism'],
'Hotels-Restaurants-Food':['Hotels','Restaurants','Food'],
'HR-Training':['HR','Training'],
'Imports-Exports':['Imports','Exports'],
'International Development':['International' 'Development'],
'Hardware-Networks-Systems':['Hardware','Networks','Systems'],
'IT-Software-DB-QA-Web-Graphics-GIS':['IT','Software','DB','QA','Web','Graphics','GIS'],
'IT-Telecoms':['IT','Telecoms'],
'KPO-BPO':['KPO','BPO'],
'Legal-Law':['Legal','Law'],
'Logistics-Warehouse-Transport':['Logistics','Warehouse','Transport'],
'Manufacturing-Operations':['Manufacturing','Operations'],
'mechanical-Maintenance-Technician-Electrical-electrician-automation-automobile-pumbling':['mechanical','Maintenance','Technician','Electrical','electrician','automation','automobile','pumbling'],
'Media-Advert-Communication':['Media','Advert','Communication'],
'Office Admin-Secretary-Receptionist':['Office Admin','Secretary','Receptionist'],
'R&D-Science-Research':['R&D','Science','Research'],
'Sales-Marketing-Merchandising':['Sales','Marketing','Merchandising'],
'Security':['Security'],
'Sports-Fitness-Recreation':['Sports','Fitness','Recreation'],
'Supervision-Quality Control':['Supervision','Quality Control'],
'Teaching-Academic-Library':['Teaching','Academic','Library'],
'Ticketing-Airline-Marine':['Ticketing','Airline','Marine']
}
def cal(KEYWORD,token_array,index1):
     for index0,token0 in token_array.items():
          print([word for word in token0.replace('\'\'',',').split(',') if word in KEYWORD and index0!=index1]) 

def cv_processing():
     
     df = pd.read_csv('cv-keywords-TFIDF.csv')
     
     matrix2 = df[df.columns[0]]
     file_name = matrix2.tolist()
     
    
     x0 =df[df.columns[1]].tolist()
     print(len(x0))
     token_array=[]
     for x,y in df[df.columns[1]].items():
                    
          
          temp_array=''
          for index0,element in enumerate(y.replace('[','').replace(']','').split(',')):
               for index1,item in enumerate(element.replace('{','').replace('}','').split(':')):
                    if len(item)>1 and index1 ==1 and (index0%2==0 or index0==0):
                         if len([character for character in list(item.replace(" ","")) if character.isalpha()])>1:
                              temp_array+=item.replace(" ","")
          
          token_array.append({x:temp_array})

     KEYWORD1=[]
     index_array=[]
     
     for token1 in token_array: 
          for attribute1,value1 in token1.items():
               index_array.append(attribute1)
               KEYWORD1.append(value1.replace('\'\'',',').split(','))
   
     
     group=[]
     for index in range(0,(len(KEYWORD1)-1)):
          
          for cvcategory in Categories:
               temp=[]
               for keyword in Categories[cvcategory]:
                    
                    if keyword.lower() in KEYWORD1[index]:                         
                         temp.append(keyword)
               if len(temp)>1:
                    temp = []
                    temp.append(index)
                    group.append({cvcategory:temp})          
     for file in group:
          
          for attribute,value in file.items():
               selected_file = file_name[value[0]][:-3]+'.pdf'
               DEST_DIR = '/home/iresha/Downloads/resume-screening-method/ROW-CATERGORIES/'+attribute
               if not os.path.exists(DEST_DIR):
                    os.makedirs(DEST_DIR)
               for fname in os.listdir(SOURCE_DIR):
                    if fname.lower().endswith('.pdf') and fname==selected_file:
                         shutil.move(SOURCE_DIR+'/'+fname, DEST_DIR)         

cv_processing()


