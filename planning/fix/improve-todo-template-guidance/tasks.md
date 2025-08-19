# Development Tasks

## Task 1: Update to-do.md Template

### Description
Update the to-do.md template to provide clear instructions that it should map 1:1 to tasks in tasks.md, not create detailed breakdowns.

### Acceptance Criteria
- Template includes clear instructions about 1:1 mapping
- Template shows example of correct vs incorrect format
- Template prevents AI assistants from creating detailed sub-tasks

### Implementation Notes
- Add prominent instructions at the top of the template
- Include concrete examples of what to do and what not to do
- Keep the template simple and focused

### Estimated Effort
Small (30 minutes)

## Task 2: Update Agent Instructions Template

### Description
Update the agent_instructions.md template to be more explicit about the relationship between tasks.md and to-do.md files.

### Acceptance Criteria
- Development workflow section clearly explains file relationship
- Instructions specify that to-do.md is a simple checklist
- Guidance prevents confusion about template purposes

### Implementation Notes
- Add explanation of file relationship to development workflow
- Clarify that tasks.md has details, to-do.md has simple checkboxes
- Keep instructions concise but clear

### Estimated Effort
Small (30 minutes)

## Task 3: Test Template Improvements

### Description
Validate that the updated templates guide AI assistants toward correct behavior by testing the template generation.

### Acceptance Criteria
- AI assistant creates simple 1:1 mapping in to-do.md when given updated templates
- No detailed breakdowns are created in to-do.md
- Workflow guidance is clear and followable

### Implementation Notes
- Test by creating a new feature branch and using claude-workflow new
- Have AI assistant fill out templates following the guidance
- Verify the output matches intended format

### Estimated Effort
Small (30 minutes)
