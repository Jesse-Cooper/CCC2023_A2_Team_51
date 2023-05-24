import csv
import couchdb
import json
import pandas as pd
import geopandas as gpd
import folium

HOST = "http://admin:admin@172.26.136.58:5984"
couch = couchdb.Server(HOST)
db = couch['test_sudo']

#get ids
i = []
count = 0
for docid in db.view('_all_docs'):
    i.append(docid['id'])

data = []
for doc_id in i:
    if not doc_id.startswith('_'):  # Skip special documents
        doc = db[doc_id]
        sa2_code = doc.get('sa2_code')
        sa2_name = doc.get('sa2_name')
        median_income = doc.get('median_income')
        female_bus_total = doc.get('female_bus_total')
        female_train_total = doc.get('female_train_total')
        female_tram_total = doc.get('female_tram_total')
        male_bus_total = doc.get('male_bus_total')
        male_train_total = doc.get('male_train_total')
        male_tram_total = doc.get('male_tram_total')
        total_pt = int(female_bus_total) + int(female_train_total) + int(female_tram_total) + int(male_bus_total) + int(male_train_total) + int(male_tram_total)
        if sa2_code: 
            data.append({'sa2_code': sa2_code, 'sa2_name': sa2_name, 'median_income': median_income, 'total_pt': total_pt})

max = 0
for i in range(len(data)):
    if data[i]['total_pt'] > max:
        max = data[i]['total_pt']
interval = max/len(data)

sorted_list = sorted(data, key=lambda x: x['total_pt'])

for i in range(len(sorted_list)):
    sorted_list[i]['total_pt'] = i+1

for i in range(len(data)):
    sorted_list[i]['total_pt'] = (sorted_list[i]['total_pt']/len(sorted_list)) * 2 - 1



geo = gpd.read_file("./data/SA2_2021_AUST_GDA2020.shp")
df = pd.DataFrame(sorted_list)
geo = geo[['SA2_NAME21', 'SA3_NAME21', 'geometry']]
geo = geo.rename(columns={'SA2_NAME21': 'sa2_name'})
geoJSON = geo.to_json()
group = pd.merge(geo, df, on='sa2_name', how='inner')
group = group.groupby(['SA3_NAME21']).mean()
group = pd.merge(group, geo, on='SA3_NAME21', how='inner').drop(['sa2_name'], axis =1)
group = group.drop_duplicates(subset=['SA3_NAME21'])



map = folium.Map(location=[-37.5, 144.5], tiles="Stamen Terrain", zoom_start=8)

c = folium.Choropleth(
    geo_data=geoJSON, # geoJSON 
    name='Transport usage in Australia', # name of plot
    data=group, # data source
    columns=['SA3_NAME21','total_pt'], # the columns required
    key_on='properties.SA3_NAME21', # this is from the geoJSON's properties
    fill_color='YlOrRd', # color scheme
    nan_fill_color='black',
    legend_name='Transport Usage'
)
c.add_to(map)
map.save('frontend/app/templates/SUDOTransport.html')
