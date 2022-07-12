import nltk
nltk.download('genesis')
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
fourgram_measures = nltk.collocations.QuadgramAssocMeasures()
finder = BigramCollocationFinder.from_words(nltk.corpus.genesis.words('english-web.txt'))

print(nltk.corpus.genesis.words('english-web.txt'))

# print(finder.nbest(bigram_measures.pmi, 10))