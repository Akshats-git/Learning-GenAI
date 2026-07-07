from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

loader = PyPDFLoader('sports.pdf')

prompt = PromptTemplate(
    template="Write a summary for the following facts: {facts}",
    input_variables=["facts"]
)

parser = StrOutputParser()

docs = loader.load()
print(docs)