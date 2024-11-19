import os
import streamlit as st
from openai import OpenAI

LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "***")
llm = OpenAI(base_url=LLM_ENDPOINT, api_key="-")

st.session_state['messages'] = st.session_state.get('messages', [{
    "role": "system", 
    "content": "Your name is KIRA and you are a helpful assistant."
}])

st.set_page_config(page_title="KIRA", page_icon="🦜", menu_items={})
st.title("🦜 Ask me anything ...")

# Show previous messages
for entry in st.session_state['messages'][1:]:
    with st.chat_message(entry['role']):
        st.write(entry['content'])

# Handle the user prompt and stream a response
if prompt := st.chat_input("🦜 Ask me anything ..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("ai"):
        completion = llm.chat.completions.create(
            messages=st.session_state.messages,
            model="", stream=True, max_tokens=4000
        )
        response = st.write_stream(m.choices[0].delta.content for m in completion if not m.choices[0].finish_reason)
        st.session_state.messages.append({"role": "ai", "content": response})