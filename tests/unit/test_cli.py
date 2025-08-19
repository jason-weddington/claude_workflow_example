"""
Unit tests for the CLI module (claude_workflow.cli).
"""

import argparse
import sys
from pathlib import Path
from unittest.mock import Mock, patch, call
from io import StringIO

import pytest

from claude_workflow import cli


class TestCreateCommand:
    """Test the create_command functionality."""
    
    def test_create_command_nonexistent_directory(self):
        """Test create_command with non-existent directory."""
        args = argparse.Namespace(
            path="/non/existent/directory",
            amazonq=False
        )
        
        result = cli.create_command(args)
        assert result == 1
    
    @patch('claude_workflow.cli.input')
    def test_create_command_non_git_repo_decline(self, mock_input, temp_dir):
        """Test create_command in non-git directory with user declining."""
        mock_input.return_value = 'n'
        
        args = argparse.Namespace(
            path=str(temp_dir),
            amazonq=False
        )
        
        result = cli.create_command(args)
        assert result == 1
    
    @patch('claude_workflow.cli.input')
    @patch('claude_workflow.cli.pkg_resources')
    def test_create_command_non_git_repo_accept(self, mock_pkg_resources, mock_input, temp_dir, sample_templates_dir):
        """Test create_command in non-git directory with user accepting."""
        mock_input.return_value = 'y'
        mock_pkg_resources.files.return_value = sample_templates_dir.parent
        
        args = argparse.Namespace(
            path=str(temp_dir),
            amazonq=False
        )
        
        result = cli.create_command(args)
        assert result == 0
        assert (temp_dir / "CLAUDE.md").exists()
    
    def test_create_command_git_repo_success(self, temp_git_repo, sample_templates_dir):
        """Test successful create_command in git repository."""
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = argparse.Namespace(
                path=str(temp_git_repo),
                amazonq=False
            )
            
            result = cli.create_command(args)
            assert result == 0
            assert (temp_git_repo / "CLAUDE.md").exists()
    
    def test_create_command_amazonq_variant(self, temp_git_repo, sample_templates_dir):
        """Test create_command with Amazon Q variant."""
        with patch('claude_workflow.cli.pkg_resources') as mock_pkg:
            mock_pkg.files.return_value = sample_templates_dir.parent
            
            args = argparse.Namespace(
                path=str(temp_git_repo),
                amazonq=True
            )
            
            result = cli.create_command(args)
            assert result == 0
            assert (temp_git_repo / "AmazonQ.md").exists()


class TestNewProjectCommand:
    """Test the new_project_command functionality."""
    
    @patch('claude_workflow.new_project.main')
    def test_new_project_command_calls_main(self, mock_main):
        """Test that new_project_command calls new_project.main."""
        mock_main.return_value = 0
        
        args = argparse.Namespace()
        result = cli.new_project_command(args)
        
        mock_main.assert_called_once()
        assert result == 0


class TestUpdateCommand:
    """Test the update_command functionality."""
    
    def test_update_command_no_agent_file(self, temp_dir):
        """Test that update command returns error when no agent file found."""
        # Change to temp directory without CLAUDE.md or AmazonQ.md
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            args = argparse.Namespace()
            result = cli.update_command(args)
            
            # Should return 1 when no agent file is found
            assert result == 1
            
        finally:
            os.chdir(original_cwd)
    
    def test_update_command_with_claude_file(self, temp_dir):
        """Test update command when CLAUDE.md exists."""
        # Create CLAUDE.md file
        (temp_dir / "CLAUDE.md").write_text("# CLAUDE.md")
        
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            args = argparse.Namespace()
            result = cli.update_command(args)
            
            # Should return 0 when agent file exists
            assert result == 0
            
        finally:
            os.chdir(original_cwd)


class TestMainFunction:
    """Test the main entry point function."""
    
    @patch('sys.argv', ['claude-workflow', 'init', '.', '--amazonq'])
    @patch('claude_workflow.cli.create_command')
    def test_main_with_init_command(self, mock_create_command, temp_dir):
        """Test main function with init command."""
        mock_create_command.return_value = 0
        
        # Change to temp directory
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            result = cli.main()
            assert result == 0
            mock_create_command.assert_called_once()
        finally:
            os.chdir(original_cwd)
    
    @patch('sys.argv', ['claude-workflow', 'new'])
    @patch('claude_workflow.new_project.main')
    def test_main_with_new_command(self, mock_new_main):
        """Test main function with new command."""
        mock_new_main.return_value = 0
        
        result = cli.main()
        assert result == 0
        mock_new_main.assert_called_once()
    
    @patch('sys.argv', ['claude-workflow'])
    def test_main_no_command_shows_help(self):
        """Test main function with no command shows help."""
        result = cli.main()
        assert result == 1


class TestArgumentParsing:
    """Test argument parsing through main function."""
    
    @patch('sys.argv', ['claude-workflow', 'init', '/tmp/test'])
    @patch('claude_workflow.cli.create_command')
    def test_init_argument_parsing(self, mock_create_command):
        """Test that init arguments are parsed correctly."""
        mock_create_command.return_value = 0
        
        cli.main()
        
        # Verify create_command was called with correct args
        mock_create_command.assert_called_once()
        args = mock_create_command.call_args[0][0]
        assert args.path == '/tmp/test'
        assert args.amazonq is False
    
    @patch('sys.argv', ['claude-workflow', 'init', '/tmp/test', '--amazonq'])
    @patch('claude_workflow.cli.create_command')
    def test_init_amazonq_argument_parsing(self, mock_create_command):
        """Test that init --amazonq arguments are parsed correctly."""
        mock_create_command.return_value = 0
        
        cli.main()
        
        # Verify create_command was called with correct args
        mock_create_command.assert_called_once()
        args = mock_create_command.call_args[0][0]
        assert args.path == '/tmp/test'
        assert args.amazonq is True


@pytest.mark.unit
class TestCLIIntegration:
    """Integration tests for CLI components working together."""
    
    def test_cli_help_output(self):
        """Test that CLI help is displayed correctly."""
        with patch('sys.argv', ['claude-workflow', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                cli.main()
            assert exc_info.value.code == 0
    
    @patch('sys.argv', ['claude-workflow', 'invalid-command'])
    def test_invalid_command_handling(self):
        """Test handling of invalid commands."""
        with pytest.raises(SystemExit) as exc_info:
            cli.main()
        assert exc_info.value.code == 2
