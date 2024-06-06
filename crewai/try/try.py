import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain_mistralai.chat_models import ChatMistralAI
# from langchain_google_vertexai import VertexAI
# from langchain_openai import AzureChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI 
from test_tools import BestDestinationsTool
search_tool = DuckDuckGoSearchRun()

mistral_api_key = os.environ.get("MISTRAL_API_KEY")
rapid_api_key = os.environ.get("RAPID_API_KEY")
llm_mistral = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-medium")
llm_mistral_coach = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-medium")

# llm_vertex = VertexAI(model_name="gemini-pro")
# llm_azure = AzureChatOpenAI(
#     openai_api_version= "2023-07-01-preview",
#     azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "openai"),
#     azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
#     api_key=os.environ.get("AZURE_OPENAI_KEY")
# )

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


# def main():
#     # Set these to your actual RapidAPI Key and Host
#     headers = {
#         "X-RapidAPI-Key": rapid_api_key,
#         "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
#     }

#     location = "paris"

#     # Task 1: Get geoId for the location
#     geo_id = get_geo_id(location, headers)
#     if geo_id:
#         print(f"GeoId for {location}: {geo_id}")

#         # Task 2: Use geoId to search for hotels
#         hotel_data = get_hotels(geo_id, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax, headers)
#         # print("Hotel search result:", hotel_data)
#         hotels_info = []    
#         for hotel in hotel_data['data']['data']:
#             hotel_info = {
#                 'id': hotel['id'],
#                 'title': hotel['title'],
#                 'primaryInfo': hotel['primaryInfo'],
#                 'bubbleRating': hotel['bubbleRating']['rating'],
#                 'priceForDisplay': hotel['priceForDisplay'],
#                 'priceDetails': hotel['priceDetails']
#             }
#             hotels_info.append(hotel_info)

#         # Creating string representation
#         hotel_info_str = ''
#         for hotel in hotels_info:
#             hotel_info_str += f"Hotel ID: {hotel['id']}\n"
#             hotel_info_str += f"Title: {hotel['title']}\n"
#             hotel_info_str += f"Primary Info: {hotel['primaryInfo']}\n"
#             hotel_info_str += f"Bubble Rating: {hotel['bubbleRating']}\n"
#             hotel_info_str += f"Price for Display: {hotel['priceForDisplay']}\n"
#             hotel_info_str += f"Pricing Details: {hotel['priceDetails']}\n\n"

#         return hotel_info_str
#     else:
#         print(f"Failed to find geoId for {location}")
#         return "."

def main() -> str:

    # Assuming the headers, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax are defined earlier in your code.
    all_hotels_info_str,hotel_info_str = "",""
    # all_hotels_info_str = ""  # This will accumulate hotel information for all locations

    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }


    for location in locations:
        # Task 1: Get geoId for the location
        geo_id = get_geo_id(location, headers)
        if not geo_id:
            print(f"Failed to get GeoId for {location}.")
            continue
        
        print(f"GeoId for {location}: {geo_id}")
        hotel_data = get_hotels(geo_id, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax, headers)

        if not (hotel_data and hotel_data.get('data', {}).get('data')):
            print(f"No hotel data found for {location}.")
            continue

        hotels = hotel_data['data']['data'][:5]

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

# loc = "paris"
# locations = best_destinations_tool.top_destinations
checkIn= "2024-03-18"
checkOut= "2024-03-18"
adults = 1
rooms = 1
rating = 4
priceMin = 2000
priceMax = 100000



openai_api_key = os.getenv("OPENAI_API_KEY")
llm_openai = ChatOpenAI(
    temperature=0,
    openai_api_key = openai_api_key
)

best_destinations_tool = BestDestinationsTool(search_tool, llm_mistral, "Pakistan")
goal_prompt = best_destinations_tool.run()
locations = best_destinations_tool.top_destinations
print(f"Locations: {locations}")
# Create Agents
coach = Agent(
    role='Travel Agent',
    goal= goal_prompt,
    backstory="You're an experienced travel agent with a keen eye for finding the perfect destination for any traveler.",
    expected_output= "Insightful Short Bullet Information for the destinations",
    verbose=True,
    allow_delegation=False,
    # tools=[search_tool],
    llm=llm_mistral_coach
)

influencer = Agent(
    role='Travel Planner',
    goal="Craft short travel plans based on selected destinantions with emoji filled bullets.",
    backstory="You're a renowned travel planner known for your ability to turn any destination into an unforgettable adventure. With a deep understanding of culture, cuisine, and hidden gems, you create personalized itineraries that cater to the interests and desires of every traveler. Your plans are not just about places to visit; they're about experiences that last a lifetime.",
    expected_output= "Emoji filled bullets of short travel plans based on selected destinantions.",
    verbose=True,
    allow_delegation=True,
    llm=llm_mistral
)

critic = Agent( 
    role="Travel Experience Enhancer",
    goal="Provide 200 words insightful feedback to refine and elevate the planned travel experiences",
    backstory="With years of globetrotting under your belt and a keen eye for detail, you've become an expert in identifying what makes a good trip great. Your experiences have taught you the importance of cultural immersion, sustainable travel, and creating moments that resonate on a personal level. Now, you lend your expertise by reviewing travel plans, suggesting enhancements that promise to deepen the traveler's connection with each destination and ensure a more memorable journey.",
    expected_output="200 words insightful feedback",
    verbose=True,
    allow_delegation=True,
    llm=llm_openai
)

hotel = Agent( 
    role = "Hotel Marketing Agent",
    goal = "Provide insightful hotel information to elevate the user experiences based on these details: " + main(),
    backstory = "As a specialized AI agent programmed to fetch hotel information from the TripAdvisor API, you're equipped with advanced algorithms to extract and interpret data about various hotels.",    
    verbose=True,
    allow_delegation=True,
    # tools=[toolss],
    llm=llm_mistral
)

# Create Tasks  
task_search = Task(
    description="Compile a report listing travel spots presented in bullet points",
    agent=coach,
    expected_output= "Insightful short Information for the destinations in bullet points",
)

task_post = Task(
    description="Create a short post with a brief headline and a maximum of 200 words",
    agent=influencer,
    expected_output= "Emoji filled short five bullets of detailed travel plans based on selected cities.",
)

task_critique = Task(
    description="Refine the post for brevity, ensuring an engaging headline and keeping within a 200-word limit",
    agent=critic,
    expected_output="Refine the post for brevity, ensuring an engaging headline and keeping within a 200-word limit",
)

task_hotel = Task(
    description="Craft an engaging hotel recommendation post that captivates readers with succinct, lively bullet points and emojis. Ensure your post remains within a 200-word limit, providing enticing details about each hotel's amenities, location highlights, and unique offerings. Infuse your recommendations with emojis to convey excitement and appeal to readers' emotions. Your goal is to entice readers to explore these hotels further and inspire them to book their next memorable stay.",
    agent=hotel,
    expected_output="Craft an engaging hotel recommendation post that captivates readers with succinct, lively bullet points and emojis. Ensure your post remains within a 200-word limit, providing enticing details about each hotel's amenities, location highlights, and unique offerings. Infuse your recommendations with emojis to convey excitement and appeal to readers' emotions. Your goal is to entice readers to explore these hotels further and inspire them to book their next memorable stay.",
)


# Create Crew
crew = Crew(
    agents=[coach, influencer, critic, hotel],
    tasks=[task_search, task_post, task_critique, task_hotel],
    verbose=2,
    process=Process.sequential
)

# Get your crew to work!
result = crew.kickoff()

print("#############")
print(result)
# main(loc)


