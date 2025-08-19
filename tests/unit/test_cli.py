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


class TestArgumentParsing:
    """Test CLI argument parsing functionality."""
    
    def test_main_parser_creation(self):
        """Test that main parser is created correctly."""
        parser = cli.create_parser()
        assert isinstance(parser, argparse.ArgumentParser)
        assert parser.prog == 'claude-workflow'
    
    def test_init_subcommand_parsing(self):
        """Test init subcommand argument parsing."""
        parser = cli.create_parser()
        
        # Test basic init command
        args = parser.parse_args(['init', '.'])
        assert args.command == 'init'
        assert args.directory == '.'
        assert args.amazonq is False
        
        # Test init with amazonq flag
        args = parser.parse_args(['init', '/tmp/test', '--amazonq'])
        assert args.command == 'init'
        assert args.directory == '/tmp/test'
        assert args.amazonq is True
    
    def test_new_subcommand_parsing(self):
        """Test new subcommand argument parsing."""
        parser = cli.create_parser()
        
        args = parser.parse_args(['new'])
        assert args.command == 'new'
    
    def test_update_subcommand_parsing(self):
        """Test update subcommand argument parsing."""
        parser = cli.create_parser()
        
        args = parser.parse_args(['update'])
        assert args.command == 'update'
    
    def test_help_generation(self):
        """Test that help messages are generated correctly."""
        parser = cli.create_parser()
        
        with pytest.raises(SystemExit):
            parser.parse_args(['--help'])
    
    def test_invalid_arguments(self):
        """Test handling of invalid arguments."""
        parser = cli.create_parser()
        
        with pytest.raises(SystemExit):
            parser.parse_args(['invalid-command'])
        
        with pytest.raises(SystemExit):
            parser.parse_args(['init'])  # Missing directory argument


class TestCreateCommand:
    """Test the create_command (init) functionality."""
    
    @patch('claude_workflow.cli.Path')
    @patch('claude_workflow.cli.pkg_resources')
    def test_create_command_success_claude(self, mock_pkg_resources, mock_path, temp_dir, sample_templates_dir):
        """Test successful init command for Claude."""
        # Setup mocks
        mock_path.return_value = temp_dir
        mock_pkg_resources.files.return_value = sample_templates_dir.parent
        
        # Mock template file
        template_file = Mock()
        template_file.read_text.return_value = "# {{FILENAME}} Template\n\nAgent: {{AGENT_NAME}}"
        (sample_templates_dir / "agent_instructions.md").write_text("# {{FILENAME}} Template\n\nAgent: {{AGENT_NAME}}")
        
        # Create mock args
        args = Mock()
        args.directory = str(temp_dir)
        args.amazonq = False
        
        # Test the command
        result = cli.create_command(args)
        
        assert result == 0
        assert (temp_dir / "CLAUDE.md").exists()
        content = (temp_dir / "CLAUDE.md").read_text()
        assert "CLAUDE.md" in content
        assert "Claude" in content
    
    @patch('claude_workflow.cli.Path')
    @patch('claude_workflow.cli.pkg_resources')
    def test_create_command_success_amazonq(self, mock_pkg_resources, mock_path, temp_dir, sample_templates_dir):
        """Test successful init command for Amazon Q."""
        # Setup mocks
        mock_path.return_value = temp_dir
        mock_pkg_resources.files.return_value = sample_templates_dir.parent
        
        # Mock template file
        (sample_templates_dir / "agent_instructions.md").write_text("# {{FILENAME}} Template\n\nAgent: {{AGENT_NAME}}")
        
        # Create mock args
        args = Mock()
        args.directory = str(temp_dir)
        args.amazonq = True
        
        # Test the command
        result = cli.create_command(args)
        
        assert result == 0
        assert (temp_dir / "AmazonQ.md").exists()
        content = (temp_dir / "AmazonQ.md").read_text()
        assert "AmazonQ.md" in content
        assert "Amazon Q" in content
    
    def test_create_command_directory_not_exists(self):
        """Test init command with non-existent directory."""
        args = Mock()
        args.directory = "/non/existent/directory"
        args.amazonq = False
        
        result = cli.create_command(args)
        assert result == 1
    
    @patch('claude_workflow.cli.input')
    @patch('claude_workflow.cli.Path')
    def test_create_command_non_git_repo_decline(self, mock_path, mock_input, temp_dir):
        """Test init command in non-git directory with user declining."""
        mock_path.return_value = temp_dir
        mock_input.return_value = 'n'
        
        args = Mock()
        args.directory = str(temp_dir)
        args.amazonq = False
        
        result = cli.create_command(args)
        assert result == 1
    
    @patch('claude_workflow.cli.input')
    @patch('claude_workflow.cli.Path')
    @patch('claude_workflow.cli.pkg_resources')
    def test_create_command_non_git_repo_accept(self, mock_pkg_resources, mock_path, mock_input, temp_dir, sample_templates_dir):
        """Test init command in non-git directory with user accepting."""
        mock_path.return_value = temp_dir
        mock_input.return_value = 'y'
        mock_pkg_resources.files.return_value = sample_templates_dir.parent
        
        (sample_templates_dir / "agent_instructions.md").write_text("# {{FILENAME}} Template")
        
        args = Mock()
        args.directory = str(temp_dir)
        args.amazonq = False
        
        result = cli.create_command(args)
        assert result == 0


