# Claude Workflow Framework

A task management framework designed to help Claude Code (or other agents) structure projects, manage tasks, and document software development processes using a standardized folder structure and markdown templates.

## Features

- Git branch-based project organization
- Automated project structure creation
- Standardized documentation templates
- Clear development workflow guidance
- Integration with Claude's task tracking capabilities

## Installation & Setup

### Step 1: Install the Framework

Choose one of these installation methods:

#### Method 1: Via pip (Recommended)

```bash
# Install directly from GitHub
pip install git+https://github.com/jason-weddington/claude_workflow_example.git
```

#### Method 2: Using the Install Script

```bash
# Clone the repo
git clone https://github.com/jason-weddington/claude_workflow_example.git
cd claude_workflow_example

# Run the install script targeting your project directory
./install.sh /path/to/your/project
```

### Step 2: Initialize Your Project

Navigate to your project repository and initialize the framework:

```bash
cd /path/to/your/project

# Initialize the project with basic structure (only run once per repository)
claude-workflow init .
```

This creates:
- `CLAUDE.md` file in your project root
- `planning/templates/` directory with documentation templates

### Step 3: Create Documentation for Your Branch

```bash
# Create or checkout a feature branch
git checkout -b feature/your-feature

# Generate branch-specific documentation structure
claude-workflow new
```

This creates branch-specific documentation in `planning/feature/your-feature/` based on your current branch name.

### Step 4: Have Claude Fill In The Templates (Most Important Step!)

Then ask Claude to analyze your codebase and document it:

```
"Please analyze our codebase and help me fill out the codebase.md and domain.md files 
based on the template instructions inside them. Get started based on what you find in the code,
but then ask me questions to clarify anything that wasn't clear from reading the code."
```

The templates contain detailed instructions for Claude to follow. This step is crucial - don't skip it!

## Project Structure

After completing the setup steps, your project will have this structure:

```
your-project/                  # Your project repository
├── CLAUDE.md                  # Project-specific build and test commands (created by init)
├── docs/                      # General project documentation (created by init)
│   ├── api-docs.md            # API documentation
│   ├── architecture.md        # System architecture
│   ├── codebase.md            # Code style and patterns
│   ├── domain.md              # Domain concepts
│   ├── setup.md               # Environment setup instructions
│   └── testing.md             # Testing strategy
├── planning/                  # Planning directory (created by init)
│   ├── templates/             # Feature-specific templates (created by init)
│   │   ├── feature.md         # Feature description template
│   │   ├── tasks.md           # Detailed development tasks template
│   │   └── to-do.md           # Task checklist template
│   └── [branch-name]/         # Mirrors your git branch structure (created by new)
│       ├── feature.md         # Feature description
│       ├── tasks.md           # Detailed development tasks
│       └── to-do.md           # Task checklist
│
│   Examples:
│   └── feature/new-auth/      # For git branch "feature/new-auth"
│   └── fix/bug-123/           # For git branch "fix/bug-123"
│   └── refactor/db-layer/     # For git branch "refactor/db-layer"
```

## Commands Reference

The framework provides two main commands:

### `claude-workflow init [directory]`

**Purpose**: One-time initialization of a project with the Claude Workflow structure
- Creates the CLAUDE.md file in your project root
- Sets up the planning directory with template files
- Only needs to be run once per repository

### `claude-workflow new`

**Purpose**: Creates documentation structure for the current branch
- Creates the appropriate directory structure (e.g., planning/feature/your-feature/)
- Creates template files for feature documentation
- Run this command whenever you create a new feature branch

## Workflow Guide

### Starting a New Project

When beginning work on a new codebase:

1. **Install & Initialize**: 
   ```bash
   pip install git+https://github.com/jason-weddington/claude_workflow_example.git
   cd /your/project
   claude-workflow init .
   ```

2. **Create Main Branch Documentation**:
   ```bash
   # Make sure you're on main branch
   git checkout main
   claude-workflow new
   ```

3. **Have Claude Analyze Your Codebase**:
   Ask Claude:
   ```
   Please review the planning/main/codebase.md and planning/main/domain.md templates, 
   then analyze our codebase to fill them out properly. Follow the first-time setup 
   instructions in the templates to document our code organization, patterns, 
   domain concepts, and business rules.
   ```

4. **Create Your First Feature Branch**:
   ```bash
   git checkout -b feature/your-feature
   claude-workflow new
   ```

### Ongoing Development Workflow

For each new task within a feature:

1. Check `to-do.md` for the next task to implement
2. Read the detailed requirements in `tasks.md` for that specific task
3. Implement only that single task completely, following TDD practices
4. Ensure all tests pass before considering the task complete
5. Update `codebase.md` with any new structures, patterns, or concepts introduced
6. Mark the task as completed in `to-do.md`
7. Commit changes to git with a meaningful commit message
8. Stop and wait for feedback before moving to the next task

### Creating New Features

When starting work on a new feature:

1. Create a new branch: `git checkout -b feature/new-feature`
2. Create documentation: `claude-workflow new`
3. Customize the template files for your specific feature
4. Define tasks in `tasks.md` and add them to `to-do.md`
5. Proceed with development using the workflow above

## Customization

Edit the templates in `planning/templates/` to match your project's specific needs and development practices.

## Contributing

Feel free to customize and extend this framework to better suit your team's workflow needs.