from dotenv import load_dotenv
load_dotenv()
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent


checkpointer = InMemorySaver()
agent = create_react_agent(
   model="groq:llama-3.3-70b-versatile", 
   tools=[], 
   checkpointer=checkpointer,
   prompt="You are a helpful assistant" 
)


config = {"configurable": {"thread_id": "1"}}

first_response = agent.invoke(
   {"messages": [{"role": "user", "content": "who is modi"}]},
   config 
)
second_response = agent.invoke(
   {"messages": [{"role": "user", "content": "when was he born?"}]},
   config
)
print(first_response["messages"][-1].content)
print('-------------')
print(second_response["messages"][-1].content)