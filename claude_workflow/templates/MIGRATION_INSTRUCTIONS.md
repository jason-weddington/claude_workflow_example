# Claude Workflow Documentation Migration Instructions

## Overview
This project needs to be migrated to the new Claude Workflow documentation structure. The new structure separates general project documentation from feature-specific planning documents.

## Target Structure
After migration, your project should have this structure:

```
your-project/
├── CLAUDE.md                  # Project-specific build and test commands
├── docs/                      # General project documentation
│   ├── api-docs.md            # API documentation
│   ├── architecture.md        # System architecture
│   ├── codebase.md            # Code style and patterns
│   ├── domain.md              # Domain concepts
│   ├── setup.md               # Environment setup instructions
│   └── testing.md             # Testing strategy
├── planning/                  # Planning directory
│   ├── templates/             # Feature-specific templates
│   │   ├── feature.md         # Feature description template
│   │   ├── tasks.md           # Detailed development tasks template
│   │   └── to-do.md           # Task checklist template
│   └── [branch-name]/         # Mirrors your git branch structure
│       ├── feature.md         # Feature description
│       ├── tasks.md           # Detailed development tasks
│       └── to-do.md           # Task checklist
│
│   Example branch structures:
│   └── feature/
│       └── new-feature/       # For branch "feature/new-feature"
│   └── fix/
│       └── bug-123/           # For branch "fix/bug-123"
│   └── main/                  # For branch "main" (if needed)
```

## Key Changes
1. **No more planning/main folder** - General documentation now lives in `docs/`
2. **Branch name mirroring** - The directory structure under `planning/` mirrors your git branch names exactly
   - If your branch is `feature/new-feature`, docs go in `planning/feature/new-feature/`
   - If your branch is `fix/bug-123`, docs go in `planning/fix/bug-123/`
   - The word "feature" is NOT a special directory - it's just part of branch names like `feature/something`
3. **Feature-specific docs only** - Only `feature.md`, `tasks.md`, and `to-do.md` belong in `planning/[branch-name]/`
4. **Everything else goes to docs/** - Files like `codebase.md`, `domain.md`, `api-docs.md`, `architecture.md`, `setup.md`, and `testing.md` should be in the `docs/` directory

## Migration Steps

1. **Create the docs directory if it doesn't exist**
   ```bash
   mkdir -p docs
   ```

2. **Review current documentation structure**
   - Look through all folders under `planning/`
   - Identify which documents are general project documentation vs feature-specific

3. **Move general documentation to docs/**
   - Documents that describe the overall project (not specific to one feature) should be moved to `docs/`
   - Common files to move: `codebase.md`, `domain.md`, `api-docs.md`, `architecture.md`, `setup.md`, `testing.md`
   - Example: If you find `planning/main/codebase.md`, move it to `docs/codebase.md`

4. **Keep feature-specific docs in place**
   - Files in branch directories (like `planning/feature/new-feature/` or `planning/fix/bug-123/`) that are named `feature.md`, `tasks.md`, or `to-do.md` should stay where they are
   - Remember: the directory path mirrors the git branch name - `feature` is not a special folder, it's part of branch names
   - Any other files in branch folders should be evaluated - if they're general docs, move them to `docs/`

5. **Update CLAUDE.md**
   - The file tree diagram in CLAUDE.md needs to be updated to reflect the new structure
   - Update any references to old paths

6. **Clean up empty directories**
   - Remove `planning/main/` if it exists and is empty
   - Remove any other empty directories

## Verification
After migration, verify:
- [ ] `docs/` directory exists and contains general project documentation
- [ ] `planning/templates/` contains only feature-specific templates
- [ ] No `planning/main/` directory exists
- [ ] Feature branches only contain `feature.md`, `tasks.md`, and `to-do.md`
- [ ] CLAUDE.md has been updated with the new structure

## Note
The latest templates have already been placed in the correct locations. Your task is to reorganize the existing documentation to match this new structure.