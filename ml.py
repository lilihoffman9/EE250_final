import requests
import pickle
import pandas as pd
import numpy as np
import paho.mqtt.client as mqtt
import socket
import time
import seaborn as sns

from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (10,7)

from sklearn.model_selection import train_test_split

broker_address = "eclipse.usc.edu"
port = 1883
topic = "sensor/data"
radius = 1500

# Callback when a message is received
def on_message(client, userdata, msg):
    print(f"Received sensor data: {msg.payload.decode()}")
    radius = (int(msg.payload)*1000)
    print(f"Set max radius: {radius}")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 500)

# Create a MQTT client
client = mqtt.Client()

# Set up the callback
client.on_message = on_message

# Connect to the broker
client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

# Subscribe to the topic
client.subscribe(topic)

start_time = 'now-180days'
min_magnitude = 3
latitude = 34.0224
longitude = -118.3

url = requests.get(f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&minmagnitude={min_magnitude}&latitude={latitude}&longitude={longitude}&maxradiuskm={radius}')
dataset = url.json()

features = dataset['features']

mags = []
lats = []
lons = []

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload) + "radius: " + msg.payload)
    # more callbacks, etc
 

# Start the MQTT loop to listen for messages
client.loop_start()

while True:
	time.sleep(1)
	for feature in features:
		mags.append(feature['properties']['mag'])
		lats.append(feature['geometry']['coordinates'][1])
		lons.append(feature['geometry']['coordinates'][0])
		
	dataml = {'Latitude': lats,
		'Longitude': lons,
		'Magnitude': mags}
	dfml = pd.DataFrame(dataml)
	dfml.to_csv("output.csv", index=False)
		
	plotdata = pd.read_csv("output.csv")
	plotdata.head(10)
		
	# test train split
	X = plotdata[['Latitude', 'Longitude']]
	y = plotdata[['Magnitude']]
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
	print(X_train.shape, X_test.shape, y_train.shape, X_test.shape)
		
	from sklearn.linear_model import LinearRegression
		
	# Train the linear regression model
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
		
	from sklearn.metrics import r2_score, mean_squared_error
		
	scores= {"Model name": ["Linear regression", "SVM", "Random Forest"], "mse": [], "R^2": []}
		
	# Predict on the testing set
	y_pred = regressor.predict(X_test)
		
	# Compute R^2 and MSE
	r2 = r2_score(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
		
	scores['mse'].append(mse)
	scores['R^2'].append(r2)
		
	print("R^2: {:.2f}, MSE: {:.2f}".format(r2, mse))

	new_data = [[latitude-(radius/2), longitude-(radius/2)], [latitude+(radius/2), longitude+(radius/2)]]
	new_pred = regressor.predict(new_data)
	print("New predictions:", new_pred)
		
	# Plot the regression line
	sns.regplot(x=X_test['Latitude'], y=y_test, color='blue', scatter_kws={'s': 10})
	sns.regplot(x=X_test['Longitude'], y=y_test, color='red', scatter_kws={'s': 10})
	plt.legend(labels=['Latitude', 'Longitude'])
	plt.title('Multiple Linear Regression Model')
	plt.xlabel('Predictor Variables')
	plt.ylabel('Magnitude')
	plt.show()
