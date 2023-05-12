from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import csv, time, json, requests
import pandas as pd

URL = 'https://mastodon.social/api/v1/timelines/public'
params = {
    'limit': 40
}

since = pd.Timestamp('now', tz='utc') - pd.DateOffset(hour=1)
is_end = False
results = []
total = 0  
while True:
    r = requests.get(URL, params=params)
    toots = json.loads(r.text)
    if total >= 1000000:
        break
    if total%10000 == 0:
        print(total)
    for t in toots:

        try:
            results.append(t['content'])
            total += 1
        except: 
             continue


file = open('toots.txt','w')
for toot in results:
	file.write(toot+"\n")
file.close()

print(total)