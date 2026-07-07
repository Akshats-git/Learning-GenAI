# LangChain Notes

These are my notes from learning LangChain. Each section explains one concept, shows a small example, and links to the actual script in this repo.

## 1. What is LangChain

LangChain is a framework for building apps powered by language models. On its own, a model just takes text in and gives text out. LangChain gives you pieces to connect around the model, like prompts, parsers, memory, document loaders, and vector stores. You connect these pieces into a pipeline instead of writing all the glue code yourself.

```
   Your Input           LangChain Pieces              Final Output
 ───────────────    ─────────────────────────      ─────────────────
   "Summarize     -> Prompt -> Model -> Parser  ->   Clean text or
    this text"                                       structured data
```

## 2. LLMs vs Chat Models

LangChain gives you two kinds of wrappers around language models.

- **LLM**: takes a plain string and returns a plain string. This is the older style API. See [LLMs/llm_demo.py](LLMs/llm_demo.py), which uses `OpenAI(model_name="gpt-3.5-turbo-instruct")`.
- **Chat Model**: takes a list of messages and returns a message. Almost all modern providers (OpenAI, Anthropic, Google, Hugging Face) are used through chat models now. See [ChatModels/](ChatModels/) for one example per provider.

```python
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model='gpt-4o-mini')
result = model.invoke("What is the capital of India?")
print(result.content)
```

The provider does not matter much to your code. `ChatOpenAI`, `ChatAnthropic`, `ChatGoogleGenerativeAI`, and `ChatHuggingFace` all expose the same `.invoke()` method. This is the whole point of LangChain: you can swap providers without rewriting your pipeline.

## 3. Prompts

A prompt template is a reusable text template with placeholders. You fill in the placeholders at run time instead of hardcoding a new string every time.

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="Generate 5 interesting facts about {topic}.",
    input_variables=["topic"]
)
prompt = template.invoke({'topic': 'Black Holes'})
```

For chat models, you build a list of messages instead of one string. `ChatPromptTemplate` builds that list from role and text pairs. See [LangchainPrompts/chat_prompt_template.py](LangchainPrompts/chat_prompt_template.py).

```python
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate([
    ('system', "You are a helpful {domain} expert."),
    ('human', "Explain in simple terms what is {topic}.")
])
```

To keep a running conversation, use `MessagesPlaceholder`. It reserves a spot in the template for a list of past messages, so the model can see chat history. See [LangchainPrompts/message_placeholder.py](LangchainPrompts/message_placeholder.py) and the CLI chat loop in [LangchainPrompts/chatbot.py](LangchainPrompts/chatbot.py).

```
System Message
Message Placeholder  <- past chat history gets inserted here
Human Message (current question)
```

## 4. Output Parsers

A model always replies with text (or a message object wrapping text). An output parser turns that raw text into something more usable in code.

| Parser | What it does | File |
|---|---|---|
| `StrOutputParser` | Just extracts the plain string content | [OutputParsers/stroutputparser.py](OutputParsers/stroutputparser.py) |
| `JsonOutputParser` | Asks the model to return JSON, then parses it into a dict | [OutputParsers/jsonoutputparser.py](OutputParsers/jsonoutputparser.py) |
| `StructuredOutputParser` | Parses output against a list of named fields (`ResponseSchema`) | [OutputParsers/structuredoutputparser.py](OutputParsers/structuredoutputparser.py) |
| `PydanticOutputParser` | Parses output into a Pydantic model, with type validation | [OutputParsers/pydanticoutputparser.py](OutputParsers/pydanticoutputparser.py) |

All of these work the same way. They generate format instructions that get added to your prompt, telling the model exactly how to format its reply. Then they parse the reply back into the format you asked for.

```
 Prompt + format instructions -> Model -> Raw text -> Parser -> Python object
```

## 5. Structured Output

Output parsers are one way to get structured data out of a model. A newer and simpler way is `.with_structured_output()`, which is built into chat models directly. You give it a schema and it returns a validated object, without needing a separate parser step.

You can describe the schema in three ways:

- **TypedDict**: a plain dictionary shape, good for simple cases. See [StructuredOutput/typeddict_demo.py](StructuredOutput/typeddict_demo.py) and [StructuredOutput/with_structured_output_typeddict.py](StructuredOutput/with_structured_output_typeddict.py).
- **Pydantic model**: adds validation rules like `gt=0` or `Literal["pos","neg"]`. See [StructuredOutput/pydantic_demo.py](StructuredOutput/pydantic_demo.py) and [StructuredOutput/with_structured_output_pydantic.py](StructuredOutput/with_structured_output_pydantic.py).
- **JSON schema**: a plain dictionary describing the shape, useful when you do not want to depend on Pydantic or TypedDict. See [StructuredOutput/with_structured_output_json.py](StructuredOutput/with_structured_output_json.py).

```python
from pydantic import BaseModel, Field
from typing import Literal

class Review(BaseModel):
    summary: str = Field(description="A brief summary of the review.")
    sentiment: Literal["pos", "neg"]

