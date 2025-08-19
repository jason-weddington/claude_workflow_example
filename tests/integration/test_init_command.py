"""
Integration tests for the init command workflow.
"""

import subprocess
from pathlib import Path
from unittest.mock import patch
import pytest

from claude_workflow import cli


@pytest.mark.integration
class TestInitCommandIntegration:
    """Integration tests for the complete init command workflow."""
    
    def test_init_command_claude_variant_complete_workflow(self, temp_git_repo):
        """Test complete init command workflow for Claude variant."""
        # Setup
        target_dir = temp_git_repo
        
        # Mock the package resources to use our test templates
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            # Create test template
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            template_content = """# {{FILENAME}} Project Template

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
            (templates_dir / "agent_instructions.md").write_text(template_content)
            
            # Mock package resources
            mock_pkg.files.return_value = templates_dir.parent
            
            # Create args
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            # Execute command
            result = cli.create_command(args)
            
            # Verify success
            assert result == 0
            
            # Verify CLAUDE.md was created
            claude_file = target_dir / "CLAUDE.md"
            assert claude_file.exists()
            
            # Verify content substitution
            content = claude_file.read_text()
            assert "CLAUDE.md Project Template" in content
            assert "Tell Claude to read the planning documents" in content
            assert "{{FILENAME}}" not in content
            assert "{{AGENT_NAME}}" not in content
            
            # Verify directory structure was created
            assert (target_dir / "docs").exists()
            assert (target_dir / "planning").exists()
            assert (target_dir / "planning" / "templates").exists()
    
    def test_init_command_amazonq_variant_complete_workflow(self, temp_git_repo):
        """Test complete init command workflow for Amazon Q variant."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            # Create test template
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            template_content = """# {{FILENAME}} Instructions

## Overview
Instructions for {{AGENT_NAME}}.

## Commands
Tell {{AGENT_NAME}} to execute commands.
"""
            (templates_dir / "agent_instructions.md").write_text(template_content)
            
            mock_pkg.files.return_value = templates_dir.parent
            
            # Create args for Amazon Q
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': True
            })()
            
            # Execute command
            result = cli.create_command(args)
            
            # Verify success
            assert result == 0
            
            # Verify AmazonQ.md was created
            amazonq_file = target_dir / "AmazonQ.md"
            assert amazonq_file.exists()
            
            # Verify content substitution
            content = amazonq_file.read_text()
            assert "AmazonQ.md Instructions" in content
            assert "Instructions for Amazon Q" in content
            assert "Tell Amazon Q to execute" in content
            assert "{{FILENAME}}" not in content
            assert "{{AGENT_NAME}}" not in content
    
    def test_init_command_directory_structure_creation(self, temp_git_repo):
        """Test that init command creates correct directory structure."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            # Setup mock templates
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            
            # Create all template files
            template_files = {
                "agent_instructions.md": "# {{FILENAME}}\nAgent: {{AGENT_NAME}}",
                "api-docs.md": "# API Documentation",
                "architecture.md": "# Architecture",
                "codebase.md": "# Codebase",
                "domain.md": "# Domain",
                "setup.md": "# Setup",
                "testing.md": "# Testing",
                "feature.md": "# Feature Template",
                "tasks.md": "# Tasks Template",
                "to-do.md": "# To-Do Template"
            }
            
            for filename, content in template_files.items():
                (templates_dir / filename).write_text(content)
            
            mock_pkg.files.return_value = templates_dir.parent
            
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            # Execute command
            result = cli.create_command(args)
            assert result == 0
            
            # Verify main structure
            assert (target_dir / "CLAUDE.md").exists()
            assert (target_dir / "docs").exists()
            assert (target_dir / "planning").exists()
            assert (target_dir / "planning" / "templates").exists()
            
            # Verify docs files
            docs_files = ["api-docs.md", "architecture.md", "codebase.md", 
                         "domain.md", "setup.md", "testing.md"]
            for doc_file in docs_files:
                assert (target_dir / "docs" / doc_file).exists()
            
            # Verify planning template files
            template_files = ["feature.md", "tasks.md", "to-do.md"]
            for template_file in template_files:
                assert (target_dir / "planning" / "templates" / template_file).exists()
    
    def test_init_command_non_git_directory_with_confirmation(self, temp_dir):
        """Test init command in non-git directory with user confirmation."""
        target_dir = temp_dir
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg, \
             patch('claude_workflow.cli.input', return_value='y') as mock_input:
            
            # Setup mock template
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            (templates_dir / "agent_instructions.md").write_text("# {{FILENAME}}")
            
            mock_pkg.files.return_value = templates_dir.parent
            
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            # Execute command
            result = cli.create_command(args)
            
            # Verify success after confirmation
            assert result == 0
            assert (target_dir / "CLAUDE.md").exists()
            
            # Verify user was prompted
            mock_input.assert_called_once()
    
    def test_init_command_non_git_directory_without_confirmation(self, temp_dir):
        """Test init command in non-git directory without user confirmation."""
        target_dir = temp_dir
        
        with patch('claude_workflow.cli.input', return_value='n') as mock_input:
            
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            # Execute command
            result = cli.create_command(args)
            
            # Verify failure when user declines
            assert result == 1
            assert not (target_dir / "CLAUDE.md").exists()
            
            # Verify user was prompted
            mock_input.assert_called_once()
    
    def test_init_command_nonexistent_directory(self):
        """Test init command with non-existent directory."""
        nonexistent_dir = "/path/that/does/not/exist"
        
        args = type('Args', (), {
            'directory': nonexistent_dir,
            'amazonq': False
        })()
        
        # Execute command
        result = cli.create_command(args)
        
        # Should fail gracefully
        assert result == 1
    
    def test_init_command_file_creation_and_content_verification(self, temp_git_repo):
        """Test that init command creates files with correct content."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            # Create comprehensive test template
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            
            agent_template = """# {{FILENAME}} - AI Assistant Instructions

## Build and Test Commands
```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Project Purpose and Domain

This project helps {{AGENT_NAME}} work more effectively.

## Development Workflow
- {{AGENT_NAME}} should read the planning documents
- Follow the systematic development approach
"""
            
            (templates_dir / "agent_instructions.md").write_text(agent_template)
            (templates_dir / "codebase.md").write_text("# Codebase Documentation")
            (templates_dir / "feature.md").write_text("# Feature Template\n\n## Overview\n[Description]")
            
            mock_pkg.files.return_value = templates_dir.parent
            
            # Test Claude variant
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            assert result == 0
            
            # Verify CLAUDE.md content
            claude_content = (target_dir / "CLAUDE.md").read_text()
            assert "CLAUDE.md - AI Assistant Instructions" in claude_content
            assert "This project helps Claude work more effectively" in claude_content
            assert "Claude should read the planning documents" in claude_content
            assert "pip install -e" in claude_content
            assert "pytest" in claude_content
            
            # Verify docs file content
            codebase_content = (target_dir / "docs" / "codebase.md").read_text()
            assert "Codebase Documentation" in codebase_content
            
            # Verify template file content
            feature_content = (target_dir / "planning" / "templates" / "feature.md").read_text()
            assert "Feature Template" in feature_content
            assert "[Description]" in feature_content


