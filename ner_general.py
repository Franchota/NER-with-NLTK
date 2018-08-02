import os
import nltk
import string
import re
from nltk.corpus import stopwords
import pandas as pd
import urllib.request
import shutil
import tempfile
nltk.download('stopwords')
nltk.download('wordnet')
stopwords.words('spanish')

if 'alvaro_uribe_speeches_2007_2010.txt' not in os.listdir('./assets'):
  with urllib.request.urlopen('https://raw.githubusercontent.com/rrodrigue2498/NER-with-NLTK/master/assets/alvaro_uribe_speeches_2007_2010.txt') as response:
    with open('./assets/alvaro_uribe_speeches_2007_2010.txt','w') as textos:
      shutil.copyfileobj(response, textos)

if 'nombres.txt' not in os.listdir('./assets'):
  with urllib.request.urlopen('https://raw.githubusercontent.com/rrodrigue2498/NER-with-NLTK/master/assets/nombres.txt') as response:
    with open('./assets/nombres.txt','w') as nombres:
      shutil.copyfileobj(response, nombres)


data = pd.read_csv('./assets/nombres.txt', sep='\t', header = None)
data.columns = ['body_text']
data.head()
# Opens previously imported file from local machine and prints its content
rawData = open('./assets/alvaro_uribe_speeches_2007_2010.txt').read()
#print (rawData[0:500])

#Eliminates empty spaces and prints list items in new lines
parsedData = rawData.replace('\t', '\n').split('\n')
parsedData[0:500]


def remove_punct(text):
  sp_characters = string.punctuation + "¡¿"
  text_nopunct = ''.join([char for char in text if char not in string.punctuation])
  return text_nopunct

data["body_text_clean"] = data['body_text'].apply(lambda x: remove_punct(x))
data.head()

#def cleaning(text):
  #result = filter(None, text)
  #return result

#data["body_text_complete"] = data["body_text_clean"].apply(lambda x: cleaning (x))

def tokenize(text):
  tokens = re.split('\s+', text)
  return tokens

# [a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]

data["body_text_tokenized"] = data["body_text_clean"].apply(lambda x: tokenize (x))

stopword = nltk.corpus.stopwords.words('spanish')
def remove_stopwords(tokenized_list):
  text = [word for word in tokenized_list if word not in stopword]
  return text

data['body_text_nostop'] = data['body_text_tokenized'].apply(lambda x: remove_stopwords(x))

data[0:50]

print(string.punctuation)
sp_characters = string.punctuation + "“¡¿"
print(sp_characters)

word_inlist = data['body_text_tokenized']

' ' in word_inlist[17:]

print(word_inlist[16])
print(word_inlist[2])
print(len(word_inlist[16]))
print(enumerate(word_inlist[16]))
#print(word_inlist[0:40])

print(len(word_inlist))

print(word_inlist[22320])

#len(word_inlist[22320]) > 1

word_inlist = data['body_text_nostop']
sp_names = open('./assets/nombres.txt').read()
name_list = []

for line in word_inlist:
  
  if len(line) > 1 :
    #print(len(line))
    
    for char, elem in enumerate(line):
      #print(line[char][0])
      
        try:
          
            if elem == '':
              continue
            
            if elem[0].isupper() and elem in sp_names:
              nextelem = line[(char + 1) % len(line)]

              if nextelem[0].isupper() and nextelem in sp_names:
                secelem = line[(char + 2) % len(line)]
                
                if not secelem[0].isupper():
                  name_list.append(line[char:char+2])

                if secelem[0].isupper() and secelem in sp_names:
                  thirdelem = line[(char + 3) % len(line)]
                  
                  if not thirdelem[0].isupper():
                      name_list.append(line[char:char+3])

                  if thirdelem[0].isupper() and thirdelem in sp_names:
                      name_list.append(line[char:char+4])
                      #print(name_list)
                      #print(name_list)

                

                  
        except:
            continue
            #print('error: ', elem)
            
#fixed_list = " ".join(name_list).split()
for sublst in name_list:
              for item in sublst:
                print(item,)        # note the ending ','

for sublst in name_list:
  for item in sublst:
    print(item,)        # note the ending ','

