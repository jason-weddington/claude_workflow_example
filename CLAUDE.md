# Claude Workflow Framework - AI Assistant Instructions

## Build and Test Commands
```bash
# Install in development mode
pip install -e .

# Install from source
pip install git+https://github.com/jason-weddington/claude_workflow_example.git

# Test the CLI commands
claude-workflow --help
claude-workflow init --help
claude-workflow new --help

# Test in a temporary directory
mkdir /tmp/test_project && cd /tmp/test_project && git init
claude-workflow init .
claude-workflow init . --amazonq  # Test Amazon Q variant
```

## Project Purpose and Domain

This is a **meta-tool** - an AI-first development framework designed to help AI assistants (Claude, Amazon Q, Cline, etc.) work more effectively on software projects. The core insight is that AI assistants need structured context and documentation to produce consistent, high-quality code that aligns with project patterns and business requirements.

### Key Domain Concepts:
- **AI-First Development**: Development workflows where AI assistants are the primary code writers
- **Context Problem**: AI assistants lose context between sessions and struggle with large codebases
- **Branch-Based Documentation**: Documentation structure that mirrors git workflow
- **Template-Driven Workflow**: Standardized templates that capture the context AI needs

## Architecture Overview

### CLI Structure
- **Entry Point**: `pyproject.toml` defines `claude-workflow` command → `claude_workflow.cli:main`
- **Command Router**: `cli.py` uses `argparse` to route to subcommands:
  - `init` → `create_command()` - Initialize project with framework
  - `new` → `new_project_command()` - Create branch-specific docs
  - `update` → `update_command()` - Update project structure

### Template System
- **Unified Template**: `claude_workflow/templates/agent_instructions.md` with placeholders
- **Template Substitution**: CLI replaces `{{FILENAME}}` and `{{AGENT_NAME}}` at runtime
- **Template Categories**:
  - **Agent Instructions**: `agent_instructions.md` → `CLAUDE.md` or `AmazonQ.md`
  - **General Docs**: `api-docs.md`, `architecture.md`, `codebase.md`, etc. → `docs/`
  - **Feature Planning**: `feature.md`, `tasks.md`, `to-do.md` → `planning/templates/`

### File Organization
```
claude_workflow_example/           # This repository
├── claude_workflow/               # Python package
│   ├── cli.py                     # Main CLI logic and command routing
│   ├── new_project.py             # Branch-specific documentation creation
│   ├── utils.py                   # Utility functions
│   └── templates/                 # Template files
│       ├── agent_instructions.md  # Unified template for CLAUDE.md/AmazonQ.md
│       ├── api-docs.md            # API documentation template
│       ├── architecture.md        # Architecture template
│       ├── codebase.md            # Code patterns template
│       ├── domain.md              # Domain concepts template
│       ├── feature.md             # Feature description template
│       ├── setup.md               # Setup instructions template
│       ├── tasks.md               # Task breakdown template
│       ├── testing.md             # Testing strategy template
│       └── to-do.md               # Task checklist template
├── pyproject.toml                     # Package configuration and CLI entry point
├── README.md                      # Public documentation for GitHub
└── CLAUDE.md                      # This file - AI assistant instructions
```

## Development Guidelines

### When Adding New Templates:
1. Create the template file in `claude_workflow/templates/`
2. Add appropriate placeholder variables if needed (e.g., `{{AGENT_NAME}}`)
3. Update the template copying logic in `cli.py`
4. Consider whether it goes to `docs/` (general) or `planning/templates/` (feature-specific)

### When Modifying CLI Commands:
1. **Command Logic**: Update functions in `cli.py` (`create_command`, `new_project_command`, etc.)
2. **Argument Parsing**: Modify the `argparse` setup in `main()`
3. **Template Handling**: Update template substitution logic if adding new placeholders
4. **Success Messages**: Update user-facing messages to be helpful and consistent

### Code Style:
- Use `pathlib.Path` for file operations
- Use `importlib.resources` for accessing package templates
- Follow Python naming conventions (snake_case for functions/variables)
- Include docstrings for public functions
- Handle errors gracefully with informative messages

## Key Implementation Details

### Template Substitution System:
The CLI uses a unified template approach to avoid duplication:
```python
# Read unified template
template_src = pkg_resources.files('claude_workflow') / 'templates' / 'agent_instructions.md'
template_content = template_src.read_text()

# Replace placeholders
content = template_content.replace('{{FILENAME}}', output_filename)
content = content.replace('{{AGENT_NAME}}', agent_name)
```

### Branch-Based Documentation:
The `new_project_command()` creates documentation that mirrors git branch structure:
- Branch: `feature/new-auth` → Directory: `planning/feature/new-auth/`
- Branch: `fix/bug-123` → Directory: `planning/fix/bug-123/`

### Package Data Handling:
Templates are included as package data via `pyproject.toml`:
```toml
[tool.setuptools.package-data]
claude_workflow = ["templates/*"]
```

## Testing Strategy

### Manual Testing Workflow:
1. Create temporary git repository
2. Test `claude-workflow init .` (creates CLAUDE.md)
3. Test `claude-workflow init . --amazonq` (creates AmazonQ.md)
4. Verify template substitution worked correctly
5. Test `claude-workflow new` on different branch types
6. Clean up test directories

### Areas Needing Attention:
- Error handling for non-git directories
- Template file validation
- Cross-platform path handling
- Package installation edge cases

## Meta-Development Notes

This tool is designed to solve the "AI context problem" - the challenge that AI assistants face when working on real codebases without sufficient context about domain concepts, architectural decisions, and coding patterns. 

When working on this project, remember:
- **Target Users**: Developers who use AI assistants as primary coding partners
- **Core Value**: Structured documentation that travels with code
- **Success Metric**: AI assistants produce better, more consistent code
- **Design Philosophy**: Minimal setup, maximum context capture

The framework should remain simple and focused on its core mission: enabling effective AI-human collaboration in software development.
