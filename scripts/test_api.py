import requests
import json
from datetime import datetime

# OpenSky API endpoint
url = "https://opensky-network.org/api/states/all"

print("Fetching live flight data...")
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Success! Got data for {len(data['states'])} flights")
    
    # Look at first flight
    if data['states']:
        first_flight = data['states'][0]
        print("\nFirst flight example:")
        print(f"Callsign: {first_flight[1]}")
        print(f"Country: {first_flight[2]}")
        print(f"Latitude: {first_flight[6]}")
        print(f"Longitude: {first_flight[5]}")
        print(f"Altitude: {first_flight[7]} meters")
else:
    print(f"Error: {response.status_code}")