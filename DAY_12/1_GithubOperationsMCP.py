from dotenv import load_dotenv
load_dotenv()
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def run_agent():
   client = MultiServerMCPClient(
       {
           "github": {
               "command": "npx",
               "args": [
                   "-y",
                   "@modelcontextprotocol/server-github"
               ],
               "env": {
                   "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
               },
               "transport": "stdio"
           },
            "filesystem": {
               "command": "npx",
               "args": [
                   "-y",
                   "@modelcontextprotocol/server-filesystem",
                   r"C:\Users\Prashanth\Desktop"
               ],
               "transport":"stdio"
           }
       }
   )
   tools = await client.get_tools()
   agent = create_react_agent("openai:gpt-4o", tools)
   response = await agent.ainvoke({"messages": "Create a file with the name genai.txt in the current directory and write 'Hello, GenAI Bootcamp!' in it."})
    
   print(f"\n \n ${response["messages"][-1].content}")



# ADD THIS LINE TO CALL THE ASYNC FUNCTION
if __name__ == "__main__":
    asyncio.run(run_agent())
