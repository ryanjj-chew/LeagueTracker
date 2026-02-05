from session import Session
from database import Database

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