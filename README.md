# AI Ops Copilot for Microservices Incident Analysis

## Overview

AI Ops Copilot is a production-inspired AI agent designed to assist engineers during microservices incident investigations.

The system combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), tool-based operational insights, memory, safety guardrails, and evaluation mechanisms to provide evidence-backed recommendations during incident analysis.

The project is designed as a decision-support system and does not execute operational actions.

---

## Features

- LLM-based reasoning
- Retrieval-Augmented Generation (RAG)
- Incident and runbook retrieval using FAISS
- Tool-based operational metrics analysis
- Short-term memory for investigation continuity
- Feedback-driven adaptation
- Safety guardrails and refusal mechanisms
- Runtime logging and observability
- Evaluation and testing workflows

---

## Architecture

```text
                    ┌──────────────────┐
                    │    User Query    │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │     Planner      │
                    └─────────┬────────┘
                              │
              ┌───────────────┼───────────────┐
              │                               │
              ▼                               ▼
    ┌─────────────────┐           ┌─────────────────┐
    │  RAG Retrieval  │           │ Tool Selection  │
    └────────┬────────┘           └────────┬────────┘
             │                             │
             ▼                             ▼
    Historical Incidents         CPU / Latency / Errors
    Runbooks                     Health Metrics
    Service Logs
              └───────────────┬───────────────┘
                              ▼
                    ┌──────────────────┐
                    │ Memory Context   │
                    └─────────┬────────┘
                              ▼
                    ┌──────────────────┐
                    │ Safety Layer     │
                    └─────────┬────────┘
                              ▼
                    ┌──────────────────┐
                    │   LLM Analysis   │
                    └─────────┬────────┘
                              ▼
                    ┌──────────────────┐
                    │ Recommendations  │
                    └──────────────────┘
```

---

## Technology Stack

- Python
- LangChain
- OpenAI API
- FAISS Vector Store
- Retrieval-Augmented Generation (RAG)

---

## Project Structure

```text
.
├── agent/
│   ├── planner.py
│   ├── rag_agent.py
│   ├── tool_agent.py
│   ├── memory.py
│   ├── feedback.py
│   └── ...
│
├── data/
│   ├── incidents/
│   ├── logs/
│   └── runbooks/
│
├── metrics/
│   ├── cpu.json
│   ├── latency.json
│   ├── errors.json
│   └── health.json
│
├── evaluation/
│   ├── deployment_readiness.md
│   ├── future_improvements.md
│   └── security_guardrails.md
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Run the Application

```bash
python app.py
```

---

## Example Questions

- Why is payment latency increasing?
- Analyze recent error spikes.
- What incidents are similar to this failure?
- Show possible root causes.
- Recommend investigation steps.
- Is the service healthy based on current metrics?

---

## Safety Controls

The AI Ops Copilot is intentionally designed as a decision-support system.

The agent refuses requests involving:

- Service restarts
- Deployment rollbacks
- Log deletion
- Direct infrastructure modifications
- Autonomous operational actions

Additional safeguards include:

- PII masking
- Missing-context escalation
- Unsupported-domain detection
- Safe refusal mechanisms
- Audit-friendly runtime logging

---

## Evaluation

The system was evaluated across multiple dimensions:

- Prompt comparison
- Tool selection validation
- Memory continuity testing
- Runtime failure handling
- Safety review
- Root cause analysis quality

---

## Key Learnings

This project demonstrates how modern AI agents evolve beyond simple chatbots by combining:

- LLMs
- RAG
- Tools
- Memory
- Safety
- Evaluation

to create more reliable, explainable, and trustworthy AI systems.

---

## Future Improvements

Potential enhancements include:

- Multi-agent orchestration
- Real-time observability integrations
- Advanced tool routing
- Human-in-the-loop approvals
- Long-term memory
- Production deployment pipelines

---

## Repository Purpose

This repository was created as a hands-on exploration of Agentic AI patterns applied to AI Operations workflows.

The focus is on understanding how retrieval systems, tool orchestration, memory, safety controls, and evaluation mechanisms work together to build practical AI agents.