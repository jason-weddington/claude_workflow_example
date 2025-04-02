"""
Utility functions for the Claude Workflow tool.
"""

import os
import subprocess
from pathlib import Path


def get_current_branch():
    """Get the name of the current git branch."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.SubprocessError as e:
        print(f"Error getting current branch: {e}")
        return None


def is_git_repository(path):
    """Check if the specified path is a git repository."""
    return os.path.exists(os.path.join(path, ".git"))