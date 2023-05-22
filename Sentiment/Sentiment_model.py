import json
import ijson
import os
import mpi4py.MPI as MPI
import pandas as pd
from collections import Counter, defaultdict
from textblob import TextBlob as tb

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def read_json_file_iteratively(filename):
    with open(filename, 'rb') as file:
        parser = ijson.items(file, 'item')
        for item in parser:
            yield item

def merge_city_tweets(city_tweets_list):
    merged = Counter()
    for city_tweets in city_tweets_list:
        for city_code, count in city_tweets.items():
            merged[city_code] += count
    return merged

def merge_top_unique_city_tweets(top_unique_city_tweets_list):
    merged = defaultdict(lambda: [0, 0])  # Default values: [unique_city_count, tweet_count]
    for top_unique_city_tweets in top_unique_city_tweets_list:
        for author, city_count, tweet_count in top_unique_city_tweets:
            merged[author][0] = max(merged[author][0], city_count)
            merged[author][1] += tweet_count
    return sorted(merged.items(), key=lambda x: (-x[1][0], -x[1][1], x[0]))[:10]


def process_data(twitter_data_iter, sal_data):
    authors = []
    city_tweets = defaultdict(int)
    unique_city_tweets = defaultdict(lambda: defaultdict(int))

    for tweet in twitter_data_iter:
        author_id = tweet['data']['author_id']
        authors.append(author_id)
        
        full_name = tweet['includes']['places'][0]['full_name']
        city = full_name.split(',')[0].strip().lower()
        
        if city in sal_data:
            city_code = sal_data[city]['gcc']
            city_tweets[city_code] += 1
            unique_city_tweets[author_id][city_code] += 1

    top10_authors = Counter(authors).most_common(10)
    user_counts = [(user, len(cities), sum(cities.values())) for user, cities in unique_city_tweets.items()]
    user_counts.sort(key=lambda x: (-x[1], -x[2]))
    top10_unique_city_tweets = user_counts[:10]

    return top10_authors, city_tweets, top10_unique_city_tweets

def get_file_chunks(filename, num_chunks):
    file_size = os.path.getsize(filename)
    chunk_size = file_size // num_chunks
    return [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_chunks)]

def sentiment(tweets):
    text = tweets['text']
    pol = []
    sub = []

    for j in tweet:
        tx = tb(j)
        pol.append(tx.sentiment.polarity)
        sub.append(tx.sentiment.subjectivity)

    df_pols = pd.DataFrame({"polarity":pol,"subjectivity":sub})
    df['polarity']=df_pols['polarity']
    df['subjectivity']=df_pols['subjectivity']
    df_sup = pd.DataFrame()
    df3 = pd.DataFrame()
    df3 = df[['polarity','subjectivity']]

    # Positive, Negative or Neutral

    negative = pd.DataFrame()
    positive= pd.DataFrame()
    neutral = pd.DataFrame()

    negative = df3[df3['polarity']<=-0.4]
    positive = df3[df3['polarity']>=0.4]
    neutral = df3[(df3['polarity'] > -0.4) & (df3['polarity'] < 0.4)]

    return negative, positive, neutral  

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_procs = comm.Get_size()

    sal_data = read_json_file('sal.json')

    # Calculate the number of lines in the file
    with open('bigTwitter.json', 'r') as f:
        total_lines = sum(1 for _ in f)

    # Calculate the lines each process should read
    lines_per_proc = total_lines // num_procs
    start_line = rank * lines_per_proc
    end_line = start_line + lines_per_proc if rank != num_procs - 1 else total_lines

    twitter_data_iter = read_json_file_iteratively('bigTwitter.json')

    top10_authors, city_tweets, top10_unique_city_tweets = process_data(twitter_data_iter, sal_data)

    # TBC

if _name_ == "_main_":
    main()
