import logging
from typing import List
from src.config import (GMAIL_TOKEN_PATH)
from langchain_classic.tools import Tool
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)


## ---------------- Logging ---------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

GMAIL_TOOLS_CACHE = None

## ---------------- Tool Initialization ---------------------
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