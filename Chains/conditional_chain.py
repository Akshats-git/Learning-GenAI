from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda

load_dotenv()

model = ChatGoogleGenerativeAI(model="models/gemini-pro-latest")

class Feedback(BaseModel):
    sentiment: Literal['positive','negative']=Field(description="Give the sentiment of the feedback.")

parser = StrOutputParser()
parser2 = PydanticOutputParser(pydantic_object=Feedback)

prompt1 = PromptTemplate(
    template="Classify the sentiment of the following feedback as positive or negative.\n {feedback}\n {format_instructions}",
    input_variables=["feedback"],
    partial_variables={"format_instructions":parser2.get_format_instructions()},
)

classifier_chain = prompt1 | model | parser2

prompt2 = PromptTemplate(
    template="Write an appropriate response to the user for this positive feedback.\n Feedback: {feedback}",
    input_variables=["feedback"]
)

prompt3 = PromptTemplate(
    template="Write an appropriate response to the user for this negative feedback.\n Feedback: {feedback}",
    input_variables=["feedback"]
)

# print(classifier_chain.invoke({'feedback':"This is a terrible smartphone."}))
branch_chain = RunnableBranch(
    (lambda x: x.sentiment=='positive',prompt2 | model | parser),
    (lambda x: x.sentiment=='negative',prompt3 | model | parser),
    RunnableLambda(lambda x: "No valid sentiment found."),
)

chain = classifier_chain | branch_chain
result = chain.invoke({'feedback':"This is a terrible smartphone."})
print(result)