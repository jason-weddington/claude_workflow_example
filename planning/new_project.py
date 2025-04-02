#!/usr/bin/env python
"""
new_project.py - Bootstrap a new project planning structure

This script creates a new project planning directory structure based on the current git branch,
copying domain.md and codebase.md from an existing project, and creating templates for other files.

Usage:
    new_project.py [--source-branch BRANCH]

Options:
    --source-branch BRANCH    Branch to copy domain.md and codebase.md from [default: main]
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import argparse


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
        sys.exit(1)


def create_project_structure(current_branch, source_branch):
    """Create the project directory structure based on the current branch name."""
    # Get the base directory
    base_dir = Path(__file__).parent.absolute()
    
    # Parse the branch name to get the directory structure
    # Example: feature/new-feature becomes feature/new-feature
    branch_parts = current_branch.split('/')
    
    # Create the target directory
    target_dir = base_dir
    for part in branch_parts:
        target_dir = target_dir / part
    
    # Create the directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    print(f"Created directory structure: {target_dir}")
    
    # Source files directory
    source_dir = base_dir
    for part in source_branch.split('/'):
        source_dir = source_dir / part
    
    # Copy the domain.md and codebase.md files from the source branch
    copy_source_files(source_dir, target_dir)
    
    # Create template files
    create_template_files(target_dir)
    
    return target_dir


def copy_source_files(source_dir, target_dir):
    """Copy domain.md and codebase.md from the source directory to the target directory."""
    files_to_copy = ['domain.md', 'codebase.md']
    
    # For first-time setup, ensure source_dir exists
    if not source_dir.exists() and source_dir.name == 'main':
        # Special handling for main branch - create it if it doesn't exist
        os.makedirs(source_dir, exist_ok=True)
        print(f"Created source directory: {source_dir} (first-time setup)")
        
        # Create template files in main for first-time setup
        templates_dir = Path(__file__).parent / 'templates'
        for file in files_to_copy:
            template_file = templates_dir / file
            source_file = source_dir / file
            if template_file.exists() and not source_file.exists():
                shutil.copy2(template_file, source_file)
                print(f"Created initial {file} in {source_dir} (first-time setup)")
    
    for file in files_to_copy:
        source_file = source_dir / file
        target_file = target_dir / file
        
        # Skip if source and target are the same file
        if source_file.resolve() == target_file.resolve():
            print(f"Skipping {file} - source and target are the same file")
            continue
        
        if source_file.exists():
            shutil.copy2(source_file, target_file)
            print(f"Copied {file} from {source_dir}")
        else:
            # If source file doesn't exist, copy from templates
            template_file = Path(__file__).parent / 'templates' / file
            if template_file.exists():
                shutil.copy2(template_file, target_file)
                print(f"Created {file} from template (source file not found)")
            else:
                print(f"Warning: Neither source file {source_file} nor template {template_file} found")


def create_template_files(target_dir):
    """Create template files in the target directory."""
    templates_dir = Path(__file__).parent / 'templates'
    
    # List of template files to copy (excluding domain.md and codebase.md which were copied directly)
    template_files = [
        'feature.md',
        'tasks.md',
        'to-do.md',
        'setup.md',
        'architecture.md',
        'api-docs.md',
        'testing.md'
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
    parser = argparse.ArgumentParser(description="Bootstrap a new project planning structure")
    parser.add_argument("--source-branch", default="main", help="Branch to copy domain.md and codebase.md from")
    args = parser.parse_args()
    source_branch = args.source_branch
    
    # Get the current branch
    current_branch = get_current_branch()
    print(f"Current branch: {current_branch}")
    
    # Create the project structure
    target_dir = create_project_structure(current_branch, source_branch)
    
    print(f"\nProject structure created successfully at: {target_dir}")
    print("\nThe following files were created or copied:")
    for file in os.listdir(target_dir):
        print(f" - {file}")


if __name__ == "__main__":
    main()