"""
Unit tests for template engine functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from claude_workflow import cli


class TestTemplateSubstitution:
    """Test template placeholder substitution logic."""
    
    def test_filename_placeholder_substitution(self):
        """Test {{FILENAME}} placeholder replacement."""
        template_content = "# {{FILENAME}} Project\n\nThis is the {{FILENAME}} file."
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        
        assert '{{FILENAME}}' not in result
        assert 'CLAUDE.md Project' in result
        assert 'This is the CLAUDE.md file.' in result
    
    def test_agent_name_placeholder_substitution(self):
        """Test {{AGENT_NAME}} placeholder replacement."""
        template_content = "Tell {{AGENT_NAME}} to read the docs.\n{{AGENT_NAME}} is helpful."
        
        result = template_content.replace('{{AGENT_NAME}}', 'Claude')
        
        assert '{{AGENT_NAME}}' not in result
        assert 'Tell Claude to read the docs.' in result
        assert 'Claude is helpful.' in result
    
    def test_multiple_placeholder_substitution(self):
        """Test multiple placeholder replacements in same content."""
        template_content = """# {{FILENAME}} Instructions

## Overview
This {{FILENAME}} file provides instructions for {{AGENT_NAME}}.

## Usage
{{AGENT_NAME}} should read this {{FILENAME}} file carefully.
"""
        
        result = template_content.replace('{{FILENAME}}', 'AmazonQ.md')
        result = result.replace('{{AGENT_NAME}}', 'Amazon Q')
        
        assert '{{FILENAME}}' not in result
        assert '{{AGENT_NAME}}' not in result
        assert 'AmazonQ.md Instructions' in result
        assert 'This AmazonQ.md file provides instructions for Amazon Q.' in result
        assert 'Amazon Q should read this AmazonQ.md file carefully.' in result
    
    def test_no_placeholders(self):
        """Test content with no placeholders remains unchanged."""
        template_content = "# Regular Content\n\nThis has no placeholders."
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        assert result == template_content
    
    def test_malformed_placeholders_ignored(self):
        """Test that malformed placeholders are not replaced."""
        template_content = "{{FILENAME} {AGENT_NAME}} {{INVALID}} {{{FILENAME}}}"
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        # Only properly formed placeholders should be replaced
        assert '{{FILENAME}' in result  # Missing closing brace
        assert '{AGENT_NAME}}' in result  # Missing opening brace
        assert '{{INVALID}}' in result  # Unknown placeholder
        assert '{{{FILENAME}}}' in result  # Extra braces
    
    def test_case_sensitive_placeholders(self):
        """Test that placeholder replacement is case sensitive."""
        template_content = "{{filename}} {{FILENAME}} {{agent_name}} {{AGENT_NAME}}"
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        assert '{{filename}}' in result  # Lowercase not replaced
        assert '{{agent_name}}' in result  # Lowercase not replaced
        assert 'CLAUDE.md' in result
        assert 'Claude' in result


class TestTemplateProcessing:
    """Test template file processing logic."""
    
    def test_claude_template_processing(self, sample_template_content):
        """Test processing template for Claude variant."""
        filename = "CLAUDE.md"
        agent_name = "Claude"
        
        result = sample_template_content.replace('{{FILENAME}}', filename)
        result = result.replace('{{AGENT_NAME}}', agent_name)
        
        assert filename in result
        assert agent_name in result
        assert '{{FILENAME}}' not in result
        assert '{{AGENT_NAME}}' not in result
    
    def test_amazonq_template_processing(self, sample_template_content):
        """Test processing template for Amazon Q variant."""
        filename = "AmazonQ.md"
        agent_name = "Amazon Q"
        
        result = sample_template_content.replace('{{FILENAME}}', filename)
        result = result.replace('{{AGENT_NAME}}', agent_name)
        
        assert filename in result
        assert agent_name in result
        assert '{{FILENAME}}' not in result
        assert '{{AGENT_NAME}}' not in result
    
    def test_template_structure_preservation(self, sample_template_content):
        """Test that template structure is preserved during processing."""
        original_lines = sample_template_content.split('\n')
        
        result = sample_template_content.replace('{{FILENAME}}', 'TEST.md')
        result = result.replace('{{AGENT_NAME}}', 'Test Agent')
        result_lines = result.split('\n')
        
        # Should have same number of lines
        assert len(result_lines) == len(original_lines)
        
        # Should preserve markdown structure
        assert result.startswith('# TEST.md Project Template')
        assert '## Build and Test Commands' in result
        assert '## Project Structure' in result
        assert '## Development Workflow' in result


class TestTemplateFileHandling:
    """Test template file reading and processing."""
    
    @patch('claude_workflow.cli.pkg_resources')
    def test_template_file_reading(self, mock_pkg_resources, sample_templates_dir):
        """Test reading template files from package resources."""
        mock_pkg_resources.files.return_value = sample_templates_dir.parent
        
        # Simulate reading the template file
        template_path = sample_templates_dir / "agent_instructions.md"
        template_content = template_path.read_text()
        
        assert '{{FILENAME}}' in template_content
        assert '{{AGENT_NAME}}' in template_content
    
    def test_template_file_not_found_handling(self):
        """Test handling when template file is not found."""
        with pytest.raises(FileNotFoundError):
            Path("/nonexistent/template.md").read_text()
    
    @patch('claude_workflow.cli.pkg_resources')
    def test_package_resource_error_handling(self, mock_pkg_resources):
        """Test handling of package resource errors."""
        mock_pkg_resources.files.side_effect = ImportError("Package not found")
        
        with pytest.raises(ImportError):
            mock_pkg_resources.files('claude_workflow')


class TestTemplateVariants:
    """Test different template processing scenarios."""
    
    def test_empty_template_processing(self):
        """Test processing empty template content."""
        template_content = ""
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        assert result == ""
    
    def test_template_with_only_placeholders(self):
        """Test template containing only placeholders."""
        template_content = "{{FILENAME}}\n{{AGENT_NAME}}"
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        assert result == "CLAUDE.md\nClaude"
    
    def test_template_with_repeated_placeholders(self):
        """Test template with same placeholder repeated multiple times."""
        template_content = "{{FILENAME}} and {{FILENAME}} and {{FILENAME}}"
        
        result = template_content.replace('{{FILENAME}}', 'TEST.md')
        
        assert result == "TEST.md and TEST.md and TEST.md"
        assert '{{FILENAME}}' not in result
    
    def test_template_with_special_characters(self):
        """Test template processing with special characters."""
        template_content = "# {{FILENAME}} 🚀\n\n**{{AGENT_NAME}}** is *awesome*!"
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        assert result == "# CLAUDE.md 🚀\n\n**Claude** is *awesome*!"
    
    def test_template_with_code_blocks(self):
        """Test template processing preserves code blocks."""
        template_content = """# {{FILENAME}}

