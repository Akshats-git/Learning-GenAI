from langchain_community.document_loaders.text import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

prompt = PromptTemplate(
    template="Write a summary for the following facts: {facts}",
    input_variables=["facts"]
)

parser = StrOutputParser()

loader = TextLoader('sports.txt',encoding='utf-8')
docs = loader.load()

# print(docs)
print(docs[0].page_content)
print(docs[0].metadata)

chain = prompt | model | parser
print(chain.invoke({"facts": docs[0].page_content}))
