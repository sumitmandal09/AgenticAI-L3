from fastmcp import FastMCP

mcp = FastMCP("Weather MCP Server")

# Mock data so this demo works out of the box, with no weather API key needed.
_MOCK_WEATHER = {
    "paris": {"condition": "Rainy", "temp_c": 16},
    "tokyo": {"condition": "Sunny", "temp_c": 29},
    "goa": {"condition": "Humid", "temp_c": 32},
    "london": {"condition": "Cloudy", "temp_c": 18},
}


@mcp.tool
def get_weather(city: str) -> dict:
    """Get the current weather for a city."""
    data = _MOCK_WEATHER.get(city.lower())
    if data is None:
        return {"city": city, "condition": "Unknown", "note": "No data for this city in the demo."}
    return {"city": city, **data}


@mcp.tool
def suggest_packing(condition: str) -> list[str]:
    """Suggest what to pack for a given weather condition (Rainy/Sunny/Cloudy/Humid)."""
    tips = {
        "rainy": ["umbrella", "raincoat", "waterproof shoes"],
        "sunny": ["sunscreen", "sunglasses", "hat"],
        "cloudy": ["light jacket"],
        "humid": ["light cotton clothes", "extra water bottle"],
    }
    return tips.get(condition.lower(), ["comfortable clothes"])


if __name__ == "__main__":
    #mcp.run()  # stdio -- lets a client launch this file as a subprocess
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
    mcp.run()

    # uv run weather_mcp_server.py
    # server listens at http://127.0.0.1:8000/mcp -- keep this running in its
    # own terminal, then run langgraph_mcp_agent.py in another one.