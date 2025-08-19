# Testing Strategy

## Current Testing Approach

The Claude Workflow Framework currently uses **manual testing** with a systematic approach for validating functionality.

### Manual Testing Workflow

1. **Create Test Environment**:
   ```bash
   mkdir /tmp/test_project && cd /tmp/test_project
   git init
   ```

2. **Test Init Command**:
   ```bash
   # Test default (Claude) initialization
   claude-workflow init .
   
   # Verify CLAUDE.md was created with correct content
   cat CLAUDE.md
   
   # Test Amazon Q initialization
   rm -rf docs planning CLAUDE.md
   claude-workflow init . --amazonq
   
   # Verify AmazonQ.md was created with correct content
   cat AmazonQ.md
   ```

3. **Test New Command**:
   ```bash
   # Create feature branch
   git checkout -b feature/test-feature
   
   # Test branch-specific documentation creation
   claude-workflow new
   
   # Verify directory structure
   ls -la planning/feature/test-feature/
   ```

4. **Verify Template Substitution**:
   - Check that `{{FILENAME}}` is replaced correctly
   - Check that `{{AGENT_NAME}}` is replaced correctly
   - Verify project structure references match the agent type

5. **Clean Up**:
   ```bash
   cd / && rm -rf /tmp/test_project
   ```

## Test Environments

### Development Testing
- **Environment**: Local development machine with temporary directories
- **Purpose**: Validate changes during development
- **Scope**: CLI functionality, template generation, file operations

### Integration Testing
- **Environment**: Fresh git repositories with various branch structures
- **Purpose**: Ensure git integration works correctly
- **Scope**: Branch detection, directory creation, cross-platform compatibility

## Test Coverage Areas

### Core Functionality
- ✅ CLI command parsing and routing
- ✅ Template substitution ({{FILENAME}}, {{AGENT_NAME}})
- ✅ File and directory creation
- ✅ Git repository detection and validation
- ✅ Branch-based directory structure creation

### Edge Cases
- ✅ Non-git directories (warning and confirmation)
- ✅ Existing files (overwrite behavior)
- ✅ Complex branch names (feature/sub/branch)
- ✅ Permission issues (handled gracefully)

### Cross-Platform Testing
- ✅ macOS (primary development platform)
- ⚠️ Linux (manual testing needed)
- ⚠️ Windows (manual testing needed)

## Future Testing Strategy

### Automated Testing Goals

**Unit Tests** (Priority: High):
```python
# Example test structure
def test_template_substitution():
    """Test that placeholders are correctly replaced."""
    
def test_cli_argument_parsing():
    """Test that CLI arguments are parsed correctly."""
    
def test_directory_creation():
    """Test that directory structures are created correctly."""
```

**Integration Tests** (Priority: Medium):
```python
def test_full_init_workflow():
    """Test complete init command workflow."""
    
def test_branch_based_documentation():
    """Test new command with various branch names."""
```

**End-to-End Tests** (Priority: Low):
```python
def test_complete_user_workflow():
    """Test full user workflow from init to feature development."""
```

### Testing Framework Recommendations

**pytest** - Recommended testing framework:
```bash
pip install pytest pytest-cov
```

**Test Structure**:
```
tests/
├── unit/
│   ├── test_cli.py
│   ├── test_template_engine.py
│   └── test_file_operations.py
├── integration/
│   ├── test_init_command.py
│   └── test_new_command.py
└── fixtures/
    ├── sample_templates/
    └── test_repositories/
```

### Test Data Strategy

**Template Fixtures**:
- Sample template files for testing substitution
- Expected output files for comparison
- Various branch name scenarios

**Repository Fixtures**:
- Temporary git repositories with different structures
- Pre-configured branch scenarios
- Edge case repository states

## Testing Best Practices

### For Manual Testing
1. **Always use temporary directories** to avoid polluting development environment
2. **Test both agent variants** (Claude and Amazon Q) for each change
3. **Verify file contents**, not just file existence
4. **Test error conditions** (non-git repos, permission issues)
5. **Clean up test artifacts** after each test run

### For Future Automated Testing
1. **Use temporary directories** with proper cleanup
2. **Mock file system operations** where appropriate
3. **Test template content**, not just structure
4. **Include cross-platform path handling** tests
5. **Test CLI exit codes** and error messages

## Continuous Integration

### Future CI/CD Pipeline
```yaml
# Example GitHub Actions workflow
name: Test Claude Workflow
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.6, 3.7, 3.8, 3.9, 3.10, 3.11]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install -e .
      - name: Run tests
        run: pytest tests/
```

## Quality Metrics

### Current Status
- **Manual Test Coverage**: ~80% of core functionality
- **Automated Test Coverage**: 0% (no automated tests yet)
- **Platform Coverage**: macOS only

### Goals
- **Automated Test Coverage**: 90%+ of core functionality
- **Platform Coverage**: macOS, Linux, Windows
- **Python Version Coverage**: 3.6 through 3.11
