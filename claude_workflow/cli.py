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
    use_amazonq = getattr(args, 'amazonq', False)
    
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
    
    # Create docs directory
    docs_dir = target_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Determine which template and filename to use
    if use_amazonq:
        template_name = 'AmazonQ.md'
        output_filename = 'AmazonQ.md'
    else:
        template_name = 'CLAUDE.md'
        output_filename = 'CLAUDE.md'
    
    # Copy the appropriate .md file to target directory, removing the H1 header
    md_src = pkg_resources.files('claude_workflow') / 'templates' / template_name
    with md_src.open('r') as src_file:
        lines = src_file.readlines()
        # Skip the first line (H1 header) and any blank lines that immediately follow
        start_index = 1
        while start_index < len(lines) and lines[start_index].strip() == '':
            start_index += 1
        
    with open(target_dir / output_filename, 'w') as dst_file:
        dst_file.writelines(lines[start_index:])
    
    # Copy new_project.py
    project_script_src = Path(__file__).parent / "new_project.py"
    shutil.copy(project_script_src, target_dir / "planning" / "new_project.py")
    os.chmod(target_dir / "planning" / "new_project.py", 0o755)  # Make executable
    
    # Define which template files go where
    feature_templates = ['feature.md', 'tasks.md', 'to-do.md']
    general_templates = ['api-docs.md', 'architecture.md', 'codebase.md', 'domain.md', 
                        'setup.md', 'testing.md']
    
    # Copy feature-specific templates to planning/templates
    for file in feature_templates:
        src_file = pkg_resources.files('claude_workflow') / 'templates' / file
        shutil.copy(src_file, planning_dir / file)
    
    # Copy general templates to docs/
    for file in general_templates:
        src_file = pkg_resources.files('claude_workflow') / 'templates' / file
        shutil.copy(src_file, docs_dir / file)
    
    print(f"Claude Workflow initialized in {target_dir}")
    print("")
    print("Next steps:")
    if use_amazonq:
        print(f"1. Edit {target_dir}/AmazonQ.md with your specific project details")
        print("2. Create a feature branch: git checkout -b feature/your-feature")
        print("3. Run claude-workflow new to create documentation for the new feature")
        print("4. Tell Amazon Q to read the planning documents to understand your project")
    else:
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
    return new_project_main()


def update_command(args):
    """Update project to the latest documentation structure."""
    # Ensure we're in a project directory with CLAUDE.md or AmazonQ.md
    if not Path("CLAUDE.md").exists() and not Path("AmazonQ.md").exists():
        print("Error: No CLAUDE.md or AmazonQ.md found. Please run this command from the project root.")
        return 1
    
    # Create necessary directories
    Path("docs").mkdir(exist_ok=True)
    Path("planning/templates").mkdir(parents=True, exist_ok=True)
    
    # Copy latest templates to the correct locations
    template_mappings = {
        # Feature-specific templates go to planning/templates
        'feature.md': 'planning/templates/feature.md',
        'tasks.md': 'planning/templates/tasks.md', 
        'to-do.md': 'planning/templates/to-do.md',
        # General templates go to docs
        'api-docs.md': 'docs/api-docs.md',
        'architecture.md': 'docs/architecture.md',
        'codebase.md': 'docs/codebase.md',
        'domain.md': 'docs/domain.md',
        'setup.md': 'docs/setup.md',
        'testing.md': 'docs/testing.md'
    }
    
    for template_file, dest_path in template_mappings.items():
        dest_file = Path(dest_path)
        if not dest_file.exists():
            src_file = pkg_resources.files('claude_workflow') / 'templates' / template_file
            shutil.copy(src_file, dest_file)
    
    # Update new_project.py script to latest version
    project_script_src = Path(__file__).parent / "new_project.py"
    project_script_dest = Path("planning/new_project.py")
    shutil.copy(project_script_src, project_script_dest)
    os.chmod(project_script_dest, 0o755)  # Make executable
    
    # Create migration instructions
    migration_src = pkg_resources.files('claude_workflow') / 'templates' / 'MIGRATION_INSTRUCTIONS.md'
    shutil.copy(migration_src, Path("MIGRATION_INSTRUCTIONS.md"))
    
    # Read and display the migration instructions
    with open("MIGRATION_INSTRUCTIONS.md", 'r') as f:
        instructions = f.read()
    
    print("="*70)
    print("CLAUDE WORKFLOW UPDATE - MIGRATION REQUIRED")
    print("="*70)
    print()
    print(instructions)
    print()
    print("="*70)
    print("Migration instructions have been saved to: MIGRATION_INSTRUCTIONS.md")
    print("Please review and follow the instructions above to complete the migration.")
    print("="*70)
    
    return 0


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Claude Workflow - A development task management framework"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new Claude Workflow in a directory")
    init_parser.add_argument("path", help="Path to the target directory")
    init_parser.add_argument("--amazonq", action="store_true", help="Initialize for Amazon Q instead of Claude")
    init_parser.set_defaults(func=create_command)
    
    # New project command
    new_parser = subparsers.add_parser("new", help="Create a new project structure")
    new_parser.set_defaults(func=new_project_command)
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update project to the latest documentation structure")
    update_parser.set_defaults(func=update_command)
    
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