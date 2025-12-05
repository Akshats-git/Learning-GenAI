from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

documents = (
    Document(page_content="Mitchell Starc is widely regarded as one of the best pink-ball bowlers. "
                          "He has taken more wickets than any other bowler in day-night Tests and "
                          "is known for his deadly swing under lights."),

    Document(page_content="In day-night Test cricket, the pink ball tends to swing more during the "
                          "twilight period. Fast bowlers who can exploit this movement often succeed, "
                          "and Australia’s pace attack has historically dominated these matches."),

    Document(page_content="Other strong pink-ball performers include Josh Hazlewood and Trent Boult. "
                          "Hazlewood has an exceptional average in day-night Tests, while Boult’s ability "
                          "to swing the ball both ways makes him dangerous."),

    Document(page_content="Mitchell Starc made his pink-ball Test debut in 2015 and quickly became dominant. "
                          "His pace above 145 km/h and late swing have resulted in multiple match-winning spells.")
)

embeddings = OpenAIEmbeddings()

vector_store = Chroma.from_documents(
    documents=documents, 
    embedding=embeddings,
    collection_name="my_collection")

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

query = "Is starc the best pink ball bowler?"
docs = retriever.invoke(query)

for i,doc in enumerate(docs):
    print(f"\n-- Result {i+1} --")
    print(doc.page_content)