# Development Tasks

## Task 1: Set Up Testing Infrastructure

### Description
Establish the basic pytest testing framework, directory structure, and configuration files needed for automated testing.

### Acceptance Criteria
- pytest and pytest-cov installed as development dependencies
- Test directory structure created (`tests/unit/`, `tests/integration/`, `tests/fixtures/`)
- pytest configuration file (`pytest.ini` or `pyproject.toml` section) created
- Basic test runner working with `pytest` command
- Code coverage reporting configured

### Implementation Notes
- Add pytest dependencies to `pyproject.toml` under `[project.optional-dependencies]`
- Create `tests/conftest.py` for shared fixtures and configuration
- Configure coverage to exclude test files themselves
- Set up pytest to discover tests in the `tests/` directory
- Consider pytest markers for different test types (unit, integration)

### Estimated Effort
Small (2-4 hours)

## Task 2: Create Test Fixtures and Utilities

### Description
Build reusable test fixtures for creating temporary git repositories, template files, and other test data needed across multiple test cases.

### Acceptance Criteria
- Fixture for creating temporary git repositories with various states
- Fixture for creating temporary directories with cleanup
- Fixture for sample template files with known content
- Utility functions for comparing file contents and directory structures
- Mock fixtures for file system operations where needed

### Implementation Notes
- Use `tempfile.TemporaryDirectory` for isolated test environments
- Create git repositories with `git init` in temporary directories
- Include fixtures for different branch scenarios (feature/, fix/, etc.)
- Create sample template files that match the real template structure
- Consider using `pytest-mock` for mocking file operations

### Estimated Effort
Medium (4-6 hours)

## Task 3: Unit Tests for CLI Module

### Description
Write comprehensive unit tests for the CLI argument parsing, command routing, and individual command functions in `cli.py`.

### Acceptance Criteria
- Test argument parsing for all commands (`init`, `new`, `update`)
- Test `--amazonq` flag handling and validation
- Test command routing to appropriate functions
- Test error handling for invalid arguments
- Test help message generation
- Mock file system operations to test logic without side effects

### Implementation Notes
- Use `argparse` testing patterns to validate argument parsing
- Mock `pkg_resources.files` to test template access without real files
- Test both success and error paths for each command
- Verify exit codes are correct (0 for success, 1 for errors)
- Test user confirmation prompts with mocked input

### Estimated Effort
Large (6-8 hours)

## Task 4: Unit Tests for Template Engine

### Description
Test the template substitution logic that replaces placeholders like `{{FILENAME}}` and `{{AGENT_NAME}}` with actual values.

### Acceptance Criteria
- Test placeholder substitution with various input combinations
- Test template reading from package resources
- Test handling of missing placeholders
- Test edge cases (empty templates, malformed placeholders)
- Test file content processing (header removal, line handling)

### Implementation Notes
- Create test templates with known placeholder patterns
- Test both Claude and Amazon Q substitution scenarios
- Verify that H1 headers are properly removed from output
- Test line ending handling across platforms
- Mock `importlib.resources` for controlled template content

### Estimated Effort
Medium (4-6 hours)

## Task 5: Unit Tests for File Operations

### Description
Test file and directory creation, copying, and permission setting operations used throughout the CLI tool.

### Acceptance Criteria
- Test directory creation with `mkdir(parents=True, exist_ok=True)`
- Test file copying from templates to target locations
- Test file permission setting (executable for scripts)
- Test error handling for permission issues
- Test path handling across different operating systems

### Implementation Notes
- Use temporary directories for all file operation tests
- Test both absolute and relative path handling
- Mock permission errors to test error handling
- Verify file contents after copying operations
- Test cleanup and rollback scenarios

### Estimated Effort
Medium (4-6 hours)

## Task 6: Unit Tests for Git Integration

### Description
Test git repository detection, branch name extraction, and git-related validation logic.

### Acceptance Criteria
- Test `.git` directory detection in various scenarios
- Test branch name extraction and parsing
- Test branch-to-directory-path conversion
- Test handling of non-git directories
- Test user confirmation flow for non-git repos

### Implementation Notes
- Create temporary directories with and without `.git` folders
- Mock git command execution where needed
- Test various branch naming patterns (feature/name, fix/bug-123, etc.)
- Mock user input for confirmation prompts
- Test error handling when git operations fail

### Estimated Effort
Medium (4-6 hours)

## Task 7: Integration Tests for Init Command

### Description
Test the complete `claude-workflow init` command workflow from start to finish, including both Claude and Amazon Q variants.

### Acceptance Criteria
- Test successful initialization in git repository
- Test initialization with `--amazonq` flag
- Test file and directory structure creation
- Test template content substitution in generated files
- Test error handling for invalid target directories
- Test user confirmation flow for non-git directories

### Implementation Notes
- Use real temporary git repositories for testing
- Verify complete directory structure matches expectations
- Check file contents for proper placeholder substitution
- Test both interactive and non-interactive scenarios
- Validate that all expected files are created with correct permissions

### Estimated Effort
Large (6-8 hours)

## Task 8: Integration Tests for New Command

### Description
Test the complete `claude-workflow new` command workflow for creating branch-specific documentation.

### Acceptance Criteria
- Test documentation creation for various branch types
- Test directory structure creation based on branch names
- Test template file copying to correct locations
- Test error handling when not in a git repository
- Test behavior with complex branch names

### Implementation Notes
- Create git repositories with different branch scenarios
- Test branch name detection and directory mapping
- Verify template files are copied correctly
- Test edge cases like deeply nested branch names
- Validate file contents and directory structure

### Estimated Effort
Large (6-8 hours)

## Task 9: Error Handling and Edge Case Tests

### Description
Comprehensive testing of error conditions, edge cases, and boundary conditions across all functionality.

### Acceptance Criteria
- Test behavior with invalid file permissions
- Test handling of corrupted or missing template files
- Test behavior with extremely long file paths
- Test handling of special characters in branch names
- Test resource cleanup on failures

### Implementation Notes
- Mock various failure scenarios (disk full, permission denied, etc.)
- Test with unusual but valid input combinations
- Verify proper error messages are displayed to users
- Test cleanup behavior when operations fail partway through
- Validate that partial operations don't leave system in bad state

### Estimated Effort
Medium (4-6 hours)

## Task 10: Test Documentation and Guidelines

### Description
Create comprehensive documentation for the testing framework and guidelines for writing new tests.

### Acceptance Criteria
- Document how to run tests locally
- Document test structure and organization
- Create guidelines for writing new tests
- Document test fixtures and utilities
- Update main project documentation with testing information

### Implementation Notes
- Add testing section to README.md
- Create TESTING.md file with detailed guidelines
- Document pytest configuration and options
- Include examples of good test patterns
- Update docs/testing.md with current testing approach

### Estimated Effort
Small (2-4 hours)
