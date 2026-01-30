import sqlite3
import jsonlines

class Database():
    def __init__(self, db_path = "data/matches.db"):
        self.con = sqlite3.connect(db_path)
        self.curs = self.con.cursor()

    def create_table(self):
        self.curs.execute("""CREATE TABLE IF NOT EXISTS match_summary (
                         match_id TEXT PRIMARY KEY,
                         puuid TEXT NOT NULL,
                         game_start_timestamp INTEGER NOT NULL,
                         champion_name TEXT NOT NULL,
                         position TEXT NOT NULL,
                         kills INTEGER,
                         deaths INTEGER,
                         assists INTEGER,
                         total_minions_killed INTEGER,
                         win INTEGER NOT NULL
                         )""")

    def update_table(self):
        successful_import = 0
        failed_import = 0
        with jsonlines.open("data/match_data.jsonl") as reader:
            for record in reader:
                try:
                    win_int = 1 if record.get("win") else 0
                    row = (
                        record["matchID"],
                        record["puuid"],
                        record["gameStartTimestamp"],
                        record["championName"],
                        record["individualPosition"],
                        record["kills"],
                        record["deaths"],
                        record["assists"],
                        record["totalMinionsKilled"],
                        win_int
                    )
                    self.curs.execute("""INSERT OR IGNORE INTO match_summary 
                                    VALUES (?,?,?,?,?,?,?,?,?,?)""", row)
                    
                    if self.curs.rowcount == 1:
                        successful_import += 1
                    else:
                        failed_import += 1

                except KeyError:
                    continue

        self.con.commit()
        return f"Imported {successful_import} rows successfully, with {failed_import} duplicates skipped"
    
    def close(self):
        self.curs.close()
        self.con.close()