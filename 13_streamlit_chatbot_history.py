import streamlit as st
from dotenv import load_dotenv
import uuid
load_dotenv()
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

st.set_page_config(page_title="Chatbot App", layout="wide")
st.title("Chatbot App")

# -----------------------
# Session State Initialization
# -----------------------
if "chats" not in st.session_state:
    st.session_state.chats = []

if "current_chat_index" not in st.session_state:
    st.session_state.current_chat_index = None

# -----------------------
# Sidebar: New Chat & Chat List
# -----------------------
st.sidebar.title("Chats")

# New Chat button
if st.sidebar.button("New Chat"):
    checkpointer = InMemorySaver()
    agent = create_react_agent(
        model="groq:llama-3.3-70b-versatile",
        tools=[],
        checkpointer=checkpointer,
        prompt="You are a helpful assistant"
    )
    st.session_state.chats.append({
        "id": str(uuid.uuid4()),   # unique, stable id
        "name": f"Chat {len(st.session_state.chats) + 1}",
        "messages": [],
        "agent": agent
    })
    st.session_state.current_chat_index = len(st.session_state.chats) - 1

# -----------------------
# Display chat buttons & handle deletion
# -----------------------
delete_chat_id = None
for idx, chat in enumerate(st.session_state.chats):
    col1, col2 = st.sidebar.columns([3, 1])
    
    # Load chat button
    if col1.button(chat["name"], key=f"load_{chat['id']}"):
        st.session_state.current_chat_index = idx

    # Delete chat button
    if col2.button("🗑️", key=f"delete_{chat['id']}"):
        delete_chat_id = chat["id"]

# Handle deletion after the loop
if delete_chat_id is not None:
    # Find index of chat with that id
    delete_index = next((i for i, c in enumerate(st.session_state.chats) if c['id'] == delete_chat_id), None)
    if delete_index is not None:
        del st.session_state.chats[delete_index]

        # Adjust current_chat_index if needed
        if st.session_state.current_chat_index == delete_index:
            st.session_state.current_chat_index = None
        elif st.session_state.current_chat_index and st.session_state.current_chat_index > delete_index:
            st.session_state.current_chat_index -= 1

# -----------------------
# Initialize Current Chat
# -----------------------
if st.session_state.current_chat_index is not None and st.session_state.current_chat_index < len(st.session_state.chats):
    current_chat = st.session_state.chats[st.session_state.current_chat_index]
    agent = current_chat["agent"]
    messages = current_chat["messages"]
else:
    current_chat = None
    agent = None
    messages = []

# -----------------------
# Chat Stream Function
# -----------------------
def stream_graph_updates(user_input: str):
    assistant_response = ""
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        for event in agent.stream({"messages": [{"role": "user", "content": user_input}]}, {"configurable": {"thread_id": "def"}}):
            for value in event.values():
                new_text = value["messages"][-1].content
                assistant_response += new_text
                message_placeholder.markdown(assistant_response)

    messages.append(("assistant", assistant_response))
    current_chat["messages"] = messages

# -----------------------
# Display Chat Messages
# -----------------------
for role, message in messages:
    with st.chat_message(role):
        st.markdown(message)

# -----------------------
# User Input
# -----------------------
if agent is not None:
    prompt = st.chat_input("What is your question?")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        messages.append(("user", prompt))
        current_chat["messages"] = messages
        stream_graph_updates(prompt)
