import requests
import json
from datetime import datetime

# Fetch flight data
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Create filename with current date/time
filename = f"raw_flights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

# Save to data folder (go up one level, then into data folder)
import os
filepath = os.path.join('..', 'data', filename)

with open(filepath, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Data saved to: {filepath}")
print(f"Total flights captured: {len(data['states'])}")