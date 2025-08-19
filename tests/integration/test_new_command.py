"""
Integration tests for the new command workflow.
"""

import subprocess
from pathlib import Path
from unittest.mock import patch, Mock
import pytest

from claude_workflow import new_project


@pytest.mark.integration
class TestNewCommandIntegration:
    """Integration tests for the complete new command workflow."""
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_feature_branch_complete_workflow(self, mock_run, temp_git_repo):
        """Test complete new command workflow for feature branch."""
        # Setup git repository
        repo_dir = temp_git_repo
        
        # Mock git branch command to return feature branch
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/test-feature\n',
            stderr=''
        )
        
        # Create planning templates directory
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create template files
        template_files = {
            "feature.md": """# Feature Template

## Overview
[Description of the feature being built.]

## Business Goals
- Goal 1
- Goal 2

## User Stories
- As a [user type], I want to [action] so that [benefit]
""",
            "tasks.md": """# Development Tasks

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
""",
            "to-do.md": """# To-Do List

**IMPORTANT**: This file should contain a simple checklist that maps 1:1 to the tasks in tasks.md.

## Tasks from tasks.md

- [ ] Task 1: [Copy exact title from "Task 1" in tasks.md]
- [ ] Task 2: [Copy exact title from "Task 2" in tasks.md]
"""
        }
        
        for filename, content in template_files.items():
            (templates_dir / filename).write_text(content)
        
        # Execute new project command
        result = new_project.create_project_structure()
        
        # Verify success
        assert result == 0
        
        # Verify branch-specific directory was created
        branch_dir = repo_dir / "planning" / "feature" / "test-feature"
        assert branch_dir.exists()
        assert branch_dir.is_dir()
        
        # Verify template files were copied
        assert (branch_dir / "feature.md").exists()
        assert (branch_dir / "tasks.md").exists()
        assert (branch_dir / "to-do.md").exists()
        
        # Verify content was copied correctly
        feature_content = (branch_dir / "feature.md").read_text()
        assert "Feature Template" in feature_content
        assert "Business Goals" in feature_content
        
        tasks_content = (branch_dir / "tasks.md").read_text()
        assert "Development Tasks" in tasks_content
        assert "Task 1: [Task Name]" in tasks_content
        
        todo_content = (branch_dir / "to-do.md").read_text()
        assert "To-Do List" in todo_content
        assert "maps 1:1 to the tasks" in todo_content
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_fix_branch_workflow(self, mock_run, temp_git_repo):
        """Test new command workflow for fix branch."""
        repo_dir = temp_git_repo
        
        # Mock git branch command to return fix branch
        mock_run.return_value = Mock(
            returncode=0,
            stdout='fix/bug-123\n',
            stderr=''
        )
        
        # Create planning templates
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        (templates_dir / "tasks.md").write_text("# Tasks Template")
        (templates_dir / "to-do.md").write_text("# To-Do Template")
        
        # Execute command
        result = new_project.create_project_structure()
        assert result == 0
        
        # Verify fix branch directory structure
        branch_dir = repo_dir / "planning" / "fix" / "bug-123"
        assert branch_dir.exists()
        assert (branch_dir / "feature.md").exists()
        assert (branch_dir / "tasks.md").exists()
        assert (branch_dir / "to-do.md").exists()
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_complex_branch_name(self, mock_run, temp_git_repo):
        """Test new command with complex branch names."""
        repo_dir = temp_git_repo
        
        # Test various complex branch names
        complex_branches = [
            'feature/auth/oauth-integration',
            'fix/ui/button-styling-issue',
            'refactor/database/migration-system'
        ]
        
        for branch_name in complex_branches:
            mock_run.return_value = Mock(
                returncode=0,
                stdout=f'{branch_name}\n',
                stderr=''
            )
            
            # Create templates
            templates_dir = repo_dir / "planning" / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)
            (templates_dir / "feature.md").write_text("# Feature Template")
            
            # Execute command
            result = new_project.create_project_structure()
            assert result == 0
            
            # Verify complex directory structure
            path_parts = branch_name.split('/')
            expected_dir = repo_dir / "planning" / Path(*path_parts)
            assert expected_dir.exists()
            assert (expected_dir / "feature.md").exists()
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_main_branch_workflow(self, mock_run, temp_git_repo):
        """Test new command workflow for main branch."""
        repo_dir = temp_git_repo
        
        # Mock git branch command to return main branch
        mock_run.return_value = Mock(
            returncode=0,
            stdout='main\n',
            stderr=''
        )
        
        # Create templates
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        (templates_dir / "tasks.md").write_text("# Tasks Template")
        (templates_dir / "to-do.md").write_text("# To-Do Template")
        
        # Execute command
        result = new_project.create_project_structure()
        assert result == 0
        
        # Verify main branch directory
        branch_dir = repo_dir / "planning" / "main"
        assert branch_dir.exists()
        assert (branch_dir / "feature.md").exists()
        assert (branch_dir / "tasks.md").exists()
        assert (branch_dir / "to-do.md").exists()
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_template_content_preservation(self, mock_run, temp_git_repo):
        """Test that template content is preserved during copying."""
        repo_dir = temp_git_repo
        
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/content-test\n',
            stderr=''
        )
        
        # Create templates with specific content
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        feature_template = """# Feature: Content Preservation Test

## Overview
This template tests content preservation during copying.

## Special Characters
- Unicode: 🚀 中文 🎉
- Markdown: **bold** *italic* `code`
- Links: [example](https://example.com)

## Code Blocks
```python
def test_function():
    return "Hello, World!"
```

## Lists
1. First item
2. Second item
   - Nested item
   - Another nested item
"""
        
        (templates_dir / "feature.md").write_text(feature_template)
        
        # Execute command
        result = new_project.create_project_structure()
        assert result == 0
        
        # Verify content preservation
        branch_dir = repo_dir / "planning" / "feature" / "content-test"
        copied_content = (branch_dir / "feature.md").read_text()
        
        assert "Content Preservation Test" in copied_content
        assert "🚀 中文 🎉" in copied_content
        assert "**bold** *italic* `code`" in copied_content
        assert "[example](https://example.com)" in copied_content
        assert "def test_function():" in copied_content
        assert "return \"Hello, World!\"" in copied_content
        assert "1. First item" in copied_content
        assert "   - Nested item" in copied_content


