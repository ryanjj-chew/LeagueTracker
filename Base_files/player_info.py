from api import Functions
import os
from dotenv import load_dotenv

class PlayerInfo:
    def __init__(self, name, tag, region):
        load_dotenv(override=True)
        try:
            self.api_key = os.getenv("RIOT_API_KEY")
        except:
            raise ValueError("No API Key")
        self.name = name
        self.tag = tag
        self.region = region

    def get_puuid(self):
        client = Functions(api = self.api_key, name = self.name, tag = self.tag, region = self.region)
        return client.get_puuid()