class TestNewProjectCommand:
    """Test the new_project_command functionality."""
    
    @patch('claude_workflow.new_project.create_project_structure')
    def test_new_project_command_success(self, mock_create_structure):
        """Test successful new project command."""
        mock_create_structure.return_value = 0
        
        result = cli.new_project_command(Mock())
        assert result == 0
        mock_create_structure.assert_called_once()
    
    @patch('claude_workflow.new_project.create_project_structure')
    def test_new_project_command_failure(self, mock_create_structure):
        """Test new project command failure."""
        mock_create_structure.return_value = 1
        
        result = cli.new_project_command(Mock())
        assert result == 1


class TestUpdateCommand:
    """Test the update_command functionality."""
    
    def test_update_command_not_implemented(self):
        """Test that update command returns not implemented."""
        result = cli.update_command(Mock())
        assert result == 1


class TestMainFunction:
    """Test the main entry point function."""
    
    @patch('claude_workflow.cli.create_command')
    @patch('sys.argv', ['claude-workflow', 'init', '.'])
    def test_main_init_command(self, mock_create_command):
        """Test main function with init command."""
        mock_create_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            cli.main()
            mock_exit.assert_called_with(0)
    
    @patch('claude_workflow.cli.new_project_command')
    @patch('sys.argv', ['claude-workflow', 'new'])
    def test_main_new_command(self, mock_new_command):
        """Test main function with new command."""
        mock_new_command.return_value = 0
        
        with patch('sys.exit') as mock_exit:
            cli.main()
            mock_exit.assert_called_with(0)
    
    @patch('claude_workflow.cli.update_command')
    @patch('sys.argv', ['claude-workflow', 'update'])
    def test_main_update_command(self, mock_update_command):
        """Test main function with update command."""
        mock_update_command.return_value = 1
        
        with patch('sys.exit') as mock_exit:
            cli.main()
            mock_exit.assert_called_with(1)
    
    @patch('sys.argv', ['claude-workflow', '--help'])
    def test_main_help(self):
        """Test main function with help flag."""
        with patch('sys.exit') as mock_exit:
            cli.main()
            mock_exit.assert_called_with(0)
    
    @patch('sys.argv', ['claude-workflow', 'invalid'])
    def test_main_invalid_command(self):
        """Test main function with invalid command."""
        with patch('sys.exit') as mock_exit:
            cli.main()
            mock_exit.assert_called_with(2)


class TestErrorHandling:
    """Test error handling in CLI functions."""
    
    @patch('claude_workflow.cli.Path')
    def test_create_command_exception_handling(self, mock_path):
        """Test that exceptions in create_command are handled gracefully."""
        mock_path.side_effect = Exception("Test exception")
        
        args = Mock()
        args.directory = "/test"
        args.amazonq = False
        
        result = cli.create_command(args)
        assert result == 1
    
    def test_command_routing_with_none_args(self):
        """Test command routing with None args."""
        # This should not crash
        result = cli.main()
        # The function should handle this gracefully


@pytest.mark.unit
class TestCLIIntegration:
    """Integration tests for CLI components working together."""
    
    def test_parser_and_command_integration(self):
        """Test that parser output works with command functions."""
        parser = cli.create_parser()
        
        # Test init command integration
        args = parser.parse_args(['init', '.', '--amazonq'])
        assert hasattr(args, 'command')
        assert hasattr(args, 'directory')
        assert hasattr(args, 'amazonq')
        
        # Test new command integration
        args = parser.parse_args(['new'])
        assert hasattr(args, 'command')
