import os
from datetime import datetime


TOOL_LOG_FILE = "logs/tool_usage.log"


def log_tool_usage(query, tool_name, service_name, tool_result):
    """
    Logs tool usage for evaluation and debugging.

    Important:
    We avoid logging sensitive user/business data.
    """

    os.makedirs("logs", exist_ok=True)

    with open(TOOL_LOG_FILE, "a", encoding="utf-8") as file:
        file.write("\n==============================\n")
        file.write(f"Timestamp: {datetime.now()}\n")
        file.write(f"Query: {query}\n")
        file.write(f"Selected Tool: {tool_name}\n")
        file.write(f"Service: {service_name}\n")
        file.write(f"Tool Result: {tool_result}\n")