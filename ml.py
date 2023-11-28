import requests
import pandas as pd
import folium
from folium.plugins import HeatMap
import pickle
import numpy as np

from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (10,7)
import seaborn as sns

from sklearn.model_selection import train_test_split

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 500)
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
rms = []
sigs = []
mage = []
tsus = []

for feature in features:
    places.append(feature['properties']['place'])
    mags.append(feature['properties']['mag'])
    times.append(pd.to_datetime(feature['properties']['time'], unit='ms').strftime('%y/%m/%d %H:%M:%S'))
    lats.append(feature['geometry']['coordinates'][1])
    lons.append(feature['geometry']['coordinates'][0])
    weights.append(feature['properties']['mag'])
    rms.append(feature['properties']['rms'])
    sigs.append(feature['properties']['sig'])
    mage.append(feature['properties']['gap'])
    tsus.append(feature['properties']['tsunami'])

dataapi = {'Latitude': lats,
	'Longitude': lons,
	'Weight': weights}
dfapi = pd.DataFrame(dataapi)

# dataml = {'Magnitude': mags,
# 	'RMS': rms}
dataml = {'Latitude': lats,
	'Longitude': lons,
	'MagE': mage,
	'Magnitude': mags,
	         'Tsu': tsus}
dfml = pd.DataFrame(dataml)
dfml.to_csv("output.csv", index=False)

plotdata = pd.read_csv("output.csv")
plotdata.head(10)

sns.scatterplot(x="Magnitude",y="Tsu",data=plotdata)

# test train split
X = plotdata[['Latitude', 'Longitude']]
y = plotdata[['Magnitude']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
print(X_train.shape, X_test.shape, y_train.shape, X_test.shape)

# X = plotdata[["Magnitude"]].to_numpy()
# y = plotdata[["RMS"]].to_numpy()
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

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

import seaborn as sns
import matplotlib.pyplot as plt

# Plot the regression line
sns.regplot(x=X_test['Latitude'], y=y_test, color='blue', scatter_kws={'s': 10})
sns.regplot(x=X_test['Longitude'], y=y_test, color='red', scatter_kws={'s': 10})
plt.legend(labels=['Latitude', 'Longitude'])
plt.title('Multiple Linear Regression Model')
plt.xlabel('Predictor Variables')
plt.ylabel('Magnitude')
plt.show()
