from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.agents.middleware import wrap_tool_call
from duckduckgo_search import ddgs
from langchain.tools import tool
from langchain.messages import ToolMessage
from dotenv import load_dotenv 
load_dotenv()



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
            tool_call_id=request.tool_call["id"],
            is_error=True
        )
    

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model="gpt-4o-mini",
    middleware=[handle_tool_errors],
    response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "I need Alugottu Prashanth name and email from linked"}]
})


print(result["structured_response"])
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')