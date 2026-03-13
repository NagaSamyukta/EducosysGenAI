from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent

agent = create_agent(
  model="groq:llama-3.3-70b-versatile",
  tools=[]
)
# Run the agents
response = agent.invoke(
  {"messages": [{"role": "user", "content": "what are large language models"}]}
)
print(response["messages"][-1].content)

