from fargate_task_validator.validators.fargate_validator import (
    UNSUPPORTED_CONTAINER_PARAMETERS,
    UNSUPPORTED_ROOT_PARAMETERS,
)

RECOMMENDATIONS = {
    "networkMode": "Fargate requires the 'awsvpc' network mode.",
    "ebsVolumes": "EBS volumes are not supported in Fargate.",
    "dockerVolumeConfiguration": "Docker volume configurations are not supported in Fargate.",
    "ephemeralStorage": "Ensure the ephemeral storage configurations in your task definition are valid for Fargate.",
    "linuxParameters": "Certain Linux parameters are not supported or have limitations in Fargate.",
    "volumes": "Fargate tasks support specific volume types. Some configurations might not be valid.",
    "cpu": "There are limitations on CPU values, especially for Windows containers on Fargate.",
    "operatingSystem": "Ensure you're using a Fargate-supported operating system.",
    "cpuArchitecture": "Fargate supports specific CPU architectures based on the OS and container type.",
    "taskCPUandMemory": "Ensure the combination of CPU and memory values is valid for Fargate.",
    "ulimits": "There are restrictions on setting ulimits in Fargate tasks.",
    "logConfiguration": "Fargate tasks support specific log drivers.",
    "taskExecutionIAMRole": "Ensure the task execution IAM role has the necessary permissions.",
    "taskStorage": "Ensure the storage configurations are compatible with Fargate.",
    "compatibilities": "Your task definition should be compatible with Fargate.",
    "requiresCompatibilities": "Your task definition should require Fargate compatibility.",
    "stopTimeout": "Ensure the stop timeout value in your task definition does not exceed the Fargate limit.",
    "GPU": "GPU configurations are not supported in Fargate.",
    "computing": "Ensure the computing configurations in your task definition are compatible with Fargate.",
}

REMEDIATIONS = {
    "networkMode": "Change the 'networkMode' in your task definition to 'awsvpc'.",
    "ebsVolumes": "Remove EBS volumes from your task definition or consider another ECS launch type.",
    "dockerVolumeConfiguration": "Remove Docker volume configurations from your task definition or consider another ECS launch type.",
    "ephemeralStorage": "Ensure the ephemeral storage configurations in your task definition are valid.",
    "linuxParameters": "Adjust the Linux parameters in your task definition according to Fargate's specifications.",
    "volumes": "Modify the volume configurations in your task definition to be compatible with Fargate.",
    "cpu": "Adjust the CPU value in your task definition to meet Fargate's requirements.",
    "operatingSystem": "Change the operating system in your task definition to one supported by Fargate.",
    "cpuArchitecture": "Ensure your task definition uses a Fargate-compatible CPU architecture.",
    "taskCPUandMemory": "Modify the CPU and memory values in your task definition to a valid combination for Fargate.",
    "ulimits": "Update or remove the ulimits configurations in your task definition for Fargate compatibility.",
    "logConfiguration": "Adjust the log configuration in your task definition to use a supported log driver.",
    "taskExecutionIAMRole": "Ensure the task execution IAM role is correctly set and has the required permissions.",
    "taskStorage": "Modify the storage settings in your task definition to be Fargate-compatible.",
    "compatibilities": "Ensure your task definition is compatible with Fargate.",
    "requiresCompatibilities": "Ensure your task definition requires Fargate compatibility.",
    "stopTimeout": "Adjust the 'stopTimeout' in your task definition to be within Fargate's limits.",
    "GPU": "Remove GPU configurations from your task definition.",
    "computing": "Ensure the computing settings in your task definition are Fargate-compatible.",
}

for param in UNSUPPORTED_CONTAINER_PARAMETERS + UNSUPPORTED_ROOT_PARAMETERS:
    RECOMMENDATIONS[param] = f"The '{param}' parameter is not supported in Fargate."
    REMEDIATIONS[
        param
    ] = f"Remove the '{param}' parameter from your task definition or ensure its value is empty or null."
