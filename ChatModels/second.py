from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-3.6-flash' , max_output_tokens=50)
result = llm.invoke("what a 5 line poem on cricket")

print(result.content[0]['text'])