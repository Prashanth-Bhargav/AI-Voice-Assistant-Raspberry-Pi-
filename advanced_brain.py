import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from load_dotenv import ACCOUNT_ID, API_TOKEN
from load_dotenv import *

# --- Cloudflare Configuration ---
# IMPORTANT: Ensure these are your REAL strings from the dashboard
MODEL_ID = "@cf/qwen/qwen3-30b-a3b-fp8"

# --- Files Folder ---
FILES_DIR = "/home/pi/Desktop/voicebot/jarvis_files"
os.makedirs(FILES_DIR, exist_ok=True)

# 1. Initialize the LLM
# Removed 'default_headers' as ChatOpenAI handles the Bearer token 
# automatically when you provide the 'api_key'.
# advanced_brain.py

llm = ChatOpenAI(
    # Ensure there are NO spaces inside your token string
    api_key=API_TOKEN, 
    # Notice: No '/v1' at the end. LangChain adds it automatically.
    base_url=f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/v1",
    model=MODEL_ID,
    temperature=0,
    # This silences the 'include_usage' error we saw earlier
    model_kwargs={"extra_body": {}} 
)
# 2. Web Search Tool
@tool
def web_search(query: str) -> str:
    """Searches the internet for real-time info like weather, news, or current events."""
    search = DuckDuckGoSearchRun()
    return search.run(query)

# 3. File Analyzer Tool
@tool
def analyze_file(filename: str) -> str:
    """Reads a file from the jarvis_files folder and returns its contents."""
    try:
        file_path = os.path.join(FILES_DIR, filename)
        if not os.path.exists(file_path):
            available = os.listdir(FILES_DIR)
            return f"File '{filename}' not found. Available: {available}"
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content[:3000] + ("\n... (truncated)" if len(content) > 3000 else "")
    except Exception as e:
        return f"Error reading file: {e}"

# 4. List Files Tool
@tool
def list_files() -> str:
    """Lists all files available in the jarvis_files folder."""
    files = os.listdir(FILES_DIR)
    return f"Available files: {', '.join(files)}" if files else "No files found."

tools = [web_search, analyze_file, list_files]

# 5. Create Agent
agent = create_agent(
    llm,
    tools=tools,
    system_prompt=(
        "You are Jarvis, a brilliant and concise AI assistant. "
        "Keep answers to 1-2 sentences. No markdown formatting. "
        "Use web_search for real-time info and analyze_file for files."
    )
)

# 6. Response Function
def get_jarvis_response(user_text: str) -> str:
    current_time = datetime.now().strftime("%I:%M %p on %A, %B %d, %Y")
    try:
        input_data = f"[System Context: It is {current_time}] {user_text}"
        response = agent.invoke({
            "messages": [HumanMessage(content=input_data)]
        })
        messages = response.get("messages", [])
        return messages[-1].content if messages else "No response found."
    except Exception as e:
        print(f"Agent Logic Error: {e}")
        return "I have encountered an authentication or logic error, sir."