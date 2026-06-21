from agent.llm_client import client, MODEL
from agent.prompts import RAG_PROMPT
from agent.retrieval import retrieve_context


def rag_agent(query, vectorstore):
    context, sources = retrieve_context(query, vectorstore)

    if not context:
        return """
No relevant operational context found.

I am not certain about the root cause because no matching logs, runbooks, or historical incidents were retrieved.

Escalation:
Please escalate this to a human analyst for further investigation.
"""

    prompt = RAG_PROMPT.format(
        context=context,
        query=query
    )

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

    source_text = "\n\nEvidence Sources:\n" + "\n".join(
        [f"- {source}" for source in sorted(set(sources))]
    )

    return answer + source_text
