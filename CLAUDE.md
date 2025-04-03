# CLAUDE.md Project Template

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
├── CLAUDE.md                  # Project-specific build and test commands (created by init)
├── planning/                  # Planning directory (created by init)
│   ├── templates/             # Template files (created by init)
│   │   ├── api-docs.md        # API documentation template
│   │   ├── architecture.md    # System architecture template
│   │   ├── codebase.md        # Code style and patterns template
│   │   ├── domain.md          # Domain concepts template
│   │   └── ...                # Other templates
│   ├── main/                  # Main branch documentation (created by new on main branch)
│   │   ├── codebase.md        # Documentation of code organization and patterns
│   │   └── domain.md          # Documentation of domain concepts and rules
│   └── feature/               # Feature branch folders (created by new on feature branches)
│       └── your-feature/      # Documentation for specific features
│           ├── api-docs.md    # API documentation for this feature
│           ├── architecture.md # Architecture changes for this feature
│           ├── codebase.md    # Code patterns (copied from main branch)
│           ├── domain.md      # Domain concepts (copied from main branch)
│           ├── feature.md     # Feature description
│           ├── tasks.md       # Detailed development tasks
│           ├── to-do.md       # Task checklist
│           ├── setup.md       # Environment setup instructions
│           └── testing.md     # Testing strategy for this feature
```

Notes for each branch are stored in the `planning` folder in a subfolder matching the git branch name. For example, documentation for branch `feature/new-feature` goes in `/planning/feature/new-feature/`.

## Creating a New Project
To bootstrap a new project with the standard planning structure:

1. Create and checkout a new feature branch (e.g., `git checkout -b feature/new-feature`)
2. Run the project bootstrap command:
   ```
   claude-workflow new
   ```
3. The command will:
   - Create the proper directory structure based on your current branch
   - Copy the latest `domain.md` and `codebase.md` from the source branch
   - Create template files for all other standard documents
4. **IMPORTANT:** Open and read the template files, particularly `codebase.md` and `domain.md`. These contain first-time setup instructions for AI assistants to analyze your codebase and document it properly.

You can optionally specify a different source branch to copy from:
```
claude-workflow new --source-branch feature/other-branch
```

## Development Workflow
- Check to-do.md for the next task to implement
- Read the detailed requirements in tasks.md for that specific task
- Implement only that single task completely, following TDD practices
- Ensure all tests pass before considering the task complete
- Update codebase.md with any new structures, patterns, or concepts introduced
- Mark the task as completed in to-do.md
- Commit changes to git with a meaningful commit message
- Stop and wait for feedback before moving to the next task

## Code Style Guidelines
- Add your project's code style guidelines here

## Project Structure
- Add your project's structure information here