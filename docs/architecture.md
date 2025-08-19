# System Architecture

## High-Level Design

The Claude Workflow Framework is a command-line tool that generates documentation structures for AI-first development workflows. It follows a simple template-based architecture with git integration.

```
User Project Repository
├── Agent Instructions (CLAUDE.md or AmazonQ.md)
├── docs/ (General Documentation)
├── planning/ (Feature Planning)
└── [existing project code]

Claude Workflow Package
├── CLI Interface (argparse-based)
├── Template Engine (placeholder substitution)
├── Git Integration (branch-aware)
└── Template Library (bundled .md files)
```

## Component Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   CLI Router     │───▶│  Command Logic  │
│ (init/new/etc.) │    │   (argparse)     │    │ (create/new/etc)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  File System    │◀───│ Template Engine  │◀───│ Template Library│
│   Operations    │    │ (substitution)   │    │ (bundled .md)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                                               ▲
         ▼                                               │
┌─────────────────┐    ┌──────────────────┐            │
│   Git Repo      │───▶│ Branch Detection │────────────┘
│  Integration    │    │   & Validation   │
└─────────────────┘    └──────────────────┘
```

## Data Flow

### 1. Initialization Flow (`claude-workflow init`)
1. User runs init command with target directory and optional `--amazonq` flag
2. CLI validates target directory exists and contains `.git` folder
3. System determines agent type (Claude or Amazon Q) and sets template variables
4. Template engine reads `agent_instructions.md` and substitutes placeholders
5. File system operations create directory structure and copy template files
6. User receives success message with next steps

### 2. New Project Flow (`claude-workflow new`)
1. User runs new command from within a git repository
2. System detects current git branch name
3. Planning directory structure is created mirroring branch name
4. Feature-specific templates are copied to branch directory
5. User can begin filling out feature planning documentation

### 3. Template Processing Flow
1. CLI accesses bundled templates via `importlib.resources`
2. Template content is read into memory
3. Placeholder substitution occurs (`{{FILENAME}}`, `{{AGENT_NAME}}`)
4. Processed content is written to target location
5. File permissions are set appropriately (executable for scripts)

## Key Components

### CLI Router (`cli.py`)
- **Purpose**: Entry point and command routing using argparse
- **Interfaces**: Command-line arguments, subcommand dispatch
- **Dependencies**: argparse, pathlib, importlib.resources

### Template Engine
- **Purpose**: Process template files with placeholder substitution
- **Interfaces**: Template files in, processed content out
- **Dependencies**: String replacement, file I/O operations

### File System Manager
- **Purpose**: Create directories, copy files, set permissions
- **Interfaces**: pathlib.Path operations, shutil for file copying
- **Dependencies**: pathlib, shutil, os (for permissions)

### Git Integration
- **Purpose**: Detect git repositories, extract branch names
- **Interfaces**: File system checks for `.git`, git command integration
- **Dependencies**: pathlib for `.git` detection, subprocess for git commands

### Template Library
- **Purpose**: Bundled markdown templates for different documentation types
- **Interfaces**: Package resource access via importlib.resources
- **Dependencies**: Package data configuration in pyproject.toml

## Design Principles

### Simplicity
- Single-purpose tool with minimal dependencies
- Clear command structure with intuitive subcommands
- Template-based approach avoids complex logic

### Git Integration
- Leverages existing git workflow patterns
- Branch-based organization mirrors developer mental model
- No custom version control - works with existing git practices

### AI-First Design
- Templates optimized for AI assistant consumption
- Structured documentation that provides context AI assistants need
- Support for multiple AI assistant types through template substitution

### Extensibility
- Template system allows easy addition of new documentation types
- CLI structure supports adding new commands
- Package data approach enables template updates through package updates
