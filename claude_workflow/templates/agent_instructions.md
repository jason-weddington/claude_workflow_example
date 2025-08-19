# {{FILENAME}} Project Template

## Build and Test Commands
```
# Add your project's build and test commands here
# Examples:
# npm install       # Install dependencies
# npm test          # Run tests
# pip install -r requirements.txt  # Install dependencies
# pytest            # Run tests
```

## Project Structure

```
your-project/                  # Your project repository
├── {{FILENAME}}               # Project-specific build and test commands (created by init)
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

Feature-specific notes are stored in the `planning` folder in a subfolder that exactly matches your git branch name. The directory structure mirrors your branch names - if your branch is called `feature/new-feature`, the docs go in `planning/feature/new-feature/`. The word "feature" is not a special directory, it's just part of common branch naming conventions.

## Creating a New Project
To bootstrap a new project with the standard planning structure:

1. Create and checkout a new feature branch (e.g., `git checkout -b feature/new-feature`)
2. Run the project bootstrap command:
   ```
   claude-workflow new
   ```
3. The command will:
   - Create the proper directory structure based on your current branch
   - Copy template files for feature-specific documents (feature.md, tasks.md, to-do.md)
4. **IMPORTANT:** Open and read the template files in the docs/ directory, particularly `codebase.md` and `domain.md`. These contain first-time setup instructions for AI assistants to analyze your codebase and document it properly.

## Development Workflow
- Check to-do.md for the next task to implement (simple checklist with 1:1 mapping to tasks.md)
- Read the detailed requirements in tasks.md for that specific task
- Implement only that single task completely, following TDD practices
- Ensure all tests pass before considering the task complete
- Update docs/codebase.md with any new structures, patterns, or concepts introduced
- Mark the task as completed in to-do.md (check the box)
- Commit changes to git with a meaningful commit message
- Stop and wait for feedback before moving to the next task

**File Relationship**: tasks.md contains detailed task descriptions with acceptance criteria and implementation notes. to-do.md contains a simple checklist that maps 1:1 to those tasks - one checkbox per task, no detailed breakdowns.

## Code Style Guidelines
- Add your project's code style guidelines here

## Project Structure
- Add your project's structure information here
