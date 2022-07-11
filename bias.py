import os
import spacy
from sklearn.feature_extraction.text import CountVectorizer

CODE_PATH = os.getcwd()
REPO_PATH = '/'.join(CODE_PATH.split('/')[0:-1])
DATA_PATH = REPO_PATH + '/' + 'data'

folderdata = 'SBW'
filename = 'sbwce.clean.sample.txt'
fileprocessed = filename[0:-4] + '.processed' + filename[-4:]

#Load the spacy model
nlp = spacy.load('es_core_news_sm', disable = ['parser','ner'])

with open(DATA_PATH + '/' + folderdata + '/' + filename, 'r') as file:
    with open(DATA_PATH + '/' + folderdata + '/' + fileprocessed, 'w') as newfile:
        for line in file:
            #Pass text to spacy and Do lowercase
            doc = nlp(line.lower())
            #Do lemmatization
            join = " ".join([token.lemma_ for token in doc])
            #Write to file "Processed"
            newfile.write(join)


vectorizer = CountVectorizer(decode_error='ignore',strip_accents='unicode',ngram_range=(1,3))
with open(DATA_PATH + '/' + folderdata + '/' + fileprocessed, 'r') as corpus:
    vectors = vectorizer.fit_transform(corpus)
        
#vectorizer.get_feature_names_out()
print(vectorizer.get_feature_names_out().shape)