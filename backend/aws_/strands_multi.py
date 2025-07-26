from contextlib import ExitStack
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import http_request
from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
import os

load_dotenv()

TAVILY_KEY = os.getenv("TAVILY_API_KEY")


MCP_CLIENT_CONFIGs = [
    {
        "name": "tavily_client",
        "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_KEY}"
    },
    {
        "name": "calculator_client",
        "url": "http://localhost:8000/mcp/"
    },
    {
        "name": "email_client",
        "url": "http://localhost:8001/mcp/"
    },
    {
        "name": "sanctions_client",
        "url": "http://localhost:8002/mcp/"
    },
    # {
    #     "name": "linkedin_client",
    #     "url": "https://mcp.brightdata.com/mcp?token=fed383f03e69eb3a5de97e4024af03eb4a131cb257014aa478786002fbd7a00b"
    # }
]

clients = {}


with ExitStack() as stack:
    for config in MCP_CLIENT_CONFIGs:
        def create_streamable_http_transport():
            return streamablehttp_client(config["url"])
        client = MCPClient(create_streamable_http_transport)
        stack.enter_context(client)  # type: ignore
        clients[config["name"]] = client

    all_tools = []
    for client in clients.values():
        all_tools.extend(client.list_tools_sync())

    agent = Agent(tools=all_tools)
    system_prompt = """You are a KYC (know your client) chatbot operating at a large bank. You have access to web search,  calculator, and email sending tools. You look over people's linkedin profiles, check adverse media (news), and sanctions lists. 
    
    Step 1: LinkedIn Search
    search the clients linkedin page. 

    Step 2: Adverse Media Search
    Search major news outlets for client_name + fraud, moneylaundering, racketeering, crime, court, judge, etc. This is a difficult task so pay close attention to a few things. First, if the client name appears, how likely is this same person? Second, how relevant is this in predicting the criminality of the client? Is the name merely a bystander or lawyer involved or the actual criminal. Third, how relevant is this crime? Is it highly severe, did it happen a long time ago and the person already served their sentence?

    Step 3: Sanctions Search
    You have a sanctions_search tool that can do fuzzy matching of name. Just like with the adverse media, consider if this is really a match or just a similar name. 

    Assign a risk score to each category. Also consider geography, occupational risk, connections, related companies (like employers), and how well the profile fits with what the client says. Summarize everything in a final report with a risk score from 0 to 100"""

    user_prompt = """Help me prepare a risk report for the client Michael Yu. He claims to be a founder of an anti money laundering startup Quantoflow based in toronto Canada. Send the report to ryanymark@gmail.com with beatufiully formatted html"""

    agent(system_prompt=system_prompt,
          prompt=user_prompt)
