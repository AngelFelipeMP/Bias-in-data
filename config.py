import os

CODE_PATH = os.getcwd()
REPO_PATH = '/'.join(CODE_PATH.split('/')[0:-1])
DATA_PATH = REPO_PATH + '/' + 'data'
PATH_RESULTS = REPO_PATH + '/' + 'results'
PATH_RESULTS_BIAS = PATH_RESULTS + '/' + 'bias_analyses'

# DETOXIS weirdness index
folder_detoxis = 'DETOXIS'
file_detoxis_test = 'DETOXIS2021_test_with_labels.csv'
file_detoxis_train = 'DETOXIS2021_train.csv'
text_column_detoxis = 'comment'
label_column_detoxis = 'toxicity'
toxic_class = 'toxic'

# EXIST weirdness index
folder_exist = 'EXIST'
file_exist_test = 'EXIST2021_test_with_labeled.tsv'
file_exist_train = 'EXIST2021_training.tsv'
text_column_exist = 'text'
label_column_exist = 'task1'
sexist_class = 'sexist'

# HatEval weirdness index
folder_hateval = 'HatEval'
file_hateval_test = 'hateval2019_es_test.csv'
file_hateval_train = 'hateval2019_es_train.csv'
file_hateval_dev = 'hateval2019_es_dev.csv'
text_column_hateval = 'text'
label_column_hateval = 'HS'
hate_class = 1

