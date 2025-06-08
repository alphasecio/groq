import os, streamlit as st
from groq import Groq
from mem0 import Memory

# Initialise session state for model, memory and API keys
if "model" not in st.session_state:
  st.session_state.model = ""

if "memory" not in st.session_state:
  st.session_state.memory = None

if "groq_api_key" not in st.session_state :
  st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    
if "openai_api_key" not in st.session_state :
  st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()

# Streamlit app config
st.set_page_config(page_title="Groq Chatbot", initial_sidebar_state="auto")

model_options = {
    "Text: Meta Llama 3.3 70B": "llama-3.3-70b-versatile",
    "Text: Meta Llama 4 Scout 17B (Preview)": "meta-llama/llama-4-scout-17b-16e-instruct",
    "Text: Google Gemma 2 9B Instruct": "gemma2-9b-it",
    "Text: Mistral Saba 24B (Preview)": "mistral-saba-24b",
    "Text: Alibaba Qwen QwQ 32B (Preview)": "qwen-qwq-32b",
    "Text: DeepSeek R1 (Preview)": "deepseek-r1-distill-llama-70b"
}

# Groq settings
with st.sidebar:
  st.title("Groq Chatbot")
  with st.expander("**⚙️ Settings**", expanded=True):
    groq_api_key = st.text_input("Groq API key", type="password", value=st.session_state.groq_api_key)
    if groq_api_key:
      st.session_state.groq_api_key = groq_api_key.strip()
    
    openai_api_key = st.text_input("OpenAI API key", type="password", value=st.session_state.openai_api_key)
    if openai_api_key:
      st.session_state.openai_api_key = openai_api_key.strip()
    
    model_option = st.selectbox("Chat model", list(model_options.keys()))
    st.session_state.model = model_options[model_option]

# Initialise session state for messages
if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Initialize Groq and Mem0 clients if keys are provided
if st.session_state.groq_api_key and st.session_state.openai_api_key:
  if "client" not in st.session_state or not isinstance(st.session_state.client, Groq):
    os.environ["GROQ_API_KEY"] = st.session_state.groq_api_key
    os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
    st.session_state.client = Groq(api_key=st.session_state.groq_api_key)

  if st.session_state.memory is None or not isinstance(st.session_state.memory, Memory):
    try:
      config = {
          "llm": {
              "provider": "groq",
              "config": {
                  "model": "llama-3.3-70b-versatile",
                  "temperature": 0.1,
                  "max_tokens": 2000,
              }
          },
          "embedder": {
              "provider": "openai",
              "config": {
                  "model": "text-embedding-3-small",
                  "api_key": st.session_state.openai_api_key,
              }
          }
      }
      st.session_state.memory = Memory.from_config(config)
    except Exception as e:
      st.error(f"Error initializing Mem0 client: {e}")

def chat_with_memory(message: str, user_id: str = "default_user") -> str:
    try:
      # Retrieve relevant memories
      memories = st.session_state.memory.search(query=message, user_id=user_id, limit=5)
      memories_str = "\n".join(f"- {entry['memory']}" for entry in memories["results"])

      # Generate Assistant response
      system_prompt = f"You are a helpful AI. Answer the question based on user query and memories.\nUser Memories:\n{memories_str}"
      messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
      response = st.session_state.client.chat.completions.create(model=st.session_state.model, messages=messages)
      assistant_response = response.choices[0].message.content
      
      # Create new memories from the conversation
      messages.append({"role": "assistant", "content": assistant_response})
      st.session_state.memory.add(messages, user_id=user_id)
    except Exception as e:
        st.error(f"Error: {e}")
    return assistant_response

# User-Assistant chat interaction
keys_ready = bool(st.session_state.groq_api_key and st.session_state.openai_api_key)
prompt = st.chat_input("Ask anything", disabled=not keys_ready)

if prompt:
  try:
    # User prompt
    with st.chat_message("user"):
      st.markdown(prompt)
      st.session_state.messages.append({"role": "user", "content": prompt})

    # Assistant response
    with st.chat_message("assistant"):
      response = chat_with_memory(prompt)
      st.markdown(response)
      st.session_state.messages.append({"role": "assistant", "content": response})
  except Exception as e:
    st.exception(f"Error during chat interaction: {e}")
elif not keys_ready:
  st.warning("Please provide API keys to start chatting...")
