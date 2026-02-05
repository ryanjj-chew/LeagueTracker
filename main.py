from session import Session
from database import Database
from dataframe import Data

session = Session(name = "Sorako Bot", tag = "Kek", region = "Europe", queue = "Ranked")
puuid = session.get_puuid()
match_history = session.fetch_match()

db = Database()
db.create_table()
msg = db.update_table()
print(msg)
rows = db.get_matches(puuid = puuid)
print(rows)
db.close()

data = Data(rows = rows)
data_rows = data.return_series()
print(data_rows)