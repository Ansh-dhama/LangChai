from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence


load_dotenv()

prompt = PromptTemplate(
    template= 'write a joke on {topic}',
    input_variables=['topic']
)

model = ChatGoogleGenerativeAI( model="gemini-3.6-flash")
parser = StrOutputParser()

chain = RunnableSequence(prompt,model,parser)

result = chain.invoke({'topic':'india'})

print(result)