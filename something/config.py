# config.py

# Eventbrite API token
EVENTBRITE_API_TOKEN = 'WY7AALIFKPGNFESMIX2G'
# eventbrite_integration.py

import requests
from config import EVENTBRITE_API_TOKEN  # Import the token from the configuration

# Define the API endpoint URL
url = 'https://www.eventbriteapi.com/v3/your_endpoint_here'

# Set up the request headers with your API key
headers = {
    'Authorization': f'Bearer {EVENTBRITE_API_TOKEN}',
}

# Send a GET request to the API
response = requests.get(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    data = response.json()
    # Process and use the data as needed
else:
    print(f'Error: {response.status_code}')