from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain.retrievers.multi_query import MultiQueryRetriever

documents = (
    Document(page_content="LangChain is a framework designed to help developers build applications powered by large language models by chaining together components like prompts, memory, and tools."),
    Document(page_content="Chroma is an open-source vector database optimized for storing embeddings and performing fast similarity search using algorithms such as cosine similarity and MMR."),
    Document(page_content="Embeddings convert text into high-dimensional vectors so that semantically similar pieces of information can be retrieved efficiently."),
    Document(page_content="LangChain integrates seamlessly with vector stores like Chroma to enable retrieval-augmented generation, where relevant documents are fetched based on embedding similarity."),
    Document(page_content="MMR, or Maximal Marginal Relevance, balances relevance and diversity when retrieving documents, ensuring that results are not only similar to the query but also different from each other.")
)

embeddings = OpenAIEmbeddings()

vector_store = FAISS.from_documents(
    documents=documents, 
    embedding=embeddings
)

retriever = MultiQueryRetriever.from_llm(
    retriever = vector_store.as_retriever(search_kwargs={"k": 2}),
    llm = ChatOpenAI(model="gpt-5")
)

query = "What is Chroma?"
docs = retriever.invoke(query)

for i,doc in enumerate(docs):
    print(f"\n-- Result {i+1} --")
    print(doc.page_content)