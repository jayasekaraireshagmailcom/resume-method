import np
import csv
from nltk import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
import num2words
csvfile = 'vac-content.csv'
output_file= 'vac-content2.csv'

STOPWORDS = set(stopwords.words('english'))

# def convert_numbers(data):
#      for index, item in enumerate(data):
#           for word in item.split(','):
#                try:
#                     if word.isdigit()==True:
#                          item = item.replace(word,'')
#                     else:
#                          item = item.replace(word,num2words.num2words(word))
#                except Exception as Argument: 
#                     f = open("log.txt", "a")
#                     f.write(str(Argument))
#                     f.close()
#           data[index]=item
#      return data
def lemmatisation(data):
     lemmatizer = WordNetLemmatizer()
     for index, item in enumerate(data):
          text_new = item     
          for word in item.split(','):
               text_new = text_new.replace(word,lemmatizer.lemmatize(word))
          data[index]=text_new
     return data


def stemming(data):
     stemmer = PorterStemmer()
     for index, item in enumerate(data):
          text_new = item     
          for word in item.split(','):
               text_new = text_new.replace(word,stemmer.stem(word))
          data[index]=text_new
     return data


def remove_stop_words(data):
     for index, item in enumerate(data):
          text_new=''
          for word in item.split(','):
               if word not in STOPWORDS:
                    text_new+=','+word
          data[index]=text_new
     return data


def remove_numbers(data):
     for index, item in enumerate(data):
          ''.join([i for i in item.split(',') if not i.isdigit()])
          # remove_empty_space=''
          # for word in remove_numbers.split(','):
          #      if bool(word and word.strip()):
          #           remove_empty_space+=','+word.strip()
          data[index]=item
     return data


def remove_single_characters(data):     
     for index, item in enumerate(data):
          text_new=''
          for index1,word in enumerate(item.split(',')):
               if len(word.strip()) >1:
                    if index1 == 0:
                         text_new+=word  
                    else:
                         text_new+=','+word
          data[index]=text_new 
     return data


def remove_apostrophe(data):
     text_new = np.char.replace(data, "'", "")
     return text_new.tolist()


def remove_punctuation(data):
     symbols = "!\"#$%&()*+./:;<=>?@[\]^_`{|}~\n"  
     text_new = [''.join(letter for letter in word if letter not in symbols) for word in data if word]     
     return text_new
          

def convert_lower_case(data): 
     for index, item in enumerate(data):
          data[index] = item.lower()
          # data[index] = re.sub("(\\d|\\W)+"," ",item)
          # print(data[index]) 
     return data             

def update_file(data):
          with open(output_file, 'w', newline='') as write_file:
               writer = csv.writer(write_file) 
               writer.writerow(data)
          write_file.close()

def preprocess(data):
     data=convert_lower_case(data)
     data=remove_punctuation(data)
     data=remove_apostrophe(data)
     data=remove_single_characters(data)
     data=remove_numbers(data)
     data=remove_stop_words(data)
     # data = stemming(data)
     data = lemmatisation(data)
     data = remove_punctuation(data)
     data = remove_numbers(data)

     update_file(data)

         
def read_file():  
     text_new= []
     with open(csvfile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
             text_new.append(row[1]+','+row[2])
        preprocess(text_new)
     file.close()
read_file()