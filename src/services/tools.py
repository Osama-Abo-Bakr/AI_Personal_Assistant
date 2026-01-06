import logging
from typing import List
from src.config import (GMAIL_TOKEN_PATH)
from langchain_classic.tools import Tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain_google_community import CalendarToolkit, GmailToolkit


## ---------------- Logging ---------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

GMAIL_TOOLS_CACHE = None

## ---------------- Tool Initialization ---------------------
def duckduckgo_search_tool() -> Tool:
    """
    Return a tool for searching the web with DuckDuckGo.

    Returns:
        Tool: A tool for searching the web with DuckDuckGo
    """
    try:
        logger.info("Initializing DuckDuckGo Search Tool")
        search = DuckDuckGoSearchResults(output_format="list")

        return Tool(
            name="duckduckgo_search",
            description="Search the web for recent information.",
            func=search.invoke,
        )

    except Exception as e:
        logger.error(f"❌ Failed to initialize DuckDuckGo Search Tool: {e}")
        raise

def get_cached_gmail_tools() -> List[Tool]:
    """
    Initialize Gmail tools once and cache them in memory.
    """
    global GMAIL_TOOLS_CACHE

    if GMAIL_TOOLS_CACHE is not None:
        return GMAIL_TOOLS_CACHE

    try:
        logger.info("🔐 Initializing Gmail Tools (one-time)")
        credentials = get_gmail_credentials(
            token_file=GMAIL_TOKEN_PATH,
            scopes=["https://mail.google.com/"],
        )

        api_resource = build_resource_service(credentials=credentials)
        toolkit = GmailToolkit(api_resource=api_resource)

        GMAIL_TOOLS_CACHE = toolkit.get_tools()
        logger.info("✅ Gmail Tools cached successfully")

        return GMAIL_TOOLS_CACHE

    except Exception as e:
        logger.error(f"❌ Gmail Tools unavailable: {e}")
        GMAIL_TOOLS_CACHE = []
        return []

def google_calendar_tools() -> List[Tool]:
    """
    Return a list of tools for interacting with Google Calendar

    Returns:
        List[Tool]: A list of tools for interacting with Google Calendar
    """
    try:
        logger.info("Initializing Google Calendar Tools")
        toolkit = CalendarToolkit()
        return toolkit.get_tools()

    except Exception as e:
        logger.error(f"❌ Failed to initialize Google Calendar Tools: {e}")
        raise
