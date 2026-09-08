import re


LOG_PATTERN = re.compile(
    r"(?P<timestamp>\S+\s+\S+)\s+"
    r"(?P<level>INFO|WARNING|ERROR)\s+"
    r"(?P<message>.*)"
)

API_PATTERN = re.compile(
    r"(?P<method>GET|POST|PUT|PATCH|DELETE)\s+"
    r"(?P<endpoint>/\S+)"
)

STATUS_LATENCY_PATTERN = re.compile(
    r"\s+(?P<status>\d{3})\s+(?P<latency>\d+)ms$"
)

STATUS_PATTERN = re.compile(
    r"\s+(?P<status>\d{3})$"
)


def parse_logs(logs: str) -> list[dict]:
    events = []

    for line in logs.splitlines():
        line = line.strip()

        if not line:
            continue

        log_match = LOG_PATTERN.match(line)

        if not log_match:
            continue

        event = {
            "timestamp": log_match.group("timestamp"),
            "level": log_match.group("level"),
            "message": log_match.group("message"),
        }

        message = event["message"]

        api_match = API_PATTERN.search(message)

        if api_match:
            event["method"] = api_match.group("method")
            event["endpoint"] = api_match.group("endpoint")

            status_latency_match = STATUS_LATENCY_PATTERN.search(message)

            if status_latency_match:
                event["status_code"] = int(
                    status_latency_match.group("status")
                )
                event["latency_ms"] = int(
                    status_latency_match.group("latency")
                )

            else:
                status_match = STATUS_PATTERN.search(message)

                if status_match:
                    event["status_code"] = int(
                        status_match.group("status")
                    )

        events.append(event)

    return events