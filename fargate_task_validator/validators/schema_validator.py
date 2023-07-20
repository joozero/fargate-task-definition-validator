from jsonschema import Draft7Validator

container_definition_schema = {
    "id": "/containerDefinition",
    "type": "object",
    "required": ["name", "image"],
    "properties": {
        "name": {"type": "string"},
        "image": {"type": "string"},
        "memory": {"type": "integer"},
        "memoryReservation": {"type": "integer"},
        "portMappings": {"type": "array", "items": {"$ref": "/containerPortMapping"}},
        "healthCheck": {"$ref": "/containerHealthCheck"},
        "cpu": {"type": "integer"},
        "essential": {"type": "boolean"},
        "entryPoint": {"type": "array", "items": {"type": "string"}},
        "command": {"type": "array", "items": {"type": "string"}},
        "workingDirectory": {"type": "string"},
        "environment": {"type": "array", "items": {"$ref": "/containerEnvironment"}},
        "secrets": {"type": "array", "items": {"$ref": "/containerSecrets"}},
        "disableNetworking": {"type": "boolean"},
        "links": {"type": "array", "items": {"type": "string"}},
        "hostname": {"type": "string"},
        "dnsServers": {"type": "array", "items": {"type": "string"}},
        "dnsSearchDomains": {"type": "array", "items": {"type": "string"}},
        "extraHosts": {"type": "array", "items": {"$ref": "/containerExtraHost"}},
        "readonlyRootFilesystem": {"type": "boolean"},
        "mountPoints": {"type": "array", "items": {"$ref": "/containerMountPoint"}},
        "volumesFrom": {"type": "array", "items": {"$ref": "/containerVolumesFrom"}},
        "logConfiguration": {"$ref": "/containerLogConfiguration"},
        "privileged": {"type": "boolean"},
        "user": {"type": "string"},
        "dockerSecurityOptions": {"type": "array", "items": {"type": "string"}},
        "ulimits": {"type": "array", "items": {"$ref": "/containerUlimits"}},
        "dockerLabels": {"type": "object"},
        "linuxParameters": {"$ref": "/containerLinuxParameters"},
    },
}

# Define the containerLinuxParametersTmpfsSchema
container_linux_parameters_tmpfs_schema = {
    "type": "object",
    "required": ["containerPath"],
    "properties": {
        "containerPath": {"type": "string"},
        "mountOptions": {"type": "array", "items": {"type": "string"}},
        "size": {"type": "integer"},
    },
}

# Define the containerLinuxParametersDeviceSchema
container_linux_parameters_device_schema = {
    "type": "object",
    "required": ["hostPath"],
    "properties": {
        "hostPath": {"type": "string"},
        "containerPath": {"type": "string"},
        "permissions": {"type": "array", "items": {"type": "string"}},
    },
}

# Define the containerLinuxParametersCapabilitySchema
container_linux_parameters_capability_schema = {
    "type": "object",
    "properties": {
        "add": {"type": "array", "items": {"type": "string"}},
        "drop": {"type": "array", "items": {"type": "string"}},
    },
}

# Define the volumeEfsVolumeConfigurationAuthorizationConfigSchema
volume_efs_volume_configuration_authorization_config_schema = {
    "type": "object",
    "properties": {
        "accessPointId": {"type": "string"},
        "iam": {"enum": ["ENABLED", "DISABLED"]},
    },
}

# Define the volumeEfsVolumeConfigurationSchema
volume_efs_volume_configuration_schema = {
    "type": "object",
    "required": ["fileSystemId"],
    "properties": {
        "fileSystemId": {"type": "string"},
        "rootDirectory": {"type": "string"},
        "transitEncryption": {"enum": ["ENABLED", "DISABLED"]},
        "transitEncryptionPort": {"type": "integer"},
        "authorizationConfig": {
            "$ref": "#/volumeEfsVolumeConfigurationAuthorizationConfig"
        },
    },
}

# Define the volumeDockerVolumeConfigurationSchema
volume_docker_volume_configuration_schema = {
    "type": "object",
    "properties": {
        "scope": {"enum": ["task", "shared"]},
        "autoprovision": {"type": "boolean"},
        "driver": {"type": "string"},
        "driverOpts": {"type": "string"},
        "labels": {"type": "string"},
    },
}

# Define the volumeHostSchema
volume_host_schema = {
    "id": "/volumeHost",
    "type": "object",
    "properties": {"sourcePath": {"type": "string"}},
}

# Define the placementConstraintSchema
placement_constraint_schema = {
    "type": "object",
    "required": ["type"],
    "properties": {
        "expression": {"type": "string"},
        "type": {"type": "string"},
    },
}

