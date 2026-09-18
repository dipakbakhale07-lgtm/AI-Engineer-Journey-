import anyio
import sys

sys.path.insert(0, r".\05-PROJECT-4-BUISSNESS-AGENT")

from mcp import Client
from mcp_server import server


async def main():
    async with Client(server) as client:
        tools = await client.list_tools()

        print("MCP CONNECTED")
        print("TOOLS:", [tool.name for tool in tools.tools])

        result = await client.call_tool(
            "faq_search",
            {"question": "What are your business hours?"}
        )

        print("RESULT:", result.structured_content)


if __name__ == "__main__":
    anyio.run(main)