import os
from crewai import Agent, Task, Crew, Process
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI 
search_tool = DuckDuckGoSearchRun()

mistral_api_key = os.environ.get("MISTRAL_API_KEY")
llm_mistral = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-medium")
llm_mistral_travel_expert = ChatMistralAI(mistral_api_key=mistral_api_key, model="mistral-medium")

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_openai = ChatOpenAI(
    temperature=0,
    openai_api_key = openai_api_key
)

# Create Agents for Travel Planning
travel_researcher = Agent(
    role='Travel Researcher',
    goal="Identify top 5 travel destinations for 2024 with activities and accommodation options",
    backstory="You're experienced in researching and compiling engaging travel plans.",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm_mistral_travel_expert
)

travel_blogger = Agent(
    role='Travel Blogger',
    goal="Create captivating travel itinerary posts for each destination",
    backstory="You specialize in creating informative and visually appealing travel content.",
    verbose=True,
    allow_delegation=True,
    llm=llm_mistral
)

travel_advisor = Agent(
    role='Travel Advisor',
    goal="Review travel plans and suggest improvements for a better travel experience",
    backstory="You offer expert advice on optimizing travel itineraries for adventurers.",
    verbose=True,
    allow_delegation=True,
    llm=llm_openai
)

# Create Tasks for Travel Planning
task_research = Task(
    description="Research and list the top 5 travel destinations for 2024, including activities and accommodation options for each.",
    agent=travel_researcher
)

task_blog_post = Task(
    description="Draft detailed itineraries for the top 5 travel destinations, ensuring each post is engaging and informative.",
    agent=travel_blogger
)

task_review = Task(
    description="Critically review the itineraries, suggesting improvements for activities, accommodations, and overall travel experience.",
    agent=travel_advisor
)

# Create Crew for Travel Planning
travel_crew = Crew(
    agents=[travel_researcher, travel_blogger, travel_advisor],
    tasks=[task_research, task_blog_post, task_review],
    verbose=2,
    process=Process.sequential 
)

# Execute the travel planning process
travel_plans_result = travel_crew.kickoff()

print("#############")
print(travel_plans_result)
