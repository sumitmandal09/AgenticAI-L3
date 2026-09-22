import asyncio
from fastmcp import Client
from dotenv import load_dotenv
load_dotenv()
import os

client = Client(
    f"https://mcp.tavily.com/mcp/?tavilyApiKey={os.getenv('TAVILY_API_KEY')}"   #This is Tavily MCP Server URL, we can use this server to call Tavily tools, we need to pass our Tavily API key in the URL as query parameter, so that we can use Tavily tools from this server.
)

async def main():
    
    async with client:
        #result = await client.call_tool("greet", {"name": name})
        tools = await client.list_tools()

        print("Available tools:")
        print("-" * 40)

        for tool in tools:
            print(tool)


        #using Tavily tools, from tavily MCP Server (Remote one)
        result = await client.call_tool("tavily_search", {"query": "What are the latest technology?"})
        print(result)

asyncio.run(main())