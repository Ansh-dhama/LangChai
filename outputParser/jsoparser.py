from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash")


parser = JsonOutputParser()


template1 = PromptTemplate(
    template='give me the name , age and city  of a fictional person \n {format_instruction}',
    input_variables=[],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

chain = template1 | model | parser

result = chain.invoke({})

print(result)

# prompt = template1.format()

# print(prompt)
# result = model.invoke(prompt)

# print("\n")
# print("\n")
# print("\n")


# print(result.content[0]['text'])
# print("\n")
# print("\n")
# print("\n")


# final = parser.parse(result.content)

# print(final)



