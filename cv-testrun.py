import tabula
# import keywords file
import csv
import pathlib
import re
import uuid
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
import numpy as np
csvfile = 'cv-testrun.csv'

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    sorted_items = sorted_items[:topn]
    score_vals = []
    feature_vals = []
    

    for idx, score in sorted_items:

        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
def get_stop_words(stop_file_path):
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)
for i in range(1,50,1):
    file = '/home/iresha/Downloads/resume-screening-method/CVRowData/cv-'+str(i)+'.pdf'
    df_idf = tabula.io.read_pdf(file, pages='all')
    df_idf=str(df_idf).lower()
    df_idf=re.sub("","",df_idf)
    df_idf=re.sub("(\\d|\\W)+"," ",df_idf)
    # stopwords=get_stop_words("resources/stop_words_english.txt")
    docs=df_idf.split()
    docs=np.array(docs).tolist()
    cv=CountVectorizer(max_df=0.85,stop_words=STOPWORDS)
    word_count_vector=cv.fit_transform(docs)
    df_idf=list(cv.vocabulary_.keys())[:10]


    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)

    feature_names=cv.get_feature_names()
    tf_idf_vector=tfidf_transformer.transform(cv.transform(docs))
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    keywords=extract_topn_from_vector(feature_names,sorted_items,200)
    df_idf=keywords

    
    
    if os.stat(csvfile).st_size == 0:
        with open(csvfile, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["id", "file", "content"])
            writer.writerow([str(uuid.uuid4()), str(file.split('/').pop()),str(df_idf)]) 
    else:
        with open(csvfile, 'a+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([str(uuid.uuid4()), str(file.split('/').pop()),str(df_idf)])
            print(str(file.split('/').pop()))


