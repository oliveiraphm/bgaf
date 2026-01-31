import requests
import streamlit as st
from io import BytesIO

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, bytes):
            st.audio(content)
        else:
            st.markdown(content)

if prompt := st.chat_input("Write your prompt in this input field"):
    response = requests.get(
        f"http://localhost:8000/generate/audio", params={"prompt": prompt}
    )
    response.raise_for_status()
    audio_bytes = response.content
    audio_io = BytesIO(audio_bytes)
    with st.chat_message("assistant"):
        st.text("Here is your generated audio")
        st.audio(audio_io, format="audio/wav")