from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("CreatingOwnMcpServer")

@mcp.tool()
def addFile(file_name : str):
    """creates a file with the given name in the current directory"""
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            pass
        return f"File '{file_name}' created successfully."
    else:
        return f"File '{file_name}' already exists."
    



@mcp.tool()
def addFolder(directory_name: str):
   """Create a new Directory in current directory"""
   if not os.path.exists(directory_name):
       os.mkdir(directory_name)
       print(f"Directory '{directory_name}' created.")
   else:
       print(f"Directory '{directory_name}' already exists.")


if __name__ == "__main__":
   mcp.run(transport="stdio")
