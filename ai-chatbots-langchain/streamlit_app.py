import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

from card_db import get_card_price

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Luthfi Card Game ChatBot",
    page_icon="🃏",
    layout="centered"
)

# --------------------------------------------------
# Banner
# --------------------------------------------------
st.markdown(
    """
    <h1 style="text-align:center;">🃏 Luthfi Card Game ChatBot</h1>
    <p style="text-align:center;">
    I only answer questions about card games and card prices.
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# API Key Input
# --------------------------------------------------
if "google_api_key" not in st.session_state:
    api_key = st.text_input(
        "🔑 Enter your Google AI API Key",
        type="password"
    )
    if not api_key:
        st.stop()
    st.session_state.google_api_key = api_key
    st.rerun()

# --------------------------------------------------
# LangChain Tool
# --------------------------------------------------
@tool
def card_price_lookup(card_name: str) -> str:
    """
    Look up a trading card price from the card database.
    """
    return get_card_price(card_name)


# --------------------------------------------------
# LLM Initialization
# --------------------------------------------------
if "llm" not in st.session_state:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=st.session_state.google_api_key,
        temperature=0.3
    )

    st.session_state.llm = llm.bind_tools([card_price_lookup])

llm = st.session_state.llm

# --------------------------------------------------
# System Prompt
# --------------------------------------------------
SYSTEM_PROMPT = """
You are Luthfi Card Game ChatBot.

Rules:
- You ONLY answer questions about card games and trading cards.
- You are allowed to look up card prices using the provided tool.
- If a question is unrelated to card games, politely refuse.
- Be concise and helpful.
"""

# --------------------------------------------------
# Session State (Chat History)
# --------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

# --------------------------------------------------
# Display Chat History
# --------------------------------------------------
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# --------------------------------------------------
# User Input
# --------------------------------------------------
user_input = st.chat_input("Ask about a card (e.g. Dark Magician price)")

if user_input:
    # Add user message
    human_msg = HumanMessage(content=user_input)
    st.session_state.chat_history.append(human_msg)

    with st.chat_message("user"):
        st.markdown(user_input)

    # Invoke LLM
    response = llm.invoke(st.session_state.chat_history)

    # Handle tool calls (IMPORTANT)
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_result = card_price_lookup.invoke(
            tool_call["args"]
        )

        ai_msg = AIMessage(content=tool_result)
    else:
        ai_msg = response

    st.session_state.chat_history.append(ai_msg)

    with st.chat_message("assistant"):
        st.markdown(ai_msg.content)
