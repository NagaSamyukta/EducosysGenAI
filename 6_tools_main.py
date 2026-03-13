from dotenv import load_dotenv
import os
load_dotenv()

from langchain.agents import create_agent

def addFile(filename: str) -> str:
   """Create a new file in current directory"""
   if not os.path.exists(filename):
      with open(filename, "w") as f:
          pass
      print(f"File '{filename}' created.")
   else:
      print(f"File '{filename}' already exists.")

def addFolder(directory_name: str):
  """Create a new Directory in current directory"""
  if not os.path.exists(directory_name):
      os.mkdir(directory_name)
      print(f"Directory '{directory_name}' created.")
  else:
      print(f"Directory '{directory_name}' already exists.")

def removeFile(filename: str) -> str:
   """deletes a file in current directory"""
   if os.path.exists(filename):
      os.remove(filename)
      print(f"File '{filename}' deleted.")
   else:
      print(f"File '{filename}' doesnt exist.")

def removeFolder(directory_name: str):
  """Deletes a Directory in current directory"""
  if os.path.exists(directory_name):
      os.rmdir(directory_name)
      print(f"Directory '{directory_name}' deleted.")
  else:
      print(f"Directory '{directory_name}' doesnt exist.")

agent = create_agent(
  model="groq:llama-3.3-70b-versatile",
  tools=[addFile, addFolder]
)
# Run the agents
response = agent.invoke(
  {"messages": [{"role": "user", "content": "create a new directory with name educosys_5"}]}
)
print(response["messages"][-1].content)

#try:
 #  img = agent.get_graph().draw_mermaid_png()
#   with open("agent2.png", "wb") as f:
 #      f.write(img)
#except Exception:
#   pass

# Run the agents
response = agent.invoke(
  {"messages": [{"role": "user", "content": "create a new directory with name educosys_2"}]}
)
print(response["messages"][-1].content)


# Run the agents
# response = agent.invoke(
#   {"messages": [{"role": "user", "content": "create a new directory with name educosys_2 and create a new file edco.txt within educosys_1 directory"}]}
# )

# print(response)

# Run the agents
#response = agent.invoke(
#  {"messages": [{"role": "user", "content": "delete all files with name edco.txt and delete educosys_1 directory"}]}
#)
# response = agent.invoke(
#   {"messages": [{"role": "user", "content": "remove the directory with name educosys_2"}]}
# )

# print(response)

## learning i was not able to delete the dir if there is a file in directory