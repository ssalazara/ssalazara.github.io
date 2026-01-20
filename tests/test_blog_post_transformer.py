"""
Unit tests for blog post transformer.
Tests SEO validation, field mapping, and graceful degradation.
"""

import pytest
from unittest.mock import Mock
from scripts.transformers.blog_post_transformer import BlogPostTransformer
from tests.fixtures import create_mock_blog_post, create_mock_seo


class TestBlogPostTransformer:
    """Test suite for BlogPostTransformer."""
    
    def test_transform_single_success(self):
        """Test successful blog post transformation with all fields."""
        # Arrange
        mock_client = Mock()
        transformer = BlogPostTransformer(mock_client, locale='en')
        mock_entry = create_mock_blog_post(locale='en', with_seo=True)
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert 'frontmatter' in result
        assert 'body' in result
        
        frontmatter = result['frontmatter']
        assert frontmatter['slug'] == 'test-blog-post'
        assert frontmatter['title'] == 'Test Blog Post'
        assert frontmatter['excerpt'] == 'This is a test blog post excerpt.'
        assert frontmatter['category'] == 'Technology'
        assert frontmatter['author'] == 'Test Author'
        assert frontmatter['publish_date'] == '2026-01-19T10:30:00Z'
        assert 'featured_image' in frontmatter
        assert 'seo_title' in frontmatter
        assert 'seo_description' in frontmatter
    
    def test_transform_single_seo_missing(self):
        """Test that transformation fails when SEO entry is missing."""
        # Arrange
        mock_client = Mock()
        transformer = BlogPostTransformer(mock_client, locale='en')
        mock_entry = create_mock_blog_post(locale='en', with_seo=False, seo=None)
        
        # Act & Assert
        with pytest.raises(ValueError, match="SEO_MISSING"):
            transformer.transform_single(mock_entry)
    
    def test_iso8601_date_preserved(self):
        """Test that publish date is passed through unchanged."""
        # Arrange
        mock_client = Mock()
        transformer = BlogPostTransformer(mock_client, locale='en')
        original_date = '2026-01-19T15:45:30Z'
        mock_entry = create_mock_blog_post(
            locale='en',
            with_seo=True,
            publishDate=original_date
        )
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['frontmatter']['publish_date'] == original_date
    
    def test_snake_case_frontmatter_keys(self):
        """Test that all frontmatter keys use snake_case."""
        # Arrange
        mock_client = Mock()
        transformer = BlogPostTransformer(mock_client, locale='en')
        mock_entry = create_mock_blog_post(locale='en', with_seo=True)
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        frontmatter = result['frontmatter']
        assert 'publish_date' in frontmatter  # snake_case
        assert 'featured_image' in frontmatter  # snake_case
        assert 'seo_title' in frontmatter  # snake_case
        assert 'publishDate' not in frontmatter  # Not camelCase
        assert 'featuredImage' not in frontmatter  # Not camelCase
    
    def test_featured_image_cdn_url(self):
        """Test that featured image is a CDN URL, not downloaded."""
        # Arrange
        mock_client = Mock()
        transformer = BlogPostTransformer(mock_client, locale='en')
        cdn_url = 'https://images.ctfassets.net/space/test-image.jpg'
        mock_entry = create_mock_blog_post(locale='en', with_seo=True)
        mock_entry.fields.return_value['image'].url.return_value = cdn_url
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['frontmatter']['featured_image'] == cdn_url
        assert result['frontmatter']['featured_image'].startswith('https://')
    
    def test_rich_text_conversion(self):
        """Test that RichText converts to Markdown correctly."""
        # Arrange
        mock_client = Mock()
        transformer = BlogPostTransformer(mock_client, locale='en')
        mock_entry = create_mock_blog_post(locale='en', with_seo=True)
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['body'] is not None
        assert len(result['body']) > 0
        assert isinstance(result['body'], str)
    
    def test_seo_fields_missing_raises_error(self):
        """Test that transformation fails when SEO fields are incomplete."""
        # Arrange
        mock_client = Mock()
        transformer = BlogPostTransformer(mock_client, locale='en')
        
        # Create SEO entry with missing required fields
        mock_seo = Mock()
        mock_seo.id = 'seo-incomplete'
        mock_seo.fields.return_value = {
            'title': 'SEO Title',
            # Missing 'description' field
        }
        
        mock_entry = create_mock_blog_post(locale='en', with_seo=True, seo=mock_seo)
        
        # Act & Assert
        with pytest.raises(ValueError):
            transformer.transform_single(mock_entry)