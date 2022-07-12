import os

CODE_PATH = os.getcwd()
REPO_PATH = '/'.join(CODE_PATH.split('/')[0:-1])
DATA_PATH = REPO_PATH + '/' + 'data'
PATH_RESULTS = REPO_PATH + '/' + 'results'
PATH_RESULTS_BIAS = PATH_RESULTS + '/' + 'bias_analyses'