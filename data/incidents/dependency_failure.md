# Historical Incident: Downstream Dependency Failure

Incident Summary:
Order-service failed to process requests because payment-service was unavailable.

Symptoms:
- Order creation failures
- Downstream service unavailable errors
- Increased payment-service latency
- Failed transactions

Root Cause:
Payment-service outage caused cascading failures in order-service.

Resolution:
Added timeout tuning, fallback handling, and dependency health checks.

Recommended Investigation:
- Check payment-service health
- Review order-service dependency logs
- Inspect latency metrics
- Validate timeout and fallback configuration