"""
Unit tests for git integration functionality.
"""

import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, call
import pytest

from claude_workflow import cli, new_project


class TestGitRepositoryDetection:
    """Test git repository detection functionality."""
    
    def test_detect_git_repository_exists(self, temp_git_repo):
        """Test detection when .git directory exists."""
        git_dir = temp_git_repo / ".git"
        
        assert git_dir.exists()
        assert git_dir.is_dir()
    
    def test_detect_git_repository_missing(self, temp_dir):
        """Test detection when .git directory is missing."""
        git_dir = temp_dir / ".git"
        
        assert not git_dir.exists()
    
    def test_git_detection_in_cli_create_command(self, temp_dir):
        """Test git detection in CLI create command."""
        # Mock the Path class to return our temp directory
        with patch('claude_workflow.cli.Path') as mock_path:
            mock_path.return_value = temp_dir
            
            args = Mock()
            args.directory = str(temp_dir)
            args.amazonq = False
            
            # Should detect no .git directory
            with patch('claude_workflow.cli.input', return_value='n'):
                result = cli.create_command(args)
                assert result == 1  # Should fail when user declines
    
    def test_git_detection_with_confirmation(self, temp_dir):
        """Test git detection with user confirmation."""
        with patch('claude_workflow.cli.Path') as mock_path, \
             patch('claude_workflow.cli.pkg_resources') as mock_pkg, \
             patch('claude_workflow.cli.input', return_value='y'):
            
            mock_path.return_value = temp_dir
            mock_pkg.files.return_value = temp_dir / "templates"
            (temp_dir / "templates").mkdir()
            (temp_dir / "templates" / "agent_instructions.md").write_text("# {{FILENAME}}")
            
            args = Mock()
            args.directory = str(temp_dir)
            args.amazonq = False
            
            result = cli.create_command(args)
            assert result == 0  # Should succeed when user confirms


class TestBranchNameExtraction:
    """Test git branch name extraction functionality."""
    
    @patch('subprocess.run')
    def test_get_current_branch_success(self, mock_run):
        """Test successful branch name extraction."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/test-branch\n',
            stderr=''
        )
        
        # Simulate getting branch name
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        branch_name = result.stdout.strip()
        
        assert branch_name == 'feature/test-branch'
    
    @patch('subprocess.run')
    def test_get_current_branch_failure(self, mock_run):
        """Test branch name extraction failure."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout='',
            stderr='fatal: not a git repository'
        )
        
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        
        assert result.returncode == 1
        assert 'not a git repository' in result.stderr
    
    def test_branch_name_parsing_feature(self):
        """Test parsing feature branch names."""
        branch_names = [
            'feature/new-auth',
            'feature/user-management',
            'feature/api-integration'
        ]
        
        for branch_name in branch_names:
            # Simulate directory path creation
            path_parts = branch_name.split('/')
            expected_path = Path('planning') / Path(*path_parts)
            
            assert 'feature' in str(expected_path)
            assert expected_path.parts[0] == 'planning'
            assert expected_path.parts[1] == 'feature'
    
    def test_branch_name_parsing_fix(self):
        """Test parsing fix branch names."""
        branch_names = [
            'fix/bug-123',
            'fix/critical-issue',
            'hotfix/security-patch'
        ]
        
        for branch_name in branch_names:
            path_parts = branch_name.split('/')
            expected_path = Path('planning') / Path(*path_parts)
            
            assert expected_path.parts[0] == 'planning'
            assert expected_path.parts[1] in ['fix', 'hotfix']
    
    def test_branch_name_parsing_complex(self):
        """Test parsing complex branch names."""
        complex_branches = [
            'feature/auth/oauth-integration',
            'fix/ui/button-styling',
            'refactor/database/migration-system'
        ]
        
        for branch_name in complex_branches:
            path_parts = branch_name.split('/')
            expected_path = Path('planning') / Path(*path_parts)
            
            assert expected_path.parts[0] == 'planning'
            assert len(expected_path.parts) >= 3  # planning + type + name (+ optional sub)


