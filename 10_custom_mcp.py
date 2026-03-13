import asyncio  # <-- FIX 1: Added import
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

async def run_agent():
   client = MultiServerMCPClient(
       {
           "NagaEducosysFileSystem": {
               "command": "python",
               "args": [
                   "./10_filesystem_custom_mcp.py"
               ],
               "transport":"stdio"
           }

       }
   )
   tools = await client.get_tools()
   #print(tools)
   #print("-----------")
   agent = create_agent("openai:gpt-4o-mini",tools)
   #response = await agent.ainvoke({"messages": "what are the files present in educosys_1 Directory"})
   response = await agent.ainvoke({"messages": "create a new file vamshi1.txt  in educosys_1 Directory"})
   print(response["messages"][-1].content)
   

if __name__ == "__main__":
   asyncio.run(run_agent())