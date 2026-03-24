from player_info import PlayerInfo
from match_ingester import MatchIngester
from match_v5 import MatchV5
from timeline import Timeline
from dataframe import Data
import jsonlines

class Session():
    def __init__(self, name , tag , region, queue):
        self.region = region
        self.queue = queue
        self.player = PlayerInfo(name = name, tag = tag, region = self.region)
        self.puuid = self.player.get_puuid()
        self.match_ingester = MatchIngester(puuid = self.puuid, region = self.region, queue = self.queue)
        self.timeline = Timeline(puuid = self.puuid, region = self.region)
        self.data = Data()

    def get_puuid(self):
        return self.puuid
    
    def get_region(self):
        return self.region
    
    def get_queue(self):
        return self.queue

    def fetch_match(self):
        return self.match_ingester.fetch_match()

    def fetch_timeline(self, match_id):
        return self.timeline.stats(match_id)
    
    def update_timeline(self):
        seen_match_ids = set()
        added = 0
        skipped = 0
        try:
            with jsonlines.open("data/match_timeline.jsonl") as reader:
                for record in reader:
                    match_id = record[0].get("match_id")
                    seen_match_ids.add(match_id)
        except FileNotFoundError:
            pass

        with jsonlines.open("data/match_data.jsonl") as reader:
            with jsonlines.open("data/match_timeline.jsonl", mode = "a") as writer:

                for record in reader:
                    match_id = record.get("matchID")
                    print(f"Checking match: {match_id}")

                    if match_id in seen_match_ids:
                        print(f"Skipping: {match_id}")
                        skipped += 1
                        continue

                    try:
                        timeline_stats = self.fetch_timeline(match_id)
                        writer.write(timeline_stats)
                        seen_match_ids.add(match_id)
                        print(f"Added timeline for {match_id}")
                        added += 1

                    except FileNotFoundError:
                        continue
        print(f"Added: {added}, Skipped: {skipped}")
        return
    
    def get_timeline(self, match_id):
        return self.data.return_timeline_stats(match_id)