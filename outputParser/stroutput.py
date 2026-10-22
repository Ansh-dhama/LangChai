from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash")


template1 = PromptTemplate(
    template='write a detail report on {topic}',
    input_variables=['topic']
)

template2 = PromptTemplate(
        template='write a 5 line summary on following {text}',
    input_variables=['text'] 
)

# prompt1= template1.invoke({'topic':'blackholl'})

# result = model.invoke(prompt1)
# print(result.content[0]['text'])
# print("\n")
# print("\n")


# prompt2 = template2.invoke({'text':result.content[0]['text']})

# result2 = model.invoke(prompt2)

# print(result2.content[0]['text'])


parser = StrOutputParser()

chain = template1 | model | parser | template2 | model

result = chain.invoke({'topic','black holl'})

print(result.content[0]['text'])

