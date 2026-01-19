# Python-Jekyll Integration Architecture
**Project:** github-page Portfolio  
**Purpose:** Detailed integration design for Contentful → Python → Jekyll pipeline  
**Date:** 2026-01-18  
**Status:** Implementation Ready

---

## 1. Overview

This document specifies the integration layer between Contentful CMS and Jekyll static site generator, powered by a Python transformation script. The architecture follows the **blog-first strategy**, prioritizing blog content transformation and homepage carousel generation.

### 1.1 Integration Goals

- **Automated**: Trigger builds on content publish (Contentful webhook → GitHub Actions)
- **Fast**: Complete transformation + build in < 5 minutes
- **Reliable**: Graceful error handling, no silent failures
- **Localized**: Full multi-language support (ISO 639-1)
- **Maintainable**: Modular, tested, documented code

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      CONTENTFUL CMS                          │
│                                                              │
│  Content Types:                                              │
│  ├── blogTemplate (Blog Posts)          ← PRIMARY           │
│  ├── profile (Author Profile)                               │
│  ├── componentCard (Reusable Cards)                         │
│  ├── componentCarousel (Blog Carousel)                      │
│  ├── pageTemplate (Homepage)                                │
│  ├── seo (SEO Metadata)                                     │
│  └── orHeader/orFooter (Navigation)                         │
│                                                              │
│  Locales: en (primary), es, ...                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Contentful Delivery API (REST)
                     │ https://cdn.contentful.com/spaces/{space_id}/...
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              PYTHON TRANSFORMATION SCRIPT                    │
│                                                              │
│  Entry Point: scripts/contentful_to_jekyll.py              │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. FETCH PHASE                                      │    │
│  │    - Connect to Contentful Delivery API            │    │
│  │    - Fetch all blog posts (all locales)            │    │
│  │    - Fetch profile data (singleton)                │    │
│  │    - Fetch header/footer config                    │    │
│  │    - Fetch homepage config                         │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 2. RESOLVE PHASE                                    │    │
│  │    - Resolve entry references (SEO, images)        │    │
│  │    - Resolve asset URLs                            │    │
│  │    - Handle rich text embedded entries             │    │
│  │    - Build reference graph (up to 2 levels)        │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 3. TRANSFORM PHASE                                  │    │
│  │    - Blog posts → Markdown + frontmatter           │    │
│  │    - Profile → YAML data file                      │    │
│  │    - Generate blog carousel data (auto)            │    │
│  │    - Homepage → Markdown page                      │    │
│  │    - Navigation → YAML data                        │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 4. WRITE PHASE                                      │    │
│  │    - Write localized posts:                        │    │
│  │      _posts/en/2026-01-18-post.md                  │    │
│  │      _posts/es/2026-01-18-post.md                  │    │
│  │    - Write data files:                             │    │
│  │      _data/profile-en.yml                          │    │
│  │      _data/blog-carousel-en.yml                    │    │
│  │    - Write pages:                                  │    │
│  │      _pages/en/index.md                            │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Output: Jekyll-compatible directory structure              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Filesystem writes
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    JEKYLL STATIC SITE                        │
│                                                              │
│  Inputs:                                                     │
│  ├── _posts/      (Blog post markdown files)                │
│  ├── _pages/      (Static pages)                            │
│  ├── _data/       (Profile, carousel, navigation)           │
│  ├── _layouts/    (HTML templates)                          │
│  ├── _includes/   (Reusable components)                     │
│  └── assets/      (CSS, JS, images)                         │
│                                                              │
│  Process:                                                    │
│  1. Read Markdown + frontmatter                             │
│  2. Apply Liquid templates                                  │
│  3. Generate static HTML/CSS/JS                             │
│                                                              │
│  Output:                                                     │
│  └── _site/       (Static files for GitHub Pages)          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ GitHub Pages deployment
                     │
                     ▼
             USER.GITHUB.IO (Live Site)
