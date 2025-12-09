from dotenv import load_dotenv
load_dotenv()
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
import os



async def run_agent():
   client = MultiServerMCPClient(
       {
           "CreatingOwnMcpServer": {
               "command": "python",
               "args": ["Creating_own_mcp_server.py"],
               "transport": "stdio"
            }
       }
   )
   tools = await client.get_tools()
   agent = create_agent("openai:gpt-4o-mini", tools)
   response = await agent.ainvoke({"messages": "Delete a file with the name genai.txt in the current directory and write 'Hello, GenAI Bootcamp!' in it."})
    
   print(f"\n \n ${response['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(run_agent())
