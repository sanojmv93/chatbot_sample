import streamlit as st
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment to run this notebook.")
client = genai.Client(api_key=api_key)
model="gemini-2.5-flash"
GEN_CFG = types.GenerateContentConfig(
    temperature=0.7, top_p=0.9, top_k=40, max_output_tokens=256
)
chat = client.chats.create(model=model,     
    config=types.GenerateContentConfig(
    temperature=GEN_CFG.temperature,
    top_p=GEN_CFG.top_p,
    top_k=GEN_CFG.top_k,
    max_output_tokens=GEN_CFG.max_output_tokens,
    system_instruction="You are helpful customer assistant bot."
))



st.set_page_config(page_title="Chatbot Demo")
st.header("Chatbot")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

input = st.text_input("Input: ", key = "input")
submit = st.button("Ask the question.")

if submit and input:
    response=chat.send_message(input)
    st.session_state["chat_history"].append(("You", input))
    st.subheader("The response is")
    candidate = None
    usage_metadata = None
    for chunk in response:
        if "candidates" in chunk:
            candidate = chunk[1][0]
            answer = candidate.content.parts[0].text
        if "usage_metadata" in chunk:
            usage_metadata = chunk[1]
    st.write(answer)
    st.session_state["chat_history"].append(("Bot", answer))


st.divider()
st.subheader("The chat history is")
for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")





