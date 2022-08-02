from tqdm import tqdm
from itertools import islice
import csv
from re import sub
from sklearn.feature_extraction.text import CountVectorizer
from numpy import array, log
# from pytopicrank import TopicRank

num_lines = sum(1 for line in open("cv-content2.csv"))

with open("cv-content2.csv") as file:
     dict_idf = {}
     with tqdm(total=num_lines) as pbar:
          for i, line in tqdm(islice(enumerate(file), 1, None)):
               try: 
                    cells = line.split(",")
                    idf = float(sub("[^0-9.]", "", cells[3]))
                    dict_idf[cells[0]] = idf
               except: 
                    print("Error on: " + line)
               finally:
                    pbar.update(1)
content=[]
with open('cv-content2.csv', 'r') as file:
     reader = csv.reader(file)
     for row in reader:
          # for i in row:
          #      content.append([i][0].split(','))  
          vectorizer = CountVectorizer()
          tf = vectorizer.fit_transform([x.lower() for x in row])
          tf = tf.toarray()
          tf = log(tf + 1)
          tfidf = tf.copy()
          words = array(vectorizer.get_feature_names())
          for k in tqdm(dict_idf.keys()):
               if k in words:
                    tfidf[:, words == k] = tfidf[:, words == k] * dict_idf[k]
               pbar.update(1)
          for j in range(tfidf.shape[0]):
               print("Keywords of article", str(j+1), words[tfidf[j, :].argsort()[-5:][::-1]])
          # for j in range(len(content)):
          #      tr = TopicRank(content[j])
          #      print("Keywords of article", str(j+1), "\n", tr.get_top_n(n=5, extract_strategy='first'))
