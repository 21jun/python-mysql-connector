from database.pymysql_conn import DataBase
import pandas as pd


db = DataBase()

SQL = "SELECT * FROM world.city;"
df = db.to_df(SQL)
print(df)
