from database.pymysql_conn import DataBase
from find_features import WordFrequency

import pandas as pd
import numpy as np
import re
import nltk
import pickle

from collections import Counter
from pathlib import Path
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def has_game_name(gameName, top5words):
    comps = gameName.lower().split()
    words = top5words[gameName].keys().tolist()
    for comp in comps:
        if comp in words:
            return True


tfidf = TfidfVectorizer(stop_words=stopwords.words('english'), min_df=3)
for gameName, item in wf.games.items():
    texts.append(clean_text(item['text']))

matrix = tfidf.fit_transform(texts)

df = pd.DataFrame(columns=tfidf.get_feature_names())

for i in range(matrix.shape[0]):
    df.loc[i] = matrix.toarray()[i]

index = {}
for i, (gameName, item) in enumerate(wf.games.items()):
    index[i] = gameName

df.rename(index=index, inplace=True)
# df.to_csv("result.csv")

top5words = {}
for index, row in df.iterrows():
    top5words[index] = row.nlargest(5)
