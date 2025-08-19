"""
Shared pytest fixtures and configuration for Claude Workflow Framework tests.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory that gets cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def temp_git_repo(temp_dir: Path) -> Path:
    """Create a temporary git repository for testing."""
    git_dir = temp_dir / ".git"
    git_dir.mkdir()
    
    # Create a minimal git config to avoid warnings
    config_dir = git_dir / "config"
    config_dir.write_text("""[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
""")
    
    return temp_dir


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
    
    # Create sample template files
    (templates_dir / "agent_instructions.md").write_text(sample_template_content)
    (templates_dir / "feature.md").write_text("# Feature Template\n\n## Overview\n[Description]")
    (templates_dir / "tasks.md").write_text("# Tasks Template\n\n## Task 1: [Name]\n[Description]")
    (templates_dir / "to-do.md").write_text("# To-Do Template\n\n- [ ] Task 1: [Name]")
    
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


@pytest.fixture(autouse=True)
def isolate_tests(monkeypatch):
    """Ensure tests don't interfere with each other or the real system."""
    # Change to a temporary directory for each test
    original_cwd = os.getcwd()
    
    def cleanup():
        os.chdir(original_cwd)
    
    # Register cleanup
    import atexit
    atexit.register(cleanup)


# Pytest markers for organizing tests
pytest_plugins = []
