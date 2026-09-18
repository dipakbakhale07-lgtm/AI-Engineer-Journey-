from mcp.server.mcpserver import MCPServer

from tool_faq import search_faq


server = MCPServer("Project4 Business Agent")


@server.tool()
def faq_search(question: str) -> dict:
    """Search the Project 4 business FAQ using a question."""
    return search_faq(question)


if __name__ == "__main__":
    server.run()
