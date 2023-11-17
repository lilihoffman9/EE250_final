import requests
import pandas as pd
import folium
from folium.plugins import HeatMap


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 500)

start_time = 'now-180days'
min_magnitude = 3
latitude = 34.0224
longitude = 118.2851
max_radius_km = 1500

url = requests.get(f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&minmagnitude={min_magnitude}&latitude={latitude}&longitude={longitude}&maxradiuskm={max_radius_km}')
dataset = url.json()

features = dataset['features']

places = []
mags = []
times = []
lats = []
lons = []
weights = []

for feature in features:
    places.append(feature['properties']['place'])
    mags.append(feature['properties']['mag'])
    times.append(pd.to_datetime(feature['properties']['time'], unit='ms').strftime('%y/%m/%d %H:%M:%S'))
    lats.append(feature['geometry']['coordinates'][1])
    lons.append(feature['geometry']['coordinates'][0])
    weights.append(feature['properties']['mag'])
    
data = {'Latitude': lats, 
	'Longitude': lons,
	'Weight': weights}
df = pd.DataFrame(data)

turkey_coord = [39, 35]
turkey_map_normal = folium.Map(location=turkey_coord, zoom_start=5.5)

HeatMap(data=df[['Latitude', 'Longitude', 'Weight']], radius=15).add_to(turkey_map_normal)



for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Weight']/2,
        color='red',
        fill_color='red').add_to(turkey_map_normal)

turkey_map_normal.save("heatmap_map.html")

