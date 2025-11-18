from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

text = """Python Code"""

splitter =  RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=300, 
    chunk_overlap=0
)

result = splitter.split_text(text)
print(result)