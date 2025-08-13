# AmazonQ.md Project Template

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
├── AmazonQ.md                 # Project-specific build and test commands (created by init)
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

## Creating Documentation for a New Feature
When starting work on a new feature, use this command to create the planning documentation structure for that feature branch:

1. Create and checkout a new feature branch (e.g., `git checkout -b feature/new-feature`)
2. Run the project bootstrap command:
   ```
   claude-workflow new
   ```
3. The command will:
   - Create the proper directory structure based on your current branch
   - Create template files for feature-specific documents
4. **IMPORTANT:** Open and read the template files, particularly those in the docs/ directory. The `codebase.md` and `domain.md` in docs/ contain first-time setup instructions for AI assistants to analyze your codebase and document it properly.

## Planning Workflow
- Discuss the current feature with the user
- Update feature.md documentation in planning/<branch-name>/feature.md
- Collaborate with the user to define detailed development tasks with clear acceptance criteria in planning/<branch-name>/tasks.md
- Add simple checkbox tasks in planning/<branch-name>/to-do.md that correspond to each task

## Development Workflow
- Check to-do.md for the next task to implement
- Read the detailed requirements in tasks.md for that specific task
- Implement only that single task completely, following TDD practices
- Ensure all tests pass before considering the task complete
- Update docs/codebase.md with any new structures, patterns, or concepts introduced
- Mark the task as completed in to-do.md
- Commit changes to git with a meaningful commit message
- Stop and wait for feedback before moving to the next task

## Code Style Guidelines
- Add your project's code style guidelines here