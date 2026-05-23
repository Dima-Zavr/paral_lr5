def calculate_metrics(response_data):

    results = response_data["results"]

    successful = sum(
        1 for r in results
        if r.get("status") == 200
    )

    failed = len(results) - successful

    timeouts = sum(
        1 for r in results
        if r.get("timeout")
    )

    return {
        "total_requests": len(results),
        "successful": successful,
        "failed": failed,
        "timeouts": timeouts,
        "total_time_ms": response_data["summary"]["total_time_ms"]
    }