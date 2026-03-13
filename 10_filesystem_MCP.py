import asyncio  # <-- FIX 1: Added import
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()
from langgraph.prebuilt import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
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
                   "/Users/nagasamyuktabheemunipati/Agents/educosys_1"
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
   response = await agent.ainvoke({"messages": "create a new file aadvik2.txt  in educosys_1 Directory"})
   print(response["messages"][-1].content)
   

if __name__ == "__main__":
   asyncio.run(run_agent())