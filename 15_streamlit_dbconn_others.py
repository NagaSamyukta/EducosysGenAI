import os
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model


load_dotenv()
DB_URL = os.getenv("NEON_DB_URL")
if not DB_URL:
    raise ValueError("Erorr to fetch the db url")


engine = create_engine(DB_URL, echo=False)


@tool("fetch_data")
def fetch_data(query: str) -> str:
    """Fetch data from the database given an SQL query string."""
    print(text(query))
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]
            if not rows:
                return "No results found."
            return str(rows)
    except Exception as e:
        return f"Error: {e}"


llm = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")
agent = create_react_agent(model=llm, tools=[fetch_data])


st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")
st.title("Chatbot")


if "conversation" not in st.session_state:
    st.session_state.conversation = []


user_input = st.chat_input("Ask me anything about your database...")
if user_input:
    st.session_state.conversation.append(("user", user_input))

    with st.spinner("⚡ Fetching data from db..."):
        result = agent.invoke({"messages": st.session_state.conversation})
        reply = result["messages"][-1].content

    st.session_state.conversation.append(("assistant", reply))

for role, msg in st.session_state.conversation:
    with st.chat_message(role):
        st.write(msg)