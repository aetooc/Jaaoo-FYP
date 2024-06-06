import requests
import serpapi
import os
from serpapi import GoogleSearch


def GetRestaurants(location):

    result_key = os.environ.get("G_FLIGHTS_KEY")

    url = f"https://serpapi.com/locations.json?q={location}&limit=5"

    headers = {
        "User-agent": "Get_Location"
    }

    response = requests.get(url, headers=headers)

    response_json = response.json()

    zoom = "15.1z"
    # Extracting the first set of GPS coordinates
    longitude, latitude = response_json[0]['gps']

    # Formatting the string as specified
    ll = f"@{latitude},{longitude},{zoom}"

    params = {
    "engine": "google_maps",
    "q": "resturants",
    "ll": ll,
    "type": "search",
    "api_key": result_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Extracting meaningful information for restaurants
    local_results = results['local_results']

    # Prepare the announcement message for restaurants
    announcement = "🍽️ Restaurants available in your area: 🍽️\n"

    for result in local_results:
        announcement += (f"🏠 {result['title']} - {result['type']}\n"
                        f"⭐ Rating: {result.get('rating', 'N/A')} (📝 {result.get('reviews', 'N/A')} reviews)\n"
                        f"📍 Address: {result['address']}\n\n")

    # Print the announcement
    print(announcement)
    return announcement


