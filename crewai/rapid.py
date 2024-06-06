# import requests

# url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"

# querystring = {"query":"london"}

# headers = {
# 	"X-RapidAPI-Key": "f6486da12amsh6bb194f4a42c4a2p1df1b9jsn07dd8eb24961",
# 	"X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())

# import requests

# url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/getHotelsFilter"

# querystring = {"geoId":"39598","checkIn":"2024-03-14","checkOut":"2024-03-21"}

# headers = {
# 	"X-RapidAPI-Key": "f6486da12amsh6bb194f4a42c4a2p1df1b9jsn07dd8eb24961",
# 	"X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())

import requests


def get_geo_id(location, headers):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"
    querystring = {"query": location}
    response = requests.get(url, headers=headers, params=querystring)
    geo_data = response.json()
    if 'data' in geo_data and len(geo_data['data']) > 0:
        # Return the first geoId found
        return geo_data['data'][0]['geoId']
    else:
        # Return None if no geoId is found
        return None


def get_hotels(geo_id, headers):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/getHotelsFilter"
    querystring = {
        "geoId": geo_id,
        "checkIn": "2024-03-13",
        "checkOut": "2024-03-14"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def main():
    # Set these to your actual RapidAPI Key and Host
    headers = {
        "X-RapidAPI-Key": "f6486da12amsh6bb194f4a42c4a2p1df1b9jsn07dd8eb24961",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    location = input("Enter a location (e.g., Paris): ").strip()

    # Task 1: Get geoId for the location
    geo_id = get_geo_id(location, headers)
    if geo_id:
        print(f"GeoId for {location}: {geo_id}")

        # Task 2: Use geoId to search for hotels
        hotel_data = get_hotels(geo_id, headers)
        print("Hotel search result:", hotel_data)
    else:
        print(f"Failed to find geoId for {location}")


if __name__ == "__main__":
    main()
