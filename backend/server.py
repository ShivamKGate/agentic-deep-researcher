from agents import run_research

class FastMCP:
    def __init__(self, name):
        self.name = name
        self.tools = {}

    def tool(self, func=None):
        def wrapper(f):
            self.tools[f.__name__] = f
            return f
        return wrapper(func) if func else wrapper

    def run(self, transport="stdio"):
        print(f"{self.name} server running with tools: {list(self.tools.keys())}")

mcp = FastMCP("crew_research")
@mcp.tool()

def crew_research(query: str) -> str:
    return run_research(query)

if __name__ == "__main__":
    mcp.run()
