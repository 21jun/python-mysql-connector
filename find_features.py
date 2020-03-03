from database.pymysql_conn import DataBase

import pandas as pd
import numpy as np
import re
import nltk

from collections import Counter
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
        self.stop_words = stopwords.words('english')

        for gameName in self.gameNames:
            text = self.comments[self.comments['gameName'] == gameName]['text']
            text = text.tolist()
            text = [clean_text(t) for t in text]
            text = ' '.join(text)
            self.games[gameName] = text

    def get_word_count(self, gameName):
        tokens = nltk.word_tokenize(self.games[gameName])
        tokens = [w for w in tokens if not w in self.stop_words]
        word_count = Counter(tokens)
        return {k: v for k, v in sorted(word_count.items(), key=lambda item: item[1], reverse=True)}


if __name__ == '__main__':

    wf = WordFrequency()
    cnt = wf.get_word_count("Neon Boost")
    print(cnt)
