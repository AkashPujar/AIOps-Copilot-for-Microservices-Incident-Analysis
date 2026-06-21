from agent.llm_client import client, MODEL
from agent.feedback import get_adaptation_guidance
from agent.retrieval import retrieve_context

from agent.tool_router import (
    is_unsafe_request,
    extract_service_name,
    select_tool,
    execute_selected_tool
)

from agent.tool_logger import log_tool_usage

from agent.memory import (
    add_to_memory,
    get_recent_memory,
    get_memory_summary,
    clear_memory
)

from agent.planner import generate_plan


GENERIC_FOLLOW_UP_QUERIES = [
    "what should i investigate next",
    "what next",
    "next steps",
    "what should i check next"
]


UNSUPPORTED_METRIC_QUERIES = [
    "memory saturation",
    "heap",
    "jvm",
    "garbage collection",
    "gc"
]


def is_generic_follow_up(query):
    return query.lower().strip().rstrip("?") in GENERIC_FOLLOW_UP_QUERIES


def memory_tool_agent(query, vectorstore):
    """
    Phase 6+ Agent:
    Combines safety, planning, memory, tool usage, RAG, feedback adaptation,
    and LLM reasoning.
    """

    if query.lower().strip() == "reset":
        clear_memory()
        return "Conversation memory has been cleared."

    if any(term in query.lower() for term in UNSUPPORTED_METRIC_QUERIES):
        if "notification-service" not in query.lower():
            response = """
I do not have service-specific memory metrics or JVM heap logs for this query.

I am not certain about the root cause because the current toolset does not include memory metrics for the requested service.

Available supported checks:
- CPU metrics
- latency metrics
- error-rate metrics
- service health
- RAG over known incidents and runbooks

Escalation Advice:
Please provide memory metrics, JVM heap logs, or service-specific memory runbooks before further diagnosis.

Memory Usage:
Previous memory was not used as verified evidence.

Evidence Sources:
- No relevant service-specific memory evidence available
"""
            add_to_memory(query, response)
            return response

    recent_memory = get_recent_memory()
    memory_available = len(recent_memory) > 0
    recent_memory_text = get_memory_summary()

    if not memory_available and is_generic_follow_up(query):
        response = """
I do not have an active incident context.

Please specify the service or symptom you want to investigate, such as:
- payment-service latency
- order-service failures
- notification-service restarts
- 5xx errors

Memory Usage:
No previous conversation memory was used.
"""
        add_to_memory(query, response)
        return response

    investigation_plan = generate_plan(query)

    if is_unsafe_request(query):
        response = """
I cannot execute operational actions such as restarting, deleting, deploying, rolling back, or modifying systems.

This AI Ops Copilot is decision-support only.

Escalation:
Please escalate this request to a human SRE or operations engineer.
"""
        add_to_memory(query, response)
        return response

    service_name = extract_service_name(query)
    tool_name = select_tool(query)

    tool_result = None

    if tool_name:
        tool_result = execute_selected_tool(tool_name, service_name)
        log_tool_usage(query, tool_name, service_name, tool_result)
    else:
        log_tool_usage(query, "no_tool_selected", service_name, None)

    retrieved_context, sources = retrieve_context(query, vectorstore)

    if not retrieved_context:
        response = f"""
I could not find relevant operational context for this query.

I am not certain about the root cause because no matching logs, runbooks, metrics, or historical incidents were found in the current knowledge base.

User Query:
{query}

Tool Used:
{tool_name if tool_name else "No matching tool selected"}

Tool Result:
{tool_result if tool_result else "No relevant tool result available"}

Escalation Advice:
Please escalate this to a human analyst or provide relevant logs, metrics, or runbooks before further diagnosis.

Memory Usage:
{"Previous conversation memory was available and used only for conversation continuity, not as verified evidence." if memory_available else "No previous conversation memory was used."}

Evidence Sources:
- No relevant RAG sources retrieved
"""
        add_to_memory(query, response)
        return response

    adaptation_guidance = get_adaptation_guidance()

    memory_usage_instruction = (
        "Previous conversation memory is available. Use it to maintain investigation continuity, but verify conclusions using tools or retrieved context."
        if memory_available
        else "No previous conversation memory is available. State that no previous memory was used."
    )

    prompt = f"""
You are an AI Operations Copilot for microservices incident analysis.

Rules:
- You are decision-support only.
- Do not execute operational actions.
- Use memory only for conversation continuity.
- Do not assume memory facts are current unless supported by tools or retrieved context.
- If Recent Conversation Memory is empty, say that no previous memory was used.
- Do not describe retrieved context as memory.
- If evidence is insufficient, say you are uncertain.
- Escalate high-risk or ambiguous cases.

Adaptation Guidance:
{adaptation_guidance}

Memory Usage Instruction:
{memory_usage_instruction}

Recent Conversation Memory:
{recent_memory_text}

Investigation Plan:
{investigation_plan}

User Query:
{query}

Detected Service:
{service_name}

Selected Tool:
{tool_name}

Tool Result:
{tool_result}

Retrieved Context:
{retrieved_context}

Evidence Sources:
{sources}

Respond in this format:

Investigation Plan:
- Show the steps followed.

Observations:
- Summarize memory, tool results, and retrieved evidence.

Possible Causes:
- List likely causes based on evidence.

Confidence Level:
- High / Medium / Low
- Explain why.

Recommended Next Steps:
- Safe investigation steps only.
- Provide numbered, concrete, service-specific checks.
- Do not write only "follow the investigation plan above."
- For each step, mention the exact signal/config/log to inspect and why it matters.

Escalation Advice:
- Mention whether human escalation is required.

Memory Usage:
- Follow the Memory Usage Instruction exactly.
- If previous memory exists, mention which earlier investigation topic was continued.
- If no previous memory exists, say no previous memory was used.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    final_response = response.choices[0].message.content or ""

    if sources:
        final_response += "\n\nEvidence Sources:\n" + "\n".join(
            [f"- {source}" for source in sorted(set(sources))]
        )
    else:
        final_response += "\n\nEvidence Sources:\n- No relevant RAG sources retrieved"

    add_to_memory(query, final_response)

    return final_response
