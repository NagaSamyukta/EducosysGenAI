from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
   model="groq:llama-3.3-70b-versatile", 
   tools=[], 
   prompt="You are a helpful assistant" 
)


try:
   img = agent.get_graph().draw_mermaid_png()
   with open("agent.png", "wb") as f:
       f.write(img)
except Exception:
   pass