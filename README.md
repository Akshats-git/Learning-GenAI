# GenAI with LangChain

This repo is where I'm learning GenAI using LangChain. It has small scripts, one folder per topic, using different providers like OpenAI, Gemini, Anthropic, and Hugging Face.

## Folders

- **LLMs** - basic LLM completion call
- **ChatModels** - chat models from different providers (OpenAI, Anthropic, Google, Hugging Face)
- **LangchainPrompts** - prompt templates, chat prompt templates, chat history, a Streamlit prompt UI, and a simple CLI chatbot
- **OutputParsers** - parsing model output as string, JSON, structured, and Pydantic
- **StructuredOutput** - getting structured output using TypedDict, Pydantic, and JSON schema
- **Chains** - simple, sequential, parallel, and conditional chains
- **Runnables** - RunnableSequence, RunnableParallel, RunnableBranch, RunnableLambda, RunnablePassthrough
- **DocumentLoaders** - loading text, CSV, PDF, directory, and web page data
- **TextSplitters** - length based, recursive, semantic, and code based splitting
- **EmbeddingModels** - generating embeddings and checking document similarity
- **Retrievers** - vector store retriever, MMR, multi query retriever, Wikipedia retriever
- **Streamlit** - small Streamlit UI experiments

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the root folder with your API keys:

```
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
HUGGINGFACEHUB_API_TOKEN=...
```

## Running a script

Each file runs on its own.

```bash
python Chains/simple_chain.py
python Retrievers/vector_store.py
streamlit run LangchainPrompts/prompt_ui.py
streamlit run Streamlit/first.py
```

## Note

These are just learning scripts, not a real project. Some use hardcoded inputs and print statements instead of proper error handling. I also switch between providers (Gemini, OpenAI, Hugging Face) depending on what I was testing at the time.
