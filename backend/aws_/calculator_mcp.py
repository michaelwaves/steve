from mcp.server import FastMCP

mcp = FastMCP("Calculator Server")


@mcp.tool(description="Add two numbers together")
def add(x: int, y: int) -> int:

    return x+y


@mcp.tool(description="Divide two numbers x/y")
def divide(x: float, y: float) -> float:
    return x/y


@mcp.tool(description="Raise x^y")
def exponentiate(x: float, y: float) -> float:
    return x**y


@mcp.tool(description="Return x times y")
def multiply(x: float, y: float) -> float:
    return x*y


mcp.run(transport="streamable-http")
