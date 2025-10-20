import os
from dotenv import load_dotenv

load_dotenv()

from langgraph.prebuilt import create_react_agent


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

def deleteFolder(directory_name: str):
    """Delete a Directory"""
    if os.path.exists(directory_name):
        if os.path.isdir(directory_name):
            shutil.rmtree(directory_name)
            print(f"Directory '{directory_name}' deleted.")
        else:
            print(f"'{directory_name}' is not a directory.")
    else:
        print(f"Directory '{directory_name}' does not exist.")


agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[addFile,addFolder,deleteFolder],
    prompt="You are a helpful assistant"
)



response = agent.invoke({"messages":[{"role":"user","content":"Delete the prasha folder"}]})
print(response)

