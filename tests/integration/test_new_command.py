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
    
    def test_create_project_structure_feature_branch(self, temp_git_repo):
        """Test create_project_structure with feature branch."""
        repo_dir = temp_git_repo
        
        # Create planning templates directory
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create template files
        (templates_dir / "feature.md").write_text("# Feature Template")
        (templates_dir / "tasks.md").write_text("# Tasks Template")
        (templates_dir / "to-do.md").write_text("# To-Do Template")
        
        # Change to repo directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_dir)
            
            # Test with feature branch
            branch_name = "feature/test-feature"
            target_dir = new_project.create_project_structure(branch_name)
            
            # Verify directory was created
            expected_dir = repo_dir / "planning" / "feature" / "test-feature"
            # Handle macOS /private symlink differences by comparing resolved paths
            assert target_dir.resolve() == expected_dir.resolve()
            assert expected_dir.exists()
            
            # Verify template files were copied
            assert (expected_dir / "feature.md").exists()
            assert (expected_dir / "tasks.md").exists()
            assert (expected_dir / "to-do.md").exists()
            
            # Verify content was copied correctly
            assert (expected_dir / "feature.md").read_text() == "# Feature Template"
            
        finally:
            os.chdir(original_cwd)
    
    def test_create_project_structure_fix_branch(self, temp_git_repo):
        """Test create_project_structure with fix branch."""
        repo_dir = temp_git_repo
        
        # Create planning templates directory
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        
        # Change to repo directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_dir)
            
            # Test with fix branch
            branch_name = "fix/bug-123"
            target_dir = new_project.create_project_structure(branch_name)
            
            # Verify directory structure
            expected_dir = repo_dir / "planning" / "fix" / "bug-123"
            assert target_dir.resolve() == expected_dir.resolve()
            assert expected_dir.exists()
            assert (expected_dir / "feature.md").exists()
            
        finally:
            os.chdir(original_cwd)
    
    def test_create_project_structure_main_branch(self, temp_git_repo):
        """Test create_project_structure with main branch."""
        repo_dir = temp_git_repo
        
        # Create planning templates directory
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        
        # Change to repo directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_dir)
            
            # Test with main branch
            branch_name = "main"
            target_dir = new_project.create_project_structure(branch_name)
            
            # Verify directory structure
            expected_dir = repo_dir / "planning" / "main"
            assert target_dir.resolve() == expected_dir.resolve()
            assert expected_dir.exists()
            
        finally:
            os.chdir(original_cwd)
    
    def test_create_project_structure_complex_branch_name(self, temp_git_repo):
        """Test create_project_structure with complex branch names."""
        repo_dir = temp_git_repo
        
        # Create planning templates directory
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        
        # Change to repo directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_dir)
            
            # Test with complex branch name
            branch_name = "feature/auth/oauth-integration"
            target_dir = new_project.create_project_structure(branch_name)
            
            # Verify nested directory structure
            expected_dir = repo_dir / "planning" / "feature" / "auth" / "oauth-integration"
            assert target_dir.resolve() == expected_dir.resolve()
            assert expected_dir.exists()
            
        finally:
            os.chdir(original_cwd)


@pytest.mark.integration
class TestNewCommandErrorHandling:
    """Integration tests for new command error handling."""
    
    def test_create_project_structure_no_planning_directory(self, temp_dir):
        """Test create_project_structure when planning directory doesn't exist."""
        # Change to directory without planning folder
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Should exit with error
            with pytest.raises(SystemExit):
                new_project.create_project_structure("feature/test")
                
        finally:
            os.chdir(original_cwd)
    
    def test_create_project_structure_no_templates(self, temp_git_repo):
        """Test create_project_structure when templates directory is missing."""
        repo_dir = temp_git_repo
        
        # Create planning directory but no templates
        planning_dir = repo_dir / "planning"
        planning_dir.mkdir(exist_ok=True)
        
        # Change to repo directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_dir)
            
            # Should still work but no files will be copied
            target_dir = new_project.create_project_structure("feature/test")
            
            # Directory should be created but empty
            assert target_dir.exists()
            assert len(list(target_dir.iterdir())) == 0
            
        finally:
            os.chdir(original_cwd)


@pytest.mark.integration  
class TestNewProjectMain:
    """Integration tests for new_project main function."""
    
    @patch('claude_workflow.new_project.get_current_branch')
    def test_main_function_success(self, mock_get_branch, temp_git_repo):
        """Test main function with successful branch detection."""
        repo_dir = temp_git_repo
        mock_get_branch.return_value = "feature/test-main"
        
        # Create planning templates
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        
        # Change to repo directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_dir)
            
            result = new_project.main()
            
            assert result == 0
            expected_dir = repo_dir / "planning" / "feature" / "test-main"
            assert expected_dir.exists()
            
        finally:
            os.chdir(original_cwd)
    
    @patch('claude_workflow.new_project.get_current_branch')
    def test_main_function_no_branch(self, mock_get_branch, temp_git_repo):
        """Test main function when branch detection fails."""
        mock_get_branch.return_value = None
        
        # Should exit with error
        with pytest.raises(SystemExit) as exc_info:
            new_project.main()
        
        assert exc_info.value.code == 1


@pytest.mark.integration
class TestNewCommandRealWorldScenarios:
    """Integration tests for real-world new command scenarios."""
    
    def test_overwrite_existing_branch_docs(self, temp_git_repo):
        """Test new command when branch documentation already exists."""
        repo_dir = temp_git_repo
        
        # Create existing branch documentation
        branch_dir = repo_dir / "planning" / "feature" / "existing-docs"
        branch_dir.mkdir(parents=True, exist_ok=True)
        (branch_dir / "feature.md").write_text("# Existing Feature Documentation")
        
        # Create templates
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# New Feature Template")
        (templates_dir / "tasks.md").write_text("# New Tasks Template")
        (templates_dir / "to-do.md").write_text("# New To-Do Template")
        
        # Change to repo directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_dir)
            
            # Execute command
            target_dir = new_project.create_project_structure("feature/existing-docs")
            
            # Verify existing files were NOT overwritten (actual behavior)
            feature_content = (branch_dir / "feature.md").read_text()
            assert "Existing Feature Documentation" in feature_content
            assert "New Feature Template" not in feature_content
            
            # Verify new files were created from templates
            assert (branch_dir / "tasks.md").exists()
            assert (branch_dir / "to-do.md").exists()
            
        finally:
            os.chdir(original_cwd)
    
    def test_unicode_branch_names(self, temp_git_repo):
        """Test new command with unicode characters in branch names."""
        repo_dir = temp_git_repo
        
        # Create templates
        templates_dir = repo_dir / "planning" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "feature.md").write_text("# Feature Template")
        
        # Change to repo directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(repo_dir)
            
            # Test with unicode branch name
            unicode_branch = 'feature/测试-功能'
            target_dir = new_project.create_project_structure(unicode_branch)
            
            # Verify unicode branch directory was created
            expected_dir = repo_dir / "planning" / "feature" / "测试-功能"
            assert target_dir.resolve() == expected_dir.resolve()
            assert expected_dir.exists()
            assert (expected_dir / "feature.md").exists()
            
        finally:
            os.chdir(original_cwd)
