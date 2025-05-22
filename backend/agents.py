from pydantic import BaseModel, Field
from typing import Type
from crewai import LLM
import os
from linkup import LinkupClient

class LinkUpSearchInput(BaseModel):
    query: str = Field(description="The search query to perform")
    depth: str = Field(default="standard", description="Search depth")
    output_type: str = Field(default="searchResults", description="Output format")

class BaseTool:
    def _run(self, *args, **kwargs):
        raise NotImplementedError

class LinkUpSearchTool(BaseTool):
    name: str = "LinkUp Search"
    description: str = "Search the web using LinkUp"
    args_schema: Type[BaseModel] = LinkUpSearchInput

    def __init__(self):
        super().__init__()

    def _run(self, query: str, depth: str = "standard", output_type: str = "searchResults") -> str:
        try:
            client = LinkupClient(api_key=os.getenv("LINKUP_API_KEY"))
            results = client.search(query=query, depth=depth, output_type=output_type)
            return str(results)
        except Exception as e:
            return f"Error occurred while searching: {str(e)}"

# crew of the agents to perform research, analyze, and write
def create_research_crew(query: str):
    linkup_tool = LinkUpSearchTool()
    client = get_llm_client()

    # web searcher agent
    web_searcher = Agent(
        role="Web Searcher",
        goal="Find the most relevant information on the web, along with source links (urls).",
        backstory="An expert at formulating search queries and retrieving relevant information. Passes the results to the 'Research Analyst' only.",
        verbose=True,
        allow_delegation=True,
        tools=[linkup_tool],
        llm=client
    )

    # research analyst agent
    research_analyst = Agent(
        role="Research Analyst",
        goal="Analyze and synthesize raw information into structured insights, with citations.",
        backstory="An expert in identifying patterns and extracting key insights.",
        verbose=True,
        allow_delegation=True,
        llm=client
    )

    # technical writer agent
    technical_writer = Agent(
        role="Technical Writer",
        goal="Create well-structured, clear, and comprehensive responses in markdown with citations.",
        backstory="An expert communicator of technical knowledge.",
        verbose=True,
        allow_delegation=False,
        llm=client
    )

    # main search task for the web searcher agent
    search_task = Task(
        description=f"Search for comprehensive information about: {query}.",
        agent=web_searcher,
        expected_output="Detailed raw search results including sources (urls).",
        tools=[linkup_tool]
    )

    # analysis task for the research analyst agent
    analysis_task = Task(
        description="Analyze the raw search results and prepare a structured analysis.",
        agent=research_analyst,
        expected_output="A structured analysis with verified facts and source links.",
        context=[search_task]
    )

    # writing task for the technical writer agent
    writing_task = Task(
        description="Create a comprehensive answer with citations.",
        agent=technical_writer,
        expected_output="A markdown-formatted, complete and well-cited response.",
        context=[analysis_task]
    )

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

def get_llm_client():
    return LLM(
        model="ollama/deepseek-r1:7b",
        base_url="http://localhost:11434"
    )
class Crew:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    def kickoff(self):
        return f"Tasks executed by: {[t.agent.role for t in self.tasks]}"

def run_research(prompt: str):
    client = get_llm_client()
    tool = LinkUpSearchTool()

    web_searcher = Agent("Web Searcher", "Finds the internet for info", "Expert at search", [tool])
    analyst = Agent("Research Analyst", "Analyzes the data found", "Synthesizes insights", [])
    writer = Agent("Technical Writer", "Formats the summary", "Clear writing", [])

    task1 = Task(f"Search: {prompt}", agent=web_searcher)
    task2 = Task("Analyze search results", agent=analyst, context=[task1])
    task3 = Task("Write answer", agent=writer, context=[task2])
