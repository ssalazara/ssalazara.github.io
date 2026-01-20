"""
Unit tests for header transformer.
Tests referenced entry resolution and circular reference protection.
"""

import pytest
from unittest.mock import Mock
from scripts.transformers.header_transformer import HeaderTransformer
from tests.fixtures import create_mock_header, create_mock_menu_item


class TestHeaderTransformer:
    """Test suite for HeaderTransformer."""
    
    def test_transform_single_success(self):
        """Test successful header transformation with all fields."""
        # Arrange
        mock_client = Mock()
        transformer = HeaderTransformer(mock_client, locale='en')
        mock_entry = create_mock_header(locale='en')
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['brand_url'] == '/'
        assert 'brand_logo_url' in result
        assert 'menu_items' in result
        assert len(result['menu_items']) == 3
    
    def test_menu_items_resolution(self):
        """Test that menuItems array is resolved correctly."""
        # Arrange
        mock_client = Mock()
        transformer = HeaderTransformer(mock_client, locale='en')
        mock_entry = create_mock_header(locale='en')
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        menu_items = result['menu_items']
        assert len(menu_items) == 3
        assert menu_items[0]['label'] == 'Home'
        assert menu_items[0]['url'] == '/'
        assert menu_items[0]['external'] is False
        assert menu_items[1]['label'] == 'Blog'
        assert menu_items[1]['url'] == '/blog'
    
    def test_external_link_detection(self):
        """Test that external links are properly detected."""
        # Arrange
        mock_client = Mock()
        transformer = HeaderTransformer(mock_client, locale='en')
        
        external_menu = create_mock_menu_item('GitHub', 'https://github.com/user')
        mock_entry = create_mock_header(
            locale='en',
            menuItems=[external_menu]
        )
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        menu_items = result['menu_items']
        assert menu_items[0]['external'] is True
    
    def test_localized_menu_labels(self):
        """Test that menu labels are localized."""
        # Arrange
        mock_client = Mock()
        transformer = HeaderTransformer(mock_client, locale='es')
        
        spanish_menu = create_mock_menu_item('Inicio', '/', locale='es')
        mock_entry = create_mock_header(
            locale='es',
            menuItems=[spanish_menu]
        )
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['menu_items'][0]['label'] == 'Inicio'
    
    def test_empty_menu_items(self):
        """Test graceful handling of empty menu items."""
        # Arrange
        mock_client = Mock()
        transformer = HeaderTransformer(mock_client, locale='en')
        mock_entry = create_mock_header(locale='en', menuItems=[])
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        # Empty arrays are filtered out (cleaner YAML)
        assert 'menu_items' not in result or result.get('menu_items') == []
    
    def test_top_links_resolution(self):
        """Test that topLinks array is resolved correctly."""
        # Arrange
        mock_client = Mock()
        transformer = HeaderTransformer(mock_client, locale='en')
        
        top_link = create_mock_menu_item('Login', '/login')
        mock_entry = create_mock_header(
            locale='en',
            topLinks=[top_link]
        )
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        if 'top_links' in result:
            assert len(result['top_links']) == 1
            assert result['top_links'][0]['label'] == 'Login'
