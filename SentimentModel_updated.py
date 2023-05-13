import json
import ijson
import os
import re
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
            
###not needed probably 
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
###

#map
import folium
def plot_locations_on_map(data):
    # map centered on Victoria, Australia
    vic_map = folium.Map(location=[-37.4713, 144.7852], zoom_start=8)
    for tweet in data:
        if tweet['place']:
            place = tweet['place']
            if place['country_code'] == 'AU' and place['place_type'] == 'city':
                lat = place['bounding_box']['coordinates'][0][0][1]
                lon = place['bounding_box']['coordinates'][0][0][0]
                name = place['name']
                folium.Marker([lat, lon], popup=name).add_to(vic_map)
    return vic_map
map = plot_locations_on_map(data)

#sentiment
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
def get_sentiment_score(tweet):
    analyzer = SentimentIntensityAnalyzer()
    tokens = word_tokenize(tweet)
    scores = analyzer.polarity_scores(tweet)
    sentiment_score = scores['compound']
    return sentiment_score

#if you want to categorise in positive/negative
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

    negative = pd.DataFrame()
    positive= pd.DataFrame()
    neutral = pd.DataFrame()

    negative = df3[df3['polarity']<=-0.4]
    positive = df3[df3['polarity']>=0.4]
    neutral = df3[(df3['polarity'] > -0.4) & (df3['polarity'] < 0.4)]

    return negative, positive, neutral 

#sentiment mastadon
from mastodon import Mastodon

def get_toot_sentiment(instance_url, access_token, #toot):
    analyzer = SentimentIntensityAnalyzer()
    #not sure if needed?
    mastodon = Mastodon(
        access_token=access_token,
        api_base_url=instance_url
    )
    for toot in timeline:
        #regex
        clean_toot = re.sub('<[^<]+?>', '', toot['content'])
        tokens = word_tokenize(clean_toot)
        scores = analyzer.polarity_scores(clean_toot)
        sentiment_score = scores['compound']
        return sentiment_score, clean_toot

#map with sentiment
def plot_sentiment_on_map(data):
    vic_map = folium.Map(location=[-37.4713, 144.7852], zoom_start=8)
    for tweet in data:
        if tweet['place']:
            place = tweet['place']
            if place['country_code'] == 'AU' and place['place_type'] == 'city':
                lat = place['bounding_box']['coordinates'][0][0][1]
                lon = place['bounding_box']['coordinates'][0][0][0]
                name = place['name']
                sentiment_score = get_sentiment_score(tweet['text'])
                if sentiment_score > 0.5:
                    color = 'green'
                elif sentiment_score > 0:
                    color = 'lightgreen'
                elif sentiment_score > -0.5:
                    color = 'yellow'
                else:
                    color = 'red'
                folium.CircleMarker([lat, lon], radius=5, color=color, fill=True, fill_opacity=0.7, popup=name + ': ' + str(sentiment_score)).add_to(vic_map)
    return vic_map

#compare twitter and mastadon sentiment based on location
def compare_sentiment_location():
    twitter_scores_by_location = {}
    toot_scores_by_location = {}
    #twitter
    twitter_tweets = get_twitter_sentiment_location(twitter_api_key, twitter_api_secret_key, twitter_access_token, twitter_access_token_secret)
    for tweet in twitter_tweets:
        location = tweet['location']
        sentiment = tweet['sentiment']
        if location in twitter_scores_by_location:
            twitter_scores_by_location[location].append(sentiment)
        else:
            twitter_scores_by_location[location] = [sentiment]
    #toots
    toot_statuses = get_toot_sentiment_location(instance_url, access_token)
    for status in toot_statuses:
        location = status['location']
        sentiment = status['sentiment']
        if location in toot_scores_by_location:
            toot_scores_by_location[location].append(sentiment)
        else:
            toot_scores_by_location[location] = [sentiment]
    
    #mean for each
    twitter_means_by_location = {}
    for location, scores in twitter_scores_by_location.items():
        mean_score = statistics.mean(scores)
        twitter_means_by_location[location] = mean_score
        
    toot_means_by_location = {}
    for location, scores in toot_scores_by_location.items():
        mean_score = statistics.mean(scores)
        toot_means_by_location[location] = mean_score
    
    #comparison
    for location in set(twitter_means_by_location.keys()) | set(toot_means_by_location.keys()):
        twitter_mean = twitter_means_by_location.get(location, 0)
        toot_mean = toot_means_by_location.get(location, 0)
        if twitter_mean > toot_mean:
            print(f"{location}: Twitter has a higher mean sentiment score than Mastodon.")
        elif toot_mean > twitter_mean:
            print(f"{location}: Mastodon has a higher mean sentiment score than Twitter.")
        else:
            print(f"{location}: The mean sentiment scores for Twitter and Mastodon are the same.")
                       
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

    return city_tweets, unique_city_tweets

#for scaling
def get_file_chunks(filename, num_chunks):
    file_size = os.path.getsize(filename)
    chunk_size = file_size // num_chunks
    return [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_chunks)]

 

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

    twitter_data_iter = read_json_file_iteratively('#######.json')


    # TBC - what we actually want to do, easy with functions

if _name_ == "_main_":
    main()
