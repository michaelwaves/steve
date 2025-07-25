from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import http_request
from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient

load_dotenv()


def create_streamable_http_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")


client = MCPClient(create_streamable_http_transport)

with client:
    tools = client.list_tools_sync()
    agent = Agent(tools=tools)
    agent("whats 432145 - 234321?")
