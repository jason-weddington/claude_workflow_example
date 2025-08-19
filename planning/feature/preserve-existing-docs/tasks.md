# Development Tasks

## Task 1: Analyze Current Behavior

### Description
Examine the current `claude-workflow init` command to understand exactly how it handles the `docs/` directory creation and what happens when a `docs/` directory already exists.

### Acceptance Criteria
- Current code behavior is documented
- Potential issues with existing `docs/` directories are identified
- Code location for docs directory handling is identified

### Implementation Notes
- Look at `claude_workflow/cli.py` in the `create_command` function
- Check how `docs_dir` is created and used
- Identify where template files are copied to docs directory
- Test current behavior with existing docs directory

### Estimated Effort
Small (30 minutes)

---

## Task 2: Modify Docs Directory Creation Logic

### Description
Update the docs directory creation logic to handle existing directories gracefully by checking if the directory exists before creating it.

### Acceptance Criteria
- Code checks if `docs/` directory exists before creating it
- Existing `docs/` directory is preserved if it exists
- New `docs/` directory is created if it doesn't exist
- No errors occur when `docs/` already exists

### Implementation Notes
- Modify the `docs_dir.mkdir(exist_ok=True)` call if needed
- Ensure the logic works for both existing and non-existing directories
- Add appropriate logging/feedback about directory status

### Estimated Effort
Small (15 minutes)

---

## Task 3: Implement Safe Template File Copying

### Description
Modify the template file copying logic to only copy files that don't already exist in the target directory, preserving any existing documentation files.

### Acceptance Criteria
- Template files are only copied if they don't already exist
- Existing files in `docs/` directory are never overwritten
- User receives feedback about which files were added vs. skipped
- All expected template files are available when they don't exist

### Implementation Notes
- Add existence check before copying each template file
- Provide user feedback about skipped files
- Ensure the copy operation is safe and non-destructive
- Consider using a helper function for safe file copying

### Estimated Effort
Medium (1 hour)

---

## Task 4: Add User Feedback and Logging

### Description
Enhance the init command to provide clear feedback to users about what happened with existing vs. new files in the docs directory.

### Acceptance Criteria
- User is informed when existing `docs/` directory is found
- User is told which template files were added
- User is told which template files were skipped (already exist)
- Feedback is clear and helpful

### Implementation Notes
- Add console output for directory status
- List files that were added vs. skipped
- Ensure messages are clear and actionable
- Follow existing CLI output patterns

### Estimated Effort
Small (30 minutes)

---

## Task 5: Write Tests for New Behavior

### Description
Create comprehensive tests to verify that the new docs directory handling works correctly in all scenarios.

### Acceptance Criteria
- Test init with no existing `docs/` directory (current behavior)
- Test init with existing empty `docs/` directory
- Test init with existing `docs/` directory containing files
- Test that existing files are preserved
- Test that new template files are added correctly
- Test user feedback messages

### Implementation Notes
- Add tests to existing test suite
- Use temporary directories for testing
- Mock file operations where appropriate
- Test both success and edge cases

### Estimated Effort
Medium (1-2 hours)

---

## Task 6: Update Documentation

### Description
Update the framework documentation to reflect the new behavior with existing docs directories.

### Acceptance Criteria
- README.md mentions the behavior with existing docs
- TESTING.md includes tests for the new functionality
- Any relevant help text is updated

### Implementation Notes
- Update installation/setup instructions
- Mention the non-destructive behavior
- Include examples of the new behavior
- Update any CLI help text if needed

### Estimated Effort
Small (30 minutes)
