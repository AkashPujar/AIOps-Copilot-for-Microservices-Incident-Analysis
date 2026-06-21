import os
import json
from datetime import datetime


RUNTIME_LOG_FILE = "logs/runtime_logs.jsonl"


def log_runtime_event(event_type, query=None, latency_ms=None, status="success", error=None):
    os.makedirs("logs", exist_ok=True)

    event = {
        "timestamp": str(datetime.now()),
        "event_type": event_type,
        "query_preview": query[:100] if query else None,
        "latency_ms": latency_ms,
        "status": status,
        "error": str(error) if error else None
    }

    with open(RUNTIME_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")