```

---

## 3. Python Script Architecture

### 3.1 Project Structure

```
scripts/
├── contentful_to_jekyll.py    # Main entry point
├── config.py                   # Configuration constants
├── requirements.txt            # Python dependencies
│
├── contentful_client/
│   ├── __init__.py
│   ├── client.py              # Contentful API wrapper
│   └── models.py              # Entry/Asset data models
│
├── transformers/
│   ├── __init__.py
│   ├── base.py                # Base transformer class
│   ├── blog_post.py           # Blog post transformer
│   ├── profile.py             # Profile transformer
│   ├── homepage.py            # Homepage transformer
│   ├── navigation.py          # Header/footer transformer
│   └── carousel.py            # Blog carousel generator
│
├── converters/
│   ├── __init__.py
│   ├── rich_text.py           # Rich text → Markdown
│   └── assets.py              # Asset URL resolution
│
├── writers/
│   ├── __init__.py
│   ├── markdown.py            # Markdown file writer
│   └── yaml.py                # YAML data writer
│
└── tests/
    ├── __init__.py
    ├── test_blog_post.py
    ├── test_profile.py
    └── fixtures/
        └── mock_entries.json
```

### 3.2 Dependencies (`requirements.txt`)

```
contentful==1.13.3
python-frontmatter==1.0.0
PyYAML==6.0
python-dateutil==2.8.2
requests==2.31.0
pytest==7.4.3
pytest-cov==4.1.0
```

---

## 4. Detailed Component Specifications

### 4.1 Main Entry Point (`contentful_to_jekyll.py`)

```python
#!/usr/bin/env python3
"""
Contentful to Jekyll Transformation Script

Fetches content from Contentful and transforms it to Jekyll-compatible format.
Prioritizes blog posts and homepage carousel generation.
"""

