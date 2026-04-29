import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Extract variables from environment
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
API_TOKEN = os.getenv("API_TOKEN")

# Function to verify they exist (optional but helpful)
def verify_env():
    if not ACCOUNT_ID or not API_TOKEN:
        print("⚠️ Warning: ACCOUNT_ID or API_TOKEN missing in .env file!")
    return ACCOUNT_ID, API_TOKEN