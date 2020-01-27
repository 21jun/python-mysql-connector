from database.pymysql_conn import DataBase
import pandas as pd


db = DataBase()

SQL = "SELECT * FROM world.city;"
db.cur.execute(SQL)

field_names = [i[0] for i in db.cur.description]
b = pd.DataFrame(columns=field_names, data=db.cur.fetchall())
print(b)
