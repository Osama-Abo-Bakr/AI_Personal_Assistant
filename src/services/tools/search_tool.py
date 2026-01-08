import logging
from langchain_classic.tools import Tool
from langchain_community.tools import DuckDuckGoSearchResults

## ---------------- Logging ---------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

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