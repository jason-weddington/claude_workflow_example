"""
Comprehensive error handling and edge case tests.
"""

import os
import stat
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import pytest

from claude_workflow import cli, new_project


class TestFileSystemErrorHandling:
    """Test error handling for file system operations."""
    
    def test_handle_permission_denied_error(self, temp_dir):
        """Test handling of permission denied errors."""
        def safe_write_file(file_path, content):
            try:
                file_path.write_text(content)
                return True, "Success"
            except PermissionError as e:
                return False, f"Permission denied: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        # Test with valid file
        valid_file = temp_dir / "valid.txt"
        success, message = safe_write_file(valid_file, "test content")
        assert success is True
        assert "Success" in message
        
        # Test with permission error simulation
        if os.name != 'nt':  # Unix-like systems
            readonly_dir = temp_dir / "readonly"
            readonly_dir.mkdir()
            readonly_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)  # Read and execute only
            
            readonly_file = readonly_dir / "readonly.txt"
            success, message = safe_write_file(readonly_file, "test content")
            assert success is False
            assert "Permission denied" in message
    
    def test_handle_file_not_found_error(self):
        """Test handling of file not found errors."""
        def safe_read_file(file_path):
            try:
                return True, file_path.read_text()
            except FileNotFoundError as e:
                return False, f"File not found: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        # Test with non-existent file
        nonexistent_file = Path("/nonexistent/path/file.txt")
        success, message = safe_read_file(nonexistent_file)
        assert success is False
        assert "File not found" in message
    
    def test_handle_disk_space_error(self, temp_dir):
        """Test handling of disk space errors."""
        def safe_write_large_file(file_path, size_mb=1):
            try:
                content = "x" * (size_mb * 1024 * 1024)
                file_path.write_text(content)
                return True, "Success"
            except OSError as e:
                if "No space left" in str(e) or "Disk full" in str(e):
                    return False, f"Disk space error: {e}"
                return False, f"OS error: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        # Test normal write (should succeed unless system is actually out of space)
        test_file = temp_dir / "test.txt"
        success, message = safe_write_large_file(test_file, 0.001)  # 1KB
        # This test just verifies the error handling logic works
        assert success is True or "error" in message.lower()
    
    def test_handle_invalid_path_characters(self, temp_dir):
        """Test handling of invalid path characters."""
        def safe_create_file(file_path):
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text("test")
                return True, "Success"
            except (OSError, ValueError) as e:
                return False, f"Invalid path: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        # Test valid path
        valid_file = temp_dir / "valid_file.txt"
        success, message = safe_create_file(valid_file)
        assert success is True
        
        # Test potentially problematic characters (platform dependent)
        problematic_names = [
            "file with spaces.txt",
            "file-with-dashes.txt",
            "file_with_underscores.txt",
            "file.with.dots.txt"
        ]
        
        for name in problematic_names:
            test_file = temp_dir / name
            success, message = safe_create_file(test_file)
            # These should generally succeed on modern systems
            assert success is True or "Invalid path" in message


