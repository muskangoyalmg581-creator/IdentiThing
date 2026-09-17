def calculate_risk(
    isolation_prediction,
    anomaly_probability,
    cpu,
    memory,
    file_events,
    network_connections,
    new_processes
):

    score = 0

    reasons = []

    if isolation_prediction == -1:

        score += 30

        reasons.append(
            "Isolation Forest detected unusual behavior"
        )

    if anomaly_probability >= 0.80:

        score += 30

        reasons.append(
            "High anomaly probability"
        )

    if cpu > 50:

        score += 10

        reasons.append(
            "High CPU utilization"
        )

    if memory > 50:

        score += 10

        reasons.append(
            "High memory utilization"
        )

    if file_events > 20:

        score += 10

        reasons.append(
            "High file activity"
        )

    if network_connections > 50:

        score += 5

        reasons.append(
            "High network activity"
        )

    if new_processes > 10:

        score += 5

        reasons.append(
            "Unusual process creation"
        )

    if score > 100:

        score = 100

    if score >= 80:

        severity = "CRITICAL"

    elif score >= 60:

        severity = "HIGH"

    elif score >= 30:

        severity = "MEDIUM"

    else:

        severity = "LOW"

    return score, severity, reasons