# Claude Workflow Framework - Improve To-Do Template Guidance

## Overview

Fix the framework templates to provide clearer guidance to AI assistants about the intended relationship between tasks.md and to-do.md. Currently, AI assistants create detailed breakdowns in to-do.md instead of simple 1:1 task mappings.

## Business Goals

- **Clear Framework Guidance**: Ensure AI assistants understand the intended workflow
- **Consistent Usage**: Prevent confusion about template purposes
- **Better User Experience**: Users get the intended simple checklist format

## User Stories

- **As an AI assistant**, I want clear template guidance so that I create the correct format for to-do.md
- **As a framework user**, I want a simple checklist in to-do.md that maps directly to my detailed tasks
- **As a framework developer**, I want templates that guide AI assistants toward correct behavior

## Acceptance Criteria

- ✅ to-do.md template clearly indicates 1:1 mapping to tasks.md
- ✅ Agent instructions template explains the relationship between files
- ✅ Template guidance prevents AI assistants from creating detailed breakdowns in to-do.md
- ✅ Examples show the correct simple checklist format

## Technical Requirements

### Template Updates
- Update `claude_workflow/templates/to-do.md` with clear instructions
- Update `claude_workflow/templates/agent_instructions.md` with better workflow explanation
- Add examples showing correct vs incorrect usage

### Validation
- Test with AI assistant to ensure guidance works
- Verify templates produce intended behavior

## Implementation Strategy

1. **Analyze Current Issue**: Review how AI assistants misinterpret current templates
2. **Update to-do.md Template**: Add clear instructions about 1:1 mapping
3. **Update Agent Instructions**: Clarify workflow relationship between files
4. **Test Guidance**: Validate that updated templates produce correct behavior

## Timeline

- **Start Date**: Current
- **Target Completion**: Same day (small fix)
