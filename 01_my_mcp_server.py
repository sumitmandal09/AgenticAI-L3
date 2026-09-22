from fastmcp import FastMCP
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os

mcp = FastMCP("My First MCP Server")

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))  # Load API key from environment variable


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.tool
def add(a: int, b: int) -> int:
    '''This is performing addition of two numbers'''   #This is Doc Strings ''' ''', its description helps out AI to understand by prompt 
    return a + b
   

@mcp.tool
def search_web(query: str) -> dict:
    '''This is performing search on web using Tavily'''   #This is Doc Strings ''' ''', its description helps out AI to understand by prompt 
    return tavily_client.search(
        query=query,
        max_results=3
        )






if __name__ == "__main__":
    #mcp.run(transport="http", port=8000)
    mcp.run()


    







# To run MCP Server
#uv run 01_my_mcp_server.py 
#or
# write in terminal --> uv run fastmcp run 01_my_mcp_server.py:mcp
# fastmcp run 01_my_mcp_server.py:mcp
#you can change transport of the server stdio/http, by default its stdio
#Terminal command --> uv runfastmcp run 01_my_mcp_server.py:mcp --transport http --port 8000
# so in url ...../mcp --> we will get our json RCP resonse
#Now we need to create MCP Client to call this server, we will create a new file 01_my_mcp_client.py


#For MCP Inspector, we can run this command in terminal --> npx @modelcontextprotocol/inspector
#npx @modelcontextprotocol/inspector
#then we can open the url in browser --> http://localhost:3000/ and then we can see our MCP server and its tools, we can test our tools from there also.
#put MCP server url in browser and debug the tools, we can also see the request and response in json format, we can also see the logs of the server in terminal where we are running the server.