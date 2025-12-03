from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from dotenv import load_dotenv 
load_dotenv()
from duckduckgo_search import DDGS
from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """Web search using DuckDuckGo."""
    results = DDGS(query, max_results=3)
    if not results:
        return "No results found."
    return "\n\n".join(f"{r['title']}\n{r['href']}\n{r.get('body','')}" for r in results)


class Context(TypedDict):
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user role."""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "You are a helpful assistant."
    print(f"User role from context: {request.runtime.context} ")
    if user_role == "expert":
        return f"{base_prompt} Provide detailed technical responses."
    elif user_role == "beginner":
        return f"{base_prompt} Explain concepts simply and avoid jargon."
   
    return base_prompt

agent = create_agent(
    model="gpt-4o",
    tools=[web_search],
    middleware=[user_role_prompt],
    context_schema=Context
)

# The system prompt will be set dynamically based on context
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Explain machine learning"}]},
    context={"user_role": "expert"}
)

print(result["messages"][-1].content)