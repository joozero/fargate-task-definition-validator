import json

UNSUPPORTED_CONTAINER_PARAMETERS = [
    "disableNetworking",
    "dnsSearchDomains",
    "dnsServers",
    "dockerSecurityOptions",
    "extraHosts",
    "links",
    "privileged",
    "systemControls",
]

UNSUPPORTED_ROOT_PARAMETERS = [
    "ipcMode",
    "pidMode",
    "placementConstraints",
]


def check_fargate_compatibility(task_definition_str):
    """
    Check if a given JSON task definition is compatible with Fargate and return detailed feedback.

    Args:
    - task_definition_str (str): JSON string representation of the task definition.

    Returns:
    - dict: Detailed feedback on compatibility checks.
    """
    task_definition = json.loads(task_definition_str)

    feedback = {}

    # 1. Check for Unsupported Root Parameters and Unsupported Container Parameters
    for param in UNSUPPORTED_ROOT_PARAMETERS:
        if task_definition.get(param) not in (None, "", []):
            feedback[param] = "FAIL"
        else:
            feedback[param] = "OK"

    container_definitions = task_definition.get("containerDefinitions", [])
    for container in container_definitions:
        for param in UNSUPPORTED_CONTAINER_PARAMETERS:
            if container.get(param) not in (None, "", []):
                feedback[param] = "FAIL"
            else:
                feedback[param] = "OK"

    # 2. Network Mode Check
    if task_definition.get("networkMode", "").lower() == "awsvpc":
        feedback["networkMode"] = "OK"
    else:
        feedback["networkMode"] = "FAIL"

    # 3. Linux Parameters
    for container_def in task_definition.get("containerDefinitions", []):
        # linuxParameters constraints
        linux_params = container_def.get("linuxParameters", {})

        # Check if there are any other keys other than 'capabilities' in linuxParameters
        if set(linux_params.keys()) - {"capabilities"}:
            feedback["linuxParameters"] = "FAIL"
        else:
            feedback["linuxParameters"] = "OK"

            # Check the 'add' in capabilities
            capabilities = linux_params.get("capabilities", {})
            allowed_caps = ["SYS_PTRACE"]
            if not all(cap in allowed_caps for cap in capabilities.get("add", [])):
                feedback["linuxParameters_capabilities"] = "FAIL"
            else:
                feedback["linuxParameters_capabilities"] = "OK"

    # 4. Volumes
    if "volumes" in task_definition:
        for volume in task_definition["volumes"]:
            if "dockerVolumeConfiguration" in volume:
                feedback["dockerVolumeConfiguration"] = "FAIL"
                break
        else:
            feedback["dockerVolumeConfiguration"] = "OK"

    # 5. CPU for Windows Containers
    if "runtimePlatform" in task_definition:
        if (
            task_definition["runtimePlatform"]
            .get("operatingSystemFamily", "")
            .startswith("WINDOWS")
            and int(task_definition.get("cpu", "0")) < 1024
        ):
            feedback["cpuWindows"] = "FAIL"
        else:
            feedback["cpuWindows"] = "OK"

    # 6. Check for compatibilities
    # compatibilities = task_definition.get("compatibilities", [])
    # if "FARGATE" not in compatibilities:
    #     feedback["compatibilities"] = "WARN"
    # else:
    #     feedback["compatibilities"] = "OK"

    # 7. Check for requiresAttributes
    requires_compatibilities = task_definition.get("requiresCompatibilities", [])
    if "FARGATE" not in requires_compatibilities:
        feedback["requiresCompatibilities"] = "FAIL"
    else:
        feedback["requiresCompatibilities"] = "OK"

    # 8. Computing Check
    valid_combinations_linux = {
        "256": ["512", "1024", "2048"],
        "512": ["1024", "2048", "3072", "4096"],
        "1024": ["2048", "3072", "4096", "5120", "6144", "7168", "8192"],
        "2048": [str(i) for i in range(4096, 16385, 1024)],
        "4096": [str(i) for i in range(8192, 30721, 1024)],
        "8192": [str(i) for i in range(16384, 61441, 4096)],
        "16384": [str(i) for i in range(32768, 122881, 8192)],
    }

    valid_combinations_windows = {
        "1024": ["2048", "3072", "4096", "5120", "6144", "7168", "8192"],
        "2048": [str(i) for i in range(4096, 16385, 1024)],
        "4096": [str(i) for i in range(8192, 30721, 1024)],
    }

    valid_os_values = [
        "LINUX",
        "WINDOWS_SERVER_2019_FULL",
        "WINDOWS_SERVER_2019_CORE",
        "WINDOWS_SERVER_2022_FULL",
        "WINDOWS_SERVER_2022_CORE",
    ]

    if not all(key in task_definition for key in ["cpu", "memory"]):
        feedback["computing"] = "FAIL"
    else:
        os_family = task_definition.get("runtimePlatform", {}).get(
            "operatingSystemFamily", ""
        )

        if os_family not in valid_os_values:
            feedback["computing"] = "FAIL"
        elif "WINDOWS" in os_family:
            memory_values = valid_combinations_windows.get(task_definition["cpu"], [])
            if task_definition["memory"] not in memory_values:
                feedback["computing"] = "FAIL"
            else:
                feedback["computing"] = "OK"
        else:
            memory_values = valid_combinations_linux.get(task_definition["cpu"], [])
            if task_definition["memory"] not in memory_values:
                feedback["computing"] = "FAIL"
            else:
                feedback["computing"] = "OK"

    # 9. Volumes Check (EBS, ephemeral, or EFS)
    volumes = task_definition.get("volumes", [])
    for volume in volumes:
        if "dockerVolumeConfiguration" in volume:
            feedback["volumes"] = "FAIL"
            break
        elif "efsVolumeConfiguration" in volume:
            feedback["volumes"] = "OK"
            break
    else:
        feedback["volumes"] = "OK"

    # 10. Ephemeral Storage Check
    if "ephemeralStorage" in task_definition:
        size_in_gib = task_definition["ephemeralStorage"].get("sizeInGiB")
        if isinstance(size_in_gib, int) and 21 <= size_in_gib <= 200:
            feedback["ephemeralStorage"] = "OK"
        else:
            feedback["ephemeralStorage"] = "FAIL"
    else:
        feedback["ephemeralStorage"] = "OK"

    # 11. Log Configuration Check
    allowed_log_drivers = ["awslogs", "splunk", "awsfirelens"]
    container_definitions = task_definition.get("containerDefinitions", [{}])
    for container in container_definitions:
        log_config = container.get("logConfiguration", {})
        if log_config.get("logDriver", "").lower() not in allowed_log_drivers:
            feedback["logConfiguration"] = "FAIL"
            break
    else:
        feedback["logConfiguration"] = "OK"

    # 12. Ulimits Check
    for container in container_definitions:
        ulimits = container.get("ulimits", [])
        for ulimit in ulimits:
            if ulimit.get("name") != "nofile":
                feedback["ulimits"] = "FAIL"
                break
        else:
            continue
        break
    else:
        feedback["ulimits"] = "OK"

    # 13. Stop Timeout Check
    for container in container_definitions:
        stop_timeout = container.get("stopTimeout", 0)
        if stop_timeout > 120:
            feedback["stopTimeout"] = "FAIL"
            break
    else:
        feedback["stopTimeout"] = "OK"

    # Add other checks as needed

    # GPU constraints
    for container_def in task_definition.get("containerDefinitions", []):
        resource_requirements = container_def.get("resourceRequirements", [])
        for requirement in resource_requirements:
            if requirement.get("type") == "GPU":
                feedback["GPU"] = "FAIL"
                break
        else:
            feedback["GPU"] = "OK"

    return feedback
