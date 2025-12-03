from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv 
load_dotenv()



@tool
def search(query: str) -> str:
    """Search for information."""
    print(f"Executing search for query: {query}")
    # raise RuntimeError("simulated search backend failure")
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    print(f"Fetching weather for location: {location}")
    return f"Weather in {location}: Sunny, 72°F"



@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle errors during tool execution."""
    try:
        print("2. Middleware: Trying to execute tool")
        return handler(request)
    except Exception as e:
        print("3. Middleware: Caught an error during tool execution")
        error_msg = f"Tool error: Please check your input and try again. ({str(e)})"
        return ToolMessage(
            content=error_msg,
            tool_call_id=request.tool_call["id"]
        )
        
        
        
model = ChatOpenAI(model="gpt-4o-mini", 
                   temperature=0, 
                   max_tokens=50, 
                   timeout=15)
agent = create_agent(
    model=model,
    tools=[search, get_weather],
    middleware=[handle_tool_errors]
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Search for the best genai course"}]
})

print(result["messages"][-1].content)



