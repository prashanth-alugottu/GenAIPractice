
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-4.1") 
#         or
# model = init_chat_model(
#     "claude-sonnet-4-5-20250929",
#     # Kwargs passed to the model:
#     temperature=0.7,
#     timeout=30,
#     max_tokens=1000,
# )
        
response = model.invoke("Why do parrots talk?")
print(response.content)