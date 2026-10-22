from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

from dotenv import load_dotenv

import streamlit as st
load_dotenv()
llm = HuggingFaceEndpoint( repo_id="google/gemma-2-2b-it",provider="featherless-ai" , task="text-generation")
st.header('Reaserach tool')
model = ChatHuggingFace(llm=llm)


user_input = st.text_input("Enter input")

if st.button('Summarze'):
   result = model.invoke(user_input)
   st.write(result.content)