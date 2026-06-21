# AI Ops Copilot for Microservices Incident Analysis

## Overview

This project implements an AI Operations Copilot for microservices incident analysis.

The agent supports:
- LLM-based reasoning
- RAG over logs, runbooks, and incidents
- tool usage over simulated metrics
- short-term memory
- feedback-based adaptation
- safety guardrails
- local deployment logging

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt