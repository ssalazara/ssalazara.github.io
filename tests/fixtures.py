"""
Test fixtures for mocking Contentful Entry objects.
Provides factory functions for creating test data.
"""

from unittest.mock import Mock
from typing import Dict, Any, Optional, List


def create_mock_asset(
    url: str = 'https://images.ctfassets.net/space/asset.jpg',
    title: str = 'Test Image',
    description: str = 'Test description'
) -> Mock:
    """
    Create a mock Contentful Asset object.
    
    Args:
        url: Asset CDN URL
        title: Asset title
        description: Asset description
    
    Returns:
        Mock Asset object
    """
    mock_asset = Mock()
    mock_asset.url.return_value = url
    mock_asset.fields.return_value = {
        'title': {'en': title},
        'description': {'en': description},
        'file': {
            'en': {
                'url': url,
                'contentType': 'image/jpeg'
            }
        }
    }
    return mock_asset


def create_mock_seo(
    locale: str = 'en',
    title: str = 'SEO Title',
    description: str = 'SEO Description',
    keywords: Optional[List[str]] = None,
    og_image_url: str = ''
) -> Mock:
    """
    Create a mock SEO entry.
    
    Args:
        locale: Locale code
        title: SEO title
        description: SEO description
        keywords: SEO keywords list
        og_image_url: OG image URL
    
    Returns:
        Mock SEO Entry
    """
    mock_seo = Mock()
    mock_seo.id = 'seo-123'
    
    seo_data = {
        'title': title,
        'description': description,
        'keywords': keywords or ['test', 'blog'],
        'noIndex': False,
        'canonicalUrl': ''
    }
    
    if og_image_url:
        seo_data['ogImage'] = create_mock_asset(url=og_image_url)
    
    mock_seo.fields.return_value = seo_data
    
    return mock_seo


def create_mock_menu_item(
    label: str = 'Home',
    url: str = '/',
    locale: str = 'en'
) -> Mock:
    """
    Create a mock menu item entry.
    
    Args:
        label: Menu label
        url: Menu URL
        locale: Locale code
    
    Returns:
        Mock menu item Entry
    """
    mock_menu = Mock()
    mock_menu.id = f'menu-{label.lower()}'
    mock_menu.fields.return_value = {
        'label': label,
        'url': url
    }
    return mock_menu


def create_mock_social_link(
    platform: str = 'Twitter',
    url: str = 'https://twitter.com/user'
) -> Mock:
    """
    Create a mock social link entry.
    
    Args:
        platform: Social platform name
        url: Profile URL
    
    Returns:
        Mock social link Entry
    """
    mock_social = Mock()
    mock_social.id = f'social-{platform.lower()}'
    mock_social.fields.return_value = {
        'platform': platform,
        'url': url
    }
    return mock_social


def create_mock_blog_post(
    locale: str = 'en',
    with_seo: bool = True,
    **overrides
) -> Mock:
    """
    Create a mock blog post entry.
    
    Args:
        locale: Locale code
        with_seo: Include SEO entry
        **overrides: Field overrides
    
    Returns:
        Mock blog post Entry
    """
    mock_entry = Mock()
    mock_entry.id = overrides.get('entry_id', 'blog-post-123')
    
    # Default fields
    fields_data = {
        'title': 'Test Blog Post',
        'url': 'test-blog-post',
        'description': 'This is a test blog post excerpt.',
        'label': 'Technology',
        'author': 'Test Author',
        'publishDate': '2026-01-19T10:30:00Z',
        'image': create_mock_asset(),
        'text': {
            'nodeType': 'document',
            'content': [
                {
                    'nodeType': 'paragraph',
                    'content': [
                        {
                            'nodeType': 'text',
                            'value': 'This is a test paragraph.',
                            'marks': []
                        }
                    ]
                }
            ]
        }
    }
    
    # Add SEO if requested
    if with_seo:
        fields_data['seo'] = create_mock_seo(locale=locale)
    
    # Apply overrides
    fields_data.update(overrides)
    
    mock_entry.fields.return_value = fields_data
    
    return mock_entry


def create_mock_profile(
    locale: str = 'en',
    **overrides
) -> Mock:
    """
    Create a mock profile entry.
    
    Args:
        locale: Locale code
        **overrides: Field overrides
    
    Returns:
        Mock profile Entry
    """
    mock_entry = Mock()
    mock_entry.id = 'profile-123'
    
    fields_data = {
        'fullName': 'John Doe',
        'title': 'Software Engineer',
        'bio': 'A passionate developer.',
        'email': 'john@example.com',
        'profileImage': create_mock_asset(),
        'socialLinks': [
            create_mock_social_link('Twitter', 'https://twitter.com/johndoe'),
            create_mock_social_link('GitHub', 'https://github.com/johndoe')
        ],
        'ctaLabel': 'Contact Me',
        'ctaUrl': '/contact'
    }
    
    fields_data.update(overrides)
    
    mock_entry.fields.return_value = fields_data
    
    return mock_entry


def create_mock_header(
    locale: str = 'en',
    **overrides
) -> Mock:
    """
    Create a mock header entry.
    
    Args:
        locale: Locale code
        **overrides: Field overrides
    
    Returns:
        Mock header Entry
    """
    mock_entry = Mock()
    mock_entry.id = 'header-123'
    
    fields_data = {
        'brandUrl': '/',
        'brandImage': create_mock_asset(),
        'menuItems': [
            create_mock_menu_item('Home', '/'),
            create_mock_menu_item('Blog', '/blog'),
            create_mock_menu_item('About', '/about')
        ],
        'topLinks': []
    }
    
    fields_data.update(overrides)
    
    mock_entry.fields.return_value = fields_data
    
    return mock_entry


def create_mock_footer(
    locale: str = 'en',
    **overrides
) -> Mock:
    """
    Create a mock footer entry.
    
    Args:
        locale: Locale code
        **overrides: Field overrides
    
    Returns:
        Mock footer Entry
    """
    mock_entry = Mock()
    mock_entry.id = 'footer-123'
    
    fields_data = {
        'brandUrl': '/',
        'brandImage': create_mock_asset(),
        'description': 'Personal website of John Doe.',
        'copyright': '© 2026 John Doe. All rights reserved.',
        'menuItems': [
            create_mock_menu_item('Privacy', '/privacy'),
            create_mock_menu_item('Terms', '/terms')
        ],
        'socialLinks': [
            create_mock_social_link('Twitter', 'https://twitter.com/johndoe')
        ]
    }
    
    fields_data.update(overrides)
    
    mock_entry.fields.return_value = fields_data
    
    return mock_entry
