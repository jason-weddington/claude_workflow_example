"""
Unit tests for file operations functionality.
"""

import os
import stat
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import pytest

from claude_workflow import cli


class TestDirectoryCreation:
    """Test directory creation operations."""
    
    def test_create_single_directory(self, temp_dir):
        """Test creating a single directory."""
        new_dir = temp_dir / "test_directory"
        
        new_dir.mkdir()
        
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_create_nested_directories(self, temp_dir):
        """Test creating nested directory structure."""
        nested_dir = temp_dir / "level1" / "level2" / "level3"
        
        nested_dir.mkdir(parents=True, exist_ok=True)
        
        assert nested_dir.exists()
        assert nested_dir.is_dir()
        assert (temp_dir / "level1").exists()
        assert (temp_dir / "level1" / "level2").exists()
    
    def test_create_directory_with_exist_ok(self, temp_dir):
        """Test creating directory with exist_ok=True."""
        test_dir = temp_dir / "existing_dir"
        test_dir.mkdir()
        
        # Should not raise error when directory already exists
        test_dir.mkdir(exist_ok=True)
        
        assert test_dir.exists()
    
    def test_create_directory_without_exist_ok(self, temp_dir):
        """Test creating directory without exist_ok raises error."""
        test_dir = temp_dir / "existing_dir"
        test_dir.mkdir()
        
        # Should raise error when directory already exists
        with pytest.raises(FileExistsError):
            test_dir.mkdir(exist_ok=False)
    
    def test_create_directory_structure_for_planning(self, temp_dir):
        """Test creating the planning directory structure."""
        docs_dir = temp_dir / "docs"
        planning_dir = temp_dir / "planning"
        templates_dir = planning_dir / "templates"
        branch_dir = planning_dir / "feature" / "test-feature"
        
        # Create structure
        docs_dir.mkdir(parents=True, exist_ok=True)
        planning_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)
        branch_dir.mkdir(parents=True, exist_ok=True)
        
        assert docs_dir.exists()
        assert planning_dir.exists()
        assert templates_dir.exists()
        assert branch_dir.exists()


class TestFileCopyOperations:
    """Test file copying operations."""
    
    def test_copy_single_file(self, temp_dir):
        """Test copying a single file."""
        source_file = temp_dir / "source.txt"
        dest_file = temp_dir / "dest.txt"
        
        source_file.write_text("Test content")
        
        # Copy file
        dest_file.write_text(source_file.read_text())
        
        assert dest_file.exists()
        assert dest_file.read_text() == "Test content"
    
    def test_copy_file_to_different_directory(self, temp_dir):
        """Test copying file to different directory."""
        source_file = temp_dir / "source.txt"
        dest_dir = temp_dir / "destination"
        dest_file = dest_dir / "source.txt"
        
        source_file.write_text("Test content")
        dest_dir.mkdir()
        
        # Copy file
        dest_file.write_text(source_file.read_text())
        
        assert dest_file.exists()
        assert dest_file.read_text() == source_file.read_text()
    
    def test_copy_template_files(self, temp_dir, sample_templates_dir):
        """Test copying template files to target directory."""
        target_dir = temp_dir / "target"
        target_dir.mkdir()
        
        # Copy all template files
        for template_file in sample_templates_dir.glob("*.md"):
            target_file = target_dir / template_file.name
            target_file.write_text(template_file.read_text())
        
        # Verify all files copied
        assert (target_dir / "agent_instructions.md").exists()
        assert (target_dir / "feature.md").exists()
        assert (target_dir / "tasks.md").exists()
        assert (target_dir / "to-do.md").exists()
    
    def test_overwrite_existing_file(self, temp_dir):
        """Test overwriting existing file."""
        test_file = temp_dir / "test.txt"
        
        test_file.write_text("Original content")
        assert test_file.read_text() == "Original content"
        
        test_file.write_text("New content")
        assert test_file.read_text() == "New content"
    
    def test_copy_file_with_different_content(self, temp_dir):
        """Test copying files with different content types."""
        # Text file
        text_file = temp_dir / "text.txt"
        text_file.write_text("Text content with unicode: 🚀")
        
        # Markdown file
        md_file = temp_dir / "test.md"
        md_file.write_text("# Markdown\n\n- List item")
        
        # Copy and verify
        text_copy = temp_dir / "text_copy.txt"
        md_copy = temp_dir / "md_copy.md"
        
        text_copy.write_text(text_file.read_text())
        md_copy.write_text(md_file.read_text())
        
        assert text_copy.read_text() == "Text content with unicode: 🚀"
        assert md_copy.read_text() == "# Markdown\n\n- List item"


