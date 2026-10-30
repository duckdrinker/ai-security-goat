from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calc")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two numbers and returns the sum."""
    return a + b
