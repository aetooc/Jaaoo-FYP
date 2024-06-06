import os
import requests

rapid_api_key = os.environ.get("RAPID_API_KEY")


def GetCarDestination(location):


    url = "https://booking-com15.p.rapidapi.com/api/v1/cars/searchDestination"
    querystring = {"query": location}

    # Headers including your RapidAPI key and host
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com",
        "User-agent": "Car_Rental"

    }

    # Make the GET request to the API
    response = requests.get(url, headers=headers, params=querystring)

    # Parse the JSON response
    data = response.json()

    if data['status'] and data['message'] == "Success":
        # Assuming the first and second locations are pickup and dropoff respectively
        if len(data['data']) >= 2:
            pickup_location = data['data'][0]
            dropoff_location = data['data'][1]

            # Extract coordinates
            pickup_lat = pickup_location['coordinates']['latitude']
            pickup_long = pickup_location['coordinates']['longitude']
            dropoff_lat = dropoff_location['coordinates']['latitude']
            dropoff_long = dropoff_location['coordinates']['longitude']

            # Store the coordinates in the specified variables
            print(
                f"Pickup Location: {pickup_location['name']} - Latitude: {pickup_lat}, Longitude: {pickup_long}")
            print(
                f"Dropoff Location: {dropoff_location['name']} - Latitude: {dropoff_lat}, Longitude: {dropoff_long}")

            return pickup_lat, pickup_long, dropoff_lat, dropoff_long
        else:
            print("Not enough locations provided.")
            return ""
    else:
        print("API call was not successful.")
        return ""


def GetCarRentals( location, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, checkIn, checkOut):

    url = "https://booking-com15.p.rapidapi.com/api/v1/cars/searchCarRentals"

    querystring = {"pick_up_latitude": pickup_lat, "pick_up_longitude": pickup_lon, "drop_off_latitude": dropoff_lat, "drop_off_longitude": dropoff_lon,
                   "pick_up_date": checkIn, "drop_off_date": checkOut, "pick_up_time": "10:00", "drop_off_time": "10:00", "currency_code": "USD"}

    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com",
        "User-agent": "Car_Rental"

    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    # print(data)
    # data = {'status': True, 'message': 'Success', 'timestamp': 1710864121369, 'data': {'discount_banner': None, 'is_genius_location': False, 'title': 'Car rentals', 'filter': [{'title': 'Air Conditioning', 'type': 'single_option', 'layout': {'layout_type': 'list'}, 'id': 'hasAirConditioning', 'categories': [{'name': '', 'id': 'hasAirConditioning::true'}]}], 'search_key': 'eyJkcml2ZXJzQWdlIjozMCwiZHJvcE9mZkRhdGVUaW1lIjoiMjAyNC0wMy0yMVQxMDowMDowMCIsImRyb3BPZmZMb2NhdGlvbiI6IjUzLjMwOTcsLTExMy41OCIsImRyb3BPZmZMb2NhdGlvblR5cGUiOiJMQVRMT05HIiwicGlja1VwRGF0ZVRpbWUiOiIyMDI0LTAzLTIwVDEwOjAwOjAwIiwicGlja1VwTG9jYXRpb24iOiI1My4zMDk3LC0xMTMuNTgiLCJwaWNrVXBMb2NhdGlvblR5cGUiOiJMQVRMT05HIiwicmVudGFsRHVyYXRpb25JbkRheXMiOjEsInNlcnZpY2VGZWF0dXJlcyI6WyJOT19PUEFRVUVTIiwiU1VQUkVTU19GSVhFRF9QUklDRV9WRUhJQ0xFUyIsIklOQ0xVREVfUFJPRFVDVF9SRUxBVElPTlNISVBTIl19', 'search_results': [], 'sort': [{'identifier': 'recommended', 'title_tag': 'tr.searchresults.sortBy.recommended', 'name': 'Recommended – best first'}, {'name': 'Price - lowest first', 'title_tag': 'tr.searchresults.sortBy.price.lowHigh', 'identifier': 'price_low_to_high'}], 'meta': {'response_code': 200}, 'content': {'discountBanner': None, 'dsaBanner': None, 'items': []}, 'type': 'cars', 'provider': 'rentalcars', 'count': 0}}


    if not data.get("status") or data.get("message") != "Success":
        print("Data retrieval was unsuccessful.")
        return ""

    results = data.get("data", {}).get("search_results", [])
    
    if not results:
        print("No Vehicle Available For The Current Destination!")
        return ""

    # Initialize an empty string to accumulate the results
    all_results = f"\nTop Five Car Rental Listings in {location}:\n"

    # Process and accumulate information for up to five entries
    for i, result in enumerate(results[:5]):  # Directly limit to 5 entries with slice
        vehicle_name = result.get("vehicle_info", {}).get("v_name", "N/A")
        deposit = result.get("pricing_info", {}).get("deposit", "N/A")
        price = result.get("pricing_info", {}).get("price", "N/A")
        no_of_ratings = result.get("rating_info", {}).get("no_of_ratings", "N/A")
        pickup_location = result.get("route_info", {}).get("pickup", {}).get("name", "N/A")
        dropoff_location = result.get("route_info", {}).get("dropoff", {}).get("name", "N/A")

        all_results += (f"\nVehicle Name: {vehicle_name}, \nPrice: ${price}, \nDeposit: ${deposit}, \n"
                        f"No of Ratings: {no_of_ratings}, \nPickup: {pickup_location}, \n"
                        f"Dropoff: {dropoff_location}\n" + "-"*80 + "\n")

    print(all_results)
    return all_results

def GetCarRental(location, checkIn, checkOut):
    pickup_lat, pickup_lon, dropoff_lat, dropoff_lon = GetCarDestination(location)
    GetCarRentals(location, pickup_lat, pickup_lon, pickup_lat, pickup_lon, checkIn, checkOut)
    return ""


# GetCarRental("New York", "2024-03-23", "2024-03-24")