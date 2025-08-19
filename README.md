# Claude Workflow Framework

An AI-first development workflow framework designed for teams and individuals who use AI coding assistants (Claude, Amazon Q, Cline, or other agents) as their primary development partners.

## Why This Framework Exists

AI coding assistants are incredibly powerful, but they need structured context to work effectively on real codebases. Without proper documentation about your domain, architecture, and coding patterns, AI assistants often:

- Make assumptions about business rules and domain concepts
- Introduce inconsistent coding patterns
- Struggle to understand the broader context of changes
- Create code that doesn't align with existing architecture

This framework solves the **AI context problem** by providing:

1. **Structured documentation templates** that capture the context AI assistants need
2. **Branch-based task organization** that mirrors your git workflow
3. **Systematic development processes** that enable effective AI-human collaboration

## Key Benefits for AI-First Development

- **Better AI Understanding**: Comprehensive documentation helps AI assistants make informed decisions
- **Consistent Code Quality**: Documented patterns and standards ensure AI-generated code fits your project
- **Systematic Task Management**: Break complex features into AI-manageable tasks
- **Improved Collaboration**: Clear documentation benefits both AI assistants and human team members
- **Reduced Context Switching**: All relevant information is organized and accessible

## Features

- Git branch-based project organization that mirrors your development workflow
- Automated project structure creation with one command
- Standardized documentation templates optimized for AI assistant consumption
- Clear development workflow guidance for AI-human collaboration
- Support for multiple AI assistants (Claude, Amazon Q, Cline, and others)
- Integration with AI assistant task tracking capabilities

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

# Initialize for Claude (default)
claude-workflow init .

# OR initialize for Amazon Q
claude-workflow init . --amazonq
```

This creates:
- `CLAUDE.md` (or `AmazonQ.md` with --amazonq flag) file in your project root
- `docs/` directory with general project documentation
- `planning/templates/` directory with feature-specific templates

### Step 3: Create Documentation for Your Branch

```bash
# Create or checkout a feature branch
git checkout -b feature/your-feature

# Generate branch-specific documentation structure
claude-workflow new
```

This creates branch-specific documentation in `planning/feature/your-feature/` based on your current branch name.

### Step 4: Have Your AI Assistant Fill In The Templates (Most Important Step!)

It's critical to invest time upfront creating the initial documentation. This will provide the requisite context for AI-first software development.

Ask your AI assistant (Claude or Amazon Q) to analyze your codebase and document it:

```
"Please analyze our codebase and help me fill out the codebase.md and domain.md files 
based on the template instructions inside them. Get started based on what you find in the code,
but then ask me questions to clarify anything that wasn't clear from reading the code."
```

Repeat this for api-docs.md, architecture.md, setup.md, and testing.md if these files are relevant to your project. Try variations of the above prompt like "help me create documentation for new team members..." and remember to ask the model to ask you questions about what it sees in the code.

The templates contain detailed instructions for your AI assistant to follow. This step is crucial - don't skip it!
## Project Structure

After completing the setup steps, your project will have this structure:

```
your-project/                  # Your project repository
├── CLAUDE.md or AmazonQ.md    # Project-specific build and test commands (created by init)
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

### `claude-workflow init [directory] [--amazonq]`

**Purpose**: One-time initialization of a project with the Claude Workflow structure
- Creates the CLAUDE.md file (or AmazonQ.md with --amazonq flag) in your project root
- Sets up the docs/ directory with general project documentation
- Sets up the planning/templates/ directory with feature-specific templates
- Only needs to be run once per repository

**Options**:
- `--amazonq`: Initialize for Amazon Q instead of Claude (creates AmazonQ.md instead of CLAUDE.md)

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

## How This Enables AI-First Development

This framework is specifically designed for development workflows where AI assistants are your primary coding partners. Here's how it addresses common AI development challenges:

### Context Management
- **Problem**: AI assistants lose context between conversations and struggle with large codebases
- **Solution**: Structured documentation provides persistent context that AI can reference across sessions

### Consistent Code Quality
- **Problem**: AI-generated code may not follow project patterns or architectural decisions
- **Solution**: `codebase.md` documents your patterns, conventions, and architectural decisions for AI to follow

### Domain Understanding
- **Problem**: AI assistants make incorrect assumptions about business rules and domain concepts
- **Solution**: `domain.md` captures business logic, terminology, and domain-specific requirements

### Task Management
- **Problem**: AI assistants work best on focused, well-defined tasks but struggle with large, ambiguous features
- **Solution**: Branch-based planning breaks features into discrete, manageable tasks with clear requirements

### Systematic Development
- **Problem**: AI assistants may skip steps or make changes without proper testing
- **Solution**: Structured workflow ensures systematic development with testing and documentation updates

The framework essentially creates a "knowledge base" that travels with your code, ensuring AI assistants have the context they need to be effective development partners.

## Dog-Fooding: Framework Building Itself

This project practices what it preaches - we use the Claude Workflow Framework to manage development of the framework itself. That's why you'll see:

- **`docs/` directory** - Contains comprehensive documentation about the framework's codebase, domain concepts, architecture, and testing strategy
- **`AmazonQ.md`** - Generated by running `claude-workflow init . --amazonq` in this repository
- **`planning/` directory** - Used for organizing feature development and task management

This serves multiple purposes:
1. **Validates the framework works** on real projects (including itself)
2. **Provides a living example** of what the documentation structure looks like when filled out
3. **Demonstrates AI-first development** in practice on a non-trivial codebase
4. **Shows both Claude and Amazon Q support** with actual generated files

If you're wondering "why does this CLI tool have so much documentation?" - it's because we're using our own tool to build it, proving that the framework scales from simple projects to complex ones.

## Testing

The Claude Workflow Framework includes comprehensive automated testing to ensure reliability and maintainability.

### Running Tests

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=claude_workflow --cov-report=term-missing

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
```

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test complete workflows end-to-end
- **Error Handling Tests**: Test edge cases and error conditions
- **80%+ Code Coverage**: Comprehensive test coverage for reliability

For detailed testing guidelines, see [TESTING.md](TESTING.md).

## Customization

Edit the templates in `planning/templates/` to match your project's specific needs and development practices.

## Contributing

Feel free to customize and extend this framework to better suit your team's workflow needs.