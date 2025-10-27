
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()
from langgraph.prebuilt import create_react_agent


class MailResponse(BaseModel):
   hotels: str
   flights: str
   placestovisit: str


agent = create_react_agent(
   model="groq:llama-3.3-70b-versatile", 
   tools=[], 
   prompt="you are helpful assistant",
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