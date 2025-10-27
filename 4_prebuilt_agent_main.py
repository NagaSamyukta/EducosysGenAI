from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import create_react_agent


agent = create_react_agent(
   model="groq:llama-3.3-70b-versatile", 
   tools=[], 
   prompt="You are a helpful assistant" 
)

# Run the agents
response = agent.invoke(
   {"messages": [{"role": "user", "content": "what are large language models"}]}
)
print(response["messages"][-1].content)