try:
    from .operations import insert_alert, check_if_alert_exist, resolve_alert
except ImportError:
    from operations import insert_alert, check_if_alert_exist, resolve_alert


def resource_analyzer(system_id, resource_usage):

    risk_label = "LOW"

    # ---------------- CPU ----------------
    if resource_usage.cpu_usage >= 90:

        risk_label = "HIGH"

        if not check_if_alert_exist(system_id, "HIGH_CPU"):
            insert_alert(
                system_id,
                "high",
                "HIGH_CPU",
                "ACTIVE",
                "High CPU usage detected"
            )
    else:
        resolve_alert(system_id, "HIGH_CPU")

    # ---------------- MEMORY ----------------
    if resource_usage.memory_usage >= 95:

        risk_label = "HIGH"

        if not check_if_alert_exist(system_id, "HIGH_MEMORY"):
            insert_alert(
                system_id,
                "high",
                "HIGH_MEMORY",
                "ACTIVE",
                "High Memory usage detected"
            )
    else:
        resolve_alert(system_id, "HIGH_MEMORY")

    # ---------------- DISK ----------------
    if resource_usage.disk_usage >= 80:

        risk_label = "HIGH"

        if not check_if_alert_exist(system_id, "HIGH_DISK"):
            insert_alert(
                system_id,
                "high",
                "HIGH_DISK",
                "ACTIVE",
                "High Disk usage detected"
            )
    else:
        resolve_alert(system_id, "HIGH_DISK")

    return risk_label