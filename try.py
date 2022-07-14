from config import *
from collections import Counter
import spacy
# from spacy.lookups import load_lookups
import pandas as pd
from math import e
import unidecode
import re

# accented_string = 'callate'
# # accented_string is of type 'unicode'
# import unidecode
# unaccented_string = unidecode.unidecode(accented_string)

# print(unaccented_string)

# nlp = spacy.load('es_core_news_sm')
# # Add Spacy lookup tables for scores
# lookups = load_lookups("es", ["lexeme_prob"])
# nlp.vocab.lookups.add_table("lexeme_prob", lookups.get_table("lexeme_prob"))


# for token in nlp("Yo tengo una propuesta aún mejor: deportarlos ya, empezando por los delincuentes y los menas. Y al que esté legal y sea delicuente multireincidente, quitarle la nacionalidad y prohibirle pisar España ni un fin de semana"):
#     if not token.is_stop and token.is_alpha and len(token.lemma_)>2:
#         print(token.text)


word_counts = Counter(['metoo','manspreading','mansplaining'])

print(word_counts)
print(word_counts['metoo'])
print(word_counts['Angel'])