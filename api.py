import requests
import json
import panda as np

from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()
auth = (user_secrets.get_secret("final-2a1585a864d9e67627c6ae04c807a2c53211770964979935989"),
          user_secrets.get_secret("9y5H9SgdaK6BYUijI8ZLnznt63MKszrDI3M0i1zW"))

# Use our stored credentials to get a "token" which authorizes all of our other requests.
# This is easier than regular Oauth because we don't need access to some random user's stuff.
#headers = {"Content-Type":"application/x-www-form-urlencoded"}
#x = requests.post("https://api.kroger.com/v1/connect/oauth2/token", 
#                  data={"grant_type":"client_credentials","scope":"product.compact"}, headers=headers, auth=auth)
#token = x.json()['access_token']

# Here we search for nearby stores based on a zipcode

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

# The response is JSON. And the "data" part an array of store objects.
stores = resp.json()["data"]
print("Found " + str(len(stores)) + " stores.")

# Let's look at the first store object
print(json.dumps(stores[0], indent=4))

# List stores in descending order of how many departments they have

sorted([str(len(store["departments"]))+" departments at store:" +
        store["locationId"]+" "+store["name"]+",   "+store["address"]["addressLine1"]+" "+store["address"]["city"]
        for store in stores],reverse=True)
