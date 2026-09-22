import asyncio
from distro import name
from fastmcp import Client

#client = Client("http://localhost:8000/mcp")
client = Client("01_my_mcp_server.py")        #here we are specifying the location of the server, make sure its up and running before you run this client code, otherwise it will give error.


#-----------------------------------------------------------------------------------------------
async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        result = await client.list_tools()

        for tool in result:
            print(f"Tool Name: {tool.name}, Description: {tool.description or 'No description'}")

        #print(result)

asyncio.run(call_tool("Sumit"))  #  Replace "Sumit" with the desired name to greet






#-----------------------------------------------------------------------------------------------

async def call_tool(query: str):
    async with client:
        #result = await client.call_tool("greet", {"name": name})
        tools = await client.list_tools()

        result = await client.call_tool("search_web", {"query": query})

        # for tool in result:
        #     print(f"Tool Name: {tool.name}, Description: {tool.description or 'No description'}")

        #print(tools)
        print(f"Result: {result}")

asyncio.run(call_tool("What are the latest advancements in AI technology?"))
#asyncio.run(call_tool("Sumit"))




















#We can run this client by command --> uv run 01_my_mcp_client.py