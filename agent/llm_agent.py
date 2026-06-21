from agent.llm_client import client, MODEL

from agent.prompts import LLM_PROMPT


def llm_agent(query):

    prompt = LLM_PROMPT.format(
        query=query
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content