structured_model = model.with_structured_output(Review)
result = structured_model.invoke("The battery life is bad but the camera is great.")
```

Pydantic also validates data on its own, outside of LangChain. `EmailStr` checks for a valid email format, and `Field(gt=0, le=10)` restricts a number to a range. This is worth knowing because LangChain uses Pydantic under the hood for a lot of its own validation.

## 6. Runnables

A Runnable is the base building block in LangChain. Prompts, models, and parsers are all Runnables, which means they all share the same `.invoke()` interface. Because of this, they can be snapped together like Lego pieces. The `Runnables/` folder demonstrates the primitives directly, before we look at the shorter `|` pipe syntax in the next section.

- **RunnableSequence**: runs steps one after another, passing the output of one as the input to the next. See [Runnables/runnable_sequence.py](Runnables/runnable_sequence.py).
- **RunnableParallel**: runs multiple steps on the same input at the same time, and returns a dict of their results. See [Runnables/runnable_parallel.py](Runnables/runnable_parallel.py).
- **RunnablePassthrough**: returns its input unchanged. Useful inside a `RunnableParallel` when you want to keep the original input alongside a transformed value. See [Runnables/runnable_passthrough.py](Runnables/runnable_passthrough.py).
- **RunnableLambda**: wraps a plain Python function so it can be used as a step in a chain. See [Runnables/runnable_lambda.py](Runnables/runnable_lambda.py).
- **RunnableBranch**: picks which step to run next based on a condition, like an if/else for chains. See [Runnables/runnable_branch.py](Runnables/runnable_branch.py).

```
RunnableSequence:        A -> B -> C

RunnableParallel:        Input -> A -> "key1": result_a
                                -> B -> "key2": result_b

RunnableBranch:          Input -> condition met?  -> yes -> chain A
                                                    -> no  -> chain B
```

## 7. Chains

A chain is just a Runnable pipeline built with the `|` (pipe) operator instead of calling `RunnableSequence` directly. It is the idiomatic way to write LangChain pipelines, also called LCEL (LangChain Expression Language).

```python
chain = prompt | model | parser
result = chain.invoke({'topic': 'Wonders of the World'})
```

### Simple chain

One prompt, one model, one parser. See [Chains/simple_chain.py](Chains/simple_chain.py).

```
{topic} -> Prompt -> Model -> Parser -> facts about topic
```

### Sequential chain

The output of one full chain feeds into another prompt. See [Chains/sequential_chain.py](Chains/sequential_chain.py).

```
{topic} -> Prompt1 -> Model -> Parser -> detailed report
                                              |
                                              v
                                      Prompt2 -> Model -> Parser -> 5 point summary
```

### Parallel chain

Two independent chains run on the same input, and their results are merged. See [Chains/parallel_chain.py](Chains/parallel_chain.py).

```
                 -> Prompt1 -> Model1 -> Parser -> notes -----
{text} -> input -|                                            |-> merge prompt -> Model -> final text
                 -> Prompt2 -> Model2 -> Parser -> Q&A -------
```

### Conditional chain

A classifier chain decides which path to take, then `RunnableBranch` routes to the matching chain. See [Chains/conditional_chain.py](Chains/conditional_chain.py).

```
{feedback} -> Classifier chain -> sentiment
                                     |
                     -----------------------------------
                     |                                   |
                 positive                             negative
                     |                                   |
             Prompt2 -> Model -> Parser        Prompt3 -> Model -> Parser
```

## 8. Document Loaders

Before you can search or summarize your own data, you need to load it into LangChain's `Document` format. Each loader knows how to read one kind of source and turn it into a list of `Document` objects, each with `page_content` and `metadata`.

| Loader | Reads from | File |
|---|---|---|
| `TextLoader` | A plain `.txt` file | [DocumentLoaders/text_loader.py](DocumentLoaders/text_loader.py) |
| `CSVLoader` | A `.csv` file, one Document per row | [DocumentLoaders/csv_loader.py](DocumentLoaders/csv_loader.py) |
| `PyPDFLoader` | A `.pdf` file, one Document per page | [DocumentLoaders/pypdf_loader.py](DocumentLoaders/pypdf_loader.py) |
| `DirectoryLoader` | All matching files in a folder, using another loader for each file | [DocumentLoaders/directory_loader.py](DocumentLoaders/directory_loader.py) |
| `WebBaseLoader` | The text content of a web page | [DocumentLoaders/webbase_loader.py](DocumentLoaders/webbase_loader.py) |

## 9. Text Splitters

Documents are often too long to fit in a model's context window, or too long to embed usefully. Text splitters break a document into smaller chunks.

- **Length based** (`CharacterTextSplitter`): cuts text every N characters, without caring about sentence or word boundaries. See [TextSplitters/length_based.py](TextSplitters/length_based.py).
- **Structure based** (`RecursiveCharacterTextSplitter`): tries to split on paragraph breaks first, then sentences, then words, so chunks stay more meaningful. See [TextSplitters/text_structure_based.py](TextSplitters/text_structure_based.py).
- **Code aware** (`RecursiveCharacterTextSplitter.from_language`): same idea, but it knows about code syntax, so it avoids splitting in the middle of a function. See [TextSplitters/python_code_splitting.py](TextSplitters/python_code_splitting.py).
- **Semantic** (`SemanticChunker`): embeds sentences and splits where the meaning shifts significantly, instead of using a fixed size. See [TextSplitters/semantic_meaning_based.py](TextSplitters/semantic_meaning_based.py).

```
Long document
      |
      v
