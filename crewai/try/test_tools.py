# from crewai_tools import tool
from crewai_tools import BaseTool  
from langchain_core.messages import HumanMessage
from pydantic import Field


class BestDestinationsTool(BaseTool):

    name: str = "Best Travel Destinations"
    description: str = "Clear description for what this tool is useful for, you agent will need this information to use it."
    top_destinations: list = Field(default_factory=list)
    
    def __init__(self, search_tool, llm_mistral, location):
        super().__init__()
        self.__search_tool = search_tool
        self.__llm_mistral = llm_mistral
        self.__location = location
        self.top_destinations = []

    def _run(self) -> str:
        
            search_query = f"Find the best two cities in {self.__location} for vacation"
            
            search_results = self.__search_tool.run(search_query)
            
            # Format the LLM query
            llm_query = f"Extract the names of the top two cities mentioned in the following snippets about {self.__location}, and format them as a comma-separated list: {search_results}"

            try:
               
                messages = [HumanMessage(content=llm_query)]
                output = self.__llm_mistral.invoke(messages)
               
               
                self.top_destinations = output.content.split(",")[:2]
                destinations_str = ", ".join(self.top_destinations)
                # print(self.description)
                return f"Provide a insigtful information of these cities: {destinations_str}"
            except Exception as e:
                print(f"Error processing LLM response: {e}")
                return "Error"