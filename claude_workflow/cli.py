#!/usr/bin/env python
"""
CLI entry point for the Claude Workflow tool.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
import importlib.resources as pkg_resources

from claude_workflow import utils


def create_command(args):
    """Initialize a new Claude Workflow in the specified directory."""
    target_dir = Path(args.path).resolve()
    
    # Verify the target directory
    if not target_dir.exists():
        print(f"Error: Target directory does not exist: {target_dir}")
        return 1
        
    # Check if target directory is a git repository
    if not (target_dir / ".git").exists():
        print(f"Warning: Target directory does not appear to be a git repository.")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            return 1
    
    # Create planning directory and subdirectories
    planning_dir = target_dir / "planning" / "templates"
    planning_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy CLAUDE.md to target directory
    claude_md_src = pkg_resources.files('claude_workflow') / 'templates' / 'CLAUDE.md'
    shutil.copy(claude_md_src, target_dir / "CLAUDE.md")
    
    # Copy new_project.py
    project_script_src = Path(__file__).parent / "new_project.py"
    shutil.copy(project_script_src, target_dir / "planning" / "new_project.py")
    os.chmod(target_dir / "planning" / "new_project.py", 0o755)  # Make executable
    
    # Copy template files
    template_files = [
        'api-docs.md', 'architecture.md', 'codebase.md', 'domain.md',
        'feature.md', 'setup.md', 'tasks.md', 'testing.md', 'to-do.md'
    ]
    
    for file in template_files:
        src_file = pkg_resources.files('claude_workflow') / 'templates' / file
        shutil.copy(src_file, target_dir / "planning" / "templates" / file)
    
    print(f"Claude Workflow initialized in {target_dir}")
    print("")
    print("Next steps:")
    print(f"1. Edit {target_dir}/CLAUDE.md with your specific project details")
    print("2. Create a feature branch: git checkout -b feature/your-feature")
    print("3. Run claude-workflow new to create documentation for the new feature")
    print("4. Tell Claude to read the planning documents to understand your project")
    print("")
    print("For more information, see the documentation.")
    
    return 0


def new_project_command(args):
    """Create a new project structure based on the current git branch."""
    # We'll reuse the existing new_project.py functionality
    from claude_workflow.new_project import main as new_project_main
    # Pass the source_branch argument
    return new_project_main(args.source_branch)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Claude Workflow - A development task management framework"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new Claude Workflow in a directory")
    init_parser.add_argument("path", help="Path to the target directory")
    init_parser.set_defaults(func=create_command)
    
    # New project command
    new_parser = subparsers.add_parser("new", help="Create a new project structure")
    new_parser.add_argument("--source-branch", default="main", 
                         help="Branch to copy domain.md and codebase.md from")
    new_parser.set_defaults(func=new_project_command)
    
    # Parse args
    args = parser.parse_args()
    
    # Display help if no subcommand is provided
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute the appropriate command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())