[chunk 1] [chunk 2] [chunk 3] [chunk 4]   <- smaller pieces, each one embeddable
```

## 10. Embedding Models

An embedding model turns text into a list of numbers (a vector) that captures its meaning. Texts with similar meaning end up with vectors that are close to each other in that vector space.

```python
from langchain_openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=32)
vector = embedding.embed_query("Delhi is the capital of India")
```

Use `embed_query()` for a single piece of text, like a search query, and `embed_documents()` for a list of texts. See [EmbeddingModels/1_embedding_openai_query.py](EmbeddingModels/1_embedding_openai_query.py) and [EmbeddingModels/2_embedding_openai_docs.py](EmbeddingModels/2_embedding_openai_docs.py). You can also run embeddings locally without any API key, using a Hugging Face sentence-transformer model, shown in [EmbeddingModels/3_embedding_hf_local.py](EmbeddingModels/3_embedding_hf_local.py).

Once you have vectors, you can measure how similar two pieces of text are with cosine similarity. See [EmbeddingModels/document_similarity.py](EmbeddingModels/document_similarity.py), which embeds a query and a list of documents, then ranks the documents by similarity to the query.

```
"Tell me about Sachin Tendulkar"  -> embedding -> [0.02, -0.15, 0.88, ...]
"Sachin Tendulkar is a legendary
 cricketer"                       -> embedding -> [0.03, -0.14, 0.85, ...]  <- closest match
"MS Dhoni is known for his
 finishing skills"                -> embedding -> [0.40,  0.22, -0.10, ...] <- less similar
```

## 11. Retrievers

A retriever's job is to take a query and return the most relevant documents from a collection. This is the core of retrieval augmented generation (RAG): instead of relying only on what the model already knows, you fetch relevant text and hand it to the model as context.

- **Vector store retriever**: stores document embeddings in a vector database and finds the closest matches to your query's embedding. See [Retrievers/vector_store.py](Retrievers/vector_store.py), which uses Chroma.
- **Maximal Marginal Relevance (MMR)**: also picks relevant documents, but avoids picking several documents that all say the same thing. It balances relevance with diversity. See [Retrievers/maximal_marginal_relevance.py](Retrievers/maximal_marginal_relevance.py).
- **Multi query retriever**: uses a model to rewrite your one query into several different phrasings, retrieves documents for each, and combines the results. This helps when a single query wording misses relevant documents. See [Retrievers/multi_query_retriever.py](Retrievers/multi_query_retriever.py).
- **Wikipedia retriever**: fetches relevant Wikipedia article snippets for a query directly, with no vector store needed. See [Retrievers/Wikipedia.py](Retrievers/Wikipedia.py).

```
Query -> rewritten into multiple versions (multi query retriever)
              |
              v
     search vector store for each version
              |
              v
     combine and deduplicate results -> final documents
```

## 12. Putting it together: a RAG pipeline

Chaining sections 8 through 11 together gives you a full retrieval augmented generation pipeline. This is not one single file in this repo, but it is what these pieces build up to.

```
Documents (files, web pages, CSVs)
      |
      v
Document Loader
      |
      v
Text Splitter (breaks into chunks)
      |
      v
Embedding Model (chunk -> vector)
      |
      v
Vector Store (stores chunk vectors)
      |
      v
User Query -> Embedding Model -> Retriever (finds closest chunks)
      |                                  |
      |                                  v
      |                          Relevant chunks
      |                                  |
      -----------------------------------
                     |
                     v
        Prompt (query + relevant chunks) -> Chat Model -> Parser -> Answer
```

## 13. Streamlit

Streamlit is used here to build small web UIs on top of these scripts, without writing any HTML or JavaScript. Every widget is just a function call, and the whole script reruns from top to bottom every time the user interacts with something.

- Basic widgets like `st.selectbox`, `st.text`, `st.write`: [Streamlit/first.py](Streamlit/first.py)
- More input widgets like buttons, checkboxes, sliders, and date input: [Streamlit/second.py](Streamlit/second.py)
- Layout with columns, a sidebar, and an expander: [Streamlit/layouts.py](Streamlit/layouts.py)
- File upload and showing a pandas dataframe: [Streamlit/fourth.py](Streamlit/fourth.py)
- A real LangChain use case, a research paper summarizer UI built on a prompt template and a chat model: [LangchainPrompts/prompt_ui.py](LangchainPrompts/prompt_ui.py)

```
User picks options in the UI
      |
      v
Streamlit script reruns top to bottom
      |
      v
Values read from widgets -> filled into a Prompt Template
      |
      v
Chain (prompt | model) -> result shown back in the UI
```
