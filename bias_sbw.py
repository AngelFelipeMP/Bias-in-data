import os
import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer

CODE_PATH = os.getcwd()
REPO_PATH = '/'.join(CODE_PATH.split('/')[0:-1])
DATA_PATH = REPO_PATH + '/' + 'data'

# folder_sbw = 'SBW'
# file_sbw = 'sbwce.clean.sample.txt'
# file_processed = file_sbw[0:-4] + '.processed' + file_sbw[-4:]

# #Load the spacy model
# nlp = spacy.load('es_core_news_sm', disable = ['parser','ner'])

# with open(DATA_PATH + '/' + folder_sbw + '/' + file_sbw, 'r') as file:
#     with open(DATA_PATH + '/' + folder_sbw + '/' + file_processed, 'w') as newfile:
#         for line in file:
#             #Pass text to spacy and Do lowercase
#             doc = nlp(line.lower())
#             #Do lemmatization
#             join = " ".join([token.lemma_ for token in doc])
#             #Write to file "Processed"
#             newfile.write(join)


## Criate a CountVectorizer

# vectorizer = CountVectorizer(decode_error='ignore',strip_accents='unicode',ngram_range=(1,3))
# with open(DATA_PATH + '/' + folderdata + '/' + file_processed, 'r') as corpus:
#     vectors = vectorizer.fit_transform(corpus)
        
# #vectorizer.get_feature_names_out()
# print(vectorizer.get_feature_names_out().shape)


folder_exist = 'EXIST'
file_exist = 'EXIST2021_test_with_labeled.tsv'

df_exist = pd.read_csv(DATA_PATH + '/' + folder_exist + '/' + file_exist, sep='\t')
print(df_exist.head())

