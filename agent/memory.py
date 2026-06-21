from datetime import datetime


MAX_MEMORY_ITEMS = 5

conversation_memory = []


def add_to_memory(user_query, agent_response):
    """
    Stores one conversation turn.

    Only short-term memory is used because incident context should not be
    retained indefinitely.
    """

    conversation_memory.append({
        "timestamp": str(datetime.now()),
        "user_query": user_query,
        "agent_response": agent_response
    })

    if len(conversation_memory) > MAX_MEMORY_ITEMS:
        conversation_memory.pop(0)


def get_recent_memory():
    """
    Returns raw recent memory.
    """

    return conversation_memory


def get_memory_summary():
    """
    Converts memory into clear text for the LLM.

    This is better than passing raw Python objects because the model can
    more reliably understand previous context.
    """

    if not conversation_memory:
        return "No previous conversation memory is available."

    summary_parts = []

    for index, item in enumerate(conversation_memory, start=1):
        summary_parts.append(
            f"Turn {index}:\n"
            f"User asked: {item['user_query']}\n"
            f"Agent response summary: {item['agent_response'][:500]}"
        )

    return "\n\n".join(summary_parts)


def clear_memory():
    """
    Clears all short-term memory.
    """

    conversation_memory.clear()