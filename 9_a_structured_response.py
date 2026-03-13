from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver 


class MailResponse(BaseModel):
   hotels: str
   flights: str
   placestovisit: str


agent = create_agent(
   model="groq:llama-3.3-70b-versatile", 
   tools=[], 
   response_format = MailResponse 
)


config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
   {"messages": [{"role": "user", "content": "write a travel itenary for a trip to europe"}]},
   config 
)
print(response)
print("------------------------------")
print(response["structured_response"])


print("------------------------------")
print(response["structured_response"].hotels)


print("------------------------------")
print(response["structured_response"].flights)

print("------------------------------")
print(response["structured_response"].placestovisit)