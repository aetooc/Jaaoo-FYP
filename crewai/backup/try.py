import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_google_vertexai import VertexAI
# from langchain_openai import AzureChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI 
search_tool = DuckDuckGoSearchRun()

mistral_api_key = os.environ.get("MISTRAL_API_KEY")
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
    querystring = {"geoId":geo_id,"checkIn":checkIn,"checkOut":checkOut,"pageNumber":"1","adults":adults,"rooms":rooms,"currencyCode":"PKR","rating":rating,"priceMin":priceMin,"priceMax":priceMax}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def main(location):
    # Set these to your actual RapidAPI Key and Host
    headers = {
        "X-RapidAPI-Key": "f6486da12amsh6bb194f4a42c4a2p1df1b9jsn07dd8eb24961",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    location = location

    # Task 1: Get geoId for the location
    geo_id = get_geo_id(location, headers)
    if geo_id:
        print(f"GeoId for {location}: {geo_id}")

        # Task 2: Use geoId to search for hotels
        hotel_data = get_hotels(geo_id, checkIn, checkOut, adults, rooms, rating, priceMin, priceMax, headers)
        print("Hotel search result:", hotel_data)
    else:
        print(f"Failed to find geoId for {location}")

loc = "karachi"
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


# Create Agents
coach = Agent(
    role='Travel Agent',
    goal=f"Find the best destinations in {loc} for vacation",
    backstory="You're an experienced travel agent with a keen eye for finding the perfect destination for any traveler.",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm_mistral_coach
)

influencer = Agent(
    role='Travel Planenr',
    goal="Craft detailed travel plans based on selected destinantions with emoji filled bullets.",
    backstory="You're a renowned travel planner known for your ability to turn any destination into an unforgettable adventure. With a deep understanding of culture, cuisine, and hidden gems, you create personalized itineraries that cater to the interests and desires of every traveler. Your plans are not just about places to visit; they're about experiences that last a lifetime.",
    verbose=True,
    allow_delegation=True,
    llm=llm_mistral
)

critic = Agent( 
    role="Travel Experience Enhancer",
    goal="Provide 200 words insightful feedback to refine and elevate the planned travel experiences",
    backstory="With years of globetrotting under your belt and a keen eye for detail, you've become an expert in identifying what makes a good trip great. Your experiences have taught you the importance of cultural immersion, sustainable travel, and creating moments that resonate on a personal level. Now, you lend your expertise by reviewing travel plans, suggesting enhancements that promise to deepen the traveler's connection with each destination and ensure a more memorable journey.",
    verbose=True,
    allow_delegation=True,
    llm=llm_openai
)

# Create Tasks  
task_search = Task(
    description="Compile a report listing at least 5 new AI and tech skills, presented in bullet points",
    agent=coach
)

task_post = Task(
    description="Create a LinkedIn post with a brief headline and a maximum of 200 words, focusing on upcoming AI and tech skills",
    agent=influencer
)

task_critique = Task(
    description="Refine the post for brevity, ensuring an engaging headline (no more than 30 characters) and keeping within a 200-word limit",
    agent=critic
)


# Create Crew
crew = Crew(
    agents=[coach, influencer, critic],
    tasks=[task_search, task_post, task_critique],
    verbose=2,
    process=Process.sequential 
)


# Get your crew to work!
result = crew.kickoff()

print("#############")
print(result)
main(loc)


