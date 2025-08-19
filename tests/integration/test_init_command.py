"""
Integration tests for the init command workflow.
"""

from pathlib import Path
from unittest.mock import patch
import pytest

from claude_workflow import cli


@pytest.mark.integration
class TestInitCommandIntegration:
    """Integration tests for the complete init command workflow."""
    
    def test_init_command_claude_variant_complete_workflow(self, temp_git_repo, sample_templates_dir):
        """Test complete init command workflow for Claude variant."""
        target_dir = temp_git_repo
        
        # Mock the package resources to use our test templates
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            # Create args
            args = type('Args', (), {
                'path': str(target_dir),
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
            assert "CLAUDE.md" in content
            assert "Claude" in content
            assert "{{FILENAME}}" not in content
            assert "{{AGENT_NAME}}" not in content
            
            # Verify directory structure was created
            assert (target_dir / "docs").exists()
            assert (target_dir / "planning").exists()
            assert (target_dir / "planning" / "templates").exists()
    
    def test_init_command_amazonq_variant_complete_workflow(self, temp_git_repo, sample_templates_dir):
        """Test complete init command workflow for Amazon Q variant."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            # Create args for Amazon Q
            args = type('Args', (), {
                'path': str(target_dir),
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
            assert "AmazonQ.md" in content
            assert "Amazon Q" in content
            assert "{{FILENAME}}" not in content
            assert "{{AGENT_NAME}}" not in content
    
    def test_init_command_directory_structure_creation(self, temp_git_repo, sample_templates_dir):
        """Test that init command creates correct directory structure."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = type('Args', (), {
                'path': str(target_dir),
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
    
    @patch('claude_workflow.cli.input')
    def test_init_command_non_git_directory_with_confirmation(self, mock_input, temp_dir, sample_templates_dir):
        """Test init command in non-git directory with user confirmation."""
        target_dir = temp_dir
        mock_input.return_value = 'y'
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = type('Args', (), {
                'path': str(target_dir),
                'amazonq': False
            })()
            
            # Execute command
            result = cli.create_command(args)
            
            # Verify success after confirmation
            assert result == 0
            assert (target_dir / "CLAUDE.md").exists()
            
            # Verify user was prompted
            mock_input.assert_called_once()
    
    @patch('claude_workflow.cli.input')
    def test_init_command_non_git_directory_without_confirmation(self, mock_input, temp_dir):
        """Test init command in non-git directory without user confirmation."""
        target_dir = temp_dir
        mock_input.return_value = 'n'
        
        args = type('Args', (), {
            'path': str(target_dir),
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
            'path': nonexistent_dir,
            'amazonq': False
        })()
        
        # Execute command
        result = cli.create_command(args)
        
        # Should fail gracefully
        assert result == 1


@pytest.mark.integration
class TestInitCommandErrorHandling:
    """Integration tests for init command error handling."""
    
    def test_init_command_template_missing_error(self, temp_git_repo):
        """Test init command when template files are missing."""
        target_dir = temp_git_repo
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            # Mock package resources to return non-existent directory
            mock_pkg.files.return_value = target_dir / "nonexistent_templates"
            
            args = type('Args', (), {
                'path': str(target_dir),
                'amazonq': False
            })()
            
            # Should handle missing templates gracefully
            with pytest.raises(FileNotFoundError):
                cli.create_command(args)


@pytest.mark.integration
class TestInitCommandRealWorldScenarios:
    """Integration tests for real-world init command scenarios."""
    
    def test_init_command_in_existing_project_with_files(self, temp_git_repo, sample_templates_dir):
        """Test init command in directory that already has files."""
        target_dir = temp_git_repo
        
        # Create some existing files
        (target_dir / "existing_file.txt").write_text("Existing content")
        (target_dir / "src").mkdir()
        (target_dir / "src" / "main.py").write_text("print('hello')")
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = type('Args', (), {
                'path': str(target_dir),
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
    
    def test_init_command_overwrite_existing_agent_file(self, temp_git_repo, sample_templates_dir):
        """Test init command when agent instruction file already exists."""
        target_dir = temp_git_repo
        
        # Create existing CLAUDE.md
        existing_claude = target_dir / "CLAUDE.md"
        existing_claude.write_text("# Existing CLAUDE.md\n\nOld content")
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = type('Args', (), {
                'path': str(target_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            
            # Should succeed and overwrite
            assert result == 0
            
            # Verify file was overwritten
            content = existing_claude.read_text()
            assert "CLAUDE.md" in content  # New template content
            assert "Old content" not in content
    
    def test_init_command_with_unicode_paths(self, temp_dir, sample_templates_dir):
        """Test init command with unicode characters in paths."""
        # Create directory with unicode name
        unicode_dir = temp_dir / "测试目录"
        unicode_dir.mkdir()
        
        # Make it a git repo
        git_dir = unicode_dir / ".git"
        git_dir.mkdir()
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = type('Args', (), {
                'path': str(unicode_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            
            # Should handle unicode paths correctly
            assert result == 0
            assert (unicode_dir / "CLAUDE.md").exists()
    
    def test_init_command_preserves_existing_docs_directory(self, temp_git_repo, sample_templates_dir):
        """Test that init command preserves existing docs directory and files."""
        target_dir = temp_git_repo
        
        # Create existing docs directory with some files
        docs_dir = target_dir / "docs"
        docs_dir.mkdir()
        (docs_dir / "existing-file.md").write_text("# My Existing Documentation")
        (docs_dir / "api-docs.md").write_text("# My Custom API Documentation")
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = type('Args', (), {
                'path': str(target_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            
            # Should succeed
            assert result == 0
            
            # Verify existing files are preserved
            assert (docs_dir / "existing-file.md").exists()
            assert (docs_dir / "existing-file.md").read_text() == "# My Existing Documentation"
            assert (docs_dir / "api-docs.md").read_text() == "# My Custom API Documentation"
            
            # Verify new template files were added (non-conflicting ones)
            assert (docs_dir / "architecture.md").exists()
            assert (docs_dir / "codebase.md").exists()
            assert (docs_dir / "domain.md").exists()
            assert (docs_dir / "testing.md").exists()
            assert (docs_dir / "setup.md").exists()
            
            # Verify template content in new files
            assert "Architecture" in (docs_dir / "architecture.md").read_text()
    
    def test_init_command_with_empty_existing_docs_directory(self, temp_git_repo, sample_templates_dir):
        """Test init command with existing but empty docs directory."""
        target_dir = temp_git_repo
        
        # Create empty docs directory
        docs_dir = target_dir / "docs"
        docs_dir.mkdir()
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = type('Args', (), {
                'path': str(target_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            
            # Should succeed
            assert result == 0
            
            # Verify all template files were added
            expected_files = ["api-docs.md", "architecture.md", "codebase.md", 
                            "domain.md", "setup.md", "testing.md"]
            for file in expected_files:
                assert (docs_dir / file).exists()
                # Verify it's template content, not empty
                assert len((docs_dir / file).read_text()) > 10
    
    def test_init_command_all_docs_files_exist(self, temp_git_repo, sample_templates_dir):
        """Test init command when all template files already exist in docs."""
        target_dir = temp_git_repo
        
        # Create docs directory with all template files
        docs_dir = target_dir / "docs"
        docs_dir.mkdir()
        
        template_files = ["api-docs.md", "architecture.md", "codebase.md", 
                         "domain.md", "setup.md", "testing.md"]
        for file in template_files:
            (docs_dir / file).write_text(f"# My Custom {file}")
        
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = type('Args', (), {
                'path': str(target_dir),
                'amazonq': False
            })()
            
            result = cli.create_command(args)
            
            # Should succeed
            assert result == 0
            
            # Verify all existing files are preserved
            for file in template_files:
                assert (docs_dir / file).exists()
                assert (docs_dir / file).read_text() == f"# My Custom {file}"
