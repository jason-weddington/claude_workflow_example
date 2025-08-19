# Testing Strategy

## Current Testing Approach

The Claude Workflow Framework uses **automated testing** with pytest as the primary testing framework.

### Testing Framework

**pytest** with comprehensive test coverage:
```bash
pip install -e ".[dev]"  # Install with test dependencies
pytest                   # Run all tests
pytest --cov=claude_workflow --cov-report=term-missing  # With coverage
```

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests for individual functions
│   ├── test_cli.py          # CLI argument parsing and routing
│   ├── test_template_engine.py  # Template substitution logic
│   ├── test_file_operations.py  # File and directory operations
│   ├── test_git_integration.py  # Git repository detection and branch parsing
│   └── test_error_handling.py   # Error handling and edge cases
├── integration/             # Integration tests for complete workflows
│   ├── test_init_command.py     # Full init command testing
│   └── test_new_command.py      # Full new command testing
└── fixtures/                # Test data and fixtures
```

## Test Coverage Areas

### Core Functionality ✅
- CLI command parsing and routing
- Template substitution ({{FILENAME}}, {{AGENT_NAME}})
- File and directory creation
- Git repository detection and validation
- Branch-based directory structure creation

### Edge Cases ✅
- Non-git directories (warning and confirmation)
- Existing files (overwrite behavior)
- Complex branch names (feature/sub/branch)
- Permission issues (handled gracefully)
- Error conditions and resource cleanup

### Cross-Platform Testing ✅
- macOS (primary development platform)
- Path handling (absolute vs relative)
- Unicode content and filenames
- File permissions and error handling

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- **CLI Module**: Argument parsing, command routing, error handling
- **Template Engine**: Placeholder substitution, content processing
- **File Operations**: Directory creation, file copying, permission handling
- **Git Integration**: Repository detection, branch parsing, error handling
- **Error Handling**: Exception handling, edge cases, resource cleanup

### Integration Tests (`@pytest.mark.integration`)
- **Init Command**: Complete initialization workflow (Claude and Amazon Q variants)
- **New Command**: Branch-specific documentation creation workflow
- **Error Scenarios**: End-to-end error handling and recovery
- **Real-World Scenarios**: Unicode paths, existing files, complex branch names

## Test Fixtures and Utilities

### Available Fixtures
- `temp_dir`: Temporary directory with automatic cleanup
- `temp_git_repo`: Temporary git repository for testing
- `sample_template_content`: Template content with placeholders
- `sample_templates_dir`: Directory with sample template files
- `mock_package_resources`: Mock for testing template access
- `file_utils`: File utility functions for tests

### Utility Functions
- `compare_file_contents()`: Compare file contents ignoring whitespace
- `compare_directory_structure()`: Compare directory structures
- `create_mock_git_repo()`: Create mock git repository without git dependencies

## Running Tests

### Basic Commands
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only

# Run specific test files
pytest tests/unit/test_cli.py
pytest tests/integration/test_init_command.py
```

### Coverage Analysis
```bash
# Run with coverage report
pytest --cov=claude_workflow --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=claude_workflow --cov-report=html
# View: open htmlcov/index.html

# Fail if coverage below threshold
pytest --cov=claude_workflow --cov-fail-under=80
```

### Advanced Options
```bash
# Run only failed tests from last run
pytest --lf

# Stop on first failure
pytest -x

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto

# Debug mode (drop into debugger on failure)
pytest --pdb
```

## Quality Metrics

### Current Status ✅
- **Automated Test Coverage**: 80%+ of core functionality
- **Test Categories**: Unit tests, integration tests, error handling tests
- **Platform Coverage**: macOS (primary), cross-platform path handling
- **Test Performance**: Complete test suite runs in under 2 minutes

### Test Quality Standards
- **Independent Tests**: Each test runs independently
- **Deterministic Results**: Tests produce consistent results
- **Fast Execution**: Unit tests complete in under 1 second each
- **Clear Assertions**: Specific assertions with helpful error messages
- **Proper Cleanup**: Temporary resources are cleaned up automatically

## Development Workflow Integration

### Pre-Commit Testing
```bash
# Quick test run for development
pytest -m unit  # Fast unit tests only

# Full test suite before commits
pytest --cov=claude_workflow --cov-fail-under=80
```

### Test-Driven Development
1. **Write failing test** for new functionality
2. **Implement minimal code** to make test pass
3. **Refactor** while keeping tests green
4. **Add edge case tests** for robustness

### Adding New Tests
1. **Follow naming conventions**: `test_*.py`, `Test*` classes, `test_*` functions
2. **Use appropriate fixtures**: Leverage existing fixtures for common setup
3. **Test both success and failure paths**: Include error condition testing
4. **Update documentation**: Add new test patterns to guidelines

## Continuous Integration Ready

The testing framework is designed for CI/CD integration:

### CI Configuration Example
```yaml
# Example GitHub Actions workflow
name: Test Claude Workflow
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.6, 3.7, 3.8, 3.9, 3.10, 3.11]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install -e ".[dev]"
      - name: Run tests
        run: pytest --cov=claude_workflow --cov-fail-under=80
```

### Local CI Simulation
```bash
# Run the same checks that CI would run
pytest --cov=claude_workflow --cov-fail-under=80
pytest -m "not slow"  # Skip slow tests for faster feedback
```

## Testing Documentation

For comprehensive testing guidelines, see [TESTING.md](../TESTING.md), which includes:

- Detailed test writing guidelines
- Mocking strategies and examples
- Debugging techniques
- Performance testing approaches
- Best practices and troubleshooting

## Future Enhancements

### Planned Improvements
- **Property-Based Testing**: Add hypothesis-based testing for edge cases
- **Performance Benchmarking**: Add performance regression testing
- **Cross-Platform CI**: Automated testing on Windows and Linux
- **Mutation Testing**: Validate test quality with mutation testing

### Test Maintenance
- **Regular Review**: Periodic review of test coverage and quality
- **Refactoring**: Keep test code clean and maintainable
- **Documentation Updates**: Keep testing documentation current
- **Tool Updates**: Stay current with pytest and testing tool updates
