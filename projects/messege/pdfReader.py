from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# -----------------------------------------
# Load environment variables
# -----------------------------------------

load_dotenv()


# -----------------------------------------
# STEP 1: Load document
# -----------------------------------------

loader = TextLoader("docs.txt")

documents = loader.load()


# -----------------------------------------
# STEP 2: Split document into chunks
# -----------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)

print("Total chunks:", len(docs))


# -----------------------------------------
# STEP 3: Create embedding model
# -----------------------------------------

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


# -----------------------------------------
# STEP 4: Create FAISS vector store
# -----------------------------------------

vectorstore = FAISS.from_documents(
    docs,
    embedding_model
)


# -----------------------------------------
# STEP 5: Create retriever
# -----------------------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3
    }
)


# -----------------------------------------
# STEP 6: User query
# -----------------------------------------

query = "What are the key takeaways from the document?"


# -----------------------------------------
# STEP 7: Retrieve relevant chunks
# -----------------------------------------

retrieved_docs = retriever.invoke(query)


print("\nRetrieved Documents:")

for i, doc in enumerate(retrieved_docs):

    print(f"\n--- Chunk {i + 1} ---")

    print(doc.page_content)


# -----------------------------------------
# STEP 8: Combine retrieved chunks
# -----------------------------------------

context = "\n\n".join(
    doc.page_content
    for doc in retrieved_docs
)


# -----------------------------------------
# STEP 9: Create RAG prompt
# -----------------------------------------

prompt = PromptTemplate(

    template="""
You are a helpful assistant.

Answer the user's question using only the context provided below.

If the answer is not present in the context,
say:

"I don't know based on the provided document."

Context:
{context}

Question:
{question}

Answer:
""",

    input_variables=[
        "context",
        "question"
    ]
)


# -----------------------------------------
# STEP 10: Create Gemini LLM
# -----------------------------------------

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# -----------------------------------------
# STEP 11: Output parser
# -----------------------------------------

parser = StrOutputParser()


# -----------------------------------------
# STEP 12: Create chain
# -----------------------------------------

chain = prompt | model | parser


# -----------------------------------------
# STEP 13: Send context + question to Gemini
# -----------------------------------------

result = chain.invoke({

    "context": context,

    "question": query
})


# -----------------------------------------
# STEP 14: Final answer
# -----------------------------------------

print("\n========================")
print("FINAL ANSWER")
print("========================")

print(result)