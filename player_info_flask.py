from api import Functions

class PlayerInfo:
    def __init__(self, name, tag, region):
        self.name = name
        self.tag = tag
        self.region = region

    def get_puuid(self, api_key):
        client = Functions(api = api_key, name = self.name, tag = self.tag, region = self.region)
        return client.get_puuid()