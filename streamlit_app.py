import os, streamlit as st
from groq import Groq

# Streamlit app config
st.set_page_config(page_title="Groq Playground", initial_sidebar_state="auto")

model_options = {
    "Text: Meta Llama 3.3 70B": "llama-3.3-70b-versatile",
    "Text: Meta Llama 4 Scout 17B": "meta-llama/llama-4-scout-17b-16e-instruct",
    "Text: Google Gemma 2 9B Instruct": "gemma2-9b-it",
    "Text: Mistral Saba 24B": "mistral-saba-24b",
    "Text: Alibaba Qwen 2.5 32B": "qwen-2.5-32b",
    "Text: DeepSeek R1 (Preview)": "deepseek-r1-distill-llama-70b"
}

# Groq settings
with st.sidebar:
  st.subheader("Groq Playground")
  groq_api_key = st.text_input("Groq API key", type="password")
  model_option = st.selectbox("Select chat model", list(model_options.keys()))
  model = model_options[model_option]

# Initialise session state for client and messages
if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Initialize Groq client if key is provided
if groq_api_key.strip():
  if "client" not in st.session_state:
    os.environ["GROQ_API_KEY"] = groq_api_key
    st.session_state.client = Groq(api_key=groq_api_key)

# User-Assistant chat interaction
if prompt := st.chat_input("Ask anything"):
  if not groq_api_key.strip():
    st.error("Please provide Groq API key.")
    st.stop()
  else:
    try:
      with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

      # Assistant response
      with st.chat_message("assistant"):
        response = st.session_state.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(response.choices[0].message.content)
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
    except Exception as e:
      st.exception(f"Exception: {e}")
