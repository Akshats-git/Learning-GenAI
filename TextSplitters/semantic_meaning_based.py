from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings   
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

text = """
The old lighthouse on the cliff flickers faintly during storms. Meanwhile, modern researchers are developing new algorithms to improve climate prediction accuracy.

Butterflies migrate long distances in search of warmer climates. These migrations help maintain ecological balance across different regions.
"""

splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="standard_deviation",
    breakpoint_threshold_amount=0.2
)

result = splitter.split_text(text)
print(result)