import logging
from config import SUPPORTED_LOCALES
from contentful_client import ContentfulClient
from transformers import (
    BlogPostTransformer,
    ProfileTransformer,
    CarouselGenerator,
    HomepageTransformer,
    NavigationTransformer
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main transformation pipeline"""
    try:
        logger.info("Starting Contentful → Jekyll transformation")
        
        # Initialize Contentful client
        client = ContentfulClient()
        
        # For each supported locale
        for locale in SUPPORTED_LOCALES:
            logger.info(f"Processing locale: {locale}")
            
            # Transform blog posts (PRIORITY)
            blog_transformer = BlogPostTransformer(client, locale)
            blog_posts = blog_transformer.transform_all()
            logger.info(f"Transformed {len(blog_posts)} blog posts ({locale})")
            
            # Generate blog carousel from latest posts
            carousel_generator = CarouselGenerator(client, locale)
            carousel_data = carousel_generator.generate_from_posts(blog_posts)
            carousel_generator.write_data_file()
            logger.info(f"Generated blog carousel with {len(carousel_data)} cards")
            
            # Transform profile (singleton)
            profile_transformer = ProfileTransformer(client, locale)
            profile_data = profile_transformer.transform()
            profile_transformer.write_data_file()
            logger.info(f"Transformed profile data ({locale})")
            
            # Transform homepage
            homepage_transformer = HomepageTransformer(client, locale)
            homepage_page = homepage_transformer.transform()
            homepage_transformer.write_page_file()
            logger.info(f"Generated homepage ({locale})")
        
        # Transform navigation (once, language-independent structure)
        nav_transformer = NavigationTransformer(client)
        nav_transformer.transform_header()
        nav_transformer.transform_footer()
        logger.info("Generated navigation data")
        
        logger.info("✅ Transformation complete!")
        return 0
    
    except Exception as e:
        logger.error(f"❌ Transformation failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())
```

---

### 4.2 Contentful Client (`contentful_client/client.py`)

```python
"""
Contentful API Client Wrapper

Handles all interactions with Contentful Delivery API.
Includes caching and error handling.
"""

from contentful import Client
from config import (
    CONTENTFUL_SPACE_ID,
    CONTENTFUL_ACCESS_TOKEN,
    CONTENTFUL_ENVIRONMENT
)
import logging

logger = logging.getLogger(__name__)


class ContentfulClient:
    """Wrapper around Contentful Python SDK"""
    
    def __init__(self):
        """Initialize Contentful client"""
        self.client = Client(
            CONTENTFUL_SPACE_ID,
            CONTENTFUL_ACCESS_TOKEN,
            environment=CONTENTFUL_ENVIRONMENT
        )
        self._cache = {}
    
    def get_blog_posts(self, locale='en', limit=100):
        """
        Fetch all published blog posts.
        
        Args:
            locale: ISO 639-1 language code
            limit: Max number of posts to fetch
        
        Returns:
            List of blog post entries
        """
        cache_key = f"blog_posts_{locale}_{limit}"
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        try:
            entries = self.client.entries({
                'content_type': 'blogTemplate',
                'locale': locale,
                'order': '-fields.publishDate',
                'limit': limit,
                'include': 2  # Resolve 2 levels of references
            })
            
            self._cache[cache_key] = entries
            logger.info(f"Fetched {len(entries)} blog posts ({locale})")
            return entries
        
        except Exception as e:
            logger.error(f"Failed to fetch blog posts: {e}")
            raise
    
    def get_profile(self, locale='en'):
        """
        Fetch profile entry (singleton).
        
        Args:
            locale: ISO 639-1 language code
        
        Returns:
            Profile entry or None
        """
        cache_key = f"profile_{locale}"
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        try:
            entries = self.client.entries({
                'content_type': 'profile',
                'locale': locale,
                'limit': 1,
                'include': 2
            })
            
            if not entries:
                logger.warning("No profile entry found")
                return None
            
            profile = entries[0]
            self._cache[cache_key] = profile
            return profile
        
        except Exception as e:
            logger.error(f"Failed to fetch profile: {e}")
            raise
    
    def get_homepage(self, locale='en'):
        """
        Fetch homepage entry.
        
        Args:
            locale: ISO 639-1 language code
        
        Returns:
            Homepage entry or None
        """
        try:
            entries = self.client.entries({
                'content_type': 'pageTemplate',
                'locale': locale,
                'fields.url': '/' if locale == 'en' else f'/{locale}/',
                'limit': 1,
                'include': 3
            })
            
            if not entries:
                logger.warning(f"No homepage entry found for locale: {locale}")
                return None
            
            return entries[0]
        
        except Exception as e:
            logger.error(f"Failed to fetch homepage: {e}")
            raise
```

---

### 4.3 Blog Post Transformer (`transformers/blog_post.py`)

```python
"""
Blog Post Transformer

Converts Contentful blog post entries to Jekyll markdown files.
"""

import os
from datetime import datetime
import frontmatter
from converters.rich_text import rich_text_to_markdown
from writers.markdown import write_markdown_file
from config import POSTS_DIR
import logging

logger = logging.getLogger(__name__)


class BlogPostTransformer:
    """Transform blog posts from Contentful to Jekyll"""
    
    def __init__(self, client, locale='en'):
        """
        Initialize transformer.
        
        Args:
            client: ContentfulClient instance
            locale: ISO 639-1 language code
        """
        self.client = client
        self.locale = locale
    
    def transform_all(self):
        """
        Transform all blog posts for the current locale.
        
        Returns:
            List of transformed post data (for carousel generation)
        """
        entries = self.client.get_blog_posts(locale=self.locale)
        transformed_posts = []
        
        for entry in entries:
            try:
                post_data = self.transform_single(entry)
                transformed_posts.append(post_data)
            except Exception as e:
                logger.error(f"Failed to transform post {entry.id}: {e}")
                # Continue with other posts
        
        return transformed_posts
    
    def transform_single(self, entry):
        """
        Transform a single blog post entry.
        
        Args:
            entry: Contentful blog post entry
        
        Returns:
            Dict with post metadata (for carousel)
        """
        # Extract fields (with locale fallback)
        fields = entry.fields(locale=self.locale, fallback_locale='en')
        
        title = fields.get('title', 'Untitled')
        description = fields.get('description', '')
        body_rich_text = fields.get('text', {})
        url_slug = fields.get('url', 'untitled')
        
        # Non-localized fields
        publish_date = entry.fields().get('publishDate')
        if not publish_date:
            publish_date = datetime.now()
        
        author = entry.fields().get('author', 'Simon Salazar')
        category = entry.fields().get('label', 'Blog')
        
        # Resolve SEO entry
        seo_entry = entry.fields().get('seo')
        seo_title = None
        seo_description = None
        canonical_url = None
        
        if seo_entry:
            seo_fields = seo_entry.fields(locale=self.locale, fallback_locale='en')
            seo_title = seo_fields.get('title')
            seo_description = seo_fields.get('description')
            canonical_url = seo_entry.fields().get('canonicalUrl')
        
        # Resolve featured image
        image_asset = entry.fields().get('image')
        image_url = ''
        if image_asset:
            image_url = f"https:{image_asset.url()}"
        
        # Convert rich text to Markdown
        markdown_body = rich_text_to_markdown(body_rich_text)
        
        # Build frontmatter
        post_frontmatter = {
            'layout': 'post',
            'title': title,
            'date': publish_date.strftime('%Y-%m-%d'),
            'author': author,
            'category': category,
            'excerpt': description[:300] if len(description) > 300 else description,
            'image': image_url,
            'lang': self.locale,
            'slug': url_slug,
        }
        
        # Add SEO fields if present
        if seo_title:
            post_frontmatter['seo_title'] = seo_title
        if seo_description:
            post_frontmatter['seo_description'] = seo_description
        if canonical_url:
            post_frontmatter['canonical_url'] = canonical_url
        
        # Create Post object (python-frontmatter)
        post = frontmatter.Post(markdown_body, **post_frontmatter)
        
        # Generate file path
        date_prefix = publish_date.strftime('%Y-%m-%d')
        file_path = os.path.join(POSTS_DIR, self.locale, f"{date_prefix}-{url_slug}.md")
        
        # Write file
        write_markdown_file(file_path, post)
        logger.info(f"Wrote blog post: {file_path}")
        
        # Return metadata for carousel
        return {
            'title': title,
            'description': description,
            'url': f"/{self.locale}/blog/{url_slug}/",
            'image': image_url,
            'date': publish_date.strftime('%Y-%m-%d'),
            'category': category
        }
```

---

### 4.4 Carousel Generator (`transformers/carousel.py`)

```python
"""
Blog Carousel Generator

Auto-generates carousel data from latest blog posts.
"""

import os
import yaml
from config import DATA_DIR, MAX_BLOG_POSTS_IN_CAROUSEL
import logging

logger = logging.getLogger(__name__)


class CarouselGenerator:
    """Generate blog carousel data for homepage"""
    
    def __init__(self, client, locale='en'):
        """
        Initialize generator.
        
        Args:
            client: ContentfulClient instance
            locale: ISO 639-1 language code
        """
        self.client = client
        self.locale = locale
        self.carousel_data = {}
    
    def generate_from_posts(self, posts):
        """
        Generate carousel data from blog posts.
        
        Args:
            posts: List of post metadata dicts (from BlogPostTransformer)
        
        Returns:
            Dict with carousel data
        """
        # Limit to max cards
        limited_posts = posts[:MAX_BLOG_POSTS_IN_CAROUSEL]
        
        # Build carousel structure
        self.carousel_data = {
            'title': 'Latest Blog Posts' if self.locale == 'en' else 'Últimas Entradas',
            'cards': []
        }
        
        for post in limited_posts:
            card = {
                'title': post['title'],
                'description': post['description'][:150],  # Truncate
                'image': post['image'],
                'url': post['url'],
                'date': post['date'],
                'category': post['category']
            }
            self.carousel_data['cards'].append(card)
        
        logger.info(f"Generated carousel with {len(self.carousel_data['cards'])} cards")
        return self.carousel_data
    
    def write_data_file(self):
        """Write carousel data to YAML file"""
        file_path = os.path.join(DATA_DIR, f"blog-carousel-{self.locale}.yml")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.carousel_data, f, allow_unicode=True, sort_keys=False)
        
        logger.info(f"Wrote carousel data: {file_path}")
```

---

### 4.5 Rich Text Converter (`converters/rich_text.py`)

```python
"""
Rich Text to Markdown Converter

Converts Contentful rich text format to Jekyll-compatible Markdown.
"""

import logging

logger = logging.getLogger(__name__)


def rich_text_to_markdown(rich_text_data):
    """
    Convert Contentful rich text to Markdown.
    
    Args:
        rich_text_data: Contentful rich text JSON structure
    
    Returns:
        String: Markdown content
    """
    if not rich_text_data or 'content' not in rich_text_data:
        return ""
    
    markdown_lines = []
    
    for node in rich_text_data['content']:
        markdown = process_node(node)
        if markdown:
            markdown_lines.append(markdown)
    
    return "\n\n".join(markdown_lines)


def process_node(node):
    """
    Recursively process a rich text node.
    
    Args:
        node: Dict representing a rich text node
    
    Returns:
        String: Markdown representation
    """
    node_type = node.get('nodeType')
    
    # Handle different node types
    if node_type == 'paragraph':
        return process_paragraph(node)
    
    elif node_type.startswith('heading-'):
        level = int(node_type.split('-')[1])
        return process_heading(node, level)
    
    elif node_type == 'unordered-list':
        return process_list(node, ordered=False)
    
    elif node_type == 'ordered-list':
        return process_list(node, ordered=True)
    
    elif node_type == 'blockquote':
        return process_blockquote(node)
    
    elif node_type == 'hr':
        return "---"
    
    elif node_type == 'embedded-asset-block':
        return process_embedded_asset(node)
    
    elif node_type == 'hyperlink':
        return process_hyperlink(node)
    
    else:
        logger.warning(f"Unhandled node type: {node_type}")
        return ""


def process_paragraph(node):
    """Process paragraph node"""
    content = process_inline_content(node.get('content', []))
    return content


def process_heading(node, level):
    """Process heading node"""
    hashes = '#' * level
    content = process_inline_content(node.get('content', []))
    return f"{hashes} {content}"


def process_inline_content(content_nodes):
    """Process inline content (text, marks)"""
    result = []
    
    for node in content_nodes:
        if node.get('nodeType') == 'text':
            text = node.get('value', '')
            marks = node.get('marks', [])
            
            # Apply marks
            for mark in marks:
                mark_type = mark.get('type')
                if mark_type == 'bold':
                    text = f"**{text}**"
                elif mark_type == 'italic':
                    text = f"*{text}*"
                elif mark_type == 'code':
                    text = f"`{text}`"
            
            result.append(text)
    
    return "".join(result)


def process_list(node, ordered=False):
    """Process list node"""
    items = []
    content = node.get('content', [])
    
    for i, item_node in enumerate(content, 1):
        item_content = []
        for child_node in item_node.get('content', []):
            item_text = process_node(child_node)
            if item_text:
                item_content.append(item_text)
        
        item_text = " ".join(item_content)
        
        if ordered:
            items.append(f"{i}. {item_text}")
        else:
            items.append(f"- {item_text}")
    
    return "\n".join(items)


def process_blockquote(node):
    """Process blockquote node"""
    content = []
    for child_node in node.get('content', []):
        child_md = process_node(child_node)
        if child_md:
            content.append(f"> {child_md}")
    
    return "\n".join(content)


def process_embedded_asset(node):
    """Process embedded asset (image)"""
    data = node.get('data', {})
    target = data.get('target', {})
    
    if target:
        url = f"https:{target.get('fields', {}).get('file', {}).get('url', '')}"
        title = target.get('fields', {}).get('title', 'Image')
        description = target.get('fields', {}).get('description', '')
        
        alt_text = description if description else title
        return f"![{alt_text}]({url})"
    
    return ""


def process_hyperlink(node):
    """Process hyperlink"""
    data = node.get('data', {})
    uri = data.get('uri', '')
    content = process_inline_content(node.get('content', []))
    
    return f"[{content}]({uri})"
```

---

## 5. Jekyll Integration

### 5.1 Expected Jekyll Directory Structure (Output)

```
_posts/
├── en/
│   ├── 2026-01-18-my-first-post.md
│   ├── 2026-01-15-another-post.md
│   └── ...
└── es/
    ├── 2026-01-18-mi-primer-post.md
    └── ...

_pages/
├── en/
│   ├── index.md
│   └── about.md
└── es/
    ├── index.md
    └── about.md

_data/
├── profile-en.yml
├── profile-es.yml
├── blog-carousel-en.yml
├── blog-carousel-es.yml
├── navigation.yml
└── i18n.yml

_layouts/
├── default.html
├── homepage.html
├── post.html
└── page.html

_includes/
├── header.html
├── footer.html
├── blog-carousel.html
├── profile-section.html
└── card.html
```

### 5.2 Example Output Files

**Blog Post Markdown (`_posts/en/2026-01-18-my-first-post.md`):**

```markdown
---
layout: post
title: "My First Blog Post"
date: 2026-01-18
author: "Simon Salazar"
category: "Technology"
excerpt: "This is my first post about building a blog-first personal website..."
image: "https://images.ctfassets.net/..."
lang: en
slug: "my-first-post"
seo_title: "My First Blog Post - Simon Salazar"
seo_description: "Learn how I built a blog-first personal website with Contentful and Jekyll"
---

Welcome to my first blog post! In this article, I'll share...

## Introduction

I've been wanting to create a personal blog for a while...

## The Technical Stack

Here's what I chose:

- **CMS**: Contentful
- **Static Site Generator**: Jekyll
- **Hosting**: GitHub Pages

## Conclusion

Building this site was a great learning experience...
```

**Blog Carousel Data (`_data/blog-carousel-en.yml`):**

```yaml
title: Latest Blog Posts
cards:
  - title: "My First Blog Post"
    description: "This is my first post about building a blog-first personal website with Contentful, Python, and Jekyll..."
    image: "https://images.ctfassets.net/..."
    url: "/en/blog/my-first-post/"
    date: "2026-01-18"
    category: "Technology"
  
  - title: "How I Optimized My Site for Performance"
    description: "In this post, I share techniques for optimizing a Jekyll site for speed..."
    image: "https://images.ctfassets.net/..."
    url: "/en/blog/performance-optimization/"
    date: "2026-01-15"
    category: "Technology"
```

**Profile Data (`_data/profile-en.yml`):**

```yaml
fullName: "Simon Salazar"
title: "Researcher & Developer"
bio: |
  I'm a researcher and developer passionate about creating tools that make 
  a difference. I write about technology, research, and personal growth.
profileImage: "https://images.ctfassets.net/..."
email: "simon@example.com"
socialLinks:
  - platform: "LinkedIn"
    url: "https://linkedin.com/in/simonsalazar"
    icon: "linkedin"
  - platform: "GitHub"
    url: "https://github.com/simonsalazar"
    icon: "github"
ctaLabel: "View My Work"
ctaUrl: "/en/projects/"
```

---

## 6. Error Handling & Edge Cases

### 6.1 Missing Content

**Scenario:** Profile entry doesn't exist in Contentful

**Handling:**
```python
profile = client.get_profile(locale='en')
if not profile:
    logger.warning("No profile entry found, using defaults")
    profile_data = {
        'fullName': 'Your Name',
        'title': 'Your Title',
        'bio': 'Bio not configured'
    }
```

### 6.2 Invalid Rich Text

**Scenario:** Blog post has malformed rich text

**Handling:**
```python
try:
    markdown_body = rich_text_to_markdown(body_rich_text)
except Exception as e:
    logger.error(f"Rich text conversion failed: {e}")
    markdown_body = "[Content could not be converted]"
```

### 6.3 Missing Localization

**Scenario:** Blog post exists in English but not Spanish

**Handling:**
```python
fields = entry.fields(locale='es', fallback_locale='en')
# Contentful SDK automatically falls back to English
```

### 6.4 Image URL Resolution

**Scenario:** Featured image asset is not published

**Handling:**
```python
image_asset = entry.fields().get('image')
if image_asset and hasattr(image_asset, 'url'):
    image_url = f"https:{image_asset.url()}"
else:
    logger.warning(f"No image for post: {entry.id}")
    image_url = "/assets/images/default-blog-image.jpg"
```

---

## 7. Performance Considerations

### 7.1 API Call Optimization

**Strategy:** Minimize Contentful API calls

- Use `include=2` to resolve references in single call
- Cache entries within script execution
- Batch fetch entries (`limit=100`)

### 7.2 Build Time Optimization

**Target:** < 5 minutes total (Python + Jekyll)

**Breakdown:**
- Python script: < 2 minutes
- Jekyll build: < 3 minutes

**Optimizations:**
- Parallel locale processing (future enhancement)
- Incremental builds (Jekyll native support)
- Image optimization offloaded to Contentful CDN

---

## 8. Testing Strategy

### 8.1 Unit Tests

**Test Coverage:**
- Blog post transformation
- Rich text → Markdown conversion
- Carousel generation
- Data file writing

**Example Test:**
```python
def test_blog_post_transformation(mock_contentful_entry):
    transformer = BlogPostTransformer(mock_client, 'en')
    post_data = transformer.transform_single(mock_contentful_entry)
    
    assert post_data['title'] == "Test Post"
    assert post_data['url'] == "/en/blog/test-post/"
    assert post_data['image'].startswith("https://")
```

### 8.2 Integration Tests

**Test Full Pipeline:**
```bash
# Run transformation with test Contentful space
export CONTENTFUL_SPACE_ID=test_space
export CONTENTFUL_ACCESS_TOKEN=test_token
python scripts/contentful_to_jekyll.py

# Verify outputs
assert [ -f "_posts/en/2026-01-18-test-post.md" ]
assert [ -f "_data/blog-carousel-en.yml" ]
assert [ -f "_data/profile-en.yml" ]
```

---

## 9. Deployment

### 9.1 GitHub Actions Integration

**Workflow Trigger:**
1. Contentful webhook → GitHub repository dispatch
2. GitHub Actions runs workflow
3. Workflow executes: `python scripts/contentful_to_jekyll.py`
4. Jekyll builds site
5. Deploy to GitHub Pages

**See `technical-specification-20260118.md` Section 7 for full workflow.**

---

## 10. Monitoring & Debugging

### 10.1 Logging

**Log Levels:**
- `INFO`: Normal operations (posts transformed, files written)
- `WARNING`: Non-critical issues (missing optional fields, fallback to defaults)
- `ERROR`: Transformation failures (skip entry, continue)
- `CRITICAL`: Build failures (abort, fail GitHub Actions)

**Example Logs:**
```
2026-01-18 14:23:10 - INFO - Starting Contentful → Jekyll transformation
2026-01-18 14:23:11 - INFO - Processing locale: en
2026-01-18 14:23:12 - INFO - Fetched 12 blog posts (en)
2026-01-18 14:23:13 - INFO - Transformed 12 blog posts (en)
2026-01-18 14:23:14 - INFO - Generated blog carousel with 10 cards
2026-01-18 14:23:15 - INFO - ✅ Transformation complete!
```

### 10.2 Debugging

**Enable Debug Mode:**
```bash
export LOG_LEVEL=DEBUG
python scripts/contentful_to_jekyll.py
```

**Debug Outputs:**
- Full Contentful API responses
- Intermediate transformation data
- File write operations
- Cache hits/misses

---

## 11. Future Enhancements

### Phase 2 Considerations

**Performance:**
- Async/parallel API calls (aiohttp)
- Incremental transformation (only changed entries)
- Redis caching for CI/CD runs

**Features:**
- Image download and optimization (Pillow)
- Automatic image WebP conversion
- Markdown lint/validation
- Content preview in GitHub PR comments

**Monitoring:**
- Transformation success metrics
- Build time tracking
- Error rate alerts

---

## Appendix: Quick Reference

### Key Files Generated by Python Script

| File Path | Source | Content |
|-----------|--------|---------|
| `_posts/{locale}/{date}-{slug}.md` | `blogTemplate` | Blog post markdown |
| `_data/profile-{locale}.yml` | `profile` | Profile data |
| `_data/blog-carousel-{locale}.yml` | Auto-generated | Latest blog posts |
| `_pages/{locale}/index.md` | `pageTemplate` | Homepage |
| `_data/navigation.yml` | `orHeader`, `orFooter` | Site navigation |

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `CONTENTFUL_SPACE_ID` | Yes | Contentful space identifier |
| `CONTENTFUL_ACCESS_TOKEN` | Yes | Delivery API token |
| `CONTENTFUL_ENVIRONMENT` | No | Defaults to `master` |
| `LOG_LEVEL` | No | Defaults to `INFO` |

---

**Document Status:** Implementation Ready  
**Next Steps:** Implement Python script modules  
**Maintained By:** Simon Salazar
