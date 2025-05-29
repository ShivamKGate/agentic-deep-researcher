# Agentic Deep Researcher

This is a `MCP`-powered multi-agent deep researcher that performs real-time web research using agents through CrewAI, LinkUp API, and DeepSeek R1 as a local LLM. It uses a team of agents to web search, analyze the research, and finally synthesize the information into structured, cited insights.
It orchestrates three roles:

- **Web Searcher**  
  Formulates and executes web searches via LinkUp API
- **Research Analyst**  
  Synthesizes raw search results into structured insights with citations of sources.
- **Technical Writer**  
  Produces clear, well-formatted Markdown responses with source links.

Under the hood, the pipeline is defined in `backend/agents.py` and runs sequentially with built-in error handling and in-memory context storage.

---

## Features

- Interactive chat UI (`Streamlit`) with history tracking and clear history functionality
- Automated multi-step research pipeline:
  1. Web searching process via LinkUp API
  2. Structured analysis of collected results
  3. Final drafting of Markdown responses
- Configurable via environment variables
- Extensible architecture: add new agents, tools, or output formats

---

## Installation

1. Clone the repository:

   ```powershell
   git clone https://github.com/ShivamKGate/agentic-deep-researcher.git
   cd agentic-deep-researcher
   ```

2. Create and activate a Python virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Obtain your LinkUp API key from [LinkUp](https://app.linkup.so/sign-in) and configure API keys and model settings in a `.env` file:

    ```ini
    LINKUP_API_KEY=<your linkup api key>
    ```

5. Download and install [Ollama](https://ollama.com/) locally, then pull the `deepseek-r1:7b` model by running:

    ```powershell
    ollama pull deepseek-r1:7b
    ```

    > **Note:** Feel free to choose any DeepSeek model with higher or lower parameters (`1.5b`, `7b`, `8b`, `14b`, `32b`, `70b`, or `671b`) based on your available GPU resources and the desired level of reasoning quality during the model selection in the terminal.

---

## Usage

### `Streamlit` Chat UI

```powershell
streamlit run backend/app.py
```

Open your browser at `http://localhost:8501` to chat with the multi-agent deep researcher!

### FastMCP RPC Server

```powershell
python backend/server.py
```

Exposes an `async` tool `crew_research` for orchestration via FastMCP protocols.

---

## Configuration

| Variable         | Description                       | Default     |
|------------------|-----------------------------------|-------------|
| `LINKUP_API_KEY` | API key for LinkUp search service | (required)  |

All other configuration values are defined in code and do not require manual setup.

---

## Project Structure

```text
root/
├── backend/
│   ├── agents.py    # Agent definitions, tool wrappers, and pipeline orchestration
│   ├── app.py       # Streamlit UI application
│   └── server.py    # FastMCP RPC server endpoint
├── LICENSE
├── README.md
└── requirements.txt # Python dependencies
```

---

## Contributing

Contributions, issues, and feature requests are welcome! Please open an issue or pull request on the GitHub repository.

---

## Future Implementations

- **Full Async & Reactive Pipeline**  
  Convert all research steps (web search, analysis, writing) to non-blocking async operations with event-driven scheduling and responsive I/O for improved throughput.

- **Enhanced Error Handling & Retry Mechanisms**  
  Implement granular retry strategies, circuit-breaker patterns, backoff policies, and comprehensive structured logging to handle transient and persistent failures at each step.

- **Memory Agent**  
  Introduce a dedicated agent to capture and persist conversational context and research state into the LLM’s memory store for long-term continuity through the agents' sequential run.

- **Feedback Agent**  
  Add an agent to validate and refine outputs from each agent in parallel by comparing raw results against quality criteria and user feedback loops before final drafting.

- **Cleaner & Customizable Outputs**  
  Introduce configurable Markdown templates, support for HTML/PDF exports, and user-defined formatting options for polished, presentation-ready reports.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
