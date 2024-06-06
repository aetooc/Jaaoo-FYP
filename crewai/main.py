import os
import re
import sys
import requests
import firbase
from io import StringIO
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from langchain_mistralai.chat_models import ChatMistralAI
# from langchain_google_vertexai import VertexAI
# from langchain_openai import AzureChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
# from langchain_openai import ChatOpenAI 
from car_rental_booking import GetCarRental
from restaurants import GetRestaurants
from flights import GetFlights
from airbnb import GetAirbnb
from news import GetNews
search_tool = DuckDuckGoSearchRun()

mistral_api_key = os.environ.get("MISTRAL_API_KEY")
rapid_api_key = os.environ.get("RAPID_API_KEY")
llm_mistral = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-medium")
llm_mistral_coach = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-medium")

# # llm_vertex = VertexAI(model_name="gemini-pro")
# # llm_azure = AzureChatOpenAI(
# #     openai_api_version= "2023-07-01-preview",
# #     azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "openai"),
# #     azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
# #     api_key=os.environ.get("AZURE_OPENAI_KEY")
# # )

headers = {
    "X-RapidAPI-Key": rapid_api_key,
    "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com",
    "User-agent": "TripAdvisor"

}

locations = [] #  Global

def append_to_file(content):
    """Append given content to a file."""
    with open('temp.txt', 'a') as file:
        file.write(content)

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


def get_hotels(geo_id, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax, headers):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotels"
    querystring = {"geoId":geo_id,"checkIn":checkIn,"checkOut":checkOut,"pageNumber":"1","adults":adults,"rooms":rooms,"currencyCode":"USD","rating":rating,"priceMin":priceMin,"priceMax":priceMax}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def find_best_destinations(location):
    # Format the search query correctly
    search_query = f"Find the best destinations in {location} for a vacation, duration of {duration_string} days" #change this
    # Execute the search using the tool
    search_results = search_tool.run(search_query)
  
    llm_query = f"Extract the names of the top best destinations mentioned in the following snippets about {location}, and format them as a comma-separated list: {search_results}"
     
    
    messages = [HumanMessage(content=llm_query)]
    output = llm_mistral.invoke(messages)
    locations = output.content.split(",")[:2]
    output = ", ".join(locations)
    return f"Provide a insigtful information of these destinations: {output}"

def find_best_cities(location):
    # Format the search query correctly
    search_query = f"Find the best two cities in {location} for vacation"
    # Execute the search using the tool
    search_results = search_tool.run(search_query)
  
    llm_query = f"Extract the names of the best two cities mentioned in the following snippets about {location}. If fewer than two cities are mentioned, add additional popular cities from {location} to complete the list. Format the output as a comma-separated list with no additional notes. {search_results}"
     
    check = False
    while not check:
        messages = [HumanMessage(content=llm_query)]
        output = llm_mistral.invoke(messages)
        cities = output.content.split(",")[:2]
        
        # Using a regex to check if locations are valid (only letters and spaces).
        if all(re.match("[A-Za-z .-]+$", city.strip()) for city in cities):
            check = True
            print(cities, flush=True)
        else:
            # Handle invalid locations.
            print(f"Locations are not valid, adjusting query or logging the issue.: {cities}", flush=True)

    return cities

def main():
    # Set these to your actual RapidAPI Key and Host
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com",
        "User-agent": "Trip Advisor"

    }
    # location = "Islamabad"  
    # Task 1: Get geoId for the location
    geo_id = get_geo_id(location, headers)
    if geo_id:
        print(f"GeoId for {location}: {geo_id}", flush=True)

        # Task 2: Use geoId to search for hotels
        hotel_data = get_hotels(geo_id, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax, headers)
        # print("Hotel search result:", hotel_data)
        hotels_info = []
        for hotel in hotel_data['data']['data'][:2]:
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
        print(f"Failed to find geoId for {location}", flush=True)
        return "."

