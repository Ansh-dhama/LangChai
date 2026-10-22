from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel ,RunnableBranch , RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

llm = HuggingFaceEndpoint( repo_id="google/gemma-2-2b-it",provider="featherless-ai" , task="text-generation")

model1 = ChatHuggingFace(llm=llm)
parser = StrOutputParser()

prompt1 = PromptTemplate(
    template="""
Classify the sentiment of the following feedback as either positive or negative.

Feedback:
{feedback}

Return only one word: positive or negative.
""",
    input_variables=["feedback"]
)


classifier_chain = prompt1 | model1 | parser


prompt2 = PromptTemplate(
    template="""
write an appopriate response to this positive feedback \n 
{feedback}
""",
    input_variables=["feedback"]
)

prompt3 = PromptTemplate(
    template="""
write an appopriate response to this negative feedback \n 
{feedback}
""",
    input_variables=["feedback"]
)
parallel_chain = RunnableParallel(
    sentiment=classifier_chain,

    feedback=RunnableLambda(
        lambda x: x["feedback"]
    )
)

branch_chain = RunnableBranch(
    (lambda x:x["sentiment"].strip().lower() == 'positive', prompt2 |model1 | parser),
    (lambda x:x["sentiment"].strip().lower() =='negative',prompt3|model1|parser),
    RunnableLambda(lambda x: "could not find sentiment")
)

chain = parallel_chain | branch_chain

print(chain.invoke({'feedback':'this is a very bad phone'}))