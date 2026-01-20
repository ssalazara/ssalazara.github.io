"""
Unit tests for data writer.
Tests YAML serialization and file creation for data files.
"""

import pytest
import os
import tempfile
import shutil
import yaml
from scripts.writers.data_writer import DataWriter


class TestDataWriter:
    """Test suite for DataWriter."""
    
    def setup_method(self):
        """Create temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def teardown_method(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_write_data_file_success(self):
        """Test successful data file creation."""
        # Arrange
        writer = DataWriter()
        data = {
            'name': 'John Doe',
            'title': 'Software Engineer',
            'email': 'john@example.com'
        }
        
        # Act
        writer.write_data_file(data, content_type='profile', locale='en')
        
        # Assert
        expected_path = '_data/profile-en.yml'
        assert os.path.exists(expected_path)
        
        with open(expected_path, 'r') as f:
            content = f.read()
            assert 'name: John Doe' in content
            assert 'title: Software Engineer' in content
    
    def test_data_directory_creation(self):
        """Test that _data directory is created if it doesn't exist."""
        # Arrange
        writer = DataWriter()
        data = {'test': 'value'}
        
        # Act
        writer.write_data_file(data, content_type='test', locale='en')
        
        # Assert
        assert os.path.exists('_data')
        assert os.path.exists('_data/test-en.yml')
    
    def test_filename_pattern(self):
        """Test that filename follows {content_type}-{locale}.yml pattern."""
        # Arrange
        writer = DataWriter()
        data = {'field': 'value'}
        
        # Act
        writer.write_data_file(data, content_type='header', locale='es')
        
        # Assert
        assert os.path.exists('_data/header-es.yml')
    
    def test_yaml_format(self):
        """Test that YAML is properly formatted."""
        # Arrange
        writer = DataWriter()
        data = {
            'brand_url': '/',
            'menu_items': [
                {'label': 'Home', 'url': '/'},
                {'label': 'Blog', 'url': '/blog'}
            ]
        }
        
        # Act
        writer.write_data_file(data, content_type='header', locale='en')
        
        # Assert
        with open('_data/header-en.yml', 'r') as f:
            loaded_data = yaml.safe_load(f)
            assert loaded_data['brand_url'] == '/'
            assert len(loaded_data['menu_items']) == 2
            assert loaded_data['menu_items'][0]['label'] == 'Home'
    
    def test_header_comment(self):
        """Test that file includes header comment."""
        # Arrange
        writer = DataWriter()
        data = {'test': 'value'}
        
        # Act
        writer.write_data_file(data, content_type='profile', locale='en')
        
        # Assert
        with open('_data/profile-en.yml', 'r') as f:
            content = f.read()
            # Should have header comment
            assert '#' in content
    
    def test_unicode_support(self):
        """Test that Unicode characters are properly handled."""
        # Arrange
        writer = DataWriter()
        data = {
            'name': 'José García',
            'bio': 'Desarrollador con pasión por la tecnología 🚀'
        }
        
        # Act
        writer.write_data_file(data, content_type='profile', locale='es')
        
        # Assert
        with open('_data/profile-es.yml', 'r', encoding='utf-8') as f:
            loaded_data = yaml.safe_load(f)
            assert loaded_data['name'] == 'José García'
            assert '🚀' in loaded_data['bio']
    
    def test_nested_data_structures(self):
        """Test that nested data structures are properly serialized."""
        # Arrange
        writer = DataWriter()
        data = {
            'cta_button': {
                'text': 'Contact Me',
                'url': '/contact',
                'external': False
            },
            'social_links': [
                {'platform': 'Twitter', 'url': 'https://twitter.com/user'},
                {'platform': 'GitHub', 'url': 'https://github.com/user'}
            ]
        }
        
        # Act
        writer.write_data_file(data, content_type='profile', locale='en')
        
        # Assert
        with open('_data/profile-en.yml', 'r') as f:
            loaded_data = yaml.safe_load(f)
            assert loaded_data['cta_button']['text'] == 'Contact Me'
            assert len(loaded_data['social_links']) == 2
    
    def test_overwrite_existing_file(self):
        """Test that existing files are overwritten."""
        # Arrange
        writer = DataWriter()
        data_v1 = {'version': 1, 'name': 'First'}
        data_v2 = {'version': 2, 'name': 'Second'}
        
        # Act
        writer.write_data_file(data_v1, content_type='test', locale='en')
        writer.write_data_file(data_v2, content_type='test', locale='en')
        
        # Assert
        with open('_data/test-en.yml', 'r') as f:
            loaded_data = yaml.safe_load(f)
            assert loaded_data['version'] == 2
            assert loaded_data['name'] == 'Second'
    
    def test_empty_data(self):
        """Test handling of empty data dict."""
        # Arrange
        writer = DataWriter()
        data = {}
        
        # Act
        writer.write_data_file(data, content_type='empty', locale='en')
        
        # Assert
        assert os.path.exists('_data/empty-en.yml')
        with open('_data/empty-en.yml', 'r') as f:
            content = f.read()
            # Should create valid YAML file even if empty
            loaded_data = yaml.safe_load(content)
            assert loaded_data == {} or loaded_data is None
    
    def test_key_order_preservation(self):
        """Test that key order is preserved (no alphabetical sorting)."""
        # Arrange
        writer = DataWriter()
        data = {
            'zebra': 'last',
            'apple': 'first',
            'middle': 'middle'
        }
        
        # Act
        writer.write_data_file(data, content_type='order', locale='en')
        
        # Assert
        with open('_data/order-en.yml', 'r') as f:
            lines = [line for line in f.readlines() if not line.strip().startswith('#')]
            # Keys should appear in insertion order, not alphabetically
            content = ''.join(lines)
            zebra_pos = content.find('zebra')
            apple_pos = content.find('apple')
            middle_pos = content.find('middle')
            
            # Zebra should come before apple (insertion order)
            assert zebra_pos < apple_pos
