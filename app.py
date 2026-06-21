import os
import time

from agent.retrieval import (
    build_vectorstore,
    load_vectorstore
)

from agent.memory_tool_agent import memory_tool_agent
from agent.feedback import store_feedback
from agent.runtime_logger import log_runtime_event


CONTROL_COMMANDS_WITHOUT_FEEDBACK = {
    "reset"
}


def load_or_build_vectorstore():
    try:
        if not os.path.exists("vectorstore/index.faiss"):
            print("Building vectorstore...")
            return build_vectorstore()

        print("Loading vectorstore...")
        return load_vectorstore()

    except Exception as error:
        log_runtime_event(
            event_type="vectorstore_load_failure",
            status="failure",
            error=error
        )
        raise RuntimeError("Failed to load or build vectorstore.") from error


def run_cli():
    vectorstore = load_or_build_vectorstore()

    print("\nAI Ops Copilot started.")
    print("Type 'exit' to quit.")
    print("Type 'reset' to clear memory.\n")

    while True:
        query = input("\nUser: ")

        if query.lower() == "exit":
            print("Exiting AI Ops Copilot.")
            break

        start_time = time.time()

        try:
            response = memory_tool_agent(query, vectorstore)

            latency_ms = round((time.time() - start_time) * 1000, 2)

            log_runtime_event(
                event_type="agent_response",
                query=query,
                latency_ms=latency_ms,
                status="success"
            )

            print("\nAgent Response:\n")
            print(response)

            if query.lower().strip() in CONTROL_COMMANDS_WITHOUT_FEEDBACK:
                continue

            rating = input("\nRate this response from 1 to 5, or press Enter to skip: ")

            if rating.strip():
                comment = input("Feedback comment: ")
                store_feedback(query, response, rating, comment)
                print("Feedback saved.")

        except Exception as error:
            latency_ms = round((time.time() - start_time) * 1000, 2)

            log_runtime_event(
                event_type="agent_response",
                query=query,
                latency_ms=latency_ms,
                status="failure",
                error=error
            )

            print("\nAgent Response:\n")
            print(
                "The agent encountered a runtime issue and could not complete the request. "
                "Please retry or escalate to a human analyst."
            )


if __name__ == "__main__":
    run_cli()
