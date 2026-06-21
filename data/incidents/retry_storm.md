# Historical Incident: Retry Storm

Incident Summary:
Order-service experienced increased latency due to aggressive retries against payment-service.

Symptoms:
- Increased API latency
- High retry count
- Downstream payment-service pressure
- Increased 5xx errors

Root Cause:
Retry logic did not use exponential backoff, causing repeated requests during downstream failure.

Resolution:
Implemented exponential backoff, circuit breaker logic, and retry limits.

Recommended Investigation:
- Check retry count
- Inspect downstream dependency health
- Review circuit breaker state
- Validate retry configuration