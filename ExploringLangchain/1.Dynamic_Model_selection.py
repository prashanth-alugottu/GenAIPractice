from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv
load_dotenv()


basic_model = ChatOpenAI(model="gpt-4o-mini")
advanced_model = ChatOpenAI(model="gpt-4o")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])
    print(f" Total messages in conversation so far: {message_count}")
    if message_count > 3:
        print("🔄 Switching to: gpt-4o (conversation is long)")
        model = advanced_model
    else:
        print("⚡ Using: gpt-4o-mini (conversation is short)")
        model = basic_model

    return handler(request.override(model=model))

checkpointer = InMemorySaver()
agent = create_agent(
    model=basic_model,  # Default model
    tools=[],
    middleware=[dynamic_model_selection],
    checkpointer=checkpointer,
    system_prompt="You are a helpful assistant with dynamic model selection based on conversation length."
)

while True:
    user_input = ""
    while not user_input.strip():
        user_input = input("You: ")
        if not user_input:
            print("⚠️ Please enter something...")
            

    if user_input.lower() in {"exit", "quit"}:
        break

    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        {"configurable": {"thread_id": "1"}}
    )

    print(f"\nAgent: {result['messages'][-1].content}")

