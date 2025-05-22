from pydantic import BaseModel, Field
from typing import Type

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

    def _run(self, query: str, depth: str = "standard", output_type: str = "searchResults") -> str:
        return f"Mock search results for: {query}"

def get_llm_client():
    return "MockLLMClient"

def run_research(prompt: str):
    return f"Researching: {prompt}"
