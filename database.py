import sqlite3
import jsonlines

class Database():
    def __init__(self, db_path = "data/matches.db"):
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row
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
    
    def get_matches(self, puuid, limit = 20):
        self.curs.execute("""SELECT 
                                match_id,
                                game_start_timestamp,
                                champion_name,
                                position,
                                kills,
                                deaths,
                                assists,
                                total_minions_killed,
                                win
                            FROM match_summary
                            WHERE puuid = ?
                            ORDER BY game_start_timestamp DESC
                            LIMIT ?
                          """, (puuid, limit,))
        
        rows = self.curs.fetchall()
        return rows
        
    def get_champion_matches(self, puuid, champion, limit = 20):
        self.curs.execute("""SELECT 
                                match_id,
                                game_start_timestamp,
                                position,
                                kills,
                                deaths,
                                assists,
                                total_minions_killed,
                                win
                            FROM match_summary
                            WHERE puuid = ?
                                AND champion_name = ?
                            ORDER BY game_start_timestamp DESC
                            LIMIT ?
                          """, (puuid, champion, limit,))
        
        rows = self.curs.fetchall()
        return rows
    
    def create_self_player_timeline(self):
        self.curs.execute("""CREATE TABLE IF NOT EXISTS player_timeline (
                            match_id TEXT,
                            minute INTEGER,
                            cs INTEGER,
                            gold INTEGER,
                            xp INTEGER,
                            level INTEGER,
                            PRIMARY KEY(match_id, minute),
                            FOREIGN KEY(match_id) REFERENCES match_summary(match_id)
                          )""")

    def update_self_player_timeline(self):
        successful_import = 0
        failed_import = 0
        with jsonlines.open("data/match_timeline.jsonl") as reader:
            for record in reader:
                try:
                    for frame in record:
                        row = (
                            frame["match_id"],
                            frame["minute"],
                            frame["cs"],
                            frame["gold"],
                            frame["xp"],
                            frame["level"]
                        )
                        self.curs.execute("""INSERT OR IGNORE INTO player_timeline
                                        VALUES (?,?,?,?,?,?)""", row)
                        
                        if self.curs.rowcount == 1:
                            successful_import += 1
                        else:
                            failed_import += 1

                except KeyError:
                    continue

        self.con.commit()
        return f"Imported {successful_import} rows successfully, with {failed_import} duplicates skipped"

    def get_match_timeline(self, match_id):
        self.curs.execute("""SELECT
                                minute,
                                cs,
                                gold,
                                xp,
                                level
                            FROM player_timeline
                            WHERE match_id = ?
                            ORDER BY minute ASC
                          """, (match_id,))
        rows = self.curs.fetchall()
        return rows

    def close(self):
        self.curs.close()
        self.con.close()