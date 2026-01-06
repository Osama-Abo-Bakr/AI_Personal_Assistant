import logging
import psycopg2
from typing import List, Dict
from src.config import POSTGRES_URL
from psycopg2.extras import RealDictCursor, Json


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

## =======================================================================================
## Chat History Connection
## =======================================================================================
def get_connection():
    """
    Returns a psycopg2 connection object to the database specified in the POSTGRES_URL environment variable.

    The connection is configured to use the RealDictCursor cursor factory, which returns
    dictionaries for each row instead of tuples.

    :return: psycopg2 connection object
    """
    return psycopg2.connect(POSTGRES_URL, cursor_factory=RealDictCursor)

## =======================================================================================
## Chat History Initialization & Deletion & Auto Deletion
## =======================================================================================
def InitializeChatHistoryTable():
    """
    Initializes the chat history table in the database.

    This function creates a table named chat_history with the following columns:

    id: A unique identifier for each chat history.
    user_id: The user ID associated with the chat history.
    chat_history: A list of dictionaries containing the chat history.
    created_at: The timestamp when the chat history was created.

    If the table already exists, this function does nothing.

    :raises: Exception if the table initialization fails
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL UNIQUE,
                chat_history JSONB NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.info("💾 Chat history table initialized")
    except Exception as e:
        logger.error(f"Failed to initialize chat history table: {e}")
        
def _delete_database():
    """
    Deletes the chat history table from the database.

    This function drops the chat history table if it exists.

    :raises: Exception if the deletion fails
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS chat_history")
        conn.commit()
        cur.close()
        conn.close()
        logger.info("💾 Chat history table deleted")
    except Exception as e:
        logger.error(f"Failed to delete chat history table: {e}")


## =======================================================================================
## Chat History Functions -> Get & Update
## =======================================================================================
def load_chat_history(user_id: str) -> List[Dict[str, str]]:
    """
    Loads the chat history for the given user_id from the database.

    :param user_id: The user ID to associate with the chat history
    :return: A list of dictionaries containing the chat history
    :rtype: List[Dict[str, str]]
    :raises: Exception if the loading fails
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT chat_history FROM chat_history WHERE user_id=%s LIMIT 1",
                (user_id,),
            )
            row = cur.fetchone()
            return row["chat_history"] if row else []
    except Exception as e:
        logger.error(f"Failed to load chat history: {e}")
        return []
    finally:
        if conn:
            conn.close()


def save_chat_history(user_id: str, chat_history: List[Dict[str, str]]):
    """
    Saves the chat history for the given user_id to the database.

    The chat history is a list of dictionaries containing the chat history.
    Each dictionary should contain the keys "from", "to", "message", and "timestamp", with
    values being strings.

    If the user_id already exists in the database, the chat history is updated.
    Otherwise, a new row is inserted.

    :param user_id: The user ID to associate with the chat history
    :param chat_history: The chat history to be saved
    :type chat_history: List[Dict[str, str]]
    :raises: Exception if the insertion fails
    :return: A dictionary containing a success message
    :rtype: Dict[str, str]
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chat_history (user_id, chat_history)
                VALUES (%s, %s)
                ON CONFLICT (user_id)
                DO UPDATE SET chat_history = EXCLUDED.chat_history;
                """,
                (user_id, Json(chat_history)),  # ✅ FIX
            )

            conn.commit()
        logger.info(f"💾 Chat history saved for user={user_id}")
    except Exception as e:
        logger.error(f"Failed to save chat history: {e}")
    finally:
        if conn:
            conn.close()

            
def delete_chat_history(user_id: str):
    """
    Deletes the chat history for the given user_id from the database.

    :param user_id: The user ID to associate with the chat history
    :return: A dictionary containing a success message
    :rtype: Dict[str, str]
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM chat_history WHERE user_id=%s",
            (user_id,),
        )
    conn.commit()
    conn.close()

    logger.info(f"🗑️ Chat history cleared for user={user_id}")
    return {"message": f"Chat history cleared for user={user_id}"}
