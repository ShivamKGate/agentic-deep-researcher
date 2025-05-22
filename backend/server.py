from mcp.server.fastmcp import FastMCP
from agents import run_research

# Create FastMCP instance
mcp = FastMCP("crew_research")
@mcp.tool()

async def crew_research(query: str) -> str:
    return run_research(query)

if __name__ == "__main__":
    mcp.run(transport="stdio")
