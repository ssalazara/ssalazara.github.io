"""
Unit tests for file writer.
Tests filename generation, locale folder creation, and error handling.
"""

import pytest
import os
import tempfile
import shutil
from scripts.writers.file_writer import FileWriter


class TestFileWriter:
    """Test suite for FileWriter."""
    
    def setup_method(self):
        """Create temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def teardown_method(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_write_blog_post_success(self):
        """Test successful blog post file creation."""
        # Arrange
        writer = FileWriter()
        post_data = {
            'frontmatter': {
                'slug': 'test-post',
                'title': 'Test Post',
                'publish_date': '2026-01-19T10:30:00Z',
                'author': 'Test Author'
            },
            'body': 'This is the post body.'
        }
        
        # Act
        writer.write_blog_post(post_data, locale='en')
        
        # Assert
        expected_path = '_posts/en/2026-01-19-test-post.md'
        assert os.path.exists(expected_path)
        
        with open(expected_path, 'r') as f:
            content = f.read()
            assert 'title: Test Post' in content
            assert 'This is the post body.' in content
    
    def test_locale_folder_creation(self):
        """Test that locale folder is created if it doesn't exist."""
        # Arrange
        writer = FileWriter()
        post_data = {
            'frontmatter': {
                'slug': 'new-post',
                'title': 'New Post',
                'publish_date': '2026-01-20T10:00:00Z'
            },
            'body': 'Content'
        }
        
        # Act
        writer.write_blog_post(post_data, locale='es')
        
        # Assert
        assert os.path.exists('_posts/es')
        assert os.path.exists('_posts/es/2026-01-20-new-post.md')
    
    def test_filename_generation_with_date(self):
        """Test that filename includes date prefix."""
        # Arrange
        writer = FileWriter()
        post_data = {
            'frontmatter': {
                'slug': 'my-post',
                'publish_date': '2026-03-15T14:30:00Z'
            },
            'body': 'Content'
        }
        
        # Act
        writer.write_blog_post(post_data, locale='en')
        
        # Assert
        expected_filename = '2026-03-15-my-post.md'
        expected_path = f'_posts/en/{expected_filename}'
        assert os.path.exists(expected_path)
    
    def test_slug_sanitization(self):
        """Test that slugs are properly sanitized to kebab-case."""
        # Arrange
        writer = FileWriter()
        post_data = {
            'frontmatter': {
                'slug': 'Test Post With Spaces',
                'publish_date': '2026-01-19T10:00:00Z'
            },
            'body': 'Content'
        }
        
        # Act
        writer.write_blog_post(post_data, locale='en')
        
        # Assert
        # Should convert to kebab-case
        files = os.listdir('_posts/en')
        assert len(files) == 1
        assert files[0].endswith('.md')
        assert ' ' not in files[0]
    
    def test_invalid_date_fallback(self):
        """Test that invalid dates fall back to current date."""
        # Arrange
        writer = FileWriter()
        post_data = {
            'frontmatter': {
                'slug': 'test-post',
                'publish_date': 'invalid-date'
            },
            'body': 'Content'
        }
        
        # Act
        writer.write_blog_post(post_data, locale='en')
        
        # Assert
        # Should create file with current date
        assert os.path.exists('_posts/en')
        files = os.listdir('_posts/en')
        assert len(files) == 1
        assert files[0].endswith('-test-post.md')
    
    def test_missing_publish_date(self):
        """Test handling of missing publish_date field."""
        # Arrange
        writer = FileWriter()
        post_data = {
            'frontmatter': {
                'slug': 'no-date-post',
                'title': 'No Date Post'
            },
            'body': 'Content'
        }
        
        # Act
        writer.write_blog_post(post_data, locale='en')
        
        # Assert
        # Should create file with current date
        assert os.path.exists('_posts/en')
        files = os.listdir('_posts/en')
        assert len(files) == 1
    
    def test_yaml_frontmatter_format(self):
        """Test that YAML frontmatter is properly formatted."""
        # Arrange
        writer = FileWriter()
        post_data = {
            'frontmatter': {
                'slug': 'yaml-test',
                'title': 'YAML Test',
                'publish_date': '2026-01-19T10:00:00Z',
                'author': 'Test Author',
                'category': 'Technology'
            },
            'body': 'Post content here.'
        }
        
        # Act
        writer.write_blog_post(post_data, locale='en')
        
        # Assert
        with open('_posts/en/2026-01-19-yaml-test.md', 'r') as f:
            content = f.read()
            # Should have YAML frontmatter delimiters
            assert content.startswith('---')
            assert content.count('---') >= 2
            # Should have all frontmatter fields
            assert 'title: YAML Test' in content
            assert 'author: Test Author' in content
            assert 'category: Technology' in content
            # Body should be after frontmatter
            assert 'Post content here.' in content
    
    def test_overwrite_existing_file(self):
        """Test that existing files are overwritten."""
        # Arrange
        writer = FileWriter()
        post_data = {
            'frontmatter': {
                'slug': 'same-post',
                'title': 'First Version',
                'publish_date': '2026-01-19T10:00:00Z'
            },
            'body': 'First content'
        }
        
        # Act - Write first version
        writer.write_blog_post(post_data, locale='en')
        
        # Update and write second version
        post_data['frontmatter']['title'] = 'Second Version'
        post_data['body'] = 'Updated content'
        writer.write_blog_post(post_data, locale='en')
        
        # Assert
        with open('_posts/en/2026-01-19-same-post.md', 'r') as f:
            content = f.read()
            assert 'Second Version' in content
            assert 'Updated content' in content
            assert 'First Version' not in content
            assert 'First content' not in content
