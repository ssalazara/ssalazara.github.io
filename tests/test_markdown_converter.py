"""
Unit tests for Rich Text to Markdown converter.
Tests all supported node types, marks, and edge cases.
"""

import pytest
from scripts.converters.markdown_converter import RichTextConverter


class TestMarkdownConverter:
    """Test suite for RichTextConverter."""
    
    def test_paragraph_conversion(self):
        """Test basic paragraph conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'paragraph',
                    'content': [
                        {
                            'nodeType': 'text',
                            'value': 'This is a paragraph.',
                            'marks': []
                        }
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert 'This is a paragraph.' in result
    
    def test_heading_conversion(self):
        """Test heading conversions (H2-H4)."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'heading-2',
                    'content': [{'nodeType': 'text', 'value': 'Heading 2', 'marks': []}]
                },
                {
                    'nodeType': 'heading-3',
                    'content': [{'nodeType': 'text', 'value': 'Heading 3', 'marks': []}]
                },
                {
                    'nodeType': 'heading-4',
                    'content': [{'nodeType': 'text', 'value': 'Heading 4', 'marks': []}]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '## Heading 2' in result
        assert '### Heading 3' in result
        assert '#### Heading 4' in result
    
    def test_bold_mark(self):
        """Test bold text conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'paragraph',
                    'content': [
                        {
                            'nodeType': 'text',
                            'value': 'bold text',
                            'marks': [{'type': 'bold'}]
                        }
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '**bold text**' in result
    
    def test_italic_mark(self):
        """Test italic text conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'paragraph',
                    'content': [
                        {
                            'nodeType': 'text',
                            'value': 'italic text',
                            'marks': [{'type': 'italic'}]
                        }
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '*italic text*' in result or '_italic text_' in result
    
    def test_code_mark(self):
        """Test inline code conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'paragraph',
                    'content': [
                        {
                            'nodeType': 'text',
                            'value': 'console.log()',
                            'marks': [{'type': 'code'}]
                        }
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '`console.log()`' in result
    
    def test_unordered_list(self):
        """Test unordered list conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'unordered-list',
                    'content': [
                        {
                            'nodeType': 'list-item',
                            'content': [
                                {
                                    'nodeType': 'paragraph',
                                    'content': [
                                        {'nodeType': 'text', 'value': 'Item 1', 'marks': []}
                                    ]
                                }
                            ]
                        },
                        {
                            'nodeType': 'list-item',
                            'content': [
                                {
                                    'nodeType': 'paragraph',
                                    'content': [
                                        {'nodeType': 'text', 'value': 'Item 2', 'marks': []}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '- Item 1' in result or '* Item 1' in result
        assert '- Item 2' in result or '* Item 2' in result
    
    def test_ordered_list(self):
        """Test ordered list conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'ordered-list',
                    'content': [
                        {
                            'nodeType': 'list-item',
                            'content': [
                                {
                                    'nodeType': 'paragraph',
                                    'content': [
                                        {'nodeType': 'text', 'value': 'First', 'marks': []}
                                    ]
                                }
                            ]
                        },
                        {
                            'nodeType': 'list-item',
                            'content': [
                                {
                                    'nodeType': 'paragraph',
                                    'content': [
                                        {'nodeType': 'text', 'value': 'Second', 'marks': []}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '1. First' in result or '1) First' in result
        assert '2. Second' in result or '2) Second' in result
    
    def test_blockquote(self):
        """Test blockquote conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'blockquote',
                    'content': [
                        {
                            'nodeType': 'paragraph',
                            'content': [
                                {'nodeType': 'text', 'value': 'This is a quote.', 'marks': []}
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '> This is a quote.' in result
    
    def test_hyperlink(self):
        """Test hyperlink conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'paragraph',
                    'content': [
                        {
                            'nodeType': 'hyperlink',
                            'data': {'uri': 'https://example.com'},
                            'content': [
                                {'nodeType': 'text', 'value': 'Example Link', 'marks': []}
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '[Example Link](https://example.com)' in result
    
    def test_horizontal_rule(self):
        """Test horizontal rule conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {'nodeType': 'hr', 'content': []}
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '---' in result or '***' in result or '___' in result
    
    def test_embedded_asset_image(self):
        """Test embedded asset (image) conversion."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'embedded-asset-block',
                    'data': {
                        'target': {
                            'fields': {
                                'title': {'en': 'Test Image'},
                                'file': {
                                    'en': {
                                        'url': '//images.ctfassets.net/test.jpg'
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert '![Test Image]' in result
        assert 'images.ctfassets.net/test.jpg' in result
    
    def test_multiple_marks(self):
        """Test text with multiple marks (bold + italic)."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'paragraph',
                    'content': [
                        {
                            'nodeType': 'text',
                            'value': 'bold and italic',
                            'marks': [{'type': 'bold'}, {'type': 'italic'}]
                        }
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        # Should contain both bold and italic markers
        assert '**' in result or '__' in result
        assert '*' in result or '_' in result
    
    def test_unknown_node_type_graceful_handling(self):
        """Test that unknown node types are handled gracefully."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'unknown-future-node',
                    'content': []
                },
                {
                    'nodeType': 'paragraph',
                    'content': [
                        {'nodeType': 'text', 'value': 'Valid paragraph', 'marks': []}
                    ]
                }
            ]
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        # Should not crash, should process valid paragraph
        assert 'Valid paragraph' in result
    
    def test_empty_document(self):
        """Test conversion of empty document."""
        # Arrange
        converter = RichTextConverter()
        rich_text = {
            'nodeType': 'document',
            'content': []
        }
        
        # Act
        result = converter.convert(rich_text)
        
        # Assert
        assert result == '' or result.strip() == ''
