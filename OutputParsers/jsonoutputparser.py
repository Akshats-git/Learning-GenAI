from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",  
    task="text-generation",
)

model = ChatHuggingFace(llm=llm)

parser = JsonOutputParser()
template = PromptTemplate(
    template="Give me the name,age,city of a fictional character.\n{format_instruction}",
    input_variables=[],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

prompt = template.format()
print(prompt)
final_result = parser.parse(model.invoke(prompt).content)
print(final_result)