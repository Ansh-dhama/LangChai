from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint( repo_id="google/gemma-2-2b-it",provider="featherless-ai" , task="text-generation")
model = ChatHuggingFace(llm=llm)
result = model.invoke("kya hal h ")

print(result.content)    