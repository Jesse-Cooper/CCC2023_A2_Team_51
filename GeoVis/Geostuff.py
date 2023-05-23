import pandas as pd
import geopandas as gpd
import folium

geo = gpd.read_file("./data/SA3_2021_AUST_GDA2020.shp")
geo = geo[['SA3_NAME21', 'geometry']]
geo = geo.rename(columns={'SA3_NAME21': 'location'})
geo = geo.drop_duplicates(subset=['location'])
geoJSON = geo.to_json()

senti = pd.read_json("./data/modified_data2.json")
senti = senti[['location', 'sentiment']]

group = pd.merge(geo, senti, on='location', how='inner')
group = group.groupby(['location']).mean()
group = pd.merge(group, geo, on='location', how='inner')

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
map.save('SentiLocation.html')