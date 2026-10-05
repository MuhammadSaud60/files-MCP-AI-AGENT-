import asyncio
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():

    client = MultiServerMCPClient(
        {
            "files": {
                "transport": "stdio",
                "command": "python",
                "args": ["server.py"],
            }
        }
    )


    tools = await client.get_tools()

    print("Available MCP tools:")

    for tool in tools:
        print("-", tool.name)


    model = ChatOllama(model='llama3.2:3b', temperature=0)

    model.bind_tools(tools)

    agent = create_agent(
        model=model,
        tools=tools
    )


    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Delete projects/test.txt."
                }
            ]
        }
    )


    print("\nAgent:")
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())