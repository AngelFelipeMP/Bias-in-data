# import os
from cmath import inf
import re
import string
import pandas as pd
import spacy
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures
from nltk.corpus import stopwords
from config import *

# Data
folder_detoxis = 'DETOXIS'
file_detoxis_test = 'DETOXIS2021_test_with_labels.csv'
file_detoxis_train = 'DETOXIS2021_train.csv'
text_column_detoxis = 'comment'

folder_exist = 'EXIST'
file_exist_test = 'EXIST2021_test_with_labeled.tsv'
file_exist_train = 'EXIST2021_training.tsv'
text_column_exist = 'text'

folder_hateval = 'HatEval'
file_hateval_test = 'hateval2019_es_test.csv'
file_hateval_train = 'hateval2019_es_train.csv'
file_hateval_dev = 'hateval2019_es_dev.csv'
text_column_hateval = 'text'

def data_preprocess(df, text_column):
    # Load Spacy Spanish model
    nlp = spacy.load('es_core_news_sm', disable = ['parser','ner'])
    
    # Do lowercase
    df['text_processed'] = df[text_column].apply(lambda text: text.lower())
    # Do Lemmatization and Spacy-Spanish preprocessing
    df['text_processed'] = df['text_processed'].apply(lambda text: " ".join([token.lemma_ for token in nlp(text) if not token.is_punct
                                                                                                                    and not token.is_currency
                                                                                                                    and not token.is_digit
                                                                                                                    and not token.is_stop
                                                                                                                    and not token.like_num]))
    # Remove punctuation
    df['text_processed'] = df['text_processed'].apply(lambda text: " ".join([char for char in word_tokenize(text) if char not in string.punctuation ]))
    # Remove stopwords
    df['text_processed'] = df['text_processed'].apply(lambda text: " ".join([word for word in word_tokenize(text) if len(word) > 2 and not word in stopwords.words('spanish')]))
    # Remove numbers
    df['text_processed'] = df['text_processed'].apply(lambda text: re.sub(r'\d+', '', text))

    return [ word for phrase in df['text_processed'].values.tolist() for word in phrase.split()]


def pms_top_2gram(folder=str(), data_list=list(), text_column=str(), top_num=20):
    
    for dataset in data_list:
        sep = '\t' if '.tsv' in dataset else ','
        df = pd.read_csv(DATA_PATH + '/' + folder + '/' + dataset, sep=sep)
        print(df.head())
        list_of_tokens = data_preprocess(df, text_column)
        
        bigram_measures = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(list_of_tokens)
        # print(list(finder.nbest(bigram_measures.pmi, 20)))
        
        df_top = pd.DataFrame({"Top_2-grams":list(finder.nbest(bigram_measures.pmi, top_num))})
        data_kind = 'test' if 'test' in dataset else 'train' if 'train' in dataset else 'dev'
        df_top.to_csv(PATH_RESULTS_BIAS + '/' + 'top_2-grams_' + folder.lower() + '_' + data_kind + '.csv', index = False)


# pms_top_2gram(folder=folder_detoxis, data_list=[file_detoxis_test,file_detoxis_train], text_column=text_column_detoxis)
# pms_top_2gram(folder=folder_exist, data_list=[file_exist_test,file_exist_train], text_column=text_column_exist)
# pms_top_2gram(folder=folder_hateval, data_list=[file_hateval_test,file_hateval_train,file_hateval_dev], text_column=text_column_hateval)