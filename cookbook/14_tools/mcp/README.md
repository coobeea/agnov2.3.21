# MCP Agents using Agno

Model Context Protocol (MCP) gives Agents the ability to interact with external systems through a standardized interface. Using Agno's MCP integration, you can build Agents that can connect to any MCP-compatible service.

## Examples in this Directory

1. Filesystem Agent (`filesystem.py`)

This example demonstrates how to create an agent that can explore, analyze, and provide insights about files and directories on your computer.

2. GitHub Agent (`github.py`)

This example shows how to create an agent that can explore GitHub repositories, analyze issues, pull requests, and more.

3. Groq with Llama using MCP (`groq_mcp.py`)

This example uses the file system MCP agent with Groq running the Llama 3.3-70b-versatile model.

4. Include/Exclude Tools (`include_exclude_tools.py`)

This example shows how to include and exclude tools from the MCP agent. This is useful for reducing the number of tools available to the agent, or for focusing on a specific set of tools.

5. Multiple MCP Servers (`multiple_servers.py`)

This example shows how to use multiple MCP servers in the same agent. 

6. Sequential Thinking (`sequential_thinking.py`)

This example shows how to use the MCP agent to perform sequential thinking.

7. Airbnb Agent (`airbnb.py`)

This example shows how to create an agent that uses MCP and Gemini 2.5 Pro to search for Airbnb listings.

8. [Parallel Search MCP](#parallel-search-mcp-without-a-parallel-api-key)

The setup below gives an agent web search and page fetching without a Parallel account or API key.


## Getting Started

### Prerequisites

Install the required dependencies:

```bash
pip install agno mcp openai
```

Export your API keys:

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

> For the GitHub example, create a Github PAT following [these steps](https://github.com/modelcontextprotocol/servers/tree/main/src/github#setup).

### Run the Examples

```bash
python filesystem.py
python github.py
```

## Parallel Search MCP without a Parallel API key

[Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp) exposes `web_search` for current information and `web_fetch` for reading specific URLs. The anonymous endpoint uses Fast mode for search and is free for exploration and light use, with rate limits. This setup uses Agno's existing Streamable HTTP transport.

From the repository root, create a Python 3.12 environment and install the dependencies:

```bash
uv venv .venvs/parallel-mcp --python 3.12
source .venvs/parallel-mcp/bin/activate
uv pip install -e libs/agno "mcp>=1.9,<2" "openai>=1,<3"
export OPENAI_API_KEY="your_openai_api_key"
```

This checkout uses the MCP 1.x client interface. The OpenAI key is for the model used below; no `PARALLEL_API_KEY` is needed.

Save this as `parallel_search_agent.py` in the repository root:

```python
import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from agno.tools.mcp.params import StreamableHTTPClientParams


async def main() -> None:
    server_params = StreamableHTTPClientParams(
        url="https://search.parallel.ai/mcp",
        headers={"User-Agent": "agno-parallel-mcp-example/2.3.21"},
    )
    async with MCPTools(
        transport="streamable-http", server_params=server_params
    ) as parallel_tools:
        agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            tools=[parallel_tools],
            instructions="Search the web, fetch relevant source pages, and include source links in your answer.",
            markdown=True,
        )
        await agent.aprint_response(
            "Find Agno's latest release, then read an official release page and summarize the changes."
        )


if __name__ == "__main__":
    asyncio.run(main())
```

Run it with `python parallel_search_agent.py`. The MCP connection stays open while the agent uses its tools and closes when the context exits. Keep your chosen model and its credentials when adapting this setup to another agent.

For authenticated Parallel MCP usage, see [`parallel.py`](parallel.py). The native [`ParallelTools` example](../parallel_tools.py) uses the Parallel API and requires a Parallel API key.

## How It Works

These examples use Agno to create agents that leverage MCP servers. The MCP servers provide standardized access to different data sources (filesystem, GitHub), and the agents use these servers to answer questions and perform tasks.

The workflow is:
1. Agent receives a query from the user
2. Agent determines which MCP tools to use
3. Agent calls the appropriate MCP server to get information
4. Agent processes the information and provides a response

## Customizing

You can modify these examples to:
- Connect to different MCP servers
- Change the agent's instructions
- Add additional tools
- Customize the agent's behavior

## More Information

- Read more about [MCP](https://modelcontextprotocol.io/introduction)
- Read about [Agno's MCP integration](https://docs.agno.com/tools/mcp)
