# Testing Guide for Claude Workflow Framework

## Overview

This document provides comprehensive guidelines for testing the Claude Workflow Framework. The testing strategy includes unit tests, integration tests, and guidelines for adding new tests.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests for individual components
│   ├── test_cli.py          # CLI argument parsing and routing
│   ├── test_template_engine.py  # Template substitution logic
│   ├── test_file_operations.py  # File and directory operations
│   ├── test_git_integration.py  # Git repository detection and branch parsing
│   └── test_error_handling.py   # Error handling and edge cases
├── integration/             # Integration tests for complete workflows
│   ├── test_init_command.py     # Full init command testing
│   └── test_new_command.py      # Full new command testing
└── fixtures/                # Test data and fixtures (currently empty)
```

## Running Tests

### Prerequisites

Ensure you have the development environment set up:

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with development dependencies
pip install --upgrade pip
pip install -e ".[dev]"
```

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=claude_workflow --cov-report=term-missing

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only

# Run specific test files
pytest tests/unit/test_cli.py
pytest tests/integration/test_init_command.py

# Run specific test functions
pytest tests/unit/test_cli.py::TestArgumentParsing::test_init_subcommand_parsing
```

### Advanced Test Options

```bash
# Run tests with HTML coverage report
pytest --cov=claude_workflow --cov-report=html
# View report: open htmlcov/index.html

# Run tests in parallel (if pytest-xdist is installed)
pytest -n auto

# Run only failed tests from last run
pytest --lf

# Run tests and stop on first failure
pytest -x

# Run tests with detailed output for debugging
pytest -s -vv
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)

Unit tests focus on individual functions and components in isolation:

- **CLI Module**: Argument parsing, command routing, error handling
- **Template Engine**: Placeholder substitution, content processing
- **File Operations**: Directory creation, file copying, permission handling
- **Git Integration**: Repository detection, branch parsing, error handling
- **Error Handling**: Exception handling, edge cases, resource cleanup

### Integration Tests (`@pytest.mark.integration`)

Integration tests verify complete workflows:

- **Init Command**: Full initialization workflow for both Claude and Amazon Q variants
- **New Command**: Complete branch-specific documentation creation workflow
- **Error Scenarios**: End-to-end error handling and recovery

## Test Fixtures

### Available Fixtures

The `conftest.py` file provides several reusable fixtures:

#### Basic Fixtures
- `temp_dir`: Temporary directory with automatic cleanup
- `temp_git_repo`: Temporary git repository for testing
- `temp_git_repo_with_branch`: Git repository with a feature branch

#### Template Fixtures
- `sample_template_content`: Template content with placeholders
- `sample_templates_dir`: Directory with sample template files
- `mock_package_resources`: Mock for testing template access

#### Utility Fixtures
- `file_utils`: File utility functions for tests
- `mock_git_repo`: Mock git repository without git dependencies
- `isolate_tests`: Ensures test isolation

### Using Fixtures

```python
def test_example(temp_dir, sample_template_content):
    """Example test using fixtures."""
    # temp_dir is automatically created and cleaned up
    test_file = temp_dir / "test.txt"
    test_file.write_text(sample_template_content)
    
    # Verify template content
    assert "{{FILENAME}}" in test_file.read_text()
```

## Writing New Tests

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*` (e.g., `TestArgumentParsing`)
- Test functions: `test_*` (e.g., `test_init_subcommand_parsing`)

### Test Structure Guidelines

```python
class TestFeatureName:
    """Test description for the feature being tested."""
    
    def test_specific_behavior(self, fixture_if_needed):
        """Test description explaining what is being tested."""
        # Arrange: Set up test data
        test_input = "example input"
        
        # Act: Execute the code being tested
        result = function_under_test(test_input)
        
        # Assert: Verify the results
        assert result == expected_output
        assert some_condition is True
```

### Unit Test Guidelines

1. **Test One Thing**: Each test should verify one specific behavior
2. **Use Descriptive Names**: Test names should clearly describe what is being tested
3. **Mock External Dependencies**: Use mocks for file system, network, or subprocess calls
4. **Test Both Success and Failure**: Include tests for error conditions
5. **Use Fixtures**: Leverage existing fixtures for common test setup

Example unit test:

```python
@patch('claude_workflow.cli.pkg_resources')
def test_create_command_success_claude(self, mock_pkg_resources, temp_dir):
    """Test successful init command for Claude variant."""
    # Setup mocks
    mock_pkg_resources.files.return_value = temp_dir / "templates"
    
    # Create test template
    templates_dir = temp_dir / "templates"
    templates_dir.mkdir()
    (templates_dir / "agent_instructions.md").write_text("# {{FILENAME}}")
    
    # Execute
    args = Mock(directory=str(temp_dir), amazonq=False)
    result = cli.create_command(args)
    
    # Verify
    assert result == 0
    assert (temp_dir / "CLAUDE.md").exists()
```

### Integration Test Guidelines

1. **Test Complete Workflows**: Verify end-to-end functionality
2. **Use Real File Operations**: Avoid mocking file system operations
3. **Test Multiple Scenarios**: Include various branch types, error conditions
4. **Verify Side Effects**: Check that files are created with correct content
5. **Clean Up**: Use temporary directories that are automatically cleaned up

Example integration test:

```python
@pytest.mark.integration
def test_init_command_complete_workflow(self, temp_git_repo):
    """Test complete init command workflow."""
    # Setup
    target_dir = temp_git_repo
    
    # Execute complete workflow
    with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
        # ... setup mocks and execute command ...
        result = cli.create_command(args)
    
    # Verify complete results
    assert result == 0
    assert (target_dir / "CLAUDE.md").exists()
    assert (target_dir / "docs").exists()
    assert (target_dir / "planning").exists()
