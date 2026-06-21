from agent.llm_client import client, MODEL
from agent.retrieval import retrieve_context
from agent.tool_router import (
    is_unsafe_request,
    extract_service_name,
    select_tool,
    execute_selected_tool
)
from agent.tool_logger import log_tool_usage


def tool_augmented_agent(query, vectorstore):
    """
    Main Phase 5 agent.

    Flow:
    1. Safety check
    2. Select tool
    3. Execute tool
    4. Retrieve RAG context
    5. Ask LLM to synthesize answer
    """

    if is_unsafe_request(query):
        return """
I cannot execute operational actions such as restarting, deleting, deploying, rolling back, or modifying systems.

This AI Ops Copilot is decision-support only.

Escalation:
Please escalate this request to a human SRE or operations engineer.
"""

    service_name = extract_service_name(query)
    tool_name = select_tool(query)

    tool_result = None

    if tool_name:
        tool_result = execute_selected_tool(tool_name, service_name)
        log_tool_usage(query, tool_name, service_name, tool_result)
    else:
        log_tool_usage(query, "no_tool_selected", service_name, None)

    retrieved_context, sources = retrieve_context(query, vectorstore)

    prompt = f"""
You are an AI Operations Copilot for microservices incident analysis.

Rules:
- You are decision-support only.
- Do not execute operational actions.
- Do not suggest destructive production changes.
- Use retrieved context and tool results only.
- If evidence is insufficient, say you are uncertain.
- Escalate high-risk or ambiguous cases to a human analyst.

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

Observations:
- Summarize relevant evidence from tool results and retrieved context.

Possible Causes:
- List likely causes based on available evidence.

Confidence Level:
- High / Medium / Low
- Explain why.

Recommended Investigation:
- Suggest safe investigation steps only.

Escalation Advice:
- Mention whether human escalation is required.

Tool Usage Explanation:
- Explain which tool was used and why.
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

    answer = response.choices[0].message.content or ""

    if sources:
        source_text = "\n\nEvidence Sources:\n" + "\n".join(
            [f"- {source}" for source in sorted(set(sources))]
        )
    else:
        source_text = "\n\nEvidence Sources:\n- No relevant RAG sources retrieved" 

    return answer + source_text