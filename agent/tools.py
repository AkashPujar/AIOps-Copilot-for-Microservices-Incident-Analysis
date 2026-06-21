import json
from pathlib import Path


METRICS_PATH = Path("metrics")


def read_json_file(file_name):
    """
    Reads a JSON metrics file from the metrics folder.

    Why this exists:
    - Avoids repeating file-reading logic in every tool.
    - Keeps tools clean and reusable.
    """

    file_path = METRICS_PATH / file_name

    if not file_path.exists():
        return {
            "error": f"Metrics file not found: {file_name}"
        }

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_cpu_metrics(service_name=None):
    """
    Simulates a CPU monitoring tool.

    In real life:
    - This could call Prometheus, Grafana, Datadog, or CloudWatch.

    In this capstone:
    - It reads cpu.json.
    """

    data = read_json_file("cpu.json")

    if service_name:
        return data.get(
            service_name,
            {"error": f"No CPU metrics found for service: {service_name}"}
        )

    return data


def get_latency_metrics(service_name=None):
    """
    Simulates a latency monitoring tool.

    It returns p95 latency values for services.
    """

    data = read_json_file("latency.json")

    if service_name:
        return data.get(
            service_name,
            {"error": f"No latency metrics found for service: {service_name}"}
        )

    return data


def get_error_metrics(service_name=None):
    """
    Simulates an error-rate monitoring tool.

    It returns error rate percentage per service.
    """

    data = read_json_file("errors.json")

    if service_name:
        return data.get(
            service_name,
            {"error": f"No error metrics found for service: {service_name}"}
        )

    return data


def get_service_health(service_name=None):
    """
    Simulates a service health API.

    It returns health status and reason for each service.
    """

    data = read_json_file("health.json")

    if service_name:
        return data.get(
            service_name,
            {"error": f"No health data found for service: {service_name}"}
        )

    return data