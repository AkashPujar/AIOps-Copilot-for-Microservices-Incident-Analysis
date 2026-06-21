# Database Timeout Incident

Symptoms:
- API latency spike
- Database connection timeout
- Increased retries

Common Causes:
- Connection pool exhaustion
- Slow queries
- DB overload

Investigation Steps:
1. Check DB pool utilization
2. Review slow query logs
3. Verify recent deployments