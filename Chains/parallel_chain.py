from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",  
    task="text-generation",
)

model1 = ChatHuggingFace(llm=llm)
# model1 = ChatGoogleGenerativeAI(model="models/gemini-pro-latest")
model2 = ChatGoogleGenerativeAI(model="models/gemini-pro-latest")

prompt1 = PromptTemplate(
    template="Generate short and simple notes from the following text.\n {text}",
    input_variables=["text"]
)

prompt2 = PromptTemplate(
    template="Generate 5 short question answers from the following text.\n {text}",
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template='Merge the following notes and Q&A into a single text.\n Notes: {notes}\n Q&A: {qa}',
    input_variables=['notes','qa']
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'notes': prompt1 | model1 | parser,
    'qa': prompt2 | model2 | parser,
})

merge_chain = prompt3 | model2 | parser
chain = parallel_chain | merge_chain

text="""
    Support Vector Machines (SVMs in short) are machine learning algorithms that are used for classification and regression purposes. SVMs are one of the powerful machine learning algorithms for classification, regression and outlier detection purposes. An SVM classifier builds a model that assigns new data points to one of the given categories. Thus, it can be viewed as a non-probabilistic binary linear classifier.

The original SVM algorithm was developed by Vladimir N Vapnik and Alexey Ya. Chervonenkis in 1963. At that time, the algorithm was in early stages. The only possibility is to draw hyperplanes for linear classifier. In 1992, Bernhard E. Boser, Isabelle M Guyon and Vladimir N Vapnik suggested a way to create non-linear classifiers by applying the kernel trick to maximum-margin hyperplanes. The current standard was proposed by Corinna Cortes and Vapnik in 1993 and published in 1995.

SVMs can be used for linear classification purposes. In addition to performing linear classification, SVMs can efficiently perform a non-linear classification using the kernel trick. It enable us to implicitly map the inputs into high dimensional feature spaces.
"""

# result = chain.invoke({'text':text})
# print(result)

chain.get_graph().print_ascii()