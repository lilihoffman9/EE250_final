import os
import json
import time 
import requests
import geopandas as gpd

#set string of url with ultrasonic ranger value in the max radius slot
response =requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude=34&longitude=118&maxradiuskm=10000')

response = response.json()
response['features'][0]

exportDf = gpd.GeoDataFrame()

for i, data in enumerate(response['features']):  
    gdf = gpd.GeoDataFrame()
    coord = data['geometry']['coordinates']
    geometry = gpd.points_from_xy([coord[0]], [coord[1]])
    gdf = gpd.GeoDataFrame(data['properties'], index = [i], geometry = geometry, crs='EPSG:4326')
    gdf = gdf[['mag', 'place', 'time', 'alert','status','tsunami', 'geometry']]
    gdf['time'] = time.strftime('%Y-%m-%d', time.gmtime(gdf['time'][i]/1000))
    exportDf = exportDf.append(gdf)

if exportDf.crs == None:
    exportDf.set_crs('epsg:4326', inplace=True)

directory = 'earthquakes'
name = strftime("%Y%m%d", time.localtime())
filename = os.path.join(directory, name + '.gpkg')
layername = "_".join([strftime("%H", time.localtime()), str(len(response['features']))])

exportDf.to_file(driver='GPKG', 
                 filename=filename, 
                 layer=layername, 
                 encoding='utf-8')
print(f'Export {name} {layername} sucessfull')