@pytest.mark.integration
class TestNewCommandErrorHandling:
    """Integration tests for new command error handling."""
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_not_in_git_repository(self, mock_run, temp_dir):
        """Test new command when not in a git repository."""
        # Mock git command failure
        mock_run.return_value = Mock(
            returncode=128,
            stdout='',
            stderr='fatal: not a git repository'
        )
        
        # Change to non-git directory
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(temp_dir)
            
            # Execute command
            result = new_project.create_project_structure()
            
            # Should handle error gracefully
            assert result == 1
            
        finally:
            os.chdir(original_cwd)
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_git_command_not_found(self, mock_run, temp_git_repo):
        """Test new command when git command is not found."""
        # Mock git command not found
        mock_run.side_effect = FileNotFoundError("git command not found")
        
        # Execute command
        result = new_project.create_project_structure()
        
        # Should handle error gracefully
        assert result == 1
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_missing_templates_directory(self, mock_run, temp_git_repo):
        """Test new command when templates directory is missing."""
        repo_dir = temp_git_repo
        
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/test\n',
            stderr=''
        )
        
        # Don't create templates directory
        # Execute command
        result = new_project.create_project_structure()
        
        # Should handle missing templates gracefully
        assert result == 1
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_permission_error(self, mock_run, temp_git_repo):
        """Test new command with permission errors."""
        repo_dir = temp_git_repo
        
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/permission-test\n',
            stderr=''
        )
        
        # Create templates
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        
        # Make planning directory read-only (Unix only)
        if hasattr(repo_dir, 'chmod'):
            planning_dir = repo_dir / "planning"
            planning_dir.chmod(0o444)
            
            try:
                result = new_project.create_project_structure()
                # Should handle permission error gracefully
                assert result == 1
                
            finally:
                # Restore permissions for cleanup
                planning_dir.chmod(0o755)
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_empty_branch_name(self, mock_run, temp_git_repo):
        """Test new command with empty branch name."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='\n',  # Empty branch name
            stderr=''
        )
        
        # Execute command
        result = new_project.create_project_structure()
        
        # Should handle empty branch name gracefully
        assert result == 1


@pytest.mark.integration
class TestNewCommandRealWorldScenarios:
    """Integration tests for real-world new command scenarios."""
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_overwrite_existing_branch_docs(self, mock_run, temp_git_repo):
        """Test new command when branch documentation already exists."""
        repo_dir = temp_git_repo
        
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/existing-docs\n',
            stderr=''
        )
        
        # Create existing branch documentation
        branch_dir = repo_dir / "planning" / "feature" / "existing-docs"
        branch_dir.mkdir(parents=True, exist_ok=True)
        (branch_dir / "feature.md").write_text("# Existing Feature Documentation")
        (branch_dir / "tasks.md").write_text("# Existing Tasks")
        
        # Create templates
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# New Feature Template")
        (templates_dir / "tasks.md").write_text("# New Tasks Template")
        
        # Execute command
        result = new_project.create_project_structure()
        assert result == 0
        
        # Verify files were overwritten with template content
        feature_content = (branch_dir / "feature.md").read_text()
        tasks_content = (branch_dir / "tasks.md").read_text()
        
        assert "New Feature Template" in feature_content
        assert "New Tasks Template" in tasks_content
        assert "Existing Feature Documentation" not in feature_content
        assert "Existing Tasks" not in tasks_content
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_with_unicode_branch_names(self, mock_run, temp_git_repo):
        """Test new command with unicode characters in branch names."""
        repo_dir = temp_git_repo
        
        # Test branch with unicode characters
        unicode_branch = 'feature/测试-功能'
        mock_run.return_value = Mock(
            returncode=0,
            stdout=f'{unicode_branch}\n',
            stderr=''
        )
        
        # Create templates
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        
        # Execute command
        result = new_project.create_project_structure()
        assert result == 0
        
        # Verify unicode branch directory was created
        branch_dir = repo_dir / "planning" / "feature" / "测试-功能"
        assert branch_dir.exists()
        assert (branch_dir / "feature.md").exists()
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_with_special_characters_in_branch(self, mock_run, temp_git_repo):
        """Test new command with special characters in branch names."""
        repo_dir = temp_git_repo
        
        # Test various special characters that might appear in branch names
        special_branches = [
            'feature/user-auth_system',
            'fix/bug-123.hotfix',
            'feature/api-v2.1-update'
        ]
        
        for branch_name in special_branches:
            mock_run.return_value = Mock(
                returncode=0,
                stdout=f'{branch_name}\n',
                stderr=''
            )
            
            # Create templates
            templates_dir = repo_dir / "planning" / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)
            (templates_dir / "feature.md").write_text("# Feature Template")
            
            # Execute command
            result = new_project.create_project_structure()
            assert result == 0
            
            # Verify directory was created with special characters
            path_parts = branch_name.split('/')
            expected_dir = repo_dir / "planning" / Path(*path_parts)
            assert expected_dir.exists()
            assert (expected_dir / "feature.md").exists()
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_multiple_template_files(self, mock_run, temp_git_repo):
        """Test new command with multiple template files."""
        repo_dir = temp_git_repo
        
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/multi-templates\n',
            stderr=''
        )
        
        # Create multiple template files
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        template_files = {
            "feature.md": "# Feature Template",
            "tasks.md": "# Tasks Template",
            "to-do.md": "# To-Do Template",
            "notes.md": "# Notes Template",
            "research.md": "# Research Template"
        }
        
        for filename, content in template_files.items():
            (templates_dir / filename).write_text(content)
        
        # Execute command
        result = new_project.create_project_structure()
        assert result == 0
        
        # Verify all template files were copied
        branch_dir = repo_dir / "planning" / "feature" / "multi-templates"
        for filename in template_files.keys():
            assert (branch_dir / filename).exists()
            content = (branch_dir / filename).read_text()
            assert template_files[filename] in content
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_nested_directory_creation(self, mock_run, temp_git_repo):
        """Test new command creates nested directories correctly."""
        repo_dir = temp_git_repo
        
        # Test deeply nested branch name
        nested_branch = 'feature/auth/oauth/google-integration'
        mock_run.return_value = Mock(
            returncode=0,
            stdout=f'{nested_branch}\n',
            stderr=''
        )
        
        # Create templates
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        
        # Execute command
        result = new_project.create_project_structure()
        assert result == 0
        
        # Verify nested directory structure
        expected_dir = repo_dir / "planning" / "feature" / "auth" / "oauth" / "google-integration"
        assert expected_dir.exists()
        assert (expected_dir / "feature.md").exists()
        
        # Verify all parent directories exist
        assert (repo_dir / "planning" / "feature").exists()
        assert (repo_dir / "planning" / "feature" / "auth").exists()
        assert (repo_dir / "planning" / "feature" / "auth" / "oauth").exists()


@pytest.mark.integration
class TestNewCommandPerformance:
    """Integration tests for new command performance characteristics."""
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_with_large_template_files(self, mock_run, temp_git_repo):
        """Test new command performance with large template files."""
        repo_dir = temp_git_repo
        
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/large-templates\n',
            stderr=''
        )
        
        # Create large template files
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create large content
        large_content = "# Large Template\n\n" + "Content line\n" * 5000
        (templates_dir / "feature.md").write_text(large_content)
        
        # Execute command
        result = new_project.create_project_structure()
        assert result == 0
        
        # Verify large file was copied correctly
        branch_dir = repo_dir / "planning" / "feature" / "large-templates"
        copied_content = (branch_dir / "feature.md").read_text()
        assert copied_content.count("Content line") == 5000
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_command_with_many_template_files(self, mock_run, temp_git_repo):
        """Test new command with many template files."""
        repo_dir = temp_git_repo
        
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/many-templates\n',
            stderr=''
        )
        
        # Create many template files
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        for i in range(20):
            (templates_dir / f"template_{i}.md").write_text(f"# Template {i}")
        
        # Execute command
        result = new_project.create_project_structure()
        assert result == 0
        
        # Verify all files were copied
        branch_dir = repo_dir / "planning" / "feature" / "many-templates"
        for i in range(20):
            template_file = branch_dir / f"template_{i}.md"
            assert template_file.exists()
            assert f"Template {i}" in template_file.read_text()
