import requests
import pandas as pd
import folium
from folium.plugins import HeatMap
from finalProject import *
import paho.mqtt.client as mqtt

MQTT_SERVER = "172.20.10.6"
MQTT_PATH = "dist"

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 500)

print(finalProject.range_val)

start_time = 'now-180days'
min_magnitude = 3
latitude = 34.0224
longitude = -118.3
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

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
client.loop_start()   #use this line if you want to write any more code here

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

turkey_coord = [latitude, longitude]
turkey_map_normal = folium.Map(location=turkey_coord, zoom_start=5.5)

HeatMap(data=df[['Latitude', 'Longitude', 'Weight']], radius=15).add_to(turkey_map_normal)



for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Weight']/2,
        color='red',
        fill_color='red').add_to(turkey_map_normal)

turkey_map_normal.save("heatmap_map.html")

