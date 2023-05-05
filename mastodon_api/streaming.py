# needs pip install Mastodon.py
# NOTE NEED TO FIX INVALID JSON SAVE

from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import csv
import time
from json import dumps
from os import environ


# server joined with and has application
URL = "https://mastodon.au"
DIR_SAVE = "data.json"
N_COLLECT = 2


data = []


class Listener(StreamListener):
    def on_update(self, toot):
        data.append(toot)
        print(f"collected {len(data)}")

        if len(data) >= N_COLLECT:
            # save newly collected data
            with open(DIR_SAVE, "a") as file:
                file.write(dumps(data, indent=2, sort_keys=True, default=str))

            # remove exit on actual
            exit()


# locally stored access token
access_token = environ["MASTODON_ACCESS_TOKEN"]

m = Mastodon(
        api_base_url=URL,
        access_token=access_token
    )

m.stream_public(Listener())
print("done")
