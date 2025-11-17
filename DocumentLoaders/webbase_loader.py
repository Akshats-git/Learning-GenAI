from langchain_community.document_loaders import WebBaseLoader

url = 'https://www.amazon.in/Sony-PS5-PlayStation-Console/dp/B0BRCP72X8'
loader = WebBaseLoader(url)

docs = loader.load()

print(docs[0].page_content)