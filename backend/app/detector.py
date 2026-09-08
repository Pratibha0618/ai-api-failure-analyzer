def detect_failures(events: list[dict]) -> list[dict]:
    failures = []

    for event in events:
        level = event["level"]
        message = event["message"].lower()

        if level == "ERROR":
            severity = "HIGH"

            if "timeout" in message:
                failure_type = "TIMEOUT"
            elif "database" in message or "db" in message:
                failure_type = "DATABASE_ERROR"
            elif "payment" in message:
                failure_type = "PAYMENT_ERROR"
            else:
                failure_type = "APPLICATION_ERROR"

            failures.append({
                "timestamp": event["timestamp"],
                "severity": severity,
                "type": failure_type,
                "message": event["message"],
            })

    return failures