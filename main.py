from session import Session
from database import Database
from dataframe import Data

session = Session(name = "Sorako Bot", tag = "Kek", region = "Europe", queue = "Ranked")
puuid = session.get_puuid()
match_history = session.fetch_match()
region = session.get_region()

session.update_timeline()

db = Database()
db.create_table()
msg = db.update_table()
print(msg)
db.create_player_timeline()
msg_timeline = db.update_player_timeline()
print(msg_timeline)

db.close()