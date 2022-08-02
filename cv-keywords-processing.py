import csv
import nltk
import math
import json 
nltk.download('punkt')
cvkeywordsIDF = 'cv-keywords-IDF.csv'
cvkeywordsTF = 'cv-keywords-TF.csv'
cvkeywordsTFIDF = 'cv-keywords-TFIDF.csv'

def update_file(data,filename):     
     with open(filename, 'w', newline='') as write_file:
          writer = csv.writer(write_file)
          if filename == 'cv-keywords-TFIDF.csv':
               writer.writerow(["file", "content"])
               for item in data:
                    writer.writerow([item[1]['word'],item[2:len(item)-1]]) 
          else:
               writer.writerow(data)
     write_file.close()

def calculate_tfidf(tf_data,idf_data):
     words_array_IDF = []
     value_array_IDF = []
     words_array_TF = []
     value_array_TF = []
     TFIDF = []
     for e in json.loads(idf_data):
          for attribute, value in e.items():
               if attribute =='word':
                    words_array_IDF.append(value)
               if attribute =='count':
                    value_array_IDF.append(value)
     for e in json.loads(tf_data):
          temp_words =[]
          temp_value =[]
          for tf in e:
               for attribute, value in tf.items():
                    if attribute =='word':
                         temp_words.append(value)
                    if attribute =='count':
                         temp_value.append(value)
          words_array_TF.append(temp_words)   
          value_array_TF.append(temp_value)

     for index0,element0 in enumerate(words_array_TF):
          temp = []
          for index1,element1 in enumerate(element0):
               x = [index for index,word in enumerate(words_array_IDF) if element1 == word]
               if len(x)==1:
                    tfidf = float(value_array_IDF[x[0]])*float(value_array_TF[index0][index1])
                    temp.append({'word':element1,'tfidf':tfidf})
          TFIDF.append(temp)
     update_file(TFIDF,cvkeywordsTFIDF)

def calculate_idf(tf_data):
     content=[]
     with open('cv-content2.csv', 'r') as file:
          reader = csv.reader(file)
          for row in reader:
               for i in row:
                    content.append([i][0].split(','))  
     
     with open('cv-content2.csv', 'r') as file:
          reader = csv.reader(file)
          num_of_documents = 0
          unique_words = []
          for row in reader:
               num_of_documents = len(row)
               text_new= []
               text_new1= []
               
               for i in range(len(row)):
                    tokens = row[i]                    
                    for w in tokens.split(','):
                         if (tokens.count(w)>=1 and (w not in unique_words)):
                              unique_words.append(w)     
          for w in unique_words:
               temp_array=[]
               for index,document in enumerate(content):
                    if w in document:
                         temp_array.append(index)
               text_new1.append({'word':w,'count':len(temp_array)})
          
          for item in text_new1:
               idf = math.log(num_of_documents/item['count'])
               item['count'] = str(idf)
          update_file(text_new1,cvkeywordsIDF)
          calculate_tfidf(tf_data,json.dumps(text_new1))

def calculate_tf():
     with open('cv-content2.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
          text_new= []
          for i in range(len(row)):
               tokens = row[i]         
               temp_array={}
               for w in tokens.split(','):
                    try:
                         temp_array[w].add(i)
                    except:
                         temp_array[w] = {i}
               text_new.append(temp_array)
          for temparray in text_new:
               for i in temparray:
                    
                    tf = len(temparray[i])/len(temparray)
                    temparray[i] = tf
          tf_array = []
          for temparray1 in text_new:
               temp = []
               for i in temparray1:
                    temp.append({'word':i,'count':str(temparray1[i])})
               tf_array.append(temp)          
          update_file(tf_array,cvkeywordsTF)
          calculate_idf(json.dumps(tf_array))


         


calculate_tf()

