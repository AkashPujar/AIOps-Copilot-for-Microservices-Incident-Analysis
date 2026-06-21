from agent.tools import (
    get_cpu_metrics,
    get_latency_metrics,
    get_error_metrics,
    get_service_health
)


SUPPORTED_SERVICES = [
    "order-service",
    "payment-service",
    "notification-service"
]


UNSAFE_ACTIONS = [
    "restart",
    "delete",
    "shutdown",
    "deploy",
    "rollback",
    "scale",
    "modify",
    "update database",
    "drop table"
]


# =========================================================
# TOOL REGISTRY
# =========================================================
#
# This acts like a lightweight tool schema registry.
#
# Why this is important:
# - centralizes tool definitions
# - improves explainability
# - simulates production agent tooling
# - easier to extend later
#
# In future:
# - can be replaced by LangChain/OpenAI function calling
#
# =========================================================

TOOL_REGISTRY = {
    "cpu": {
        "name": "get_cpu_metrics",
        "description": "Fetch CPU usage metrics for a microservice",
        "args": ["service_name"],
        "function": get_cpu_metrics
    },

    "latency": {
        "name": "get_latency_metrics",
        "description": "Fetch p95 latency metrics for a microservice",
        "args": ["service_name"],
        "function": get_latency_metrics
    },

    "errors": {
        "name": "get_error_metrics",
        "description": "Fetch error-rate metrics for a microservice",
        "args": ["service_name"],
        "function": get_error_metrics
    },

    "health": {
        "name": "get_service_health",
        "description": "Fetch operational health status for a microservice",
        "args": ["service_name"],
        "function": get_service_health
    }
}


def is_unsafe_request(query):
    """
    Detects unsafe operational requests.

    Safety is enforced BEFORE:
    - retrieval
    - tool execution
    - LLM reasoning
    """

    query_lower = query.lower()

    return any(action in query_lower for action in UNSAFE_ACTIONS)


def extract_service_name(query):
    """
    Extracts service name from query.

    Example:
    'Why is payment-service failing?'
    -> payment-service
    """

    query_lower = query.lower()

    for service in SUPPORTED_SERVICES:
        if service in query_lower:
            return service

    return None


def select_tool(query):
    """
    Selects tool using deterministic routing.

    Why deterministic?
    - explainable
    - reproducible
    - easy to debug
    - suitable for evaluation

    Future roadmap:
    - LLM function calling
    - autonomous tool selection
    """

    query_lower = query.lower()

    if "cpu" in query_lower:
        return "cpu"

    if "latency" in query_lower or "slow" in query_lower:
        return "latency"

    if "error" in query_lower or "5xx" in query_lower:
        return "errors"

    if "health" in query_lower or "status" in query_lower or "failing" in query_lower:
        return "health"

    return None


def execute_selected_tool(tool_key, service_name=None):
    """
    Executes tool from TOOL_REGISTRY.

    This is the actual tool invocation layer.
    """

    if tool_key not in TOOL_REGISTRY:

        return {
            "error": f"Unknown tool: {tool_key}"
        }

    tool = TOOL_REGISTRY[tool_key]

    tool_function = tool["function"]

    return tool_function(service_name)