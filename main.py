from session import Session
from database import Database
from dataframe import Data
import jsonlines

session = Session(name = "Sorako Bot", tag = "Kek", region = "Europe", queue = "Ranked")
puuid = session.get_puuid()
match_history = session.fetch_match()
region = session.get_region()


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

seen_match_ids = set()
with jsonlines.open("data/match_timeline.jsonl") as reader:
    for record in reader:
        match_id = record[0].get("match_id")
        seen_match_ids.add(match_id)

with jsonlines.open("data/match_data.jsonl") as reader:
    with jsonlines.open("data/match_timeline.jsonl", mode = "a") as writer:

        for record in reader:
            match_id = record.get("matchID")

            if not match_id or match_id in seen_match_ids:
                continue

            try:
                timeline_stats = session.get_timeline(match_id)
                writer.write(timeline_stats)
                seen_match_ids.add(match_id)
                print(f"Added timeline for {match_id}")

            except FileNotFoundError:
                continue