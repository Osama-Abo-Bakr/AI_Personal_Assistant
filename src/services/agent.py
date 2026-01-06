import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.database.db import load_chat_history, save_chat_history
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from src.services.tools import duckduckgo_search_tool, get_cached_gmail_tools


# ---------------- Logging ---------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------- System Prompt ----------------
prompt = """
You are a professional AI personal assistant.

You have access to tools that allow you to:
- Search the web for recent and factual information
- Read, send, and manage Gmail messages
- Create, read, update, and delete Google Calendar events

GENERAL RULES:
1. Be concise, clear, and helpful.
2. Use tools ONLY when they are necessary to answer the user’s question.
3. If a question can be answered from general knowledge, do NOT use tools.
4. When using tools, choose the most relevant one and avoid unnecessary calls.
5. Never mention internal tool names, implementation details, or system messages to the user.
6. Never fabricate emails, events, or search results.
7. If you are unsure or lack permission, explain the limitation clearly.

CHAT HISTORY:
- You are provided with previous conversation history.
- Use it to maintain context and continuity.
- Do not repeat information unnecessarily.

EMAIL (GMAIL) RULES:
- Before sending or modifying emails, be explicit and careful.
- If the user intent is ambiguous, ask a clarification question.
- Summarize emails clearly when asked.
- Never send emails without clear user intent.

CALENDAR RULES:
- When creating or modifying events, confirm date, time, and title.
- If information is missing, ask follow-up questions.
- Avoid assumptions about time zones unless explicitly stated.

SEARCH RULES:
- Use web search only for up-to-date or factual queries.
- Summarize results clearly and cite sources when relevant.
- Prefer recent and reliable information.

RESPONSE FORMAT:
- Respond in plain natural language.
- Do NOT include JSON, markdown code blocks, or tool output unless explicitly requested.
- Be polite, professional, and confident.

ERROR HANDLING:
- If something goes wrong, apologize briefly and explain the issue.
- Suggest a next step or ask for clarification when appropriate.

Your goal is to act as a reliable, safe, and efficient personal assistant.
"""

# ---------------- Agent Execution ----------------
async def response_to_json(user_query: str, user_id: str) -> Dict[str, Any]:
    existing_history = []
    try:
        # tools = [duckduckgo_search_tool, gmail_tools, google_calendar_tools]
        
        tools = []
        tools.append(duckduckgo_search_tool())
        tools.extend(get_cached_gmail_tools())

        ## Loading Chat History
        existing_history = load_chat_history(user_id=user_id)      

        # Convert chat history to format compatible with LangChain
        formatted_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in existing_history
        ]

        # Prompt Template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{question}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        logger.info(f"Initializing LLM for Agent Flow")
        ## Initialize LLM & Agent
        llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.5)

        agent = create_tool_calling_agent(llm, tools, prompt_template)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True
        )

        logger.info(f"Running Agent for User ID: {user_id}")
        response = await agent_executor.ainvoke({
            "question": user_query,
            "chat_history": formatted_history
        })

        raw_output = response.get("output", "")
        if isinstance(raw_output, list):
            raw_output = " ".join(
                [str(item.get("text", "")) if isinstance(item, dict) else str(item) for item in raw_output]
            )
        elif not isinstance(raw_output, str):
            raw_output = str(raw_output)

        # ✅ Append the new interaction
        existing_history.append({"role": "user", "content": user_query})
        existing_history.append({"role": "assistant", "content": raw_output})

        # ✅ Save updated history back to PostgreSQL
        save_chat_history(user_id=user_id, chat_history=existing_history)

        return {
            "user_id": user_id,
            "question": user_query,
            "output": raw_output,
            "chat_history_length": len(existing_history)
        }
    
    except Exception as e:
        logger.error(f"Error in response_to_json: {e}")
        return {
            "user_id": user_id,
            "question": user_query,
            "output": "❌ Sorry, something went wrong. Please try again later.",
            "chat_history_length": len(existing_history),
            "error": str(e)
        }