def for_country(locations):

    # Assuming the headers, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax are defined earlier in your code.
    all_hotels_info_str,hotel_info_str = "",""
    # all_hotels_info_str = ""  # This will accumulate hotel information for all locations

    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com",
        "User-agent": "TripAdvisor"

    }


    for location in locations:
        # Task 1: Get geoId for the location
        geo_id = get_geo_id(location, headers)
        if not geo_id:
            print(f"Failed to get GeoId for {location}.", flush=True)
            continue
        
        print(f"GeoId for {location}: {geo_id}", flush=True)
        hotel_data = get_hotels(geo_id, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax, headers)

        if not (hotel_data and hotel_data.get('data', {}).get('data')):
            print(f"No hotel data found for {location}.", flush=True)
            continue

        hotels = hotel_data['data']['data'][:2]

        hotels_info = [{
            'id': hotel['id'],
            'title': hotel['title'],
            'primaryInfo': hotel['primaryInfo'],
            'bubbleRating': hotel.get('bubbleRating', {}).get('rating', 'N/A'),
            'priceForDisplay': hotel.get('priceForDisplay', 'N/A'),
            'priceDetails': hotel.get('priceDetails', 'N/A')
        } for hotel in hotels]
        
        hotel_info_str = f"Hotels in {location}:\n"  # Add location name to the string
        for hotel in hotels_info:
            hotel_info_str += f"Hotel ID: {hotel['id']}\n"
            hotel_info_str += f"Title: {hotel['title']}\n"
            hotel_info_str += f"Primary Info: {hotel['primaryInfo']}\n"
            hotel_info_str += f"Bubble Rating: {hotel['bubbleRating']}\n"
            hotel_info_str += f"Price for Display: {hotel['priceForDisplay']}\n"
            hotel_info_str += f"Pricing Details: {hotel['priceDetails']}\n\n"

        all_hotels_info_str += hotel_info_str + "\n\n"
    # print(all_hotels_info_str)
    return all_hotels_info_str






# openai_api_key = os.getenv("OPENAI_API_KEY")
# llm_openai = ChatOpenAI(
#     temperature=0,
#     openai_api_key = openai_api_key
# )
if __name__ == "__main__":
    # Actual Parameters without firebase
    # userHome = "Dubai"
    # userLocation = "Sydney"
    # # locations = find_best_cities(userLocation)
    # # for location in locations:
    # location = userLocation
    # loc = userLocation
    # checkIn= "2024-06-07"
    # checkOut= "2024-06-10"
    # adults = "2"
    # rooms = "1"     
    # rating = "4"
    # priceMin = "3000"
    # priceMax = "5000"
    # checkIn_date = datetime.strptime(checkIn, "%Y-%m-%d")
    # checkOut_date = datetime.strptime(checkOut, "%Y-%m-%d")

    # # Calculate the duration between the check-in and check-out dates
    # duration = checkOut_date - checkIn_date

    # # Format the duration as a string
    # # Note: duration.days will give you the number of days between the dates
    # duration_string = f"{duration.days}"
    # print(f"duration_string: {duration_string}")

    firebase_parameters = firbase.get_document_fields("Users", "iN8eRU7kXTthHBTRpHSk")
    userHome = firebase_parameters['userHome']
    userLocation = firebase_parameters['userLocation']
    # locations = find_best_cities(userLocation)
    # for location in locations:
    location = userLocation
    loc = userLocation
    checkIn= str(firebase_parameters['checkIn'])
    checkOut= str(firebase_parameters['checkOut'])
    adults = firebase_parameters['adults']
    rooms = firebase_parameters['rooms']     
    rating = firebase_parameters['rating']
    priceMin = firebase_parameters['priceMin']
    priceMax = firebase_parameters['priceMax']
    checkIn_date = datetime.strptime(checkIn, "%Y-%m-%d")
    checkOut_date = datetime.strptime(checkOut, "%Y-%m-%d")

    # Calculate the duration between the check-in and check-out dates
    duration = checkOut_date - checkIn_date

    # Format the duration as a string
    # Note: duration.days will give you the number of days between the dates
    duration_string = f"{duration.days}"
    print(f"duration_string: {duration_string}", flush=True)

        # Create Agents
    coach = Agent(
        role='Travel Agent',
        goal=find_best_destinations(loc),
        backstory=f"You're an experienced travel agent with a keen eye for finding the perfect destination for any traveler, traveling for {duration_string} days duration, with budget ranging from {priceMin} to {priceMax}.", #change this
        verbose=True,
        allow_delegation=False,
        # tools=[search_tool],
        llm=llm_mistral_coach
    )

    influencer = Agent(
        role='Travel Planenr',
        goal=f"Craft detailed day wise travel plans with bullet points based on selected destinantions, traveling for {duration_string} days duration, with budget ranging from {priceMin} to {priceMax}",
        backstory="You're a renowned travel planner known for your ability to turn any destination into an unforgettable adventure. With a deep understanding of culture, cuisine, and hidden gems, you create bullet pointed personalized itineraries that cater to the interests and desires of every traveler. Your plans are not just about places to visit; they're about experiences that last a lifetime.",
        verbose=True,
        allow_delegation=True,
        llm=llm_mistral
    )

    critic = Agent( 
        role="Travel Experience Enhancer",
        goal="Provide two hundred words insightful feedback to refine and elevate the planned travel experiences",
        backstory="With years of experience under your belt and a keen eye for detail, you've become an expert in identifying what makes a good trip great. Your experiences have taught you the importance of cultural immersion, sustainable travel, and creating moments that resonate on a personal level. Now, you lend your expertise by reviewing travel plans, suggesting enhancements that promise to deepen the traveler's connection with each destination and ensure a more memorable journey.",
        verbose=True,
        allow_delegation=True,
        llm=llm_mistral
    )

    hotel = Agent( 
        role = "Hotel Marketing Agent",
        goal = "Provide insightful and hotel information to elevate the user experiences" + main(),
        backstory = "As a specialized AI agent programmed to fetch hotel information from the TripAdvisor API, you're equipped with advanced algorithms to extract and interpret data about various hotels.",
        verbose=True,
        allow_delegation=True,
        # tools=[toolss],
        llm=llm_mistral
    )

    # Create Tasks  
    task_search = Task(
        description="Insightful precise information for the destinations in bullet points",
        agent=coach
    )

    task_post = Task(
        description="Craft detailed travel plans based on selected destinantions with bullets.",
        agent=influencer
    )

    task_critique = Task(
        description="Refine the post for brevity, ensure an engaging content and keeping within a two hundred words limit",
        agent=critic
    )

    task_hotel = Task(
        description="Craft an engaging hotel recommendation that captivates readers with succinct, lively bullet points. Ensure it remains within a two hundred words limit, providing enticing details about each hotel's amenities, location highlights, and unique offerings. Infuse your recommendations to convey excitement and appeal to readers' emotions. Your goal is to entice readers to explore these hotels further and inspire them to book their next memorable stay.",
        agent=hotel
    )


    # Create Crew
    crew = Crew(
        agents=[coach, influencer, critic, hotel],
        tasks=[task_search, task_post, task_critique, task_hotel],
        verbose=2,
        process=Process.sequential
    )


