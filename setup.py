#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="claude-workflow",
    version="0.1.0",
    description="A task management framework for Claude-assisted development",
    author="Claude Workflow Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pathlib",
    ],
    entry_points={
        "console_scripts": [
            "claude-workflow=claude_workflow.cli:main",
        ],
    },
    package_data={
        "claude_workflow": ["templates/*"],
    },
    python_requires=">=3.6",
)