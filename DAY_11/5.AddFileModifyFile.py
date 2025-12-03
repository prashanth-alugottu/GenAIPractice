import os
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent


def addFile(filename : str) -> str :
    """Create a new file in the current directory"""
    if not os.path.exists(filename):
        with open(filename,"w") as f:
            pass
        print(f"File {filename} created successfully")
    else :
        print(f"File {filename} already exists")



def addFolder(directory_name: str):
  """Create a new Directory in current directory"""
  if not os.path.exists(directory_name):
      os.mkdir(directory_name)
      print(f"Directory '{directory_name}' created.")
  else:
      print(f"Directory '{directory_name}' already exists.")

import shutil

def deleteFile(filename: str) -> str:
    """Delete a file in the current directory."""
    if not os.path.exists(filename):
        return f"File '{filename}' does not exist."

    if os.path.isdir(filename):
        return f"'{filename}' is a directory, not a file."

    os.remove(filename)
    return f"File '{filename}' deleted successfully."


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[addFile,addFolder,deleteFile],
    system_prompt="You are a helpful assistant"
)



response = agent.invoke({"messages":[{"role":"user","content":"delete the filename  ppppp.txt"}]})
print(response['messages'][-1].content)

