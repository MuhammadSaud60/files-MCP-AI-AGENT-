# MCP File Server

A small MCP server I built while learning how Model Context Protocol works with LangChain agents.
Instead of giving an AI agent direct access to files, the agent communicates with an MCP server, and the MCP server provides controlled file operations as tools.
I built this project to understand the complete flow rather than just using MCP through an existing integration.

## What it can do

The server currently provides these tools:

 - List files in the workspace
 - Read a text file
 - Search for text across files
 - Create directories
 - Create or update files
 - Delete files

The server is restricted to a dedicated workspace directory so the tools don't access arbitrary files outside the project.

How it works

The basic architecture is:

User -> LangChain Agent -> MCP Client -> MCP File Server
  
  +-- list_files()
  +-- read_file()
  +-- search_files()
  +-- write_file()
  +-- create_directory()
  +-- delete_file()
  
workspace/

### For example, if I ask the agent: Find where I mentioned LangChain in my files.

The agent can decide to use:

search_files("LangChain")

The MCP server searches the workspace and returns the results to the agent.

The important part for me is that the agent doesn't contain the file-search implementation itself. 
MCP provides the standard connection between the agent and the external capability.

## Running the project

### Install the dependencies:

pip install mcp langchain langchain-google-genai langchain-mcp-adapters

Add your gemini api key to your environment or use ollama models.

Then run:

python agent.py

The LangChain application starts the MCP server using stdio and loads the available MCP tools.

