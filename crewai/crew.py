import os
import requests

class RapidAPIHotelSearch:
    def __init__(self, api_key):
        self.api_key = "f6486da12amsh6bb194f4a42c4a2p1df1b9jsn07dd8eb24961"
        self.base_url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels"  # Update this with the actual API base URL

    def get_hotels(self, location):
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com" # Update this with the actual host from Rapid API
        }
        params = {"destination": location}  # Dynamically sets the destination based on user input
        response = requests.get(f"{self.base_url}/getHotelsFilter", headers=headers, params=params)
        if response.status_code == 200:
            return response.json()  # Returns the API response as a JSON object
        else:
            return {"error": "Failed to fetch hotel data", "statusCode": response.status_code}

# Simulation of a task-oriented approach with the hotel search tool
def execute_hotel_search_task(location, hotel_search_tool):
    print(f"Searching for hotels in {location}...")
    hotel_data = hotel_search_tool.get_hotels(location)
    
    if "error" not in hotel_data:
        # Assuming the API returns a list of hotels in 'hotels' key
        hotels = hotel_data.get('hotels', [])
        if hotels:
            print(f"Found {len(hotels)} hotels in {location}:")
            for hotel in hotels:
                # Assuming each hotel data includes 'name' and 'rating'
                print(f"- {hotel['name']} with rating {hotel['rating']}")
        else:
            print(f"No hotels found in {location}.")
    else:
        print(f"Error fetching hotel data for {location}: {hotel_data['error']} statusCode: {hotel_data['statusCode']}")

if __name__ == "__main__":
    # api_key = os.getenv("RAPIDAPI_KEY")  # Make sure to set your RapidAPI key in your environment variables
    # if not api_key:
    #     raise ValueError("RAPIDAPI_KEY environment variable not set")

    hotel_search_tool = RapidAPIHotelSearch(api_key="f6486da12amsh6bb194f4a42c4a2p1df1b9jsn07dd8eb24961")

    # Example usage with user input
    location = input("Enter a location to search for hotels (e.g., London, Paris): ").strip()
    execute_hotel_search_task(location, hotel_search_tool)
