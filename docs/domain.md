# Domain Concepts

## Core Terminology

- **AI-First Development**: Development workflows where AI coding assistants (Claude, Amazon Q, Cline, etc.) are the primary code writers, with humans providing guidance and review
- **AI Context Problem**: The challenge that AI assistants face when working on codebases without sufficient context about domain concepts, architectural decisions, and coding patterns
- **Branch-Based Documentation**: Documentation structure that mirrors git branch workflow, with planning docs organized by branch name (e.g., `planning/feature/auth/`)
- **Template-Driven Workflow**: Using standardized markdown templates to capture the context AI assistants need to work effectively
- **Meta-Tool**: A tool designed to help other tools work better - in this case, helping AI assistants work more effectively on software projects
- **Dog-Fooding**: Using your own tool to develop itself, validating that it works for real projects
- **Agent Instructions**: Markdown files (CLAUDE.md, AmazonQ.md) that provide AI assistants with project-specific context and commands

## Business Rules

### Framework Initialization
- Projects must be git repositories (or user must confirm to proceed)
- Only one agent instruction file per project (CLAUDE.md OR AmazonQ.md, not both)
- Template files are copied to appropriate locations: general docs to `docs/`, feature-specific to `planning/templates/`
- Branch-specific documentation mirrors exact git branch names

### Template System
- All templates use `.md` (Markdown) format for AI assistant readability
- Placeholder substitution uses `{{VARIABLE}}` syntax
- Templates are bundled with the package and accessed via `importlib.resources`
- Template content should be optimized for AI assistant consumption, not human presentation

### Documentation Organization
- **General Documentation** (`docs/`): Project-wide information that applies across all features
- **Feature Planning** (`planning/templates/`): Templates for feature-specific documentation
- **Branch Planning** (`planning/[branch-name]/`): Actual planning docs for specific features/branches

## User Roles

- **Framework User**: Developer who installs and uses the Claude Workflow Framework on their projects
  - Responsibilities: Initialize framework, fill out templates, follow workflow
  - Permissions: Can customize templates, create branch documentation
  
- **AI Assistant**: Claude, Amazon Q, Cline, or other coding assistant working on a project
  - Responsibilities: Read documentation, follow patterns, implement features systematically
  - Permissions: Access to all project documentation, can suggest updates to templates

- **Framework Developer**: Developer working on the Claude Workflow Framework itself
  - Responsibilities: Maintain CLI tool, update templates, ensure cross-AI compatibility
  - Permissions: Modify core framework code, update template system

## Process Flows

### 1. Project Initialization Flow
1. User runs `claude-workflow init [directory] [--amazonq]`
2. System validates target directory exists and is a git repository
3. System creates directory structure (`docs/`, `planning/templates/`)
4. System copies appropriate agent instruction file (CLAUDE.md or AmazonQ.md)
5. System copies template files to correct locations
6. User receives next steps guidance

### 2. Feature Development Flow
1. Developer creates feature branch: `git checkout -b feature/new-feature`
2. Developer runs `claude-workflow new` to create branch-specific documentation
3. AI assistant analyzes templates and asks clarifying questions
4. Developer and AI assistant collaborate to fill out feature planning docs
5. Development proceeds using systematic task-by-task approach
6. Documentation is updated as implementation progresses

### 3. Template Substitution Flow
1. CLI reads unified template file (`agent_instructions.md`)
2. System determines target agent (Claude or Amazon Q) based on flags
3. System replaces `{{FILENAME}}` with appropriate filename
4. System replaces `{{AGENT_NAME}}` with appropriate agent name
5. System writes processed content to target file

## Domain Models

### Project Structure
- **Root Directory**: Contains agent instruction file and main project code
- **Docs Directory**: General project documentation (architecture, domain, codebase, etc.)
- **Planning Directory**: Contains templates and branch-specific planning docs
- **Templates Directory**: Template files that get copied for new features

### CLI Command Structure
- **Init Command**: One-time project setup with optional agent selection
- **New Command**: Branch-specific documentation creation
- **Update Command**: Framework version updates and migrations

### Template Categories
- **Agent Instructions**: Project-specific guidance for AI assistants
- **General Documentation**: Cross-cutting project information
- **Feature Planning**: Task breakdown and feature-specific requirements

## Key Constraints

### Technical Constraints
- Must work with git repositories (branch-based organization)
- Templates must be readable by multiple AI assistant types
- CLI must be cross-platform compatible
- Package must be installable via pip

### Workflow Constraints
- Documentation structure must mirror git branch structure
- AI assistants should work on one task at a time
- All changes should be tested before moving to next task
- Documentation must be kept up-to-date with code changes

### Design Philosophy
- **Minimal Setup**: Framework should be easy to adopt
- **Maximum Context**: Capture all information AI assistants need
- **Systematic Development**: Encourage methodical, test-driven development
- **AI-Agnostic**: Work with multiple AI assistant types
