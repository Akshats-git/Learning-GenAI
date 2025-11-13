from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
# from pydantic import BaseModel
from typing import TypedDict, Annotated, Optional, Literal

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-1.5-pro')

# schema
class Review(TypedDict):
    # summary:str
    summary:Annotated[str, "A brief summary of the review in one sentence."]
    key_themes:Annotated[list[str],"Write down all the key themes discussed in the review in a list."]
    sentiment:Annotated[Literal["pos","neg"], "Return review of the sentiment as either 'pos' or 'neg'."]
    pros:Annotated[Optional[list[str]],"List the pros mentioned in the review."]
    cons:Annotated[Optional[list[str]],"List the cons mentioned in the review."]

structured_model = model.with_structured_output(Review) #passing TypedDict doesnt work anymore

result = structured_model.invoke("""The hardware is great but the software feels very bloated. There are too many pre-installed apps that I never use and they just take up space. The battery life is decent but could be better. Overall, it's an average phone with some good features but also some drawbacks.""")

print(result)