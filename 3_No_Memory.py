from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import create_react_agent


#  No Memory Example
agent = create_react_agent(
   model="groq:llama-3.3-70b-versatile", 
   tools=[], 
   prompt="You are a helpful assistant" 
)


# Run the agent
response = agent.invoke(
   {"messages": [{"role": "user", "content": "when was he born"}]}
)
print(response)

