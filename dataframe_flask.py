import pandas as pd

class Data_Flask():
    def __init__(self, rows):
        self.rows = rows

    def return_stats(self):
        rows = [dict(row) for row in self.rows]
        df = pd.DataFrame(rows)

        if df.empty:
            return df
        
        df["cs"] = df["total_minions_killed"] + df["neutral_minions_killed"]
        df["kda"] = ((df["kills"] + df["assists"]) / df["deaths"].replace(0,1)).round(1)
        df["game_start_time"] = pd.to_datetime(df["game_start_timestamp"], unit = "ms")
        df.drop(columns=["total_minions_killed", "neutral_minions_killed", "game_start_timestamp"], inplace=True)

        return df.to_dict(orient="records")