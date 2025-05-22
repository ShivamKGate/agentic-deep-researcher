from backend.agents import run_research

def handler(query):
    return run_research(query)