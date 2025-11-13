from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-large',dimensions=300)

document = [
    "Virat Kohli is a famous cricketer",
    "Sachin Tendulkar is a legendary cricketer",
    "Rohit Sharma is the captain of the Indian cricket team",
    "MS Dhoni is known for his finishing skills in cricket",
    "Ravindra Jadeja is an all-rounder in cricket",
    "Yuvraj Singh is famous for his six sixes in an over",
]

query = "Tell me about Sachin Tendulkar"

doc_embeddings = embedding.embed_documents(document)
query_embedding = embedding.embed_query(query)

scores = cosine_similarity([query_embedding], doc_embeddings)[0]
index,score = sorted(list(enumerate(scores)), key=lambda x:x[1])[-1]

print(query)
print(document[index])
print("Similarity score is: ",score)
