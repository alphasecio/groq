import os, streamlit as st
from groq import Groq

# Streamlit app
st.subheader("Groq Playground")
with st.sidebar:
  groq_api_key = st.text_input("Groq API Key", type="password")
  option = st.selectbox("Select Model", [
    "Text: Meta Llama 3.1 70B",
    "Text: Google Gemma 2 9B Instruct",
    "Text: Mixtral 8x7B Instruct"]
    )

prompt = st.text_input("Prompt", label_visibility="collapsed")

os.environ["GROQ_API_KEY"] = groq_api_key
client = Groq(api_key=groq_api_key)

# If Generate button is clicked
if st.button("Generate"):
  if not groq_api_key.strip() or not prompt.strip():
    st.error("Please provide the missing fields.")
  else:
    try:
      with st.spinner("Please wait..."):
        if option == "Text: Meta Llama 3.1 70B":
          # Run llama-3.1-70b-versatile model on Groq
          chat_completion = client.chat.completions.create(
              messages=[
                  {
                      "role": "user",
                      "content": prompt,
                  }
              ],
              model="llama-3.1-70b-versatile",
          )
          st.success(chat_completion.choices[0].message.content)
        elif option == "Text: Google Gemma 2 9B Instruct":
          # Run gemma2-9b-it model on Groq
          chat_completion = client.chat.completions.create(
              messages=[
                  {
                      "role": "user",
                      "content": prompt,
                  }
              ],
              model="gemma2-9b-it",
          )
          st.success(chat_completion.choices[0].message.content)
        elif option == "Text: Mixtral 8x7B Instruct":
          # Run mixtral-8x7b-32768 model on Groq
          chat_completion = client.chat.completions.create(
              messages=[
                  {
                      "role": "user",
                      "content": prompt,
                  }
              ],
              model="mixtral-8x7b-32768",
          )
          st.success(chat_completion.choices[0].message.content)
    except Exception as e:
      st.exception(f"Exception: {e}")
