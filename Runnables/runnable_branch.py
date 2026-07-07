from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough ,RunnableLambda, RunnableBranch

load_dotenv()

def word_count(text):
    return len(text.split())

prompt1 = PromptTemplate(
    template = 'Write a detialed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template = 'Summarize the following text: {text}',
    input_variables=['text']
)

model = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

report_chain = RunnableSequence(prompt1,model,parser)
summary_chain = RunnableSequence(prompt2,model,parser)
branch_chain = RunnableBranch(
    (lambda x:len(x.split())>100,summary_chain),
    RunnablePassthrough()
)

chain = RunnableSequence(report_chain, branch_chain)
print(chain.invoke({'topic':'Artificial Intelligence'}))