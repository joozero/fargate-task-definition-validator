import pytest
from fargate_task_validator.validators.fargate_validator import (
    check_fargate_compatibility,
    UNSUPPORTED_ROOT_PARAMETERS,
    UNSUPPORTED_CONTAINER_PARAMETERS,
)


# Some helper functions to load the JSON samples:
def load_json(file_path):
    with open(file_path, "r") as f:
        return f.read()


# Positive Tests
def test_valid_amazon_linux_2_task():
    task_definition = load_json("examples/amazon_linux_2_task.json")
    feedback = check_fargate_compatibility(task_definition)
    for key, value in feedback.items():
        assert value.startswith("OK") or value.startswith(
            "WARN"
        ), "Unexpected failure for {key} in amazon_linux_2_task"


def test_valid_windows_task():
    task_definition = load_json("examples/windows_task.json")
    feedback = check_fargate_compatibility(task_definition)
    for key, value in feedback.items():
        assert value.startswith("OK") or value.startswith(
            "WARN"
        ), "Unexpected failure for {key} in windows_task"


# Negative Tests
## GPU Tests
def test_invalid_gpu_task():
    task_definition = """
    {
        "containerDefinitions": [{
            "resourceRequirements": [{"type":"GPU", "value": "2"}]
        }]
    }
    """
    feedback = check_fargate_compatibility(task_definition)
    assert feedback["GPU"] == "FAIL", "GPU resource requirement not flagged as invalid."


## Unsupported Root Parameters Test
def test_unsupported_root_parameters():
    for param in UNSUPPORTED_ROOT_PARAMETERS:
        task_definition = f"""{{ "{param}": "invalid_value" }}"""
        feedback = check_fargate_compatibility(task_definition)
        assert (
            feedback[param] == "FAIL"
        ), f"Parameter {param} was not flagged as invalid."


## Unsupported Container Parameters Test
def test_unsupported_container_parameters():
    for param in UNSUPPORTED_CONTAINER_PARAMETERS:
        task_definition = f"""
        {{
            "containerDefinitions": [
                {{
                    "{param}": "invalid_value"
                }}
            ]
        }}
        """
        feedback = check_fargate_compatibility(task_definition)
        assert (
            feedback[param] == "FAIL"
        ), f"Parameter {param} within containerDefinitions was not flagged as invalid."


## Network Mode Test
def test_invalid_network_mode():
    task_definition = """{ "networkMode": "bridge" }"""
    feedback = check_fargate_compatibility(task_definition)
    assert feedback["networkMode"] == "FAIL", "Network mode not flagged as invalid."


## Volumes Test
def test_invalid_docker_volume():
    task_definition = """
    {
        "volumes": [{
            "name": "invalid_volume",
            "dockerVolumeConfiguration": {}
        }]
    }
    """
    feedback = check_fargate_compatibility(task_definition)
    assert (
        feedback["dockerVolumeConfiguration"] == "FAIL"
    ), "Docker volume configuration not flagged as invalid."


## Linux Parameters Test
def test_invalid_linux_parameters():
    invalid_keys = ["devices", "sharedMemorySize", "tmpfs"]
    for key in invalid_keys:
        task_definition = f"""
        {{
            "containerDefinitions": [
                {{
                    "linuxParameters": {{ "{key}": "invalid_value" }}
                }}
            ]
        }}
        """
        feedback = check_fargate_compatibility(task_definition)
        assert (
            feedback["linuxParameters"] == "FAIL"
        ), f"Linux parameter {key} was not flagged as invalid."


## Log Configuration Test
def test_invalid_log_driver():
    task_definition = """
    {
        "containerDefinitions": [{
            "logConfiguration": {
                "logDriver": "invalid_driver"
            }
        }]
    }
    """
    feedback = check_fargate_compatibility(task_definition)
    assert feedback["logConfiguration"] == "FAIL", "Log driver not flagged as invalid."


## Ulimits Test
def test_invalid_ulimits():
    task_definition = """
    {
        "containerDefinitions": [{
            "ulimits": [{"name": "invalid_name"}]
        }]
    }
    """
    feedback = check_fargate_compatibility(task_definition)
    assert feedback["ulimits"] == "FAIL", "Ulimits not flagged as invalid."


## Stop Timeout Test
def test_invalid_stop_timeout():
    task_definition = """
    {
        "containerDefinitions": [{
            "stopTimeout": 200
        }]
    }
    """
    feedback = check_fargate_compatibility(task_definition)
    assert feedback["stopTimeout"] == "FAIL", "Stop timeout not flagged as invalid."
