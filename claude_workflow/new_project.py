#!/usr/bin/env python
"""
new_project.py - Bootstrap a new project planning structure

This script creates a new project planning directory structure based on the current git branch
and creates templates for feature-specific files.

Usage:
    new_project.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import argparse
import importlib.resources as pkg_resources

from claude_workflow.utils import get_current_branch


def create_project_structure(current_branch):
    """Create the project directory structure based on the current branch name."""
    # Determine the planning directory
    planning_dir = Path("planning").absolute()
    if not planning_dir.exists():
        print(f"Error: Planning directory not found at {planning_dir}")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Parse the branch name to get the directory structure
    # Example: feature/new-feature becomes feature/new-feature
    branch_parts = current_branch.split('/')
    
    # Create the target directory
    target_dir = planning_dir
    for part in branch_parts:
        target_dir = target_dir / part
    
    # Create the directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    print(f"Created directory structure: {target_dir}")
    
    
    # Create template files
    create_template_files(target_dir, planning_dir)
    
    return target_dir


def create_template_files(target_dir, planning_dir):
    """Create template files in the target directory."""
    templates_dir = planning_dir / 'templates'
    
    # List of feature-specific template files to copy
    template_files = [
        'feature.md',
        'tasks.md',
        'to-do.md'
    ]
    
    for file in template_files:
        source_file = templates_dir / file
        target_file = target_dir / file
        
        # Only create the file if it doesn't exist and the template exists
        if not target_file.exists() and source_file.exists():
            shutil.copy2(source_file, target_file)
            print(f"Created {file} from template")
        elif not source_file.exists():
            print(f"Warning: Template file {source_file} not found")


def main():
    """Main function."""
    
    # Get the current branch
    current_branch = get_current_branch()
    if not current_branch:
        print("Error: Could not determine current git branch")
        sys.exit(1)
        
    print(f"Current branch: {current_branch}")
    
    # Create the project structure
    target_dir = create_project_structure(current_branch)
    
    print(f"\nProject structure created successfully at: {target_dir}")
    print("\nThe following files were created or copied:")
    for file in os.listdir(target_dir):
        print(f" - {file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())