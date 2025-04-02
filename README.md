# Claude Workflow Framework

A task management framework designed to help Claude Code (or other agents) structure projects, manage tasks, and document software development processes using a standardized folder structure and markdown templates.

## Features

- Git branch-based project organization
- Automated project structure creation
- Standardized documentation templates
- Clear development workflow guidance
- Integration with Claude's task tracking capabilities

## Installation

### Method 1: Installation via pip

The simplest way to install the Claude Workflow Framework is via pip:

```bash
# Install directly from GitHub
pip install git+https://github.com/jason-weddington/claude_workflow_example.git

# Or install locally in development mode
git clone https://github.com/jason-weddington/claude_workflow_example.git
cd claude_workflow_example
pip install -e .
```

After installation, you can initialize a project with:

```bash
# Navigate to your project
cd /path/to/your/project

# Initialize the Claude Workflow
claude-workflow init .

# Create branch-specific documentation
git checkout -b feature/your-feature
claude-workflow new
```

### Method 2: Using the Install Script

Alternatively, you can use the provided install script:

1. Clone the repository
2. Run the install script with your target project path

```bash
# Clone the repo
git clone https://github.com/jason-weddington/claude_workflow_example.git
cd claude_workflow_example

# Run the install script
./install.sh /path/to/your/project
```

## First-Time Setup

When using this framework in a new repository:

1. Initialize the project structure:
   ```
   python planning/new_project.py --source-branch main
   ```

2. Ask Claude to help create your initial documentation:
   ```
   cat planning/main/codebase.md  # Read the template with setup instructions
   cat planning/main/domain.md    # Read the template with setup instructions
   ```

3. Work with Claude to analyze your codebase and create comprehensive documentation
4. Both template files contain instructions that Claude can follow to help document your project

## Project Structure

```
your-project/
├── CLAUDE.md                  # Project-specific build and test commands
├── planning/                  # Planning directory
│   ├── new_project.py         # Script to bootstrap new feature documentation
│   ├── templates/             # Template files
│   │   ├── api-docs.md        # API documentation template
│   │   ├── architecture.md    # System architecture template
│   │   ├── codebase.md        # Code style and patterns template
│   │   ├── domain.md          # Domain concepts template
│   │   ├── feature.md         # Feature description template
│   │   ├── setup.md           # Environment setup template
│   │   ├── tasks.md           # Development tasks template
│   │   ├── testing.md         # Testing strategy template
│   │   └── to-do.md           # Task checklist template
│   └── feature/               # Branch-specific folders will be created here
│       └── my-feature/        # Example feature folder created by new_project.py
```

## Usage

### Creating a New Feature

1. Create and checkout a new feature branch:
   ```
   git checkout -b feature/new-feature
   ```

2. Run the project bootstrap script:
   ```
   # If installed via pip:
   claude-workflow new
   
   # Or if using the manual installation:
   python planning/new_project.py
   ```

3. The script will:
   - Create the proper directory structure based on your current branch
   - Copy the latest `domain.md` and `codebase.md` from the source branch
   - Create template files for all other standard documents

4. Customize the template files for your specific project

### Development Workflow

1. Check `to-do.md` for the next task to implement
2. Read the detailed requirements in `tasks.md` for that specific task
3. Implement only that single task completely, following TDD practices
4. Ensure all tests pass before considering the task complete
5. Update `codebase.md` with any new structures, patterns, or concepts introduced
6. Mark the task as completed in `to-do.md`
7. Commit changes to git with a meaningful commit message
8. Stop and wait for feedback before moving to the next task

## Customization

Edit the templates in `planning/templates/` to match your project's specific needs and development practices.

## Contributing

Feel free to customize and extend this framework to better suit your team's workflow needs.