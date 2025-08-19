# Codebase Structure and Patterns

## Code Organization

### Main Directories
- **`claude_workflow/`** - Main Python package containing all source code
  - **`cli.py`** - CLI entry point and command routing using argparse
  - **`new_project.py`** - Branch-specific documentation creation logic
  - **`utils.py`** - Utility functions (currently minimal)
  - **`templates/`** - Template files that get copied to user projects
- **`docs/`** - Project documentation (created by dog-fooding the framework)
- **`planning/`** - Planning templates and project-specific planning docs
- **`pyproject.toml`** - Modern Python package configuration and dependencies
- **`README.md`** - Public-facing documentation for GitHub
- **`CLAUDE.md`** - AI assistant instructions for working on this project
- **`AmazonQ.md`** - Generated template showing framework output

### Architecture Pattern
- **CLI Tool Architecture**: Single-purpose command-line tool with subcommands
- **Template-Based Generation**: Uses template files with placeholder substitution
- **Package Resource Access**: Uses `importlib.resources` to access bundled templates
- **Git-Aware**: Integrates with git branch structure for organization

## Style Guide

### Python Conventions
- **Naming**: snake_case for functions and variables, PascalCase for classes
- **Imports**: Use `pathlib.Path` for file operations, `importlib.resources` for package data
- **Error Handling**: Graceful error messages for user-facing failures
- **Documentation**: Docstrings for public functions, inline comments for complex logic

### File Organization
- **Template Files**: All templates in `claude_workflow/templates/` with `.md` extension
- **CLI Commands**: Each subcommand has its own function in `cli.py`
- **Package Data**: Templates included via `pyproject.toml` package-data configuration

## Common Patterns

### Template Substitution Pattern
```python
# Read template with placeholders
template_content = template_src.read_text()

# Replace placeholders with actual values
content = template_content.replace('{{PLACEHOLDER}}', actual_value)
```

### CLI Command Pattern
```python
def command_function(args):
    """Command implementation with error handling."""
    # Validate inputs
    # Perform operations
    # Provide user feedback
    return 0  # Success exit code
```

### File Operations Pattern
- Use `pathlib.Path` for all file operations
- Create directories with `mkdir(parents=True, exist_ok=True)`
- Handle file existence checks before operations
- Use context managers for file operations

### Git Integration Pattern
- Check for `.git` directory to validate git repositories
- Use current branch name to determine documentation structure
- Mirror git branch structure in planning directories

## Testing

### Current State
- **Manual Testing**: CLI commands tested in temporary directories
- **No Automated Tests**: Project currently relies on manual testing workflow
- **Test Approach**: Create temp git repos, run commands, verify output

### Testing Workflow
```bash
# Create test environment
mkdir /tmp/test_project && cd /tmp/test_project && git init

# Test init command
claude-workflow init .
claude-workflow init . --amazonq

# Test new command
git checkout -b feature/test
claude-workflow new

# Verify file creation and content
```

## Developer Onboarding

### What to Read First
1. **README.md** - Understand the project purpose and AI-first development context
2. **CLAUDE.md** - Detailed technical documentation and architecture
3. **`claude_workflow/cli.py`** - Main entry point and command structure
4. **Template files** - Understand what gets generated for users

### Local Development Setup
```bash
# Clone and install in development mode
git clone <repo-url>
cd claude_workflow_example
pip install -e . --user

# Test installation
claude-workflow --help
```

### Key Implementation Details
- **Template System**: Single `agent_instructions.md` template with `{{FILENAME}}` and `{{AGENT_NAME}}` placeholders
- **Branch Mapping**: Branch names like `feature/auth` create directories `planning/feature/auth/`
- **Package Data**: Templates bundled with package and accessed via `importlib.resources`
- **CLI Structure**: Uses argparse with subparsers for clean command organization

### Common Development Tasks
- **Adding Templates**: Create in `templates/`, update CLI copying logic
- **New CLI Commands**: Add function to `cli.py`, wire up in `main()`
- **Template Changes**: Modify unified template, test with both Claude and Amazon Q variants
- **Testing Changes**: Use temporary directories to avoid polluting development environment

### Meta-Development Notes
This project is a "meta-tool" - it helps AI assistants work better on codebases. When working on it:
- Consider how changes affect AI assistant workflows
- Test with both `--amazonq` and default (Claude) variants
- Remember the target users are developers using AI assistants as primary coding partners
- Keep the tool simple and focused on solving the "AI context problem"
