from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()



agent = create_agent(model="openai:gpt-4o-mini", 
                     tools=[],
                     system_prompt="You are a helpful assistant that answers questions about programming."
                    )

result = agent.invoke({
    "messages":[ {"role":"user","content":"Who is indian PM"} ]
})

print(result["messages"][-1].content)