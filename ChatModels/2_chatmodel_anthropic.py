from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(model = 'calude-3-5-sonnet-20241022')

result = model.invoke("What is 4+4?")
print(result.content)