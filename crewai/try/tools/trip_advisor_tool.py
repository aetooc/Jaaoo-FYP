# def get_geo_id(location, headers):
#     url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"
#     querystring = {"query": location}
#     response = requests.get(url, headers=headers, params=querystring)
#     geo_data = response.json()
#     if 'data' in geo_data and len(geo_data['data']) > 0:
#         # Return the first geoId found
#         return geo_data['data'][0]['geoId']
#     else:
#         # Return None if no geoId is found
#         return None


# def get_hotels(geo_id, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax, headers):
#     url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotels"
#     querystring = {"geoId":geo_id,"checkIn":checkIn,"checkOut":checkOut,"pageNumber":"1","adults":adults,"rooms":rooms,"currencyCode":"PKR","rating":rating,"priceMin":priceMin,"priceMax":priceMax}
#     response = requests.get(url, headers=headers, params=querystring)
#     return response.json()


# def main(location):
#     # Set these to your actual RapidAPI Key and Host
#     headers = {
#         "X-RapidAPI-Key": "f6486da12amsh6bb194f4a42c4a2p1df1b9jsn07dd8eb24961",
#         "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
#     }

#     location = location

#     # Task 1: Get geoId for the location
#     geo_id = get_geo_id(location, headers)
#     if geo_id:
#         print(f"GeoId for {location}: {geo_id}")

#         # Task 2: Use geoId to search for hotels
#         hotel_data = get_hotels(geo_id, headers)
#         print("Hotel search result:", hotel_data)
#     else:
#         print(f"Failed to find geoId for {location}")

import requests

class TripAdvisorTool:
    def __init__(self):
        self.headers = {
        "X-RapidAPI-Key": "f6486da12amsh6bb194f4a42c4a2p1df1b9jsn07dd8eb24961",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
        }

    def get_geo_id(self, location):
        url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation"
        querystring = {"query": location}
        response = requests.get(url, headers=self.headers, params=querystring)
        geo_data = response.json()
        if 'data' in geo_data and len(geo_data['data']) > 0:
            # Return the first geoId found
            return geo_data['data'][0]['geoId']
        else:
            # Return None if no geoId is found
            return None

    def get_hotels(self, geo_id, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax):
        url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotels"
        querystring = {
            "geoId": geo_id,
            "checkIn": checkIn,
            "checkOut": checkOut,
            "pageNumber": "1",
            "adults": adults,
            "rooms": rooms,
            "currencyCode": "PKR",
            "rating": rating,
            "priceMin": priceMin,
            "priceMax": priceMax
        }
        response = requests.get(url, headers=self.headers, params=querystring)
        return response.json()

    def main(self):
        location = "karachi"
        checkIn= "2024-03-18"
        checkOut= "2024-03-18"
        adults = 1
        rooms = 1
        rating = 4
        priceMin = 2000
        priceMax = 100000

        # Task 1: Get geoId for the location
        geo_id = self.get_geo_id(location)
        if geo_id:
            print(f"GeoId for {location}: {geo_id}")

            # Task 2: Use geoId to search for hotels
            hotel_data = self.get_hotels(geo_id, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax)
            # print("Hotel search result:", hotel_data)
            hotels_info = []
            for hotel in hotel_data['data']['data']:
                hotel_info = {
                    'id': hotel['id'],
                    'title': hotel['title'],
                    'primaryInfo': hotel['primaryInfo'],
                    'bubbleRating': hotel['bubbleRating']['rating'],
                    'priceForDisplay': hotel['priceForDisplay'],
                    'priceDetails': hotel['priceDetails']
                }
                hotels_info.append(hotel_info)

            # Creating string representation
            hotel_info_str = ''
            for hotel in hotels_info:
                hotel_info_str += f"Hotel ID: {hotel['id']}\n"
                hotel_info_str += f"Title: {hotel['title']}\n"
                hotel_info_str += f"Primary Info: {hotel['primaryInfo']}\n"
                hotel_info_str += f"Bubble Rating: {hotel['bubbleRating']}\n"
                hotel_info_str += f"Price for Display: {hotel['priceForDisplay']}\n"
                hotel_info_str += f"Pricing Details: {hotel['priceDetails']}\n\n"

            return hotel_info_str
        else:
            print(f"Failed to find geoId for {location}")
