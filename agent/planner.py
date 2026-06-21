def generate_plan(query):
    """
    Generates an investigation plan based on user query.

    This is deterministic planning for Phase 6.
    It makes the agent explain how it will investigate.
    """

    query_lower = query.lower()

    if "latency" in query_lower or "slow" in query_lower:
        return [
            "Check latency metrics",
            "Review service health",
            "Retrieve related logs and incidents",
            "Identify likely bottleneck",
            "Recommend safe investigation steps"
        ]

    if "error" in query_lower or "5xx" in query_lower or "failure" in query_lower:
        return [
            "Check error-rate metrics",
            "Review service health",
            "Retrieve failure logs",
            "Compare with historical incidents",
            "Recommend escalation if severity is high"
        ]

    if "cpu" in query_lower:
        return [
            "Check CPU metrics",
            "Review service health",
            "Look for related incident patterns",
            "Recommend safe investigation steps"
        ]

    if "restart" in query_lower or "delete" in query_lower or "deploy" in query_lower:
        return [
            "Identify unsafe operational action",
            "Refuse execution",
            "Recommend human escalation"
        ]

    return [
        "Understand the operational symptom",
        "Retrieve relevant context",
        "Check available metrics if applicable",
        "Provide uncertainty-aware recommendation"
    ]