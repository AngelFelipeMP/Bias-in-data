from config import *
from collections import Counter
import pandas as pd
from math import e
import unidecode
import string

class Pointwise_Mutual_Information():
    def __init__(self, folder, data_list, text_column, label_column, positive_class, top_num=20):
        self.folder = folder
        self.data_list = data_list
        self.text_column = text_column
        self.label_column = label_column
        self.positive_class = positive_class
        self.top_num = top_num
        self.run()
        
    def run(self):
        print('\n############# ' + self.folder + ' #############')
        self.load_data()
        self.preprocessing()
        self.split_data()
    
        print('Postive class: ')
        self.pwi(self.corpus_math(self.df_positive_label), self.corpus_math(self.df_negative_label), self.df_positive_label[self.label_column].values[0])
        print('\nNegative class: ')
        self.pwi(self.corpus_math(self.df_negative_label), self.corpus_math(self.df_positive_label), self.df_negative_label[self.label_column].values[0])
    
    def load_data(self):
        merge_list = []
        for dataset in self.data_list:
            # Load data
            sep = '\t' if '.tsv' in dataset else ','
            df = pd.read_csv(DATA_PATH + '/' + self.folder + '/' + dataset, sep=sep)
            merge_list.append(df)
            
        df = pd.concat(merge_list, ignore_index=True)
        self.df = df.loc[df['language']=='es'].copy() if 'language' in df.columns else df.copy()
    
    def preprocessing(self):
        # split string to a list
        self.df['text_processed'] = self.df[self.text_column].apply(lambda text: text.split())
        # lowercase
        self.df['text_processed'] = self.df['text_processed'].apply(lambda text: [token.lower() for token in text])
        # remove punctuation and expecial caracters apart from "@#"
        self.df['text_processed'] = self.df['text_processed'].apply(lambda text: [token.strip(string.punctuation.strip('@#') + '¡¿*”“') for token in text])
        # remove accents
        self.df['text_processed'] = self.df['text_processed'].apply(lambda text: [unidecode.unidecode(token) for token in text])
        
    def split_data(self):
        #split corpora positiva/negativa class
        self.df_positive_label = self.df.loc[self.df[self.label_column]==self.positive_class]
        self.df_negative_label = self.df.loc[~self.df.index.isin(self.df_positive_label.index)]
        
    def pwi(self, dict_ref, dict_comp, label):
        # caculate polarized weirdness index
        scores = [(item, dict_ref['word_freq'][item]/(dict_comp['word_freq'][item] + 0.01), dict_ref['word_freq'][item], dict_comp['word_freq'][item]) for item in dict_ref['unique_words']]
        
        #Save score to ".csv"
        df_pwd = pd.DataFrame(sorted(scores, reverse=True, key=lambda x: x[1]), columns=['word', 'pwi', 'freq_ref', 'preq_comp'])
        print(df_pwd.head(self.top_num))
        df_pwd = self.join_msg(df_pwd, label)
        df_pwd.to_csv(PATH_RESULTS_BIAS + '/' + 'pwi_score_' + self.folder.lower() + '_' + str(label) + '.csv', index = False)
        
    def corpus_math(self, df):
        corpora = [token for token_list in df['text_processed'].values.tolist() for token in token_list]
        word_counts = Counter(corpora)
        unique_words = list(set(word_counts))
                
        return {'word_freq':word_counts, 'unique_words':unique_words}
    
    def join_msg(self, df, label):
        msgs = [(token_list[0],token_list[1]) for token_list in self.df.loc[self.df[self.label_column]==label,[self.text_column, 'text_processed']].values.tolist()]
        # df['msg'] = df.loc[:self.top_num]['word'].apply(lambda x: [ tuple_[0] for tuple_ in msg if x in tuple_[1] ])
        df['msg'] = df.loc[:self.top_num]['word'].apply(lambda x: [ string for string, list in msgs if x in list ])
        return df
    
if __name__ == "__main__":
    
    Pointwise_Mutual_Information(folder_detoxis, 
            data_list=[file_detoxis_test, file_detoxis_train], 
            text_column=text_column_detoxis, 
            label_column=label_column_detoxis,
            positive_class=toxic_class)
    
    Pointwise_Mutual_Information(folder=folder_exist, 
            data_list=[file_exist_test,file_exist_train], 
            text_column=text_column_exist, 
            label_column=label_column_exist,
            positive_class=sexist_class)

    Pointwise_Mutual_Information(folder=folder_hateval,
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