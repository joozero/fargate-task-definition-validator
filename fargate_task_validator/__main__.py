#!/usr/bin/env python3

import json
from termcolor import colored
from fargate_task_validator.validators.fargate_validator import (
    check_fargate_compatibility,
)
from fargate_task_validator.validators.recommendations import (
    RECOMMENDATIONS,
    REMEDIATIONS,
)
from jsonschema.exceptions import ValidationError
from fargate_task_validator.validators.schema_validator import validator
import sys


def display_results(results):
    max_length = (
        max(map(len, results.keys())) + 4
    )  # 4 is just a buffer for better visualization
    failures = []

    print("\nValidation Results:")
    print("--------------------")

    for key, value in results.items():
        key_padding = max_length - len(key)

        if value.startswith("OK"):
            status = colored(value, "green")
        elif value.startswith("WARN"):
            status = colored(value, "yellow")
        else:
            status = colored(value, "red")
            failures.append(key)

        print(f"{key}{' ' * key_padding}{status}")

    # Summary
    print("\n" + "-" * 50)
    print(
        f"Total Results: {colored('PASS', 'green') if not failures else colored('FAIL', 'red')}"
    )

    if failures:
        print("\nFailures:")
        for failure in failures:
            print(f"- {failure}")
            if failure in RECOMMENDATIONS:
                print(f"  Recommendation: {RECOMMENDATIONS[failure]}")
            if failure in REMEDIATIONS:
                print(f"  Remediation: {REMEDIATIONS[failure]}")
        print("\n")


def validate_task_definition(task_definition):
    try:
        validator.validate(task_definition)
        return "Task definition is valid!"
    except ValidationError as e:
        return f"Task definition is invalid! {e}"


def main():
    if len(sys.argv) < 2:
        print("Usage: fargate-validator <path_to_task_definition>")
        sys.exit(1)

    task_definition_path = sys.argv[1]

    with open(task_definition_path, "r") as f:
        task_definition_str = f.read()

    results = check_fargate_compatibility(task_definition_str)
    display_results(results)

    result = validate_task_definition(json.loads(task_definition_str))
    print(result)


if __name__ == "__main__":
    main()
