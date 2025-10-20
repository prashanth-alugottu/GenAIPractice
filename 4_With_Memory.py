from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver


checkpointer = InMemorySaver()
agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile", 
    tools=[], 
    checkpointer=checkpointer,
    prompt="You are a helpful assistant with memory"
)

config = {"configurable": {"thread_id": "1"}}

first_response = agent.invoke(
    {"messages": [{"role": "user", "content": "who is modi"}]},
    config=config)

config = {"configurable": {"thread_id": "2"}}


second_response = agent.invoke(
    {"messages": [{"role": "user", "content": "When was he born?"}]},
    config=config
)

print(first_response)
print("--------------------------")
print(second_response)



