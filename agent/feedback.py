import json
import os
from datetime import datetime


FEEDBACK_FILE = "logs/feedback.json"


def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []

    with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_feedback(feedback_data):
    os.makedirs("logs", exist_ok=True)

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as file:
        json.dump(feedback_data, file, indent=2)


def store_feedback(query, response, rating, comment):
    feedback_data = load_feedback()

    feedback_data.append({
        "timestamp": str(datetime.now()),
        "query": query,
        "response_summary": response[:300],
        "rating": rating,
        "comment": comment
    })

    save_feedback(feedback_data)


def is_valid_rating(rating):
    return str(rating).strip() in {"1", "2", "3", "4", "5"}


def get_adaptation_guidance():
    feedback_data = load_feedback()

    low_rated = [
        item for item in feedback_data
        if is_valid_rating(item.get("rating"))
        and int(item["rating"]) <= 2
    ]

    if not low_rated:
        return "No negative feedback trends found."

    latest_low_rated = low_rated[-1]
    common_comments = [item["comment"] for item in low_rated]

    return f"""
Previous low-rated feedback:
{common_comments}

Most recent low-rated feedback to fix first:
{latest_low_rated["comment"]}

Adaptation instruction:
- Do not repeat the same generic response style.
- Convert feedback into concrete changes in the next answer.
- Treat the most recent low-rated feedback as a required correction.
- If the feedback asks for clearer investigation steps, provide numbered steps.
- Each investigation step must include:
  1. what to check
  2. where to check it
  3. why it matters
  4. which evidence supports it
- Prefer service-specific checks over generic advice.
- For payment-service latency issues, include exact checks for payment-service health, p95 latency, DB connection pool saturation, order-service retry logs, retry backoff/jitter settings, timeout/fallback configuration, and matching historical incident evidence.
- Do not say "follow the investigation plan above" as the only next step. The next steps must be concrete and actionable.
"""
