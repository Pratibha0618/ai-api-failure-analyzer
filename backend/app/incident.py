from datetime import datetime


def group_into_incidents(
    failures: list[dict],
    metrics: dict
) -> list[dict]:
    if not failures:
        return []

    incidents = []
    current_incident = [failures[0]]

    for failure in failures[1:]:
        previous_time = datetime.strptime(
            current_incident[-1]["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )

        current_time = datetime.strptime(
            failure["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )

        time_difference = (
            current_time - previous_time
        ).total_seconds()

        if time_difference <= 10:
            current_incident.append(failure)
        else:
            incidents.append(current_incident)
            current_incident = [failure]

    incidents.append(current_incident)

    result = []

    for index, incident in enumerate(incidents):
        affected_endpoints = set()

        for failure in incident:
            message = failure["message"]

            for endpoint in metrics.get("endpoints", {}):
                if endpoint in message:
                    affected_endpoints.add(endpoint)

        incident_anomalies = []

        for anomaly in metrics.get("latency_anomalies", []):
            anomaly_time = datetime.strptime(
                anomaly["timestamp"],
                "%Y-%m-%d %H:%M:%S"
            )

            incident_start = datetime.strptime(
                incident[0]["timestamp"],
                "%Y-%m-%d %H:%M:%S"
            )

            incident_end = datetime.strptime(
                incident[-1]["timestamp"],
                "%Y-%m-%d %H:%M:%S"
            )

            if incident_start <= anomaly_time <= incident_end:
                incident_anomalies.append(anomaly)

        root_cause_signals = []

        for failure in incident:
            root_cause_signals.append(
                failure["message"]
            )

        if incident_anomalies:
            root_cause_signals.append(
                "Abnormally high API latency"
            )

        result.append({
            "incident_id": index + 1,
            "severity": determine_severity(
                incident,
                incident_anomalies
            ),
            "failure_count": len(incident),
            "affected_endpoints": sorted(
                affected_endpoints
            ),
            "anomalies": incident_anomalies,
            "root_cause_signals": root_cause_signals,
            "failures": incident,
        })

    return result


def determine_severity(
    failures: list[dict],
    anomalies: list[dict]
) -> str:
    if any(
        failure["type"] == "TIMEOUT"
        for failure in failures
    ):
        return "CRITICAL"

    if anomalies:
        return "HIGH"

    if len(failures) >= 3:
        return "HIGH"

    return "MEDIUM"