from database.pymysql_conn import DataBase
import pandas as pd


db = DataBase()

SQL = "SELECT * FROM yt.yt_video_info where filter=1"
df = db.to_df(SQL)

query = """
UPDATE yt.yt_comment_steam
SET filter = 1
WHERE videoId = '{videoId}'
"""

for index, row in df.iterrows():
    videoId = row['videoId']
    print(index, videoId)
    db.cur.execute(query.format(videoId=videoId))