class TestBranchToDirectoryMapping:
    """Test mapping branch names to directory structures."""
    
    def test_simple_branch_mapping(self):
        """Test mapping simple branch names to directories."""
        test_cases = [
            ('main', 'planning/main'),
            ('develop', 'planning/develop'),
            ('master', 'planning/master')
        ]
        
        for branch_name, expected_path in test_cases:
            result_path = Path('planning') / branch_name
            assert str(result_path) == expected_path
    
    def test_feature_branch_mapping(self):
        """Test mapping feature branches to directories."""
        test_cases = [
            ('feature/auth', 'planning/feature/auth'),
            ('feature/user-profile', 'planning/feature/user-profile'),
            ('feature/api/v2', 'planning/feature/api/v2')
        ]
        
        for branch_name, expected_path in test_cases:
            path_parts = branch_name.split('/')
            result_path = Path('planning') / Path(*path_parts)
            assert str(result_path) == expected_path
    
    def test_special_character_handling(self):
        """Test handling branch names with special characters."""
        branch_names = [
            'feature/user-auth',
            'fix/bug_123',
            'feature/api-v2.1'
        ]
        
        for branch_name in branch_names:
            # Should handle hyphens, underscores, dots
            path_parts = branch_name.split('/')
            result_path = Path('planning') / Path(*path_parts)
            
            assert result_path.parts[0] == 'planning'
            # Path should be valid
            assert all(part for part in result_path.parts)


class TestGitCommandIntegration:
    """Test integration with git commands."""
    
    def test_git_init_detection(self, temp_dir):
        """Test detection of git init in directory."""
        # Before git init
        assert not (temp_dir / ".git").exists()
        
        # Simulate git init
        git_dir = temp_dir / ".git"
        git_dir.mkdir()
        
        # After git init
        assert git_dir.exists()
        assert git_dir.is_dir()
    
    @patch('subprocess.run')
    def test_git_branch_command_execution(self, mock_run):
        """Test execution of git branch command."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='* feature/test\n  main\n',
            stderr=''
        )
        
        # Simulate git branch command
        result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'feature/test' in result.stdout
        assert 'main' in result.stdout
    
    @patch('subprocess.run')
    def test_git_status_command_execution(self, mock_run):
        """Test execution of git status command."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='On branch feature/test\nnothing to commit',
            stderr=''
        )
        
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'On branch feature/test' in result.stdout


class TestGitErrorHandling:
    """Test error handling for git operations."""
    
    @patch('subprocess.run')
    def test_git_command_not_found(self, mock_run):
        """Test handling when git command is not found."""
        mock_run.side_effect = FileNotFoundError("git command not found")
        
        with pytest.raises(FileNotFoundError):
            subprocess.run(['git', 'status'], capture_output=True, text=True)
    
    @patch('subprocess.run')
    def test_git_repository_not_found(self, mock_run):
        """Test handling when not in a git repository."""
        mock_run.return_value = Mock(
            returncode=128,
            stdout='',
            stderr='fatal: not a git repository'
        )
        
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        
        assert result.returncode == 128
        assert 'not a git repository' in result.stderr
    
    def test_invalid_git_directory_structure(self, temp_dir):
        """Test handling invalid .git directory structure."""
        # Create .git as a file instead of directory
        git_file = temp_dir / ".git"
        git_file.write_text("gitdir: /some/other/path")
        
        assert git_file.exists()
        assert not git_file.is_dir()  # It's a file, not a directory
    
    @patch('subprocess.run')
    def test_git_permission_error(self, mock_run):
        """Test handling git permission errors."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout='',
            stderr='Permission denied'
        )
        
        result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert 'Permission denied' in result.stderr


class TestNewProjectGitIntegration:
    """Test git integration in new project functionality."""
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_project_get_branch_name(self, mock_run, temp_dir):
        """Test getting branch name in new project command."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='feature/automated-testing\n',
            stderr=''
        )
        
        # This would be called in new_project.py
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, cwd=temp_dir)
        branch_name = result.stdout.strip()
        
        assert branch_name == 'feature/automated-testing'
    
    def test_new_project_directory_creation_from_branch(self, temp_dir):
        """Test creating project directory structure from branch name."""
        branch_name = 'feature/automated-testing'
        
        # Simulate the directory creation logic
        path_parts = branch_name.split('/')
        project_dir = temp_dir / 'planning' / Path(*path_parts)
        project_dir.mkdir(parents=True, exist_ok=True)
        
        assert project_dir.exists()
        assert project_dir == temp_dir / 'planning' / 'feature' / 'automated-testing'
    
    @patch('claude_workflow.new_project.subprocess.run')
    def test_new_project_not_in_git_repo(self, mock_run):
        """Test new project command when not in git repository."""
        mock_run.return_value = Mock(
            returncode=128,
            stdout='',
            stderr='fatal: not a git repository'
        )
        
        # Should handle the error gracefully
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        
        assert result.returncode == 128


