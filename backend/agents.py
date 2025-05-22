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

    crew = Crew([web_searcher, analyst, writer], [task1, task2, task3])
    return crew.kickoff()