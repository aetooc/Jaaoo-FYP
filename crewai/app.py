import os
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

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_openai = ChatOpenAI(
    temperature=0,
    openai_api_key = openai_api_key
)

# Create Agents
coach = Agent(
    role='Senior Career Coach',
    goal="Discover and examine key tech and AI career skills for 2024",
    backstory="You're an expert in spotting new trends and essential skills in AI and technology.",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm_mistral_coach
)

influencer = Agent(
    role='LinkedIn Influencer Writer',
    goal="Write catchy, emoji-filled LinkedIn posts within 200 words",
    backstory="You're a specialised writer on LinkedIn, focusing on AI and technology.",
    verbose=True,
    allow_delegation=True,
    llm=llm_mistral
)

critic = Agent(
    role='Expert Writing Critic',
    goal="Give constructive feedback on post drafts",
    backstory="You're skilled in offering straightforward, effective advice to tech writers. Ensure posts are concise, under 200 words, with emojis and hashtags.",
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
