from pydantic import BaseModel, Field
from typing import Type
from crewai import LLM, Process, Crew, Agent, Task
import os
from linkup import LinkupClient
from crewai.tools import BaseTool

# main LLM client model for the agents to use
def get_llm_client():
    return LLM(
        model="ollama/deepseek-r1:7b",
        base_url="http://localhost:11434"
    )

# pipeline for the LinkUp search tool
class LinkUpSearchInput(BaseModel):
    query: str = Field(description="The search query to perform")
    depth: str = Field(default="standard", description="Depth of search: 'standard' or 'deep'")
    output_type: str = Field(default="searchResults", description="Output type: 'searchResults', 'sourcedAnswer', or 'structured'")
       
# LinkUp search tool for web search       
class LinkUpSearchTool(BaseTool):
    name: str = "LinkUp Search"
    description: str = "Search the web for information using LinkUp and return comprehensive results"
    args_schema: Type[BaseModel] = LinkUpSearchInput

    def __init__(self):
        super().__init__()

    def _run(self, query: str, depth: str = "standard", output_type: str = "searchResults") -> str:
        try:
            # initializing LinkUp client with API key from environment variables
            linkup_client = LinkupClient(api_key=os.getenv("LINKUP_API_KEY"))

            # starting search
            search_response = linkup_client.search(
                query=query,
                depth=depth,
                output_type=output_type
            )
            return str(search_response)
        except Exception as e:
            return f"Error occurred while searching: {str(e)}"

# crew of the agents to perform research, analyze, and write
def create_research_crew(query: str):
    linkup_search_tool = LinkUpSearchTool()
    client = get_llm_client()

    # web searcher agent
    web_searcher = Agent(
        role="Web Searcher",
        goal="Find the most relevant information on the web, along with source links (urls).",
        backstory="An expert at formulating search queries and retrieving relevant information. Passes the results to the 'Research Analyst' only.",
        verbose=True,
        allow_delegation=True,
        tools=[linkup_search_tool],
        llm=client
    )

    # research analyst agent
    research_analyst = Agent(
        role="Research Analyst",
        goal="Analyze and synthesize raw information into structured insights, along with source links (urls) as citations.",
        backstory="An expert at analyzing information, identifying patterns, and extracting key insights. If required, can delagate the task of fact checking/verification to 'Web Searcher' only. Passes the final results to the 'Technical Writer' only.",
        verbose=True,
        allow_delegation=True,
        llm=client
    )

    # technical writer agent
    technical_writer = Agent(
        role="Technical Writer",
        goal="Create well-structured, clear, and comprehensive responses in markdown format, with citations/source links (urls).",
        backstory="An expert at communicating complex information in an accessible way.",
        verbose=True,
        allow_delegation=False,
        llm=client
    )

    # search task for the web searcher agent
    search_task = Task(
        description=f"Search for comprehensive information about: {query}.",
        agent=web_searcher,
        expected_output="Detailed raw search results including sources (urls).",
        tools=[linkup_search_tool]
    )

    # analysis task for the research analyst agent
    analysis_task = Task(
        description="Analyze the raw search results, identify key information, verify facts and prepare a structured analysis.",
        agent=research_analyst,
        expected_output="A structured analysis of the information with verified facts and key insights, along with source links",
        context=[search_task]
    )

    # writing task for the technical writer agent
    writing_task = Task(
        description="Create a comprehensive, well-organized response based on the research analysis.",
        agent=technical_writer,
        expected_output="A clear, comprehensive response that directly answers the query with proper citations/source links (urls).",
        context=[analysis_task]
    )

    # final crew assembly with the agents and tasks
    crew = Crew(
        agents=[web_searcher, research_analyst, technical_writer],
        tasks=[search_task, analysis_task, writing_task],
        verbose=True,
        process=Process.sequential
    )
    return crew

"""
class Agent:
    def __init__(self, role, goal, backstory, tools=None):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []

class Task:
    def __init__(self, description, agent, context=None):
        self.description = description
        self.agent = agent
        self.context = context or []

class Crew:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    def kickoff(self):
        return f"Tasks executed by: {[t.agent.role for t in self.tasks]}"
"""

# running the research process through the crew of agents
def run_research(query: str):
    crew = create_research_crew(query)
    result = crew.kickoff()
    return result.raw
