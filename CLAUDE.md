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

## Project Notes
- Store notes in the `planning` folder in a subfolder matching the git branch name
- Example: for branch `feature/new-feature`, notes should go in `/planning/feature/new-feature/`
- Standard files in each notes folder:
  - `codebase.md`: Code style, test locations, domain structure, and developer onboarding info
  - `feature.md`: Description of the feature being built, including business goals
  - `tasks.md`: Detailed development tasks with clear acceptance criteria for new developers
  - `to-do.md`: Simple checklist that corresponds to the detailed tasks in tasks.md
  - `setup.md`: Environment setup instructions, required dependencies, and troubleshooting tips
  - `domain.md`: Explanation of key domain concepts, terminology, and business rules
  - `architecture.md`: High-level system design, component relationships, and data flow diagrams
  - `api-docs.md`: Documentation of any APIs this code interacts with, including examples
  - `testing.md`: Testing strategy, test data setup, and how to validate changes

## Creating a New Project
To bootstrap a new project with the standard planning structure:

1. Create and checkout a new feature branch (e.g., `git checkout -b feature/new-feature`)
2. Run the project bootstrap script:
   ```
   python planning/new_project.py
   ```
3. The script will:
   - Create the proper directory structure based on your current branch
   - Copy the latest `domain.md` and `codebase.md` from the source branch
   - Create template files for all other standard documents
4. Customize the template files for your specific project

You can optionally specify a different source branch to copy from:
```
python planning/new_project.py --source-branch feature/other-branch
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