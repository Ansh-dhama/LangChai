from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


chat_template = ChatPromptTemplate.from_messages([

    (
        "system",
        "You are a helpful customer support agent"
    ),

    MessagesPlaceholder(
        variable_name="chat_history"
    ),

    (
        "human",
        "{query}"
    )

])


chat_history = []


with open("chat_history.txt", "r") as file:

    for line in file:

        role, message = line.strip().split("|", 1)

        if role == "human":

            chat_history.append(
                HumanMessage(content=message)
            )

        elif role == "ai":

            chat_history.append(
                AIMessage(content=message)
            )


chain = chat_template | model


result = chain.invoke({

    "chat_history": chat_history,

    "query": "Where is my refund?"

})


print(result.content[0]['text'])