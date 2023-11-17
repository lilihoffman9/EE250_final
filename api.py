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
latitude = 39.1458
longitude = 34.1614
max_radius_km = 1500

url = requests.get(f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&minmagnitude={min_magnitude}&latitude={latitude}&longitude={longitude}&maxradiuskm={max_radius_km}')
dataset = url.json()

url
<Output:> <Response [200]>
