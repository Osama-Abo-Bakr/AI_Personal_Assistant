import os
from dotenv import load_dotenv

# Load environment variables from .env file
_ = load_dotenv(override=True)

## OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

## PostgreSQL Database URL
POSTGRES_URL = os.getenv("POSTGRES_URL", "")

## GCP Credientials Path
GCP_CREDENTIALS_PATH = os.getenv("GCP_CREDENTIALS_PATH", "./credentials.json")

## Tokens Paths
GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", ".gmail_token.json")
CALENDAR_TOKEN_PATH = os.getenv("CALENDAR_TOKEN_PATH", "./calendar_token.json")

API_TOKEN= os.getenv("API_TOKEN", "123456")