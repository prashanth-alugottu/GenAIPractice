from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver



checkpointer = InMemorySaver()
model = ChatOpenAI(model="gpt-4o-mini",
                   temperature=0.2,
                   max_tokens=100,
                   timeout=30)

agent = create_agent(
        model=model, 
        tools=[], 
        checkpointer=checkpointer,
        system_prompt="You are a helpful assistant with memory")


result = agent.invoke(
    {"messages":
        [{"role":"user","content":"Who is PM for India"}]},
                      {"configurable": {"thread_id": "1"}})
print(result["messages"][-1].content)
print("----------------------------------------")
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "Who is he"}]},
    {"configurable": {"thread_id": "1"}},  
)

print(result2["messages"][-1].content)

print("----------------------------------------")
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "When was"}]},
    {"configurable": {"thread_id": "1"}},  
)

print(result2["messages"][-1].content)


