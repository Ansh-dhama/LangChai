from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()


llm = HuggingFaceEndpoint( repo_id="google/gemma-2-2b-it",provider="featherless-ai" , task="text-generation")
model = ChatHuggingFace(llm=llm)


template1 = PromptTemplate(
    template='write a detail report on {topic}',
    input_variables=['topic']
)

template2 = PromptTemplate(
        template='write a 5 line summary on following {text}',
    input_variables=['text'] 
)

parser = StrOutputParser()

chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({'topic':'black holl'})

print(result)

chain.get_graph().print_ascii()
