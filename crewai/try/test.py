from crewai import Agent, Task, Crew, Process
# from crewai_tools import tool
import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain_mistralai.chat_models import ChatMistralAI
# from langchain_google_vertexai import VertexAI
# from langchain_openai import AzureChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import DuckDuckGoSearchResults
from langchain_openai import ChatOpenAI 
from langchain_core.messages import HumanMessage
from test_tools import BestDestinationsTool

# search_tool = DuckDuckGoSearchRun()

mistral_api_key = os.environ.get("MISTRAL_API_KEY")
llm_mistral = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-medium")
llm_mistral_coach = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-medium")

# Placeholder for the actual user input location
loc = "Karachi"

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# Customize the API wrapper as needed, for example, to search within a specific region or time frame.
# wrapper = DuckDuckGoSearchAPIWrapper(region="us-en", time="d", max_results=5)  # Adjust parameters as needed

# Initialize DuckDuckGoSearchResults with the customized API wrapper.
search_tool = DuckDuckGoSearchResults()
search_tool2 = DuckDuckGoSearchResults()

# Define a task to perform the search and process the results
def find_best_destinations(location):
    # Format the search query correctly
    search_query = f"Find the best five destinations in {location} for vacation"
    # Execute the search using the tool
    search_results = search_tool.run(search_query)
    # print("Search Results:", search_results)
    
    # Assuming `mistral` is a function or an object with a method to process text.
    # This call should be adjusted to fit how your LLM is implemented.
    # Here, we're asking Mistral to summarize the results or extract specific information.
    llm_query = f"Extract the names of the top 5 destinations for a vacation in {location} based on the following information. NOTE: Strictly follow the output format. Output format should be like this: name1,name2,name3,name4,name5,: {search_results}"
     
    
    try:
        # Call to Mistral with the query, adjust according to your setup
        messages = [HumanMessage(content=llm_query)]
        output = llm_mistral.invoke(messages)
        print(output)
        output = output.content.split(",")[:5]
        print(output)

        
        # Process the LLM's response to extract the destination names.
        # This step is highly dependent on the format of the LLM's response.
        # Here, we're assuming `llm_response` contains the extracted names directly.
        # top_destinations = llm_response.split(',')  # A simple split, assuming a comma-separated list of destinations
    except Exception as e:
        print(f"Error processing LLM response: {e}")
        # top_destinations = []
    
    # return top_destinations
# Define your agent
search_tool = DuckDuckGoSearchResults()
llm_mistral = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-medium")
best_destinations_tool = BestDestinationsTool(search_tool, llm_mistral, "Karachi")

coach = Agent(
    role='Travel Agent',
    goal=f"Provide a curated list of the top five vacation destinations within a specified location. Those Locations are: {best_destinations_tool.run()}",
    backstory="You're an experienced travel agent with a keen eye for finding the perfect destination for any traveler.",
    verbose=True,
    allow_delegation=False,
    # tools=[best_destinations_tool],  # Ensure the search tool is correctly referenced here
    llm=llm_mistral_coach
)

# Create Tasks  
task_search = Task(
    description="Compile a report listing all five Destinations, presented in bullet points",
    expected_output='A bullet list summary of the five destinations',
    agent=coach
)


# Set up and run the crew
crew = Crew(agents=[coach], tasks=[task_search], process=Process.sequential)

# print(find_best_destinations("Karachi"))
result = crew.kickoff()
print(result)
# best_destinations_tool = BestDestinationsTool(search_tool, llm_mistral, "Karachi")

# # Directly invoke the tool's run method to see if it works as expected
# try:
#     result = best_destinations_tool.run()
#     print("Tool Output:", result)
#     print(f"test.py: {best_destinations_tool.top_destinations}")
# except Exception as e:
#     print("Error running tool:", e)

