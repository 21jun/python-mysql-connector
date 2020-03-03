from database.pymysql_conn import DataBase

import pandas as pd
import numpy as np
import re
import nltk
import pickle

from collections import Counter
from pathlib import Path
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def clean_text(text):
    text = text.lower()
    # replace special chars and keep spaces
    text = re.sub(r"[ ](?=[ ])|[^A-Za-z0-9 ]+", '', text)
    text = re.sub(' +', ' ', text)  # replace multiple spaces and keep one
    return text


class WordFrequency:

    def __init__(self):
        self.db = DataBase()
        self.SQL = \
            """
        SELECT appid, gameName, videoId, likeCount, replyCount, text FROM yt_comment_steam where language='en';
        """
        self.comments = self.db.to_df(self.SQL)
        self.games = {}
        self.gameNames = self.comments['gameName'].unique()
        self.appids = self.comments
        self.stop_words = stopwords.words('english')

        g = self.comments.groupby(['appid', 'gameName']).size().reset_index()
        appids, gameNames = g['appid'].tolist(), g['gameName'].tolist()

        for appid, gameName in zip(appids, gameNames):
            text = self.comments[self.comments['gameName'] == gameName]['text']
            text = text.tolist()
            text = [clean_text(t) for t in text]
            text = ' '.join(text)
            # print(appid)
            # print(text)
            self.games[gameName] = {'appid': appid, 'text': text}
        # for gameName in self.gameNames:
        #     text = self.comments[self.comments['gameName'] == gameName]['text']
        #     text = text.tolist()
        #     text = [clean_text(t) for t in text]
        #     text = ' '.join(text)
        #     self.games[gameName] = text

    def get_word_count(self, gameName):
        tokens = nltk.word_tokenize(self.games[gameName]['text'])
        tokens = [w for w in tokens if not w in self.stop_words]
        word_count = Counter(tokens)
        return {k: v for k, v in sorted(word_count.items(), key=lambda item: item[1], reverse=True)}

    def save_word_count(self, gameName, word_count, path):
        path = Path(path)
        appid = self.games[gameName]['appid']
        fileName = gameName + '_' + str(appid) + '.pickle'
        # fileName = gameName+'.pickle'
        with open(path/fileName, 'wb+') as f:
            pickle.dump(word_count, f, pickle.HIGHEST_PROTOCOL)

    def load_word_count(self, gameName, path):
        # path = Path(path).glob("**/*.pickle")
        # files = [x for x in path if x.is_file()]
        path = Path(path)
        appid = self.games[gameName]['appid']
        fileName = gameName + '_' + str(appid) + '.pickle'

        with open(path/fileName, 'rb') as f:
            word_counts = pickle.load(f)

        return word_counts


if __name__ == '__main__':

    gameName = "Dota Underlords"
    path = Path("word_counts")

    wf = WordFrequency()
    cnt = wf.get_word_count(gameName)
    wf.save_word_count(gameName, cnt, "word_counts")
    # cnt = wf.load_word_count(gameName, path)
    print(cnt)
