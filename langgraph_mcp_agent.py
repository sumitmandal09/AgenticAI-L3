import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

# Same local/cloud Ollama setup used in chatbot_with_hitl.py.
MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:120b-cloud")
llm = ChatOllama(model=MODEL, temperature=0)

# weather_mcp_server.py must already be running (uv run weather_mcp_server.py)
# and serving streamable-http on http://127.0.0.1:8000/mcp.
#
# "deepwiki" is DeepWiki's public remote MCP server -- no API key needed, and
# it responds fast, so it's a reliable way to see a *real* remote MCP server
# in a LangGraph agent. It answers questions about any public GitHub repo.
#
# "tavily" points at the same remote MCP server used in tavily_mcp_client.py.
# It's left commented out because mcp.tavily.com was hanging on connect during
# testing (get_tools() awaits every server, so one stuck server blocks all of
# them) -- uncomment it once that endpoint is responsive again.
mcp_client = MultiServerMCPClient(
    {
        "weather": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        },
        "deepwiki": {
            "url": "https://mcp.deepwiki.com/mcp",
            "transport": "streamable_http",
        },
        "tavily": {
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={os.getenv('TAVILY_API_KEY')}",
            "transport": "streamable_http",
        },
    }
)


async def main():
    tools = await mcp_client.get_tools()
    print(tools)
    agent = create_agent(llm, tools)

    result = await agent.ainvoke(
        {
            "messages": [
                (
                    "user",
                    "I'm travelling to Goa next week. What's the weather like and what should I pack? "
                    "Also, ask the langchain-ai/langgraph GitHub repo what LangGraph is used for, "
                    "in one sentence.",
                )
            ]
        }
    )

    for msg in result["messages"]:
        msg.pretty_print()


asyncio.run(main())








# uv run langgraph_mcp_agent.py