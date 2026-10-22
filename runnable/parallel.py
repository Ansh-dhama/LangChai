from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel , RunnableSequence



load_dotenv()



model = ChatGoogleGenerativeAI( model="gemini-3.6-flash")
parser = StrOutputParser()


prompt1 = PromptTemplate(
    template= 'generate a tweet about  {topic}',
    input_variables=['topic']
)
prompt2 = PromptTemplate(
    template= 'generate a linkdien post  {topic}',
    input_variables=['topic']
)

chain = RunnableParallel({
    'tweet':RunnableSequence(prompt1,model,parser),
    'topic':RunnableSequence(prompt2,model,parser)
})

result = chain.invoke({'topic':'ai'} )

print(result['tweet'])

print('\n\n')

print(result['topic'])