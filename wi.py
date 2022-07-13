from config import *
from collections import Counter
import spacy
import pandas as pd
from math import e

if __name__ == "__main__":
    
    folder_detoxis = 'DETOXIS'
    file_detoxis_test = 'DETOXIS2021_test_with_labels.csv'
    file_detoxis_train = 'DETOXIS2021_train.csv'
    text_column_detoxis = 'comment'
    
    def wi_fuc(folder, data_list, text_column, top_num=20):
        # Load Spacy Spanish model
        nlp = spacy.load('es_core_news_sm')
    
        print('\n#############' + folder + '#############')
        for dataset in data_list:
            
            sep = '\t' if '.tsv' in dataset else ','
            df = pd.read_csv(DATA_PATH + '/' + folder + '/' + dataset, sep=sep)
            df = df.loc[df['language']=='es'].copy() if 'language' in df.columns else df.copy()
            
            # pre-processing
            df['text_processed'] = df[text_column].apply(lambda text: [token.lemma_.lower() for token in nlp(text) if not token.is_stop 
                                                                                                                    and token.is_alpha
                                                                                                                    and len(token.lemma_)>2])
            
            
            print('Dataset: ' + dataset)
            # print(df.head())
            
            corpora = [token for token_list in df['text_processed'].values.tolist() for token in token_list]
            word_counts = Counter(corpora)
            total_words = sum(word_counts.values())
            # word_prob = [(item[0], word_counts[item[0]] / total_words) for item in word_counts.items()]
            unique_words = list(set(word_counts))
            
            square_weirdness = [(item, pow(word_counts[item]/total_words, 2) / e**nlp.vocab[item].prob) for item in unique_words]
    
            
            print([item[0] for item in sorted(square_weirdness, reverse=True, key=lambda x: x[1])][:15])
    
    
    wi_fuc(folder_detoxis, [file_detoxis_test, file_detoxis_train], text_column_detoxis)
            
            
            
            

# square_weirdness = [(item, pow(word_counts[item]/total_words, 2) / e**nlp.vocab[item].prob) for item in unique_words]