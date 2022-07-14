from config import *
from collections import Counter
import spacy
from spacy.lookups import load_lookups
import pandas as pd
from math import e
import unidecode


def wi_fuc(folder, data_list, text_column, top_num=20):
    # Load Spacy Spanish model
    nlp = spacy.load('es_core_news_sm')
    # Add/load Spacy lookup tables for scores
    lookups = load_lookups("es", ["lexeme_prob"])
    nlp.vocab.lookups.add_table("lexeme_prob", lookups.get_table("lexeme_prob"))

    print('\n#############' + folder + '#############')
    for dataset in data_list:
        
        # Load data
        sep = '\t' if '.tsv' in dataset else ','
        df = pd.read_csv(DATA_PATH + '/' + folder + '/' + dataset, sep=sep)
        df = df.loc[df['language']=='es'].copy() if 'language' in df.columns else df.copy()
        
        # pre-processing
        df['text_processed'] = df[text_column].apply(lambda text: [token.text.lower() for token in nlp(text) if token.is_alpha
                                                                                                                and len(token.lemma_)>2])
        
        # Caculate weirdness index
        print('\nData: ' + dataset)
        
        # create a list of all the words in the text + remove accents
        corpora = [unidecode.unidecode(token) for token_list in df['text_processed'].values.tolist() for token in token_list]
        word_counts = Counter(corpora)
        total_words = sum(word_counts.values())
        unique_words = list(set(word_counts))
        square_weirdness = [(item, pow(word_counts[item]/total_words, 2) / e**nlp.vocab[item].prob, pow(word_counts[item]/total_words, 2), e**nlp.vocab[item].prob) for item in unique_words]
        
        #Save weirdness index ".csv"
        df_top = pd.DataFrame(sorted(square_weirdness, reverse=True, key=lambda x: x[1]), columns=['word', 'wi', 'prob_' + folder, 'prob_corpus'])
        
        print(df_top.head(top_num))
        data_type = 'test' if 'test' in dataset else 'train' if 'train' in dataset else 'dev'
        df_top.to_csv(PATH_RESULTS_BIAS + '/' + 'wi_score_' + folder.lower() + '_' + data_type + '.csv', index = False)
        


if __name__ == "__main__":
    
    # DETOXIS weirdness index
    wi_fuc(folder_detoxis, [file_detoxis_test, file_detoxis_train], text_column_detoxis)
    
    
    # EXIST weirdness index
    wi_fuc(folder_exist, [file_exist_test, file_exist_train], text_column_exist)
    
    
    # HatEval weirdness index
    wi_fuc(folder_hateval, [file_hateval_test, file_hateval_train, file_hateval_dev], text_column_hateval)