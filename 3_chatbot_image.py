import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

load_dotenv()
# create state
class State(TypedDict):
   messages: Annotated[list, add_messages]

# create state graph
graph_builder = StateGraph(State)

llm = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

# create function as node
def chatbot(state: State):
   return {"messages": [llm.invoke(state["messages"])]}

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
# add node
graph_builder.add_node("chatbot", chatbot)

# add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()



try:
   img = graph.get_graph().draw_mermaid_png()
   with open("graph.png", "wb") as f:
       f.write(img)
except Exception:
   pass