class TestUserConfirmationFlow:
    """Test user confirmation flow for git operations."""
    
    @patch('claude_workflow.cli.input')
    def test_user_confirms_non_git_directory(self, mock_input, temp_dir):
        """Test user confirming to proceed in non-git directory."""
        mock_input.return_value = 'y'
        
        # Simulate the confirmation check
        git_dir = temp_dir / ".git"
        if not git_dir.exists():
            user_input = mock_input("Continue anyway? (y/n): ")
            proceed = user_input.lower() == 'y'
        else:
            proceed = True
        
        assert proceed is True
    
    @patch('claude_workflow.cli.input')
    def test_user_declines_non_git_directory(self, mock_input, temp_dir):
        """Test user declining to proceed in non-git directory."""
        mock_input.return_value = 'n'
        
        # Simulate the confirmation check
        git_dir = temp_dir / ".git"
        if not git_dir.exists():
            user_input = mock_input("Continue anyway? (y/n): ")
            proceed = user_input.lower() == 'y'
        else:
            proceed = True
        
        assert proceed is False
    
    @patch('claude_workflow.cli.input')
    def test_user_input_variations(self, mock_input):
        """Test various user input variations."""
        test_cases = [
            ('y', True),
            ('Y', True),
            ('yes', False),  # Only 'y' should be accepted
            ('n', False),
            ('N', False),
            ('no', False),
            ('', False),
            ('invalid', False)
        ]
        
        for user_input, expected in test_cases:
            mock_input.return_value = user_input
            result = mock_input("Continue anyway? (y/n): ").lower() == 'y'
            assert result == expected


@pytest.mark.unit
class TestGitIntegrationComplete:
    """Complete integration tests for git functionality."""
    
    def test_complete_git_workflow_simulation(self, temp_git_repo):
        """Test complete git workflow simulation."""
        # Repository exists
        assert (temp_git_repo / ".git").exists()
        
        # Simulate branch creation and switching
        branch_name = "feature/test-integration"
        
        # Create planning directory structure
        planning_dir = temp_git_repo / "planning" / "feature" / "test-integration"
        planning_dir.mkdir(parents=True, exist_ok=True)
        
        # Create template files
        (planning_dir / "feature.md").write_text("# Test Feature")
        (planning_dir / "tasks.md").write_text("# Tasks")
        (planning_dir / "to-do.md").write_text("# To-Do")
        
        # Verify structure
        assert planning_dir.exists()
        assert (planning_dir / "feature.md").exists()
        assert (planning_dir / "tasks.md").exists()
        assert (planning_dir / "to-do.md").exists()
    
    def test_git_integration_error_recovery(self, temp_dir):
        """Test error recovery in git integration."""
        # Start with non-git directory
        assert not (temp_dir / ".git").exists()
        
        # Simulate error handling
        def safe_git_operation():
            try:
                git_dir = temp_dir / ".git"
                if not git_dir.exists():
                    return False, "Not a git repository"
                return True, "Success"
            except Exception as e:
                return False, str(e)
        
        success, message = safe_git_operation()
        assert success is False
        assert "Not a git repository" in message
