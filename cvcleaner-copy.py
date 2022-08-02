# import keywords file
import csv
import pdfplumber
import pathlib
import docx2txt
import re
import spacy
from nltk.corpus import stopwords
import uuid
import os

nlp = spacy.load('en_core_web_sm')
STOPWORDS = set(stopwords.words('english'))
file = '/home/iresha/Downloads/resume-screening-method/CVRowData/cv-38.pdf'
file_extension = pathlib.Path(file).suffix

edu = {}

def store_csv(text):
    csvfile = 'cv-content.csv'
    if os.stat(csvfile).st_size == 0:
        with open(csvfile, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["id", "file", "content"])
            writer.writerow([str(uuid.uuid4()), str(file.split('/').pop()),str(text)]) 
    else:
        with open(csvfile, 'a+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([str(uuid.uuid4()), str(file.split('/').pop()),str(text)])
            print(str(file.split('/').pop()))

# Check file extention and extract the keywords          
if(file_extension == '.pdf'):
    with pdfplumber.open(file) as pdf:
       for page in pdf.pages:
            text = page.extract_text()
            nlp_text = nlp(text)

            
            nlp_text = [sent.text.strip() for sent in nlp_text.sents] 
            for index, text in enumerate(nlp_text):
                for tex in text.split():
                    tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                    # if tex in cvkeywordsarray and tex not in STOPWORDS:
                    #     edu[tex] = text + text[index+1]
                    if tex not in STOPWORDS:
                        if index in range(len(text)):
                            edu[tex] = text + text[index+1]
    store_csv(list(edu.keys()))
            
if(file_extension == '.docx'):
    content = docx2txt.process(file)
    nlp_text = nlp(content)
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex not in STOPWORDS:
                edu[tex] = text + text[index+1] 
    store_csv(list(edu.keys()))