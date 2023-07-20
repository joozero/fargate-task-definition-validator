from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="fargate_validator",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "fargate-validator = fargate_task_validator.__main__:main",
        ],
    },
    install_requires=requirements,
    author="Jooyoung Kim",
    author_email="joozero@amazon.com",
    description="A utility to validate AWS ECS task definitions for Fargate compatibility",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/joozero/fargate-task-definition-validator",
)
