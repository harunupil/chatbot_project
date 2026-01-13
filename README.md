# Luthfi Card Game ChatBot

An interactive **LLM-powered chatbot** built with **Streamlit** and **LangChain**, designed to answer questions **only about card games and trading card prices**.  
The chatbot integrates with **Google Gemini** and uses a custom tool to fetch card prices from a local card database.

---

## ✨ Features

- Conversational chatbot interface using Streamlit
- Powered by Google Gemini via LangChain
- Restricted domain: card games & trading cards only
- Real-time card price lookup via LangChain tools
- Secure API key input using Streamlit session state
- Context-aware chat history with system-level rules

## ✨ System Prompt Rules

The chatbot is constrained by the following rules:

- Only answers questions related to **card games and trading cards**
- Can look up card prices using a predefined tool
- Politely refuses unrelated questions
- Provides concise and helpful responses

## ✨ How to Run Locally

### 1. Install dependencies
```bash
pip install streamlit langchain langchain-google-genai

streamlit run app.py


