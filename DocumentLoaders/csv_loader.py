from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path="tech_gadgets.csv")

docs = loader.load()

print(len(docs))
print(docs[0])