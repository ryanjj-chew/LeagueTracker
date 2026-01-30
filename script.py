from match_store import Match
from database import Database

match_example = Match(name = "Sorako Bot", tag = "Kek", region = "Europe", queue = "Ranked")

match_details = match_example.get_match()
db = Database()
db.create_table()
msg = db.update_table()
print(msg)
db.close()