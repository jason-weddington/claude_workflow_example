"""
Shared pytest fixtures and configuration for Claude Workflow Framework tests.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Generator, Dict, Any

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory that gets cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def temp_git_repo(temp_dir: Path) -> Path:
    """Create a temporary git repository for testing."""
    # Initialize git repository
    subprocess.run(['git', 'init'], cwd=temp_dir, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=temp_dir, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=temp_dir, capture_output=True)
    
    # Create initial commit
    readme = temp_dir / "README.md"
    readme.write_text("# Test Repository")
    subprocess.run(['git', 'add', 'README.md'], cwd=temp_dir, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=temp_dir, capture_output=True)
    
    return temp_dir


@pytest.fixture
def temp_git_repo_with_branch(temp_git_repo: Path) -> Dict[str, Any]:
    """Create a git repository with a feature branch."""
    # Create and checkout feature branch
    subprocess.run(['git', 'checkout', '-b', 'feature/test-feature'], cwd=temp_git_repo, capture_output=True)
    
    return {
        'repo_path': temp_git_repo,
        'branch_name': 'feature/test-feature',
        'main_branch': 'main'
    }


@pytest.fixture
def sample_template_content() -> str:
    """Sample template content with placeholders for testing."""
    return """# {{FILENAME}} Project Template

## Build and Test Commands
```
# Add your project's build and test commands here
```

## Project Structure
```
your-project/
├── {{FILENAME}}               # Project-specific build and test commands
├── docs/                      # General project documentation
```

## Development Workflow
- Tell {{AGENT_NAME}} to read the planning documents
"""


@pytest.fixture
def sample_templates_dir(temp_dir: Path, sample_template_content: str) -> Path:
    """Create a directory with sample template files for testing."""
    templates_dir = temp_dir / "templates"
    templates_dir.mkdir()
    
    # Create sample template files that the CLI expects
    (templates_dir / "agent_instructions.md").write_text(sample_template_content)
    
    # Feature-specific templates
    (templates_dir / "feature.md").write_text("""# Feature Template

## Overview
[Description of the feature being built.]

## Business Goals
- Goal 1
- Goal 2

## User Stories
- As a [user type], I want to [action] so that [benefit]
""")
    (templates_dir / "tasks.md").write_text("""# Development Tasks

## Task 1: [Task Name]

### Description
Detailed description of the task.

### Acceptance Criteria
- Criterion 1
- Criterion 2

### Implementation Notes
- Note 1
- Note 2

### Estimated Effort
[Small/Medium/Large]
""")
    (templates_dir / "to-do.md").write_text("""# To-Do List

**IMPORTANT**: This file should contain a simple checklist that maps 1:1 to the tasks in tasks.md.

## Tasks from tasks.md

- [ ] Task 1: [Copy exact title from "Task 1" in tasks.md]
- [ ] Task 2: [Copy exact title from "Task 2" in tasks.md]
""")
    
    # General documentation templates
    (templates_dir / "api-docs.md").write_text("# API Documentation\n\n[API documentation content]")
    (templates_dir / "architecture.md").write_text("# Architecture\n\n[Architecture documentation]")
    (templates_dir / "codebase.md").write_text("# Codebase\n\n[Codebase documentation]")
    (templates_dir / "domain.md").write_text("# Domain\n\n[Domain documentation]")
    (templates_dir / "setup.md").write_text("# Setup\n\n[Setup documentation]")
    (templates_dir / "testing.md").write_text("# Testing\n\n[Testing documentation]")
    
    # Add new_project.py that CLI expects to copy
    (templates_dir.parent / "new_project.py").write_text("""#!/usr/bin/env python
# Test new_project.py file
print("Test new project script")
""")
    
    return templates_dir


@pytest.fixture
def mock_package_resources(monkeypatch, sample_templates_dir: Path):
    """Mock importlib.resources to return our test templates."""
    def mock_files(package):
        if package == 'claude_workflow':
            return sample_templates_dir.parent
        raise ImportError(f"No module named {package}")
    
    # Mock the importlib.resources.files function
    import importlib.resources as pkg_resources
    monkeypatch.setattr(pkg_resources, 'files', mock_files)
    
    return sample_templates_dir


# Utility functions for tests
def compare_file_contents(file1: Path, file2: Path) -> bool:
    """Compare contents of two files, ignoring whitespace differences."""
    if not file1.exists() or not file2.exists():
        return False
    
    content1 = file1.read_text().strip()
    content2 = file2.read_text().strip()
    return content1 == content2


def compare_directory_structure(dir1: Path, dir2: Path, ignore_files: set = None) -> bool:
    """Compare directory structures, optionally ignoring certain files."""
    if ignore_files is None:
        ignore_files = {'.DS_Store', '__pycache__', '.pytest_cache'}
    
    def get_structure(path: Path) -> set:
        structure = set()
        for item in path.rglob('*'):
            if item.name not in ignore_files:
                rel_path = item.relative_to(path)
                structure.add(str(rel_path))
        return structure
    
    return get_structure(dir1) == get_structure(dir2)


def create_mock_git_repo(path: Path, branch_name: str = 'main') -> Path:
    """Create a mock git repository without actually running git commands."""
    git_dir = path / '.git'
    git_dir.mkdir(parents=True, exist_ok=True)
    
    # Create minimal git structure
    (git_dir / 'HEAD').write_text(f'ref: refs/heads/{branch_name}\n')
    refs_heads = git_dir / 'refs' / 'heads'
    refs_heads.mkdir(parents=True, exist_ok=True)
    (refs_heads / branch_name).write_text('fake-commit-hash\n')
    
    return path


@pytest.fixture
def mock_git_repo(temp_dir: Path) -> Path:
    """Create a mock git repository for testing without git dependencies."""
    return create_mock_git_repo(temp_dir)


@pytest.fixture
def mock_git_repo_with_branch(temp_dir: Path) -> Dict[str, Any]:
    """Create a mock git repository with a specific branch."""
    branch_name = 'feature/test-branch'
    repo_path = create_mock_git_repo(temp_dir, branch_name)
    
    return {
        'repo_path': repo_path,
        'branch_name': branch_name,
        'main_branch': 'main'
    }


@pytest.fixture(autouse=True)
def isolate_tests(monkeypatch):
    """Ensure tests don't interfere with each other or the real system."""
    # Store original working directory
    original_cwd = os.getcwd()
    
    def restore_cwd():
        os.chdir(original_cwd)
    
    # Register cleanup
    import atexit
    atexit.register(restore_cwd)


# Make utility functions available to tests
@pytest.fixture
def file_utils():
    """Provide file utility functions to tests."""
    return {
        'compare_file_contents': compare_file_contents,
        'compare_directory_structure': compare_directory_structure,
        'create_mock_git_repo': create_mock_git_repo,
    }


# Pytest markers for organizing tests
pytest_plugins = []
