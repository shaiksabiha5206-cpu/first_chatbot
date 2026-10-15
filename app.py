import streamlit as st
from google import genai
from google.genai import types
import os 
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_LEY"))
st.title("SABIHA AI CHATBOT")
st.sidebar.metric ("TOTAL MESSAGES",len(st.session_state.messages))
file = st.file_uploader("uploaded pdf",type=["pdf"])
if file:
    st.write("FILE UPLOAD",file.name)
if "history" not in st.session_state:
    st.session_state.history = []
for hist in st.session_state.history:
    with st.chat_message(hist["role"]):
        st.write(hist["content"])
if prompt := st.chat_input("ASK ME ANYTHING"):
    st.session_state.history.append(prompt)
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("THINKING"):
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config = types.GenerateContentConfig(
                    system_instruction="you are sabiha ,a helpful and friendly ai assistent .answer short and clear.",
                    temperature=0.2,
                    max_output_tokens=200
                )
            ) 
            answer = response.text 
            st.write(answer)
    st.session_state.history.append({"role":"assistant","content":answer})