# Removing the incorrect reference to 'volume'
task_definition_schema = {
    "type": "object",
    "required": ["family", "containerDefinitions"],
    "properties": {
        "volumes": {"type": "array", "items": {"$ref": "#/volume"}},
        "placementConstraints": {
            "type": "array",
            "items": {"$ref": "#/placementConstraint"},
        },
    },
    "volumeHost": volume_host_schema,
    "volumeDockerVolumeConfiguration": volume_docker_volume_configuration_schema,
    "volumeEfsVolumeConfiguration": volume_efs_volume_configuration_schema,
    "volumeEfsVolumeConfigurationAuthorizationConfig": volume_efs_volume_configuration_authorization_config_schema,
    "placementConstraint": placement_constraint_schema,
    "containerDefinition": container_definition_schema,
}

# Define containerLinuxParametersTmpfsSchema
container_linux_parameters_tmpfs_schema = {
    "type": "object",
    "required": ["containerPath"],
    "properties": {
        "containerPath": {"type": "string"},
        "mountOptions": {"type": "array", "items": {"type": "string"}},
        "size": {"type": "integer"},
    },
}

# Define containerLinuxParametersDeviceSchema
container_linux_parameters_device_schema = {
    "type": "object",
    "required": ["hostPath"],
    "properties": {
        "hostPath": {"type": "string"},
        "containerPath": {"type": "string"},
        "permissions": {"type": "array", "items": {"type": "string"}},
    },
}

# Define containerLinuxParametersCapabilitySchema
container_linux_parameters_capability_schema = {
    "type": "object",
    "properties": {
        "add": {"type": "array", "items": {"type": "string"}},
        "drop": {"type": "array", "items": {"type": "string"}},
    },
}

# Define containerLinuxParametersSchema
container_linux_parameters_schema = {
    "type": "object",
    "properties": {
        "capabilities": {"$ref": "#/containerLinuxParametersCapability"},
        "devices": {
            "type": "array",
            "items": {"$ref": "#/containerLinuxParametersDevice"},
        },
        "initProcessEnabled": {"type": "boolean"},
        "sharedMemorySize": {"type": "integer"},
        "tmpfs": {
            "type": "array",
            "items": {"$ref": "#/containerLinuxParametersTmpfs"},
        },
    },
}

# Update the main taskDefinitionSchema to incorporate references
task_definition_schema.update(
    {
        "containerLinuxParametersTmpfs": container_linux_parameters_tmpfs_schema,
        "containerLinuxParametersDevice": container_linux_parameters_device_schema,
        "containerLinuxParametersCapability": container_linux_parameters_capability_schema,
        "containerLinuxParameters": container_linux_parameters_schema,
    }
)

# Define volumeEfsVolumeConfigurationAuthorizationConfigSchema
volume_efs_volume_configuration_authorization_config_schema = {
    "type": "object",
    "properties": {
        "accessPointId": {"type": "string"},
        "iam": {"enum": ["ENABLED", "DISABLED"]},
    },
}

# Define volumeEfsVolumeConfigurationSchema
volume_efs_volume_configuration_schema = {
    "type": "object",
    "required": ["fileSystemId"],
    "properties": {
        "fileSystemId": {"type": "string"},
        "rootDirectory": {"type": "string"},
        "transitEncryption": {"enum": ["ENABLED", "DISABLED"]},
        "transitEncryptionPort": {"type": "integer"},
        "authorizationConfig": {
            "$ref": "#/volumeEfsVolumeConfigurationAuthorizationConfig"
        },
    },
}

# Define volumeDockerVolumeConfigurationSchema
volume_docker_volume_configuration_schema = {
    "type": "object",
    "properties": {
        "scope": {"enum": ["task", "shared"]},
        "autoprovision": {"type": "boolean"},
        "driver": {"type": "string"},
        "driverOpts": {"type": "string"},
        "labels": {"type": "string"},
    },
}

# Define volumeHostSchema
volume_host_schema = {
    "type": "object",
    "properties": {"sourcePath": {"type": "string"}},
}

# Define volume schema
volume_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "host": {"$ref": "#/volumeHost"},
        "dockerVolumeConfiguration": {"$ref": "#/volumeDockerVolumeConfiguration"},
        "efsVolumeConfiguration": {"$ref": "#/volumeEfsVolumeConfiguration"},
    },
}

# Define placementConstraintSchema
placement_constraint_schema = {
    "type": "object",
    "required": ["type"],
    "properties": {
        "expression": {"type": "string"},
        "type": {"type": "string"},
    },
}

# Updating the main taskDefinitionSchema
task_definition_schema.update(
    {
        "volumeEfsVolumeConfigurationAuthorizationConfig": volume_efs_volume_configuration_authorization_config_schema,
        "volumeEfsVolumeConfiguration": volume_efs_volume_configuration_schema,
        "volumeDockerVolumeConfiguration": volume_docker_volume_configuration_schema,
        "volumeHost": volume_host_schema,
        "volume": volume_schema,
        "placementConstraint": placement_constraint_schema,
    }
)

validator = Draft7Validator(task_definition_schema)