@pytest.mark.integration
class TestInitCommandErrorHandling:
    """Integration tests for init command error handling."""
    
    def test_init_command_permission_error_handling(self, temp_dir):
        """Test init command handling of permission errors."""
        # This test is platform-dependent and may not work on all systems
        if hasattr(temp_dir, 'chmod'):
            # Make directory read-only
            temp_dir.chmod(0o444)
            
            try:
                args = type('Args', (), {
                    'directory': str(temp_dir),
                    'amazonq': False
                })()
                
                result = cli.create_command(args)
                
                # Should handle permission error gracefully
                assert result == 1
                
            finally:
                # Restore permissions for cleanup
                temp_dir.chmod(0o755)
    
    def test_init_command_template_missing_error(self, temp_git_repo):
        """Test init command when template files are missing."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            # Mock package resources to return non-existent directory
            mock_pkg.files.return_value = target_dir / "nonexistent_templates"
            
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            # Should handle missing templates gracefully
            result = cli.create_command(args)
            assert result == 1
    
    def test_init_command_disk_space_simulation(self, temp_git_repo):
        """Test init command behavior when simulating disk space issues."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg, \
             patch('pathlib.Path.write_text') as mock_write:
            
            # Setup mock template
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            (templates_dir / "agent_instructions.md").write_text("# {{FILENAME}}")
            
            mock_pkg.files.return_value = templates_dir.parent
            
            # Simulate disk space error
            mock_write.side_effect = OSError("No space left on device")
            
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            
            # Should handle disk space error gracefully
            assert result == 1


