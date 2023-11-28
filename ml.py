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

df.to_csv("output.csv", index=False)

coins = pd.read_csv("coins.csv")
coins.head(10)

sns.scatterplot(x="reflectance",y="weight",data=coins, hue="denomination")

# test train split
X = coins[["reflectance","weight"]].to_numpy()
y = coins[["denomination"]].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

## Import your favourite classifier and train it using the X_train data and hte y_train labels
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris  # You can use any dataset you prefer

## make sure you instantiate your classifier and name it clf
clf = KNeighborsClassifier(n_neighbors=5)
clf.fit(X_train, y_train)

## test the accuracy of your model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

## plot the decision boundary of your classifier along with the scatterplot of the training data
## hint: look at the ann example
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))

Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.4)
plt.scatter(X[:, 0], X[:, 1], c=y, marker='o', edgecolor='k')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title(f'K-Nearest Neighbors (K={5})')
plt.show()

# dump your classifier into a pickle file
pickle.dump(clf, open("model.pickle","wb"))


