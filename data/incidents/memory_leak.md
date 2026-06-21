# Historical Incident: Memory Leak in Notification Service

Incident Summary:
Notification-service experienced repeated pod restarts and degraded performance.

Symptoms:
- Increasing memory usage over time
- Frequent pod restarts
- Slow notification delivery
- JVM heap pressure warnings

Root Cause:
A memory leak caused by unreleased object references in the message batching logic.

Resolution:
The batching logic was refactored, heap monitoring was improved, and alert thresholds were updated.

Recommended Investigation:
- Check memory utilization trends
- Review pod restart count
- Inspect JVM heap logs
- Compare with recent deployments