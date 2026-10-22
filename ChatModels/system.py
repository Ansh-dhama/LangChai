from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    pipeline_kwargs={
          "max_new_tokens": 50,
        "temperature": 0.2,
        "do_sample": True,
        "return_full_text": False
    }
)
result = llm.invoke("what is india capital")

print(result)    