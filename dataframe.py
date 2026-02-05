import pandas as pd
import numpy as np

class Data():
    def __init__(self, rows):
        self.df = pd.DataFrame(rows, columns = ["match_id", "game_start_timestamp", "champion_name", "position", "kills", "deaths", "assists", "total_minions_killed", "win"])
        self.df["kda"] = ((self.df["kills"] + self.df["assists"]) / self.df["deaths"].replace(0,1)).round(1)
        self.df["game_time"] = pd.to_datetime(self.df["game_start_timestamp"], unit = "ms")
    
    def return_series(self):
        self.df.sort_values("game_time")
        return self.df