@pytest.mark.integration
class TestInitCommandRealWorldScenarios:
    """Integration tests for real-world init command scenarios."""
    
    def test_init_command_in_existing_project_with_files(self, temp_git_repo):
        """Test init command in directory that already has files."""
        target_dir = temp_git_repo
        
        # Create some existing files
        (target_dir / "existing_file.txt").write_text("Existing content")
        (target_dir / "src").mkdir()
        (target_dir / "src" / "main.py").write_text("print('hello')")
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            (templates_dir / "agent_instructions.md").write_text("# {{FILENAME}}")
            
            mock_pkg.files.return_value = templates_dir.parent
            
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            
            # Should succeed and preserve existing files
            assert result == 0
            assert (target_dir / "CLAUDE.md").exists()
            assert (target_dir / "existing_file.txt").exists()
            assert (target_dir / "src" / "main.py").exists()
            
            # Verify existing content preserved
            assert (target_dir / "existing_file.txt").read_text() == "Existing content"
    
    def test_init_command_overwrite_existing_agent_file(self, temp_git_repo):
        """Test init command when agent instruction file already exists."""
        target_dir = temp_git_repo
        
        # Create existing CLAUDE.md
        existing_claude = target_dir / "CLAUDE.md"
        existing_claude.write_text("# Existing CLAUDE.md\n\nOld content")
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            (templates_dir / "agent_instructions.md").write_text("# {{FILENAME}}\n\nNew content")
            
            mock_pkg.files.return_value = templates_dir.parent
            
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            
            # Should succeed and overwrite
            assert result == 0
            
            # Verify file was overwritten
            content = existing_claude.read_text()
            assert "New content" in content
            assert "Old content" not in content
    
    def test_init_command_with_unicode_paths(self, temp_dir):
        """Test init command with unicode characters in paths."""
        # Create directory with unicode name
        unicode_dir = temp_dir / "测试目录"
        unicode_dir.mkdir()
        
        # Make it a git repo
        git_dir = unicode_dir / ".git"
        git_dir.mkdir()
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            templates_dir = temp_dir / "test_templates"
            templates_dir.mkdir()
            (templates_dir / "agent_instructions.md").write_text("# {{FILENAME}}")
            
            mock_pkg.files.return_value = templates_dir.parent
            
            args = type('Args', (), {
                'directory': str(unicode_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            
            # Should handle unicode paths correctly
            assert result == 0
            assert (unicode_dir / "CLAUDE.md").exists()


@pytest.mark.integration
class TestInitCommandPerformance:
    """Integration tests for init command performance characteristics."""
    
    def test_init_command_with_large_template_files(self, temp_git_repo):
        """Test init command performance with large template files."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            
            # Create large template content
            large_content = "# {{FILENAME}}\n\n" + "Content line\n" * 10000
            (templates_dir / "agent_instructions.md").write_text(large_content)
            
            mock_pkg.files.return_value = templates_dir.parent
            
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            # Should handle large files efficiently
            result = cli.create_command(args)
            assert result == 0
            
            # Verify content was processed correctly
            content = (target_dir / "CLAUDE.md").read_text()
            assert "CLAUDE.md" in content
            assert content.count("Content line") == 10000
    
    def test_init_command_with_many_template_files(self, temp_git_repo):
        """Test init command with many template files."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            templates_dir = target_dir / "test_templates"
            templates_dir.mkdir()
            
            # Create many template files
            (templates_dir / "agent_instructions.md").write_text("# {{FILENAME}}")
            
            for i in range(50):
                (templates_dir / f"template_{i}.md").write_text(f"# Template {i}")
            
            mock_pkg.files.return_value = templates_dir.parent
            
            args = type('Args', (), {
                'directory': str(target_dir),
                'amazonq': False
            })()
            
            # Should handle many files efficiently
            result = cli.create_command(args)
            assert result == 0
            
            # Verify main file was created
            assert (target_dir / "CLAUDE.md").exists()
