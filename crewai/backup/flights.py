import requests
import serpapi
import os
from serpapi import GoogleSearch

rapid_api_key = os.environ.get("RAPID_API_KEY")
google_flights_key = os.environ.get("G_FLIGHTS_KEY")

latitude, longitude = None, None


def get_airport_code(city, headers = 0):
    """
    Fetch the airport code for a given city using TripAdvisor API.
    """
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchAirport"
    querystring = {"query": city}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    print(data)
    if data['status'] and 'data' in data and len(data['data']) > 0:
        # Assuming the first entry in 'data' is the relevant airport
        airport_data = data['data'][0]
        if 'coords' in airport_data:
            coords = airport_data['coords']
            latitude, longitude = map(float, coords.split(","))
        if 'airportCode' in airport_data:
            return airport_data['airportCode']
    return ""


def GetLocation():
    if latitude != None and longitude != None:
        return latitude, longitude
    else:
        return "51.51924", "-0.096654"

def search_flights(departure_code, arrival_code, adate, ddate):
    """
    Search for flights from departure_code to arrival_code on a given date.
    """

    params = {
        "engine": "google_flights",
        "departure_id": departure_code,
        "arrival_id": arrival_code,
        "outbound_date": adate,
        "return_date": ddate,
        "currency": "USD",
        "hl": "en",
        "api_key": google_flights_key,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return str(results)
    # Execute the search using the tool


def GetFlights(departure_city, arrival_city, adate, ddate) -> str:
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com",
        "User-agent": "GetFlights"

    }

    departure_code = get_airport_code(departure_city, headers)
    arrival_code = get_airport_code(arrival_city, headers)

    # departure_code = "ISB"
    # arrival_code = "LHE"

    print(departure_code, arrival_code)
    if not departure_code or not arrival_code:
        print("Failed to get airport codes.")
    try:
        flights = search_flights(departure_code, arrival_code, adate, ddate)
        return flights
    except Exception as e:
        # Handle any exceptions that might occur during function execution
        return f"."