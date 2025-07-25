from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import http_request
from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
import os

load_dotenv()

TAVILY_KEY = os.getenv("TAVILY_API_KEY")


def create_streamable_http_transport():
    return streamablehttp_client(f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_KEY}")


client = MCPClient(create_streamable_http_transport)


def create_streamable_http_transport_calculator():
    return streamablehttp_client("http://localhost:8000/mcp/")


calculator_client = MCPClient(create_streamable_http_transport_calculator)


with client:
    with calculator_client:
        calc_tools = calculator_client.list_tools_sync()
        tools = client.list_tools_sync()
        agent = Agent(tools=tools+calc_tools)
        agent("tell me the latest news headlines about tesla and calculate the stock price in a year using math tools")