class TestFilePermissions:
    """Test file permission operations."""
    
    def test_set_file_readable(self, temp_dir):
        """Test setting file as readable."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")
        
        # Make readable
        test_file.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        
        # Should be able to read
        assert test_file.read_text() == "Test content"
    
    def test_set_file_writable(self, temp_dir):
        """Test setting file as writable."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Original content")
        
        # Make writable
        test_file.chmod(stat.S_IRUSR | stat.S_IWUSR)
        
        # Should be able to write
        test_file.write_text("Modified content")
        assert test_file.read_text() == "Modified content"
    
    @pytest.mark.skipif(os.name == 'nt', reason="Unix permissions not applicable on Windows")
    def test_set_file_executable(self, temp_dir):
        """Test setting file as executable (Unix only)."""
        script_file = temp_dir / "script.sh"
        script_file.write_text("#!/bin/bash\necho 'Hello'")
        
        # Make executable
        script_file.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        
        # Check permissions
        file_stat = script_file.stat()
        assert file_stat.st_mode & stat.S_IXUSR


class TestPathHandling:
    """Test path handling operations."""
    
    def test_absolute_path_handling(self, temp_dir):
        """Test handling absolute paths."""
        abs_path = temp_dir.resolve()
        test_file = abs_path / "test.txt"
        
        test_file.write_text("Test content")
        
        assert test_file.is_absolute()
        assert test_file.exists()
    
    def test_relative_path_handling(self, temp_dir):
        """Test handling relative paths."""
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            rel_path = Path("test.txt")
            rel_path.write_text("Test content")
            
            assert not rel_path.is_absolute()
            assert rel_path.exists()
        finally:
            os.chdir(original_cwd)
    
    def test_path_resolution(self, temp_dir):
        """Test path resolution with .. and . components."""
        nested_dir = temp_dir / "nested"
        nested_dir.mkdir()
        
        # Create path with .. component
        complex_path = nested_dir / ".." / "test.txt"
        resolved_path = complex_path.resolve()
        
        assert resolved_path == temp_dir / "test.txt"
    
    def test_cross_platform_path_handling(self, temp_dir):
        """Test cross-platform path handling."""
        # Test with forward slashes (should work on all platforms)
        path_with_slashes = temp_dir / "sub/dir/file.txt"
        path_with_slashes.parent.mkdir(parents=True, exist_ok=True)
        path_with_slashes.write_text("Test")
        
        assert path_with_slashes.exists()
        assert path_with_slashes.read_text() == "Test"


class TestErrorHandling:
    """Test error handling in file operations."""
    
    def test_read_nonexistent_file(self, temp_dir):
        """Test reading non-existent file raises error."""
        nonexistent_file = temp_dir / "nonexistent.txt"
        
        with pytest.raises(FileNotFoundError):
            nonexistent_file.read_text()
    
    def test_write_to_readonly_directory(self, temp_dir):
        """Test writing to read-only directory."""
        readonly_dir = temp_dir / "readonly"
        readonly_dir.mkdir()
        
        # Make directory read-only (Unix only)
        if os.name != 'nt':
            readonly_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)
            
            test_file = readonly_dir / "test.txt"
            with pytest.raises(PermissionError):
                test_file.write_text("Test content")
    
    def test_create_directory_in_nonexistent_parent(self, temp_dir):
        """Test creating directory when parent doesn't exist."""
        nested_dir = temp_dir / "nonexistent" / "nested"
        
        # Should fail without parents=True
        with pytest.raises(FileNotFoundError):
            nested_dir.mkdir()
        
        # Should succeed with parents=True
        nested_dir.mkdir(parents=True)
        assert nested_dir.exists()
    
    def test_handle_file_operation_exceptions(self, temp_dir):
        """Test graceful handling of file operation exceptions."""
        def safe_file_operation(file_path, content):
            try:
                file_path.write_text(content)
                return True
            except (PermissionError, FileNotFoundError, OSError):
                return False
        
        # Valid operation
        valid_file = temp_dir / "valid.txt"
        assert safe_file_operation(valid_file, "content") is True
        
        # Invalid operation (non-existent parent)
        invalid_file = temp_dir / "nonexistent" / "invalid.txt"
        assert safe_file_operation(invalid_file, "content") is False