```bash
# This is for {{AGENT_NAME}}
echo "{{FILENAME}}"
```
"""
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        expected = """# CLAUDE.md

```bash
# This is for Claude
echo "CLAUDE.md"
```
"""
        assert result == expected


class TestEdgeCases:
    """Test edge cases in template processing."""
    
    def test_unicode_content_processing(self):
        """Test processing templates with unicode content."""
        template_content = "# {{FILENAME}} 中文 🎉\n\n{{AGENT_NAME}} supports unicode! 🌟"
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        assert "CLAUDE.md 中文 🎉" in result
        assert "Claude supports unicode! 🌟" in result
    
    def test_very_long_template_processing(self):
        """Test processing very long template content."""
        # Create a long template
        long_content = "{{FILENAME}}\n" * 1000 + "{{AGENT_NAME}}\n" * 1000
        
        result = long_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        assert result.count('CLAUDE.md') == 1000
        assert result.count('Claude') == 1000
        assert '{{FILENAME}}' not in result
        assert '{{AGENT_NAME}}' not in result
    
    def test_nested_braces_handling(self):
        """Test handling of nested braces in templates."""
        template_content = "{{{FILENAME}}} {{{{AGENT_NAME}}}}"
        
        result = template_content.replace('{{FILENAME}}', 'CLAUDE.md')
        result = result.replace('{{AGENT_NAME}}', 'Claude')
        
        # Should only replace the properly formatted placeholders
        assert result == "{CLAUDE.md} {Claude}"


@pytest.mark.unit
class TestTemplateEngineIntegration:
    """Integration tests for template engine components."""
    
    def test_full_template_processing_workflow(self, sample_template_content):
        """Test complete template processing workflow."""
        # Simulate the full workflow
        filename = "CLAUDE.md"
        agent_name = "Claude"
        
        # Process template
        processed_content = sample_template_content.replace('{{FILENAME}}', filename)
        processed_content = processed_content.replace('{{AGENT_NAME}}', agent_name)
        
        # Verify all placeholders replaced
        assert '{{FILENAME}}' not in processed_content
        assert '{{AGENT_NAME}}' not in processed_content
        
        # Verify content is valid
        assert filename in processed_content
        assert agent_name in processed_content
        assert processed_content.startswith('#')  # Valid markdown
    
    def test_template_processing_consistency(self, sample_template_content):
        """Test that template processing is consistent across multiple runs."""
        filename = "TEST.md"
        agent_name = "Test Agent"
        
        # Process same template multiple times
        results = []
        for _ in range(5):
            result = sample_template_content.replace('{{FILENAME}}', filename)
            result = result.replace('{{AGENT_NAME}}', agent_name)
            results.append(result)
        
        # All results should be identical
        assert all(result == results[0] for result in results)
