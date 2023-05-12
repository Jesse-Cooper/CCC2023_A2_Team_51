from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import csv, time, json, requests
import pandas as pd
import pickle

print("test")
# MASTODON_ACCESS_TOKEN='X5d8FChQNZKd2Za3NxIFoDMnY517F8JxZyMaKuZWu1Y'

# mastodon = Mastodon(api_base_url='https://mastodon.online', access_token = MASTODON_ACCESS_TOKEN)
# mastodon.retrieve_mastodon_version()
# mastodon.status("109666136628267939")["content"]

# m = Mastodon(
#         api_base_url=f'https://mastodon.online',
#         access_token=MASTODON_ACCESS_TOKEN
#     )
# URL = "https://mastodon.au"
# DIR_SAVE = "data.json"
# N_COLLECT = 2
# data = []

# class Listener(StreamListener):
#     def on_update(self, toot):
#         data.append(toot)
#         print(f"collected {len(data)}")

#         if len(data) >= N_COLLECT:
#             with open(DIR_SAVE, "a") as file:
#                 file.write(json.dumps(data, indent=2, sort_keys=True, default=str))
#             exit()

# m.stream_public(Listener())


# def ingest_data(data_dict):
#     filename = '%s.pickles' % date.strftime('%Y-%m-%d_%H')
#     with open(filename, 'ab') as outf:
#         pickle.dump(data_dict, outf, pickle.HIGHEST_PROTOCOL)

# URL = 'https://mastodon.social/api/v1/timelines/public'


# since = pd.Timestamp('now', tz='utc') - pd.DateOffset(hour=1)
# is_end = False

# results = []
# r = requests.get(URL)
# toots = json.loads(r.text)
# if len(toots) != 0:
#     for t in toots:
#         results.append(t)


# while total < max:

#     while True:
#         r = requests.get(URL+ '$limit=50000')
#         toots = json.loads(r.text)
#         if len(results) > max:
#             break

#         if len(toots) == 0:
#             break
        
#         for t in toots:
#             timestamp = pd.Timestamp(t['created_at'], tz='utc')
#             if timestamp <= since:
#                 is_end = True
#                 break
                
#             results.append(t)
#             total = len(results)

        
#         if is_end:
#             break
        
#         max_id = toots[-1]['id']
#         params['max_id'] = max_id


# results = results[:max]    
# df = pd.DataFrame(results)
# # print(df.head())
# df.to_csv('mastodon_mil_toots.csv')

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
        # timestamp = pd.Timestamp(t['created_at'], tz='utc')
        # if timestamp <= since:
        #     is_end = True
        #     break
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