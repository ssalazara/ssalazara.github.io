"""
Unit tests for footer transformer.
Tests referenced entry resolution for menuItems and socialLinks.
"""

import pytest
from unittest.mock import Mock
from scripts.transformers.footer_transformer import FooterTransformer
from tests.fixtures import create_mock_footer, create_mock_menu_item, create_mock_social_link


class TestFooterTransformer:
    """Test suite for FooterTransformer."""
    
    def test_transform_single_success(self):
        """Test successful footer transformation with all fields."""
        # Arrange
        mock_client = Mock()
        transformer = FooterTransformer(mock_client, locale='en')
        mock_entry = create_mock_footer(locale='en')
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['brand_url'] == '/'
        assert 'brand_logo_url' in result
        assert result['description'] == 'Personal website of John Doe.'
        assert result['copyright'] == '© 2026 John Doe. All rights reserved.'
        assert 'menu_items' in result
        assert 'social_links' in result
    
    def test_menu_items_resolution(self):
        """Test that menuItems array is resolved correctly."""
        # Arrange
        mock_client = Mock()
        transformer = FooterTransformer(mock_client, locale='en')
        mock_entry = create_mock_footer(locale='en')
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        menu_items = result['menu_items']
        assert len(menu_items) == 2
        assert menu_items[0]['label'] == 'Privacy'
        assert menu_items[0]['url'] == '/privacy'
        assert menu_items[1]['label'] == 'Terms'
        assert menu_items[1]['url'] == '/terms'
    
    def test_social_links_resolution(self):
        """Test that socialLinks array is resolved correctly."""
        # Arrange
        mock_client = Mock()
        transformer = FooterTransformer(mock_client, locale='en')
        mock_entry = create_mock_footer(locale='en')
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        social_links = result['social_links']
        assert len(social_links) == 1
        assert social_links[0]['platform'] == 'Twitter'
        assert social_links[0]['url'] == 'https://twitter.com/johndoe'
    
    def test_localized_description(self):
        """Test that description is localized."""
        # Arrange
        mock_client = Mock()
        transformer = FooterTransformer(mock_client, locale='es')
        mock_entry = create_mock_footer(
            locale='es',
            description='Sitio web personal de Juan Pérez.',
            copyright='© 2026 Juan Pérez. Todos los derechos reservados.'
        )
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['description'] == 'Sitio web personal de Juan Pérez.'
        assert result['copyright'] == '© 2026 Juan Pérez. Todos los derechos reservados.'
    
    def test_empty_social_links(self):
        """Test graceful handling of empty social links."""
        # Arrange
        mock_client = Mock()
        transformer = FooterTransformer(mock_client, locale='en')
        mock_entry = create_mock_footer(locale='en', socialLinks=[])
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        # Empty arrays are filtered out (cleaner YAML)
        assert 'social_links' not in result or result.get('social_links') == []
    
    def test_multiple_social_platforms(self):
        """Test footer with multiple social platforms."""
        # Arrange
        mock_client = Mock()
        transformer = FooterTransformer(mock_client, locale='en')
        
        social_links = [
            create_mock_social_link('Twitter', 'https://twitter.com/user'),
            create_mock_social_link('GitHub', 'https://github.com/user'),
            create_mock_social_link('LinkedIn', 'https://linkedin.com/in/user')
        ]
        
        mock_entry = create_mock_footer(locale='en', socialLinks=social_links)
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert len(result['social_links']) == 3
        assert result['social_links'][0]['platform'] == 'Twitter'
        assert result['social_links'][1]['platform'] == 'GitHub'
        assert result['social_links'][2]['platform'] == 'LinkedIn'