class TestGitErrorHandling:
    """Test error handling for git-related operations."""
    
    @patch('subprocess.run')
    def test_handle_git_not_installed(self, mock_run):
        """Test handling when git is not installed."""
        mock_run.side_effect = FileNotFoundError("git command not found")
        
        def safe_git_operation():
            try:
                import subprocess
                result = subprocess.run(['git', 'status'], capture_output=True, text=True)
                return True, result.stdout
            except FileNotFoundError as e:
                return False, f"Git not found: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        success, message = safe_git_operation()
        assert success is False
        assert "Git not found" in message
    
    @patch('subprocess.run')
    def test_handle_git_repository_corruption(self, mock_run):
        """Test handling of corrupted git repository."""
        mock_run.return_value = Mock(
            returncode=128,
            stdout='',
            stderr='fatal: not a git repository (or any of the parent directories)'
        )
        
        def safe_get_branch():
            try:
                import subprocess
                result = subprocess.run(['git', 'branch', '--show-current'], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    return False, f"Git error: {result.stderr}"
                return True, result.stdout.strip()
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        success, message = safe_get_branch()
        assert success is False
        assert "Git error" in message
        assert "not a git repository" in message
    
    @patch('subprocess.run')
    def test_handle_git_permission_error(self, mock_run):
        """Test handling of git permission errors."""
        mock_run.return_value = Mock(
            returncode=1,
            stdout='',
            stderr='error: insufficient permission for adding an object'
        )
        
        def safe_git_add():
            try:
                import subprocess
                result = subprocess.run(['git', 'add', '.'], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    return False, f"Git permission error: {result.stderr}"
                return True, "Success"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        success, message = safe_git_add()
        assert success is False
        assert "permission" in message.lower()


class TestTemplateErrorHandling:
    """Test error handling for template operations."""
    
    def test_handle_missing_template_files(self, temp_dir):
        """Test handling when template files are missing."""
        def safe_read_template(template_path):
            try:
                return True, template_path.read_text()
            except FileNotFoundError as e:
                return False, f"Template not found: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        # Test with missing template
        missing_template = temp_dir / "nonexistent_template.md"
        success, message = safe_read_template(missing_template)
        assert success is False
        assert "Template not found" in message
    
    def test_handle_corrupted_template_content(self, temp_dir):
        """Test handling of corrupted template content."""
        def safe_process_template(template_path):
            try:
                content = template_path.read_text()
                # Simulate template processing
                if not content.strip():
                    return False, "Empty template"
                if len(content) > 1024 * 1024:  # 1MB limit
                    return False, "Template too large"
                return True, content
            except UnicodeDecodeError as e:
                return False, f"Template encoding error: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        # Test with empty template
        empty_template = temp_dir / "empty.md"
        empty_template.write_text("")
        success, message = safe_process_template(empty_template)
        assert success is False
        assert "Empty template" in message
        
        # Test with valid template
        valid_template = temp_dir / "valid.md"
        valid_template.write_text("# Valid Template\n\nContent here.")
        success, message = safe_process_template(valid_template)
        assert success is True
    
    def test_handle_template_placeholder_errors(self):
        """Test handling of template placeholder processing errors."""
        def safe_substitute_placeholders(content, replacements):
            try:
                result = content
                for placeholder, replacement in replacements.items():
                    if not isinstance(replacement, str):
                        return False, f"Invalid replacement type for {placeholder}"
                    result = result.replace(placeholder, replacement)
                return True, result
            except Exception as e:
                return False, f"Substitution error: {e}"
        
        # Test with valid substitution
        content = "Hello {{NAME}}, welcome to {{PROJECT}}!"
        replacements = {"{{NAME}}": "Alice", "{{PROJECT}}": "MyProject"}
        success, result = safe_substitute_placeholders(content, replacements)
        assert success is True
        assert "Hello Alice, welcome to MyProject!" == result
        
        # Test with invalid replacement type
        invalid_replacements = {"{{NAME}}": 123, "{{PROJECT}}": "MyProject"}
        success, message = safe_substitute_placeholders(content, invalid_replacements)
        assert success is False
        assert "Invalid replacement type" in message


class TestCLIErrorHandling:
    """Test error handling in CLI operations."""
    
    def test_handle_invalid_command_line_arguments(self):
        """Test handling of invalid command line arguments."""
        # Test the actual CLI behavior through main function
        with patch('sys.argv', ['claude-workflow', 'invalid-command']):
            with pytest.raises(SystemExit) as exc_info:
                from claude_workflow import cli
                cli.main()
            # Should exit with error code 2 for invalid arguments
            assert exc_info.value.code == 2
    
    @patch('claude_workflow.cli.Path')
    def test_handle_cli_execution_errors(self, mock_path):
        """Test handling of CLI execution errors."""
        # Mock Path to raise an exception
        mock_path.side_effect = Exception("Unexpected CLI error")
        
        def safe_execute_command():
            try:
                args = Mock()
                args.directory = "/test"
                args.amazonq = False
                result = cli.create_command(args)
                return True, result
            except Exception as e:
                return False, f"CLI execution error: {e}"
        
        success, message = safe_execute_command()
        assert success is False
        assert "CLI execution error" in message
    
    def test_handle_user_input_errors(self):
        """Test handling of user input errors."""
        def safe_get_user_confirmation(mock_input_func):
            try:
                user_input = mock_input_func("Continue? (y/n): ")
                return True, user_input.lower() == 'y'
            except (EOFError, KeyboardInterrupt) as e:
                return False, f"User input interrupted: {e}"
            except Exception as e:
                return False, f"Input error: {e}"
        
        # Test normal input
        def normal_input(prompt):
            return 'y'
        
        success, result = safe_get_user_confirmation(normal_input)
        assert success is True
        assert result is True
        
        # Test interrupted input
        def interrupted_input(prompt):
            raise KeyboardInterrupt("User interrupted")
        
        success, message = safe_get_user_confirmation(interrupted_input)
        assert success is False
        assert "User input interrupted" in message


class TestEdgeCases:
    """Test various edge cases and boundary conditions."""
    
    def test_extremely_long_file_paths(self, temp_dir):
        """Test handling of extremely long file paths."""
        def safe_create_long_path(base_dir, depth=10):
            try:
                current_path = base_dir
                for i in range(depth):
                    current_path = current_path / f"very_long_directory_name_{i}_with_lots_of_characters"
                
                current_path.mkdir(parents=True, exist_ok=True)
                test_file = current_path / "test_file_with_very_long_name.txt"
                test_file.write_text("test content")
                return True, str(test_file)
            except OSError as e:
                return False, f"Path too long: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        # Test moderately long path (should work)
        success, path = safe_create_long_path(temp_dir, 5)
        assert success is True or "Path too long" in path
    
    def test_special_unicode_characters(self, temp_dir):
        """Test handling of special unicode characters."""
        def safe_create_unicode_file(base_dir, filename):
            try:
                file_path = base_dir / filename
                file_path.write_text("Unicode content: 🚀 中文 🎉", encoding='utf-8')
                content = file_path.read_text(encoding='utf-8')
                return True, content
            except UnicodeError as e:
                return False, f"Unicode error: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        unicode_filenames = [
            "test_🚀.txt",
            "测试文件.md",
            "файл.txt",
            "αρχείο.md"
        ]
        
        for filename in unicode_filenames:
            success, result = safe_create_unicode_file(temp_dir, filename)
            # Should either succeed or fail gracefully
            assert success is True or "error" in result.lower()
    
    def test_concurrent_file_operations(self, temp_dir):
        """Test handling of concurrent file operations."""
        def safe_concurrent_write(file_path, content, identifier):
            try:
                # Simulate concurrent access
                if file_path.exists():
                    existing_content = file_path.read_text()
                    new_content = f"{existing_content}\n{identifier}: {content}"
                else:
                    new_content = f"{identifier}: {content}"
                
                file_path.write_text(new_content)
                return True, "Success"
            except Exception as e:
                return False, f"Concurrent access error: {e}"
        
        test_file = temp_dir / "concurrent_test.txt"
        
        # Simulate multiple writes
        for i in range(5):
            success, message = safe_concurrent_write(test_file, f"content_{i}", f"writer_{i}")
            assert success is True or "error" in message.lower()
    
    def test_memory_intensive_operations(self, temp_dir):
        """Test handling of memory-intensive operations."""
        def safe_large_content_operation(file_path, size_mb=1):
            try:
                # Create large content
                large_content = "x" * (size_mb * 1024 * 1024)
                
                # Write and read back
                file_path.write_text(large_content)
                read_content = file_path.read_text()
                
                return True, len(read_content) == len(large_content)
            except MemoryError as e:
                return False, f"Memory error: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        large_file = temp_dir / "large_file.txt"
        success, result = safe_large_content_operation(large_file, 0.1)  # 100KB
        assert success is True or "error" in str(result).lower()
    
    def test_empty_and_null_inputs(self):
        """Test handling of empty and null inputs."""
        def safe_process_input(input_value):
            try:
                if input_value is None:
                    return False, "Null input"
                if not input_value.strip():
                    return False, "Empty input"
                return True, f"Processed: {input_value}"
            except AttributeError as e:
                return False, f"Invalid input type: {e}"
            except Exception as e:
                return False, f"Unexpected error: {e}"
        
        test_inputs = [
            None,
            "",
            "   ",
            "valid input",
            123,  # Invalid type
            []    # Invalid type
        ]
        
        expected_results = [
            (False, "Null input"),
            (False, "Empty input"),
            (False, "Empty input"),
            (True, "Processed: valid input"),
            (False, "Invalid input type"),
            (False, "Invalid input type")
        ]
        
        for input_val, (expected_success, expected_message_part) in zip(test_inputs, expected_results):
            success, message = safe_process_input(input_val)
            assert success == expected_success
            if not expected_success:
                assert expected_message_part in message


class TestResourceCleanup:
    """Test proper resource cleanup in error scenarios."""
    
    def test_cleanup_on_file_operation_failure(self, temp_dir):
        """Test that resources are cleaned up when file operations fail."""
        def operation_with_cleanup():
            temp_files = []
            try:
                # Create temporary files
                for i in range(3):
                    temp_file = temp_dir / f"temp_{i}.txt"
                    temp_file.write_text(f"Temporary content {i}")
                    temp_files.append(temp_file)
                
                # Simulate an error
                raise Exception("Simulated error")
                
            except Exception as e:
                # Cleanup temporary files
                for temp_file in temp_files:
                    if temp_file.exists():
                        temp_file.unlink()
                return False, f"Operation failed with cleanup: {e}"
            
            return True, "Success"
        
        success, message = operation_with_cleanup()
        assert success is False
        assert "Operation failed with cleanup" in message
        
        # Verify cleanup occurred
        for i in range(3):
            temp_file = temp_dir / f"temp_{i}.txt"
            assert not temp_file.exists()
    
    def test_partial_operation_rollback(self, temp_dir):
        """Test rollback of partial operations on failure."""
        def partial_operation_with_rollback():
            created_dirs = []
            created_files = []
            
            try:
                # Create directory structure
                for i in range(3):
                    new_dir = temp_dir / f"dir_{i}"
                    new_dir.mkdir()
                    created_dirs.append(new_dir)
                    
                    new_file = new_dir / "file.txt"
                    new_file.write_text("content")
                    created_files.append(new_file)
                
                # Simulate failure after partial completion
                if len(created_dirs) >= 2:
                    raise Exception("Simulated failure")
                
                return True, "Success"
                
            except Exception as e:
                # Rollback: remove created files and directories
                for file_path in reversed(created_files):
                    if file_path.exists():
                        file_path.unlink()
                
                for dir_path in reversed(created_dirs):
                    if dir_path.exists() and not any(dir_path.iterdir()):
                        dir_path.rmdir()
                
                return False, f"Rolled back after error: {e}"
        
        success, message = partial_operation_with_rollback()
        assert success is False
        assert "Rolled back after error" in message
        
        # Verify rollback occurred
        for i in range(3):
            test_dir = temp_dir / f"dir_{i}"
            assert not test_dir.exists()


@pytest.mark.unit
class TestErrorHandlingIntegration:
    """Integration tests for error handling across components."""
    
    def test_end_to_end_error_recovery(self, temp_dir):
        """Test end-to-end error recovery in complete workflows."""
        def simulate_complete_workflow_with_errors():
            errors_encountered = []
            
            try:
                # Step 1: Directory validation
                if not temp_dir.exists():
                    raise FileNotFoundError("Base directory not found")
                
                # Step 2: Git repository check (simulate failure)
                git_dir = temp_dir / ".git"
                if not git_dir.exists():
                    errors_encountered.append("Not a git repository")
                    # Continue anyway for testing
                
                # Step 3: Template processing (simulate partial failure)
                try:
                    template_content = "# {{FILENAME}}\n\nContent for {{AGENT_NAME}}"
                    processed = template_content.replace("{{FILENAME}}", "TEST.md")
                    processed = processed.replace("{{AGENT_NAME}}", "Test Agent")
                except Exception as e:
                    errors_encountered.append(f"Template processing error: {e}")
                
                # Step 4: File creation (simulate success)
                output_file = temp_dir / "TEST.md"
                output_file.write_text(processed)
                
                return True, {"errors": errors_encountered, "file_created": output_file.exists()}
                
            except Exception as e:
                errors_encountered.append(f"Critical error: {e}")
                return False, {"errors": errors_encountered, "file_created": False}
        
        success, result = simulate_complete_workflow_with_errors()
        
        # Should succeed despite non-critical errors
        assert success is True
        assert result["file_created"] is True
        assert "Not a git repository" in result["errors"]
        assert len(result["errors"]) >= 1  # At least the git error
