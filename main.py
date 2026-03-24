from session import Session
from database import Database
from graph import Graph

session = Session(name = "Sorako Bot", tag = "Kek", region = "Europe", queue = "Ranked")
puuid = session.get_puuid()
match_history = session.fetch_match()
region = session.get_region()
graph = Graph()

session.update_timeline()

db = Database()
db.create_table()
db.update_table()
db.create_self_player_timeline()
db.update_self_player_timeline()

db.close()