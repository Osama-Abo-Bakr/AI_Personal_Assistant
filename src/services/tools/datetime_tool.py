import pytz
from typing import Optional
from datetime import datetime
from langchain_community.tools import Tool

def get_current_datetime(timezone: Optional[str] = None) -> str:
    """
    Returns the current date and time as a string, in the format:
        "Current [local/date and time in <timezone>] : <YYYY-MM-DD HH:MM:SS [TZ]>"

    Args:
        timezone (str, optional): timezone string (e.g. 'UTC', 'America/New_York').
            If None, returns the local time.

    Returns:
        str: the current date and time as a string
    """
    now = datetime.now()
    if timezone:
        try:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            return f"Current date and time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        except Exception as e:
            return f"Error with timezone: {str(e)}. Showing local time instead: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    return f"Current local date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

def datetime_tool() -> Tool:
    """
    Returns a Tool that gets the current date and time as a string, in the format:
        "Current [local/date and time in <timezone>] : <YYYY-MM-DD HH:MM:SS [TZ]>"
    """
    return Tool(
        name="current_datetime",
        description=(
            "Useful for getting the current date and time. "
            "Input can be empty or a timezone string (e.g., 'UTC', 'America/New_York'). "
            "Always use this when asked about time or date."
        ),
        func=get_current_datetime
    )