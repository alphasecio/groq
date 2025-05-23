# Groq Chatbot with Memory
[Groq](https://groq.com) is a platform for running large language models (LLMs) with token-based pricing and no infrastructure management. Groq uses LPU Inference Engines, a new type of end-to-end processing unit system that provides fast inference for computationally intensive systems. This project showcases a Streamlit app using Groq-hosted models combined with [Mem0](https://github.com/mem0ai/mem0) for persistent conversational memory.

Sign up for an account at [GroqCloud](https://console.groq.com/keys) and get an API key, which you'll need for this project. You'll also need an [OpenAI API key](https://platform.openai.com/account/api-keys) for the embeddings model used by Mem0.

![groq-playground](./groq-playground.png)

### Supported Models
* Groq (for chat response)
  * `llama-3.3-70b-versatile`
  * `meta-llama/llama-4-scout-17b-16e-instruct`
  * `gemma2-9b-it`
  * `mistral-saba-24b`
  * `qwen-qwq-32b`
  * `deepseek-r1-distill-llama-70b`
* Mem0 (for memory backend)
  * `mixtral-8x7b-32768`: for semantic memory retrieval
  * `text-embedding-3-small`: for embeddings

### Usage
1. Clone the repository. Alternatively, deploy to [Railway](https://railway.app/?referralCode=alphasec), Render, or Google Cloud Run.
```bash
git clone https://github.com/alphasecio/groq.git
cd groq
```
2. Set your API keys either as environment variables or via the Streamlit sidebar inputs.
3. Run the app.
```bash
streamlit run streamlit_app.py
````
