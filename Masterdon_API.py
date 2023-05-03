from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import csv, time, json, requests
import pandas as pd

# MASTODON_ACCESS_TOKEN='X5d8FChQNZKd2Za3NxIFoDMnY517F8JxZyMaKuZWu1Y'

# mastodon = Mastodon(api_base_url='https://mastodon.online', access_token = MASTODON_ACCESS_TOKEN)
# mastodon.retrieve_mastodon_version()
# mastodon.status("109666136628267939")["content"]

# m = Mastodon(
#         api_base_url=f'https://mastodon.online',
#         access_token=MASTODON_ACCESS_TOKEN
#     )

# class Listener(StreamListener):
#     def on_update(self, status):
#         print(json.dumps(status, indent=2, sort_keys=True, default=str))

#m.stream_public(Listener())

URL = 'https://mastodon.online/api/v1/timelines/public'
params = {
    'limit': 40
}

since = pd.Timestamp('now', tz='utc') - pd.DateOffset(hour=2)
is_end = False

results = []

while True:
    r = requests.get(URL, params=params)
    toots = json.loads(r.text)

    if len(toots) == 0:
        break
    
    for t in toots:
        timestamp = pd.Timestamp(t['created_at'], tz='utc')
        if timestamp <= since:
            is_end = True
            break
            
        results.append(t)
    
    if is_end:
        break
    
    max_id = toots[-1]['id']
    params['max_id'] = max_id
    
df = pd.DataFrame(results)
df.to_csv('mastodon.csv')