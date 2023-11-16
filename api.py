import requests
import json
import panda as np


zipcode_str = "48198"          # We can also seach like: filter.latLong.near=39.306346,-84.278902
search_radius_miles = 20
max_results = 200              # 200 is the maximu allowed
chain = "Kroger"               # The Kroger company owns other grocery chains, gas stations, etc.

headers = {"Authorization": "Bearer " + token}
params = {"filter.zipCode.near":zipcode_str, 
          "filter.limit":max_results,
          "filter.radiusInMiles":search_radius_miles,
          "filter.chain":chain}
resp = requests.get("https://api.kroger.com/v1/locations", headers=headers, params=params)
print("done")
