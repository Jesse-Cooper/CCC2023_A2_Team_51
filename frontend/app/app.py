from flask import Flask
from flask import render_template, jsonify 
import csv
import couchdb
import json
import pandas as pd
import geopandas as gpd
import folium

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

def load_sudo_pt():
    HOST = "http://admin:admin@172.26.136.58:5984"
    couch = couchdb.Server(HOST)
    db = couch['test_sudo']

    docs = db.view('pt/pt-view', reduce=False)
    data = [{'SA2_NAME21': doc['key'], 'total_pt': doc['value']} for doc in docs]
    stats = db.view('pt/pt-view', reduce=True)
    stat = [s['value'] for s in stats][0]

    scaling_factor = 2 / (stat['max'] - stat['min'])
    for i in range(len(data)):
        data[i]['total_pt'] = (data[i]['total_pt'] - stat['min']) * scaling_factor - 1
    df = pd.DataFrame(data)

    return df

def load_sudo_income():
    HOST = "http://admin:admin@172.26.136.58:5984"
    couch = couchdb.Server(HOST)
    db = couch['test_sudo']

    docs = db.view('income/income-view', reduce=False)
    data = [{'SA2_NAME21': doc['key'], 'median_income': doc['value']} for doc in docs]
    stats = db.view('income/income-view', reduce=True)
    stat = [s['value'] for s in stats][0]

    scaling_factor = 2 / (stat['max'] - stat['min'])
    for i in range(len(data)):
        data[i]['median_income'] = (data[i]['median_income'] - stat['min']) * scaling_factor - 1
    df = pd.DataFrame(data)

    return df    

def combine_geo(df):
    geo = gpd.read_file("./data/SA3_2021_AUST_GDA2020.shp")
    geo = geo[['SA3_NAME21', 'geometry']]
    geoJSON = geo.to_json()
    sa2_sa3 = gpd.read_file("./data/SA2_2021_AUST_GDA2020.shp")
    sa2_sa3 = sa2_sa3[['SA2_NAME21', 'SA3_NAME21']]
    group = pd.merge(sa2_sa3, df, on='SA2_NAME21', how='inner')
    group = group.drop(['SA2_NAME21'], axis=1)
    group = group.groupby(['SA3_NAME21']).mean()
    group = pd.merge(group, geo, on='SA3_NAME21', how='inner')

    return geoJSON, group

#Home Page
@app.route('/')
def homepage_test():
    return render_template('index.html')

# Sentiment vs. Location
@app.route('/SentiLocation')
def sentilocation():

    geo = gpd.read_file("./data/SA3_2021_AUST_GDA2020.shp")
    geo = geo[['SA3_NAME21', 'geometry']]
    geo = geo.rename(columns={'SA3_NAME21': 'location'})
    geo = geo.drop_duplicates(subset=['location'])
    geoJSON = geo.to_json()

    senti = pd.read_json("./data/modified_data2.json")
    senti = senti[['location', 'sentiment']]
    senti = senti.groupby(['location']).mean()
    group = pd.merge(senti, geo, on='location', how='inner')

    map = folium.Map(location=[-37.5, 144.5], tiles="Stamen Terrain", zoom_start=8)

    c = folium.Choropleth(
        geo_data=geoJSON, # geoJSON 
        name='Sentiment of Tweets', # name of plot
        data=group, # data source
        columns=['location','sentiment'], # the columns required
        key_on='properties.location', # this is from the geoJSON's properties
        fill_color='YlOrRd', # color scheme
        nan_fill_color='black',
        legend_name='Sentiment'
    )
    c.add_to(map)

    return map.get_root().render()

# Mastodon vs. Twitter
@app.route('/MastoTwitter')
def mastotwitter():
    return render_template('mastotwitter.html')

#Member Page
@app.route('/Group_Members')
def members():
    return render_template('members.html')

#Correlation of between public transport locations and sentiment
@app.route('/Correlation')
def correlation():
    return render_template('correlation.html')

#Transport usage in australia
@app.route('/SUDOTransport')
def SUDOTransport():
    
    df = load_sudo_pt()
    geoJSON, group = combine_geo(df)

    map = folium.Map(location=[-37.5, 144.5], tiles="Stamen Terrain", zoom_start=8)

    c = folium.Choropleth(
        geo_data=geoJSON, # geoJSON 
        name='Transport usage in Australia', # name of plot
        data=group, # data source
        columns=['SA3_NAME21','total_pt'], # the columns required
        key_on='properties.SA3_NAME21', # this is from the geoJSON's properties
        fill_color='YlOrRd', # color scheme
        nan_fill_color='black',
        legend_name='Transport Usage (scaled)'
    )
    c.add_to(map)

    return map.get_root().render()

#Income in australia
@app.route('/SUDOIncome')
def SUDOIncome():

    df = load_sudo_income()
    geoJSON, group = combine_geo(df)

    map = folium.Map(location=[-37.5, 144.5], tiles="Stamen Terrain", zoom_start=8)

    c = folium.Choropleth(
        geo_data=geoJSON, # geoJSON 
        name='Income in Australia', # name of plot
        data=group, # data source
        columns=['SA3_NAME21','median_income'], # the columns required
        key_on='properties.SA3_NAME21', # this is from the geoJSON's properties
        fill_color='YlOrRd', # color scheme
        nan_fill_color='black',
        legend_name='Median_income (scaled)'
    )
    c.add_to(map)

    return map.get_root().render()


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = int('8080'), debug = True)