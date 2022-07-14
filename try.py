# # from cmath import inf
# import re
# import string
# import pandas as pd
# import spacy
# import nltk
# # nltk.download('stopwords')
# # nltk.download('punkt')
# from nltk.tokenize import word_tokenize
# from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures
# from nltk.corpus import stopwords
# from config import *

# def data_preprocess(df, text_column):
#     # Load Spacy Spanish model
#     nlp = spacy.load('es_core_news_sm', disable = ['parser','ner'])
    
#     # Do lowercase
#     df['text_processed'] = df[text_column].apply(lambda text: text.lower())
#     # Remove url
#     df['text_processed'] = df['text_processed'].apply(lambda text: re.sub(r'http\S+', '', text))
#     # Do Lemmatization and Spacy-Spanish preprocessing
#     df['text_processed'] = df['text_processed'].apply(lambda text: " ".join([token.lemma_ for token in nlp(text) if not token.is_punct
#                                                                                                                     and not token.is_currency
#                                                                                                                     and not token.is_digit
#                                                                                                                     and not token.is_stop
#                                                                                                                     and not token.like_num
#                                                                                                                     and not token.like_url]))
#     # Remove punctuation
#     df['text_processed'] = df['text_processed'].apply(lambda text: " ".join([char for char in word_tokenize(text) if char not in string.punctuation ]))
#     # Remove stopwords
#     df['text_processed'] = df['text_processed'].apply(lambda text: " ".join([word for word in word_tokenize(text) if not word in stopwords.words('spanish')]))
#     # df['text_processed'] = df['text_processed'].apply(lambda text: " ".join([word for word in word_tokenize(text) if len(word) > 2 and not word in stopwords.words('spanish')]))
#     # Remove numbers
#     df['text_processed'] = df['text_processed'].apply(lambda text: re.sub(r'\d+', '', text))
#     # Remove set of characters [-+/,_.]
#     df['text_processed'] = df['text_processed'].apply(lambda text: re.sub('[-+/,_.:"^]', '', text))
#     # Remove token that repeats more than 3 times
#     df['text_processed'] = df['text_processed'].apply(lambda text: re.sub(r'\b(\S)\1{3,}\S*\s?', '', text))
#     # remove token smaller than 3 characters and bigger than 32 characters
#     df['text_processed'] = df['text_processed'].apply(lambda text: " ".join([word for word in word_tokenize(text) if len(word) > 2 and len(word)<=28]))
#     # Replave multiple repited characters with 2 characters
#     df['text_processed'] = df['text_processed'].apply(lambda text: re.sub(r"(.)\1+", r"\1\1", text))

#     return [ word for phrase in df['text_processed'].values.tolist() for word in phrase.split()]


# def pms_top_2gram(folder, data_list, text_column, label_column, positive_class, top_num=20):
    
#     print('\n#############' + folder + '#############')
#     for dataset in data_list:
#         sep = '\t' if '.tsv' in dataset else ','
#         df = pd.read_csv(DATA_PATH + '/' + folder + '/' + dataset, sep=sep)
#         df = df.loc[(df['language']=='es') & (df[label_column]==positive_class)].copy() if 'language' in df.columns else df.loc[df[label_column]==positive_class].copy()

#         print('\nDataset: ' + dataset)
#         # print(df.head())
#         list_of_tokens = data_preprocess(df, text_column)
        
#         bigram_measures = BigramAssocMeasures()
#         finder = BigramCollocationFinder.from_words(list_of_tokens)

#         df_top = pd.DataFrame({"Top_2-grams": [ '_'.join(bigram) for bigram in finder.nbest(bigram_measures.pmi, top_num)]})
#         print(df_top)
#         data_kind = 'test' if 'test' in dataset else 'train' if 'train' in dataset else 'dev'
#         df_top.to_csv(PATH_RESULTS_BIAS + '/' + 'top_2-grams_' + folder.lower() + '_' + data_kind + '.csv', index = False)



# if __name__ == "__main__":
#     # DETOXIS pmi for top 2-grams
#     pms_top_2gram(folder=folder_detoxis, 
#                 data_list=[file_detoxis_test,file_detoxis_train], 
#                 text_column=text_column_detoxis, 
#                 label_column=label_column_detoxis,
#                 positive_class=toxic_class)

    # # EXIST pmi for top 2-grams
    # pms_top_2gram(folder=folder_exist, 
    #         data_list=[file_exist_test,file_exist_train], 
    #         text_column=text_column_exist, 
    #         label_column=label_column_exist,
    #         positive_class=sexist_class)

    # # HatEval pmi for top 2-grams
    # pms_top_2gram(folder=folder_hateval,
    #         data_list=[file_hateval_test,file_hateval_train,file_hateval_dev], 
    #         text_column=text_column_hateval, 
    #         label_column=label_column_hateval,
    #         positive_class=hate_class)