import asyncio
import os
from typing import Any

import streamlit as st
from langchain_core.messages import HumanMessage

from agent import CustomerSupportAgent
from agent import get_agent as build_agent
from chats import get_configuration as build_configuration
from mcp_client import get_client

# @TODO: small hack to deploy on streamlit cloud
if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = st.secrets.get("GROQ_API_KEY") or ""


@st.cache_data
def get_configuration():
    return build_configuration()


@st.cache_resource
def get_agent(configuration: dict[str, Any]):
    client = get_client(st.secrets.get("SHOP_MCP_SERVER_URL"))
    coroutine = build_agent(client)
    lc_agent = asyncio.run(coroutine)
    return CustomerSupportAgent(lc_agent, configuration)


configuration = get_configuration()
agent = get_agent(configuration)

# Basic session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI
st.title("Customer Support Agent")

# Display chat history
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Chat input
if prompt := st.chat_input("Start a conversation with our customer support agent!"):
    # Add user message
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mock AI response (replace with your agent)
    response = asyncio.run(agent.query(prompt))
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant message to history
    st.session_state.messages.append(response)
