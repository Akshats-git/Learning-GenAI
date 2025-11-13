from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGoogleGenerativeAI(model="models/gemini-pro-latest")  # correct model

result = model.invoke("Who is the most beautiful actress of India?")
print(result.content)

# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # List all models
# for m in genai.list_models():
#     print(m.name, m.supported_generation_methods)
