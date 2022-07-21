from config import *
from collections import Counter
import spacy
import pandas as pd
from math import e
import unidecode
import string



def pwi_fuc(folder, data_list, text_column, label_column, positive_class, top_num=10):
    # Load Spacy Spanish model
    nlp = spacy.load('es_core_news_sm')
    merge_list = []

    print('\n############# ' + folder + ' #############')
    for dataset in data_list:
        # Load data
        sep = '\t' if '.tsv' in dataset else ','
        df = pd.read_csv(DATA_PATH + '/' + folder + '/' + dataset, sep=sep)
        merge_list.append(df)
        
        
        
    df = pd.concat(merge_list, ignore_index=True)
    df = df.loc[df['language']=='es'].copy() if 'language' in df.columns else df.copy()
        
    # pre-processing:
    # split string to a list
    df['text_processed'] = df[text_column].apply(lambda text: text.split())
    # lowercase
    df['text_processed'] = df['text_processed'].apply(lambda text: [token.lower() for token in text])
    # remove punctuation
    df['text_processed'] = df['text_processed'].apply(lambda text: [token.translate(str.maketrans('', '', string.punctuation + '¡¿')) for token in text])
    # remove accents
    df['text_processed'] = df['text_processed'].apply(lambda text: [unidecode.unidecode(token) for token in text])
    
    

        
    #split corpora positiva/negativa class
    df_positive_label = df.loc[df[label_column]==positive_class]
    df_negative_label = df.loc[~df.index.isin(df_positive_label.index)]
        
    print('Postive class: ')
    pwi_score(corpus_math(df_positive_label), corpus_math(df_negative_label), folder, df_positive_label[label_column].values[0], top_num)
    print('\nNegative class: ')
    pwi_score(corpus_math(df_negative_label), corpus_math(df_positive_label), folder, df_negative_label[label_column].values[0], top_num)


def pwi_score(dict_ref, dict_comp, folder, label, top_num):
    # caculate polarized weirdness index
    scores = [(item, dict_ref['word_freq'][item]/(dict_comp['word_freq'][item] + 0.01), dict_ref['word_freq'][item], dict_comp['word_freq'][item]) for item in dict_ref['unique_words']]
    
    #Save score to ".csv"
    df_top = pd.DataFrame(sorted(scores, reverse=True, key=lambda x: x[1]), columns=['word', 'pwi', 'freq_ref', 'preq_comp'])
    print(df_top.head(top_num))
    df_top.to_csv(PATH_RESULTS_BIAS + '/' + 'pwi_score_' + folder.lower() + '_' + str(label) + '.csv', index = False)
        


def corpus_math(df):
    corpora = [token for token_list in df['text_processed'].values.tolist() for token in token_list]
    word_counts = Counter(corpora)
    unique_words = list(set(word_counts))
            
    return {'word_freq':word_counts, 'unique_words':unique_words}
        


if __name__ == "__main__":
    
    pwi_fuc(folder_detoxis, 
            data_list=[file_detoxis_test, file_detoxis_train], 
            text_column=text_column_detoxis, 
            label_column=label_column_detoxis,
            positive_class=toxic_class)
    
    pwi_fuc(folder=folder_exist, 
            data_list=[file_exist_test,file_exist_train], 
            text_column=text_column_exist, 
            label_column=label_column_exist,
            positive_class=sexist_class)

    pwi_fuc(folder=folder_hateval,
            data_list=[file_hateval_test,file_hateval_train,file_hateval_dev], 
            text_column=text_column_hateval, 
            label_column=label_column_hateval,
            positive_class=hate_class)





















# from config import *
# from collections import Counter
# import spacy
# import pandas as pd
# from math import e
# import unidecode


# def pwi_fuc(folder, data_list, text_column, label_column, positive_class, top_num=10):
#     # Load Spacy Spanish model
#     nlp = spacy.load('es_core_news_sm')

#     print('\n#############' + folder + '#############')
#     for dataset in data_list:
        
#         # Load data
#         sep = '\t' if '.tsv' in dataset else ','
#         df = pd.read_csv(DATA_PATH + '/' + folder + '/' + dataset, sep=sep)
#         df = df.loc[df['language']=='es'].copy() if 'language' in df.columns else df.copy()
        
#         # pre-processing
#         df['text_processed'] = df[text_column].apply(lambda text: [token.text.lower() for token in nlp(text) if token.is_alpha
#                                                                                                                 and len(token.lemma_)>2])
#         # Caculate weirdness index
#         print('\nData: ' + dataset)
        
#         #split corpora positiva/negativa class
#         df_positive_label = df.loc[df[label_column]==positive_class]
#         df_negative_label = df.loc[~df.index.isin(df_positive_label.index)]
        
#         print('Postive class: ')
#         pwi_score(corpus_math(df_positive_label), corpus_math(df_negative_label), folder, dataset, df_positive_label[label_column].values[0], top_num)
#         print('\nNegative class: ')
#         pwi_score(corpus_math(df_negative_label), corpus_math(df_positive_label), folder, dataset, df_negative_label[label_column].values[0], top_num)


# def pwi_score(dict_ref, dict_comp, folder, dataset, label, top_num):
#     # caculate polarized weirdness index
#     scores = [(item, dict_ref['word_freq'][item]/(dict_comp['word_freq'][item] + 0.01), dict_ref['word_freq'][item], dict_comp['word_freq'][item]) for item in dict_ref['unique_words']]
    
#     #Save score to ".csv"
#     df_top = pd.DataFrame(sorted(scores, reverse=True, key=lambda x: x[1]), columns=['word', 'pwi', 'freq_ref', 'preq_comp'])
#     print(df_top.head(top_num))
#     data_type = 'test' if 'test' in dataset else 'train' if 'train' in dataset else 'dev'
#     df_top.to_csv(PATH_RESULTS_BIAS + '/' + 'pwi_score_' + folder.lower() + '_' + data_type + '_' + str(label) + '.csv', index = False)
        


# def corpus_math(df):
#     corpora = [unidecode.unidecode(token) for token_list in df['text_processed'].values.tolist() for token in token_list]
#     word_counts = Counter(corpora)
#     unique_words = list(set(word_counts))
            
#     return {'word_freq':word_counts, 'unique_words':unique_words}
        


# if __name__ == "__main__":
    
#     pwi_fuc(folder_detoxis, 
#             data_list=[file_detoxis_test, file_detoxis_train], 
#             text_column=text_column_detoxis, 
#             label_column=label_column_detoxis,
#             positive_class=toxic_class)
    
#     pwi_fuc(folder=folder_exist, 
#             data_list=[file_exist_test,file_exist_train], 
#             text_column=text_column_exist, 
#             label_column=label_column_exist,
#             positive_class=sexist_class)

#     pwi_fuc(folder=folder_hateval,
#             data_list=[file_hateval_test,file_hateval_train,file_hateval_dev], 
#             text_column=text_column_hateval, 
#             label_column=label_column_hateval,
#             positive_class=hate_class)