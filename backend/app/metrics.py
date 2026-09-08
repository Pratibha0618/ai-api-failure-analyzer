from collections import Counter


def calculate_metrics(events: list[dict]) -> dict:
    total_requests = 0
    failed_requests = 0

    status_codes = Counter()
    endpoints = Counter()

    endpoint_stats = {}

    latencies = []

    for event in events:
        if "status_code" not in event:
            continue

        total_requests += 1

        status_code = event["status_code"]
        endpoint = event.get("endpoint", "unknown")

        status_codes[str(status_code)] += 1
        endpoints[endpoint] += 1

        # Initialize endpoint statistics
        if endpoint not in endpoint_stats:
            endpoint_stats[endpoint] = {
                "total_requests": 0,
                "failed_requests": 0,
                "latencies": [],
            }

        endpoint_stats[endpoint]["total_requests"] += 1

        if status_code >= 500:
            failed_requests += 1
            endpoint_stats[endpoint]["failed_requests"] += 1

        if "latency_ms" in event:
            latency = event["latency_ms"]

            latencies.append(latency)
            endpoint_stats[endpoint]["latencies"].append(latency)

    # Overall error rate
    error_rate = 0

    if total_requests > 0:
        error_rate = round(
            (failed_requests / total_requests) * 100,
            2
        )

    # Overall latency
    average_latency = 0
    latency_median = 0
    mad = 0

    if latencies:
        average_latency = round(
            sum(latencies) / len(latencies),
            2
        )

        sorted_latencies = sorted(latencies)
        middle = len(sorted_latencies) // 2

        if len(sorted_latencies) % 2 == 0:
            latency_median = (
                sorted_latencies[middle - 1]
                + sorted_latencies[middle]
            ) / 2
        else:
            latency_median = sorted_latencies[middle]

        deviations = [
            abs(latency - latency_median)
            for latency in latencies
        ]

        sorted_deviations = sorted(deviations)
        middle = len(sorted_deviations) // 2

        if len(sorted_deviations) % 2 == 0:
            mad = (
                sorted_deviations[middle - 1]
                + sorted_deviations[middle]
            ) / 2
        else:
            mad = sorted_deviations[middle]

    # Detect latency anomalies
    anomalies = []

    if mad > 0:
        for event in events:
            if "latency_ms" not in event:
                continue

            latency = event["latency_ms"]

            modified_z_score = (
                0.6745 * (latency - latency_median)
            ) / mad

            if modified_z_score >= 3.5:
                anomalies.append({
                    "timestamp": event["timestamp"],
                    "endpoint": event.get("endpoint"),
                    "latency_ms": latency,
                    "modified_z_score": round(
                        modified_z_score,
                        2
                    ),
                    "reason": "Unusually high latency",
                })

    # Calculate endpoint-level statistics
    for endpoint, stats in endpoint_stats.items():
        request_count = stats["total_requests"]
        failure_count = stats["failed_requests"]
        endpoint_latencies = stats["latencies"]

        endpoint_error_rate = 0
        endpoint_average_latency = 0

        if request_count > 0:
            endpoint_error_rate = round(
                (failure_count / request_count) * 100,
                2
            )

        if endpoint_latencies:
            endpoint_average_latency = round(
                sum(endpoint_latencies)
                / len(endpoint_latencies),
                2
            )

        stats["error_rate_percent"] = endpoint_error_rate
        stats["average_latency_ms"] = endpoint_average_latency

        # Don't expose raw latency list in API response
        del stats["latencies"]

    return {
        "total_requests": total_requests,
        "failed_requests": failed_requests,
        "error_rate_percent": error_rate,
        "average_latency_ms": average_latency,
        "latency_median_ms": latency_median,
        "latency_mad_ms": round(mad, 2),
        "status_codes": dict(status_codes),
        "endpoints": dict(endpoints),
        "endpoint_stats": endpoint_stats,
        "latency_anomalies": anomalies,
    }