# Get your crew to work!
    # result = crew.kickoff()
    # for task in crew.tasks:
    #     result = task.execute()  # Assuming a method like this exists or similar logic
    #     append_to_file(str(result))
    # print("#############")
    # print(result)

    # Temporarily redirect stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = StringIO()  # Create a StringIO object to capture output
    sys.stderr = StringIO()  # Optional: Capture stderr if needed

    try:
        # Execute your crew tasks
        crew.kickoff()

        # Capture the output
        captured_output = sys.stdout.getvalue()
        captured_errors = sys.stderr.getvalue()  # Optional: Capture stderr if needed
    finally:
        # Restore original stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    # At this point, `captured_output` contains the stdout from your crew's execution
    print("Captured Output:", flush=True)
    print(captured_output, flush=True)
    append_to_file(captured_output)

    # Optional: Print errors if you're also capturing stderr
    print("Captured Errors:", flush=True)
    print(captured_errors, flush=True)
    append_to_file(captured_errors)

    # append_to_file(result)
    # llm_query = f"Make given google flights json data in human readable important data" + GetFlights("Islamabad", "Karachi", "2024-03-18", "2024-03-22")
    llm_query = f"Extract the air ticket details from the Google Flights JSON data, including departure and arrival airports, flight numbers, dates, times, and price. The data is stored in the 'other_flights' list, and each flight is represented as a dictionary with keys such as 'departure_airport', 'arrival_airport', 'flight_number', 'price', and 'flights', which contains a list of dictionaries with the details of each leg of the flight. The relevant information should be extracted and formatted in a clear and concise manner. If there's this error statement: 'Google Flights hasn't returned any results for this query.' or any other error, Simply Return that No Flights Are Available At The Moment " + GetFlights(userHome, location, checkIn, checkOut)
        

    messages = [HumanMessage(content=llm_query)]
    output = llm_mistral.invoke(messages)
    print(output.content, flush=True)
    append_to_file(output.content)

    airbnb_data = GetAirbnb(loc, checkIn, checkOut, adults)
    append_to_file(airbnb_data)

    restaurants_data  = GetRestaurants(loc)
    append_to_file(restaurants_data)

    car_rental_data = GetCarRental(loc, checkIn, checkOut)
    append_to_file(car_rental_data)

    news_data = GetNews(loc)    
    append_to_file(news_data)




    # main(loc)