class TestFileContentOperations:
    """Test file content manipulation operations."""
    
    def test_read_write_text_content(self, temp_dir):
        """Test reading and writing text content."""
        test_file = temp_dir / "text.txt"
        content = "Line 1\nLine 2\nLine 3"
        
        test_file.write_text(content)
        read_content = test_file.read_text()
        
        assert read_content == content
    
    def test_read_write_unicode_content(self, temp_dir):
        """Test reading and writing unicode content."""
        test_file = temp_dir / "unicode.txt"
        content = "Unicode: 🚀 中文 🎉"
        
        test_file.write_text(content, encoding='utf-8')
        read_content = test_file.read_text(encoding='utf-8')
        
        assert read_content == content
    
    def test_append_to_file(self, temp_dir):
        """Test appending content to existing file."""
        test_file = temp_dir / "append.txt"
        
        test_file.write_text("Line 1\n")
        
        # Simulate append operation
        existing_content = test_file.read_text()
        new_content = existing_content + "Line 2\n"
        test_file.write_text(new_content)
        
        assert test_file.read_text() == "Line 1\nLine 2\n"
    
    def test_file_size_operations(self, temp_dir):
        """Test file size related operations."""
        test_file = temp_dir / "size_test.txt"
        
        # Empty file
        test_file.write_text("")
        assert test_file.stat().st_size == 0
        
        # File with content
        content = "Test content"
        test_file.write_text(content)
        assert test_file.stat().st_size == len(content.encode('utf-8'))


@pytest.mark.unit
class TestFileOperationsIntegration:
    """Integration tests for file operations."""
    
    def test_complete_project_setup_workflow(self, temp_dir):
        """Test complete project setup file operations."""
        # Create project structure
        docs_dir = temp_dir / "docs"
        planning_dir = temp_dir / "planning"
        templates_dir = planning_dir / "templates"
        
        docs_dir.mkdir(parents=True, exist_ok=True)
        planning_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create files
        (temp_dir / "CLAUDE.md").write_text("# CLAUDE.md\n\nInstructions for Claude.")
        (docs_dir / "codebase.md").write_text("# Codebase\n\nCode documentation.")
        (templates_dir / "feature.md").write_text("# Feature Template")
        
        # Verify structure
        assert (temp_dir / "CLAUDE.md").exists()
        assert (docs_dir / "codebase.md").exists()
        assert (templates_dir / "feature.md").exists()
        
        # Verify content
        assert "Instructions for Claude" in (temp_dir / "CLAUDE.md").read_text()
        assert "Code documentation" in (docs_dir / "codebase.md").read_text()
    
    def test_template_processing_and_file_creation(self, temp_dir, sample_template_content):
        """Test processing templates and creating files."""
        # Process template
        processed_content = sample_template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        processed_content = processed_content.replace('{{AGENT_NAME}}', 'Claude')
        
        # Create file
        output_file = temp_dir / "CLAUDE.md"
        output_file.write_text(processed_content)
        
        # Verify
        assert output_file.exists()
        content = output_file.read_text()
        assert 'CLAUDE.md' in content
        assert 'Claude' in content
        assert '{{FILENAME}}' not in content
        assert '{{AGENT_NAME}}' not in content
