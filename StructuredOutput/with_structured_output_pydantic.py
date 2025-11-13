from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, Field

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-1.5-pro')

# schema
class Review(BaseModel):
    # summary:str
    key_themes: list[str]= Field(description="Write down all the key themes discussed in the review in a list.")
    summary: str = Field(description="A brief summary of the review in one sentence.")
    sentiment: Literal["pos","neg"] = Field(description="Return review of the sentiment as either 'pos' or 'neg'.")
    pros: Optional[list[str]] = Field(default=None, description="List the pros mentioned in the review.")
    cons: Optional[list[str]] = Field(default=None, description="List the cons mentioned in the review.")
    name: Optional[str] = Field(default=None, description="Write the name of the reviewer")

structured_model = model.with_structured_output(Review) #passing TypedDict doesnt work anymore

result = structured_model.invoke("""The hardware is great but the software feels very bloated. There are too many pre-installed apps that I never use and they just take up space. The battery life is decent but could be better. Overall, it's an average phone with some good features but also some drawbacks.""")

print(result)