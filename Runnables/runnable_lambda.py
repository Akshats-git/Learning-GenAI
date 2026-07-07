from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough ,RunnableLambda

load_dotenv()

def word_count(text):
    return len(text.split())

prompt1 = PromptTemplate(
    template = 'Generate a joke about {topic}',
    input_variables=['topic']
)

model = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

first_chain = RunnableSequence(prompt1,model,parser)

parallel_chain = RunnableParallel({
    'joke':RunnablePassthrough(),
    'length':RunnableLambda(word_count)
})

chain = RunnableSequence(first_chain,parallel_chain)

result = chain.invoke({'topic':'IIT'})
print(result)