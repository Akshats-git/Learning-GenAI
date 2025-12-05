from langchain_community.retrievers import WikipediaRetriever

retriever = WikipediaRetriever(top_k_results=2, lang="en")

query = "Is test cricket the best format?"
docs = retriever.invoke(query)

for i,doc in enumerate(docs):
    print(f"\n-- Result {i+1} --")
    print(doc.page_content)