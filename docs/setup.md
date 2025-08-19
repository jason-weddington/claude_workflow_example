# Environment Setup

## Prerequisites

- **Python 3.6+** (Python 3.9+ recommended)
- **Git** (for repository management and branch detection)
- **pip** (for package installation)

## Installation Options

### Option 1: Install from GitHub (Recommended for Users)
```bash
pip install git+https://github.com/jason-weddington/claude_workflow_example.git
```

### Option 2: Development Installation (For Contributors)
```bash
# Clone the repository
git clone https://github.com/jason-weddington/claude_workflow_example.git
cd claude_workflow_example

# Install in editable mode
pip install -e . --user
```

### Option 3: Using the Install Script (Legacy)
```bash
# Clone and run install script
git clone https://github.com/jason-weddington/claude_workflow_example.git
cd claude_workflow_example
./install.sh /path/to/your/project
```

## Verification

After installation, verify the tool works:

```bash
# Check installation
claude-workflow --help

# Should show:
# usage: claude-workflow [-h] {init,new,update} ...
# Claude Workflow - A development task management framework
```

## Configuration

No additional configuration is required. The tool works out of the box with any git repository.

### Optional: Shell Completion
For bash completion (optional):
```bash
# Add to ~/.bashrc or ~/.bash_profile
eval "$(_CLAUDE_WORKFLOW_COMPLETE=source_bash claude-workflow)"
```

## Development Environment Setup

### For Framework Development

1. **Clone and Install**:
   ```bash
   git clone <repo-url>
   cd claude_workflow_example
   pip install -e . --user
   ```

2. **Verify Development Installation**:
   ```bash
   # Test CLI commands
   claude-workflow --help
   claude-workflow init --help
   claude-workflow new --help
   ```

3. **Test in Temporary Environment**:
   ```bash
   # Create test project
   mkdir /tmp/test_project && cd /tmp/test_project
   git init
   
   # Test framework
   claude-workflow init .
   claude-workflow init . --amazonq  # Test Amazon Q variant
   
   # Clean up
   rm -rf /tmp/test_project
   ```

### Development Dependencies

The framework has minimal dependencies by design:
- **Core**: Python standard library (pathlib, argparse, importlib.resources)
- **No external dependencies** required for basic functionality

### IDE Setup

Recommended for development:
- **VS Code** with Python extension
- **PyCharm** (Community or Professional)
- Any editor with Python syntax highlighting

## Troubleshooting

### Common Issues

**"Command not found: claude-workflow"**
- Ensure pip installation completed successfully
- Check that pip install location is in your PATH
- Try `python -m claude_workflow.cli` as alternative

**"Error: Target directory does not exist"**
- Ensure you're providing the correct path to `claude-workflow init`
- Use absolute paths if relative paths aren't working

**"Warning: Target directory does not appear to be a git repository"**
- Initialize git in your project: `git init`
- Or confirm you want to proceed anyway when prompted

**Template files not found**
- Reinstall the package: `pip install -e . --user --force-reinstall`
- Verify templates exist: `python -c "import claude_workflow; print(claude_workflow.__file__)"`

### Platform-Specific Notes

**macOS/Linux**:
- Use `pip3` instead of `pip` if you have both Python 2 and 3
- May need `--user` flag if you don't have admin privileges

**Windows**:
- Use Command Prompt or PowerShell
- Ensure Python Scripts directory is in PATH
- May need to use `py -m pip` instead of `pip`

## Uninstallation

To remove the framework:
```bash
pip uninstall claude-workflow
```

This will remove the CLI tool but leave any documentation you've created in your projects.