```

## Mocking Guidelines

### When to Mock

- External dependencies (subprocess, file system in unit tests)
- Package resources (importlib.resources)
- User input (input() function)
- Network operations
- Time-dependent operations

### Mocking Examples

```python
# Mock subprocess calls
@patch('subprocess.run')
def test_git_operation(self, mock_run):
    mock_run.return_value = Mock(returncode=0, stdout='main\n')
    # ... test code ...

# Mock file operations
@patch('pathlib.Path.write_text')
def test_file_write_error(self, mock_write):
    mock_write.side_effect = PermissionError("Access denied")
    # ... test code ...

# Mock user input
@patch('claude_workflow.cli.input', return_value='y')
def test_user_confirmation(self, mock_input):
    # ... test code ...
```

## Test Data Management

### Creating Test Data

- Use fixtures for reusable test data
- Create minimal test data that covers the test case
- Use realistic but simple examples
- Avoid hardcoding paths or system-specific values

### Template Test Data

```python
# Good: Minimal template for testing
template_content = "# {{FILENAME}}\n\nAgent: {{AGENT_NAME}}"

# Good: Realistic branch names
branch_names = ['feature/auth', 'fix/bug-123', 'main']

# Avoid: Overly complex test data
# complex_template = "..." # 1000 lines of template content
```

## Performance Testing

### Guidelines for Performance Tests

- Mark slow tests with `@pytest.mark.slow`
- Test with reasonable data sizes (not production scale)
- Focus on algorithmic performance, not hardware limits
- Use timeouts for tests that might hang

```python
@pytest.mark.slow
def test_large_template_processing(self, temp_dir):
    """Test processing of large template files."""
    large_content = "# Template\n" + "Content\n" * 1000
    # ... test processing time is reasonable ...
```

## Debugging Tests

### Common Debugging Techniques

```bash
# Run single test with detailed output
pytest tests/unit/test_cli.py::test_specific_function -s -vv

# Add print statements (use -s flag to see output)
def test_debug_example():
    result = function_under_test()
    print(f"Debug: result = {result}")  # Will show with -s flag
    assert result == expected

# Use pytest's built-in debugging
pytest --pdb  # Drop into debugger on failure
pytest --pdb-trace  # Drop into debugger at start of each test
```

### Using Fixtures for Debugging

```python
@pytest.fixture
def debug_temp_dir(tmp_path):
    """Fixture that doesn't clean up for debugging."""
    print(f"Debug: temp directory at {tmp_path}")
    return tmp_path
    # Note: tmp_path is automatically cleaned up, 
    # but you can see the path during test execution
```

## Continuous Integration

### Local CI Simulation

```bash
# Run the same checks that CI would run
pytest --cov=claude_workflow --cov-fail-under=80
pytest -m "not slow"  # Skip slow tests for faster feedback
```

### Coverage Requirements

- Maintain minimum 80% code coverage
- Focus on covering critical paths and error handling
- Exclude test files from coverage calculation
- Review coverage reports to identify untested code

```bash
# Generate coverage report
pytest --cov=claude_workflow --cov-report=html --cov-fail-under=80

# View detailed coverage
open htmlcov/index.html  # macOS
# or browse to htmlcov/index.html
```

## Best Practices

### Test Organization

1. **Group Related Tests**: Use test classes to group related functionality
2. **Logical Test Order**: Arrange tests from simple to complex
3. **Clear Test Documentation**: Include docstrings explaining test purpose
4. **Consistent Naming**: Follow naming conventions throughout

### Test Quality

1. **Independent Tests**: Each test should be able to run independently
2. **Deterministic Results**: Tests should produce consistent results
3. **Fast Execution**: Unit tests should run quickly (< 1 second each)
4. **Clear Assertions**: Use specific assertions with helpful error messages

### Maintenance

1. **Update Tests with Code Changes**: Keep tests in sync with implementation
2. **Refactor Test Code**: Apply same quality standards to test code
3. **Remove Obsolete Tests**: Delete tests for removed functionality
4. **Document Test Changes**: Explain why tests were added or modified

## Troubleshooting Common Issues

### Test Failures

```bash
# Test fails intermittently
# - Check for race conditions
# - Ensure proper test isolation
# - Look for shared state between tests

# Test fails on different platforms
# - Check for platform-specific code paths
# - Use appropriate pytest.mark.skipif decorators
# - Avoid hardcoded paths or system assumptions

# Test is too slow
# - Profile the test to find bottlenecks
# - Use smaller test data
# - Mock expensive operations
# - Consider marking as @pytest.mark.slow
```

### Coverage Issues

```bash
# Coverage lower than expected
# - Check if new code is being tested
# - Look for unreachable code paths
# - Add tests for error conditions
# - Review coverage report for specific lines

# Coverage report inaccurate
# - Ensure test files are excluded from coverage
# - Check coverage configuration in pyproject.toml
# - Verify source paths are correct
```

## Adding New Test Categories

When adding new functionality, consider adding new test categories:

1. **Create new test file** following naming conventions
2. **Add appropriate pytest markers** for test organization
3. **Update this documentation** with new test patterns
4. **Add fixtures** if new test data patterns are needed

Example of adding a new test category:

```python
# tests/unit/test_new_feature.py
import pytest
from claude_workflow import new_feature

@pytest.mark.unit
class TestNewFeature:
    """Tests for new feature functionality."""
    
    def test_new_feature_basic_case(self):
        """Test basic functionality of new feature."""
        # ... test implementation ...
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py documentation](https://coverage.readthedocs.io/)

## Getting Help

If you encounter issues with testing:

1. Check this documentation for common patterns
2. Look at existing tests for examples
3. Review pytest documentation for advanced features
4. Consider asking for help in code reviews
