from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, Field

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-1.5-pro')

# schema
json_schema = {}

structured_model = model.with_structured_output(json_schema) #passing TypedDict doesnt work anymore

result = structured_model.invoke("""The hardware is great but the software feels very bloated. There are too many pre-installed apps that I never use and they just take up space. The battery life is decent but could be better. Overall, it's an average phone with some good features but also some drawbacks.""")

print(result)