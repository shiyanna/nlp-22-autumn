import os
import re
import pickle
import pandas as pd
from math import log10

with open("../../assets/df_cropped_dictionary", "rb") as file:
    dictionary = pickle.load(file)

#  добавить функцию для ввода произвольного текста
data_path = '../../assets/annotated-corpus/test'
sentence_list = []
with open(data_path + '/comp.graphics/38758.tsv') as file:
    sentence = []
    for line in file:
        if line != '\n':
            token = re.split(r'\t', line)[0]
            # punctuation cleaner
            if re.fullmatch(r'[\'!()\\\-\[\]{};@?<>:\",./^&*_|+`%#=~]+', token):
                continue
            sentence.append(token)
        elif line == '\n':
            if sentence:
                sentence_list.append(sentence)
            sentence = []
print(sentence_list)

# Матрица частот
freq_df = pd.DataFrame(columns=dictionary.keys())
for sentence in sentence_list:
    # из term-document matrix - найти и добавить dfs в словарь
    # из словаря - брать dfs
    str_sentence = ""
    for token in sentence:
        str_sentence += ' ' + token
    str_sentence = str_sentence[1:]
    freq_df.loc[str_sentence] = 0
    for token in sentence:
        try:
            freq_df.at[str_sentence, token] += 1
        except:
            pass
freq_df.to_csv('../../assets/freq_matrix')
freq_df = pd.read_csv('../../assets/freq_matrix')
print(freq_df)

# Матрица tf-idf  (как считать? что tf, что df? для чего нужен общий tf в словаре?)
tf_idf_df = pd.read_csv('../../assets/freq_matrix')
with open("../../assets/token_list_by_file", "rb") as file:
    token_list_by_file = pickle.load(file)
N = len(token_list_by_file) # общее число документов в train
del token_list_by_file
for index, row in tf_idf_df.iterrows():
    for token in dictionary:
        # print(row[token], log10((N + 1)/(dictionary[token][1] + 1)))
        tf_idf_df.at[index, token] = row[token] * log10((N + 1)/(dictionary[token][1] + 1))
print(tf_idf_df)
tf_idf_df.to_csv('../../assets/tf_idf_matrix')
tf_idf_df = pd.read_csv('../../assets/tf_idf_matrix')
vectorized_doc = []

for token in dictionary:
    vectorized_doc.append(round(tf_idf_df[token].mean(), 3))

for index, value in enumerate(vectorized_doc):
    if value > 0:
        print(index, value)