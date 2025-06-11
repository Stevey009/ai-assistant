import os
import json
from datetime import datetime

import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not set in .env")
else:
    openai.api_key = OPENAI_API_KEY

LOG_FILE = "journal.json"


def load_history():
    if "history" not in st.session_state:
        st.session_state.history = []
    return st.session_state.history


def append_log(user_msg, assistant_msg, rating=None):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user_msg,
        "assistant": assistant_msg,
        "rating": rating,
    }
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def get_response(prompt: str) -> str:
    history = load_history()
    messages = [
        {"role": "system", "content": "You are a helpful personal assistant."},
    ]
    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
    answer = response["choices"][0]["message"]["content"]
    history.append({"user": prompt, "assistant": answer})
    return answer


st.title("Personal AI Assistant")
user_input = st.text_input("You:")

if st.button("Send"):
    if user_input:
        with st.spinner("Thinking..."):
            reply = get_response(user_input)
        st.markdown(f"**Assistant:** {reply}")
        rating = st.slider(
            "Rate the response:", 1, 5, 3, key=f"rating_{len(st.session_state.history)}"
        )
        append_log(user_input, reply, rating)
        st.session_state.user_input = ""

st.header("Conversation History")
for entry in st.session_state.get("history", []):
    st.markdown(f"**You:** {entry['user']}")
    st.markdown(f"**Assistant:** {entry['assistant']}")
    st.write("---")
