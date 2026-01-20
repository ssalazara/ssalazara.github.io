"""
Unit tests for profile transformer.
Tests field mapping, locale handling, and referenced entry resolution.
"""

import pytest
from unittest.mock import Mock
from scripts.transformers.profile_transformer import ProfileTransformer
from tests.fixtures import create_mock_profile, create_mock_social_link


class TestProfileTransformer:
    """Test suite for ProfileTransformer."""
    
    def test_transform_single_success(self):
        """Test successful profile transformation with all fields."""
        # Arrange
        mock_client = Mock()
        transformer = ProfileTransformer(mock_client, locale='en')
        mock_entry = create_mock_profile(locale='en')
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['name'] == 'John Doe'
        assert result['title'] == 'Software Engineer'
        assert result['bio'] == 'A passionate developer.'
        assert result['email'] == 'john@example.com'
        assert 'photo_url' in result
        assert 'social_links' in result
        assert len(result['social_links']) == 2
    
    def test_localized_fields(self):
        """Test that localized fields are properly extracted."""
        # Arrange
        mock_client = Mock()
        transformer = ProfileTransformer(mock_client, locale='es')
        mock_entry = create_mock_profile(
            locale='es',
            title='Ingeniero de Software',
            bio='Un desarrollador apasionado.'
        )
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['title'] == 'Ingeniero de Software'
        assert result['bio'] == 'Un desarrollador apasionado.'
    
    def test_social_links_resolution(self):
        """Test that socialLinks array is resolved correctly."""
        # Arrange
        mock_client = Mock()
        transformer = ProfileTransformer(mock_client, locale='en')
        mock_entry = create_mock_profile(locale='en')
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        social_links = result['social_links']
        assert len(social_links) == 2
        assert social_links[0]['platform'] == 'Twitter'
        assert social_links[0]['url'] == 'https://twitter.com/johndoe'
        assert social_links[1]['platform'] == 'GitHub'
        assert social_links[1]['url'] == 'https://github.com/johndoe'
    
    def test_cta_button_mapping(self):
        """Test that CTA button fields are mapped correctly."""
        # Arrange
        mock_client = Mock()
        transformer = ProfileTransformer(mock_client, locale='en')
        mock_entry = create_mock_profile(
            locale='en',
            ctaLabel='Hire Me',
            ctaUrl='https://example.com/contact'
        )
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert 'cta_button' in result
        assert result['cta_button']['text'] == 'Hire Me'
        assert result['cta_button']['url'] == 'https://example.com/contact'
        assert result['cta_button']['external'] is True
    
    def test_cta_internal_link(self):
        """Test that internal CTA links are marked as not external."""
        # Arrange
        mock_client = Mock()
        transformer = ProfileTransformer(mock_client, locale='en')
        mock_entry = create_mock_profile(
            locale='en',
            ctaUrl='/contact'
        )
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['cta_button']['external'] is False
    
    def test_missing_optional_fields(self):
        """Test graceful handling of missing optional fields."""
        # Arrange
        mock_client = Mock()
        transformer = ProfileTransformer(mock_client, locale='en')
        mock_entry = create_mock_profile(
            locale='en',
            ctaLabel=None,
            ctaUrl=None
        )
        
        # Remove optional fields
        fields = mock_entry.fields.return_value
        del fields['ctaLabel']
        del fields['ctaUrl']
        
        # Act
        result = transformer.transform_single(mock_entry)
        
        # Assert
        assert result['name'] == 'John Doe'
        # Should handle missing CTA gracefully
