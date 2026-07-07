from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

model = ChatGoogleGenerativeAI(model='models/gemini-pro-latest')

class Person(BaseModel):
    name: str = Field(description="The name of the person")
    age: int = Field(gt=18,description="The age of the person")
    city: str = Field(description="The city where the person lives")

parser = PydanticOutputParser(pydantic_object=Person)
template = PromptTemplate(
    template="Generate the name,age,city of a fictional {place} person.\n{format_instructions}",
    input_variables=["place"],
    partial_variables={"format_instructions":parser.get_format_instructions()}
)
prompt = template.format(place="Russia")
result = model.invoke(prompt)
final_result = parser.parse(result.content)
print(final_result)
