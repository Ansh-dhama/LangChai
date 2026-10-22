import time
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# 1. Initialize the Gemini LLM
# disable_streaming=True ensures max_retries works properly for 429 and 503 errors
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    max_retries=10,
    disable_streaming=True
)

# 2. Create the Search Tool
search_tool = DuckDuckGoSearchRun()

# 3. Define the exact 'hwchase17/react' prompt locally
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# 4. Create the ReAct Agent combining Gemini, Tools, and Prompt
agent = create_react_agent(
    llm=llm,
    tools=[search_tool],
    prompt=prompt
)

# 5. Create the Agent Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

# 6. Invoke the Agent with a query (with a retry fallback for 503 server spikes)
for attempt in range(3):
    try:
        response = agent_executor.invoke({
            "input": "What are the three ways to reach Goa from Delhi?"
        })
        print("\n--- Final Answer ---")
        print(response["output"])
        break
    except Exception as e:
        print(f"\n[Warning] Server busy or rate-limited (Attempt {attempt + 1}/3). Waiting 15 seconds...")
        time.sleep(15)