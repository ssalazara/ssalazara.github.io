# Technical Specification: github-page Portfolio
**Status:** Draft / Implementation Ready  
**Approach:** Spec-Driven Development (SDD)  
**Version:** 2.0  
**Last Updated:** 2026-01-18

---

## 1. Project Philosophy: Spec-Driven Development (SDD)

The project adheres to SDD as its core foundation. No implementation (content types, scripts, or UI) shall proceed without a preceding specification.

### 1.1 Core Principles

- **Spec-First:** Every feature must have a defined interface and behavior before code is written.
- **Contract Integrity:** The Contentful schema is the "Contract" between content creators and the codebase.
- **Atomic Implementation:** Features are broken down into the smallest testable units.
- **Traceability:** Every technical task must reference a specific requirement in this Master Spec or the PRD.
- **Blog-First Priority:** Blog content management is P0; all other features support this goal.

### 1.2 Definition of Done (DoD)

A feature is considered "Done" when:
1. It matches the defined Spec (acceptance criteria).
2. Contentful validations are configured and tested.
3. The Python transformation script handles the data correctly (with unit tests).
4. The Jekyll UI renders the data across all supported ISO languages.
5. Documentation is updated.
6. The feature supports the blog-first user experience.

---

## 2. Standards & Naming Conventions

### 2.1 Localization (ISO 639-1)

- **Standard:** ISO 639-1 (two-letter codes).
- **Primary Locale:** `en` (English).
- **Secondary Locales:** To be defined (e.g., `es`, `fr`, `de`).
- **Convention:** All localized fields in Contentful must have fallbacks to `en`.
- **URL Pattern:** `/{locale}/{content-type}/{slug}/`
  - Example: `/en/blog/my-first-post/`
  - Example: `/es/blog/mi-primer-post/`

### 2.2 Contentful Conventions

- **Content Type IDs:** camelCase with descriptive prefixes
  - Templates: `pageTemplate`, `blogTemplate`
  - Organisms: `orHeader`, `orFooter`, `heroBanner`
  - Molecules: `componentCarousel`, `componentRichText`
  - Atoms: `componentCard`, `componentSocialLink`, `mlMenuItem`
  - Utilities: `seo`, `profile`
- **Field IDs:** camelCase (e.g., `publishDate`, `featuredImage`).
- **Slugs:** Required for all top-level entries; must be unique and URL-safe.
- **Localized Fields:** Marked explicitly with `"localized": true`.

### 2.3 Python Standards

- **Coding Style:** PEP 8 compliance.
- **Python Version:** 3.11+ (for better performance and type hints).
- **Libraries:**
  - `contentful.py` (official SDK)
  - `PyYAML` (for Jekyll frontmatter)
  - `Pillow` (for image processing, if needed)
  - `python-frontmatter` (for generating Markdown with YAML)
- **Error Handling:** Graceful failure with logging; the build must fail loudly if critical content is missing.
- **Testing:** Unit tests with `pytest` for all transformation functions.

### 2.4 Jekyll Conventions

- **Version:** Jekyll 4.x
- **Collections:** `_posts/`, `_pages/`, `_data/`
- **Localized Structure:**
  ```
  _posts/
    en/
      2026-01-18-my-post.md
    es/
      2026-01-18-mi-post.md
  _pages/
    en/
      index.md
      about.md
    es/
      index.md
      about.md
  ```
- **Frontmatter Fields:** Standardized across all content types.
- **Layouts:** `default.html`, `post.html`, `page.html`, `homepage.html`.

---

## 3. High-Level Architecture

### 3.1 System Components

```
┌───────────────────────────────────────────────────────────┐
│                      CONTENTFUL CMS                        │
│  (Content Types: Blog, Profile, Card, Carousel, etc.)    │
└────────────────────┬──────────────────────────────────────┘
                     │
                     │ Webhook Trigger (on publish)
                     ▼
┌───────────────────────────────────────────────────────────┐
│                   GITHUB ACTIONS (CI/CD)                   │
│  - Triggered by Contentful webhook                        │
│  - Runs Python transformation script                      │
│  - Builds Jekyll site                                      │
│  - Deploys to GitHub Pages                                │
└────────────────────┬──────────────────────────────────────┘
                     │
                     │ Runs Python Script
                     ▼
┌───────────────────────────────────────────────────────────┐
│              PYTHON TRANSFORMATION LAYER                   │
│  1. Fetch content from Contentful Delivery API           │
│  2. Resolve references (SEO, images, related content)    │
│  3. Transform JSON → Jekyll Markdown + frontmatter       │
│  4. Generate localized file structure                     │
│  5. Auto-generate blog carousel data                      │
└────────────────────┬──────────────────────────────────────┘
                     │
                     │ Writes Markdown Files
                     ▼
┌───────────────────────────────────────────────────────────┐
│                   JEKYLL STATIC SITE                       │
│  - Markdown files in _posts/, _pages/                    │
│  - Data files in _data/ (profile, carousel)              │
│  - Layouts and includes for rendering                    │
│  - Builds static HTML/CSS/JS                             │
└────────────────────┬──────────────────────────────────────┘
                     │
                     │ Deploys Static Files
                     ▼
┌───────────────────────────────────────────────────────────┐
│                     GITHUB PAGES                           │
│  - Serves static files at user.github.io                 │
│  - SSL/TLS enabled                                         │
│  - Global CDN distribution                                │
└────────────────────┬──────────────────────────────────────┘
                     │
                     │ HTTP/HTTPS Requests
                     ▼
               SITE VISITORS
        (Fellows, Recruiters, Public)
```

### 3.2 Data Flow (Blog Post Publication)

```
1. Content Creator publishes blog post in Contentful
   ↓
2. Contentful triggers webhook → GitHub repository
   ↓
3. GitHub Actions workflow starts
   ↓
4. Python script executes:
   a. Connects to Contentful Delivery API
   b. Fetches blog post entry (all locales)
   c. Resolves linked SEO entry
   d. Resolves featured image asset
   e. Transforms to Jekyll frontmatter:
      ---
      layout: post
      title: "My First Post"
      date: 2026-01-18
      author: "Simon Salazar"
      category: "Technology"
      image: "/assets/images/my-post.jpg"
      excerpt: "This is my first post..."
      lang: en
      ---
   f. Writes body content (Markdown)
   g. Saves to: _posts/en/2026-01-18-my-first-post.md
   h. Repeats for Spanish: _posts/es/2026-01-18-mi-primer-post.md
   i. Updates blog carousel data: _data/blog-carousel.yml
   ↓
5. Jekyll builds site:
   a. Processes Markdown → HTML
   b. Applies layouts and includes
   c. Generates: /en/blog/my-first-post/index.html
   d. Generates: /es/blog/mi-primer-post/index.html
   ↓
6. GitHub Pages deploys built site
   ↓
7. Site live within 3-5 minutes
```

---

## 4. Content Transformation Pipeline

### 4.1 Python Script Architecture

**File Structure:**
```
scripts/
  contentful_to_jekyll.py   # Main transformation logic
  config.py                  # Configuration and constants
  models.py                  # Data models for content types
  transformers/
    blog_post.py             # Blog post transformer
    profile.py               # Profile transformer
    carousel.py              # Carousel generator
    seo.py                   # SEO metadata transformer
  utils/
    contentful_client.py     # Contentful API wrapper
    markdown_generator.py    # Markdown file writer
    image_processor.py       # Image optimization
  tests/
    test_blog_post.py
    test_profile.py
```

### 4.2 Core Transformation Functions

#### 4.2.1 Blog Post Transformation

**Input:** Contentful `blogTemplate` entry (JSON)

**Output:** Jekyll Markdown file with frontmatter

**Pseudo-code:**
```python
def transform_blog_post(entry, locale='en'):
    """
    Transform a Contentful blog post entry to Jekyll markdown.
    
    Args:
        entry: Contentful blog post entry object
        locale: ISO 639-1 language code
    
    Returns:
        Tuple[str, str]: (file_path, markdown_content)
    """
    # Extract localized fields
    title = entry.fields(locale).get('title')
    description = entry.fields(locale).get('description')
    body = entry.fields(locale).get('text')  # Rich text
    url_slug = entry.fields(locale).get('url')
    
    # Extract non-localized fields
    publish_date = entry.fields().get('publishDate')
    author = entry.fields().get('author', 'Simon Salazar')
    category = entry.fields().get('label', 'Uncategorized')
    
    # Resolve linked SEO entry
    seo_entry = entry.fields().get('seo')
    seo_data = transform_seo(seo_entry, locale) if seo_entry else {}
    
    # Resolve featured image asset
    image_asset = entry.fields().get('image')
    image_url = image_asset.url() if image_asset else ''
    
    # Generate frontmatter
    frontmatter = {
        'layout': 'post',
        'title': title,
        'date': publish_date.strftime('%Y-%m-%d'),
        'author': author,
        'category': category,
        'excerpt': description,
        'image': image_url,
        'lang': locale,
        'slug': url_slug,
        'seo_title': seo_data.get('title'),
        'seo_description': seo_data.get('description'),
        'canonical_url': seo_data.get('canonicalUrl'),
    }
    
    # Convert rich text to Markdown
    markdown_body = rich_text_to_markdown(body)
    
    # Combine frontmatter + body
    markdown_content = generate_markdown(frontmatter, markdown_body)
    
    # Generate file path
    date_prefix = publish_date.strftime('%Y-%m-%d')
    file_path = f"_posts/{locale}/{date_prefix}-{url_slug}.md"
    
    return file_path, markdown_content
```

#### 4.2.2 Blog Carousel Generation

**Purpose:** Auto-generate carousel data from latest blog posts

**Pseudo-code:**
```python
def generate_blog_carousel(locale='en', limit=10):
    """
    Generate blog carousel data for homepage.
    
    Args:
        locale: ISO 639-1 language code
        limit: Number of latest posts to include
    
    Returns:
        dict: Carousel data structure
    """
    # Fetch latest blog posts
    client = get_contentful_client()
    entries = client.entries({
        'content_type': 'blogTemplate',
        'order': '-fields.publishDate',
        'limit': limit,
        'locale': locale
    })
    
    carousel_cards = []
    for entry in entries:
        card = {
            'title': entry.fields(locale).get('title'),
            'description': entry.fields(locale).get('description')[:150],
            'image': entry.fields().get('image').url(),
            'url': f"/{locale}/blog/{entry.fields(locale).get('url')}/",
            'date': entry.fields().get('publishDate').strftime('%Y-%m-%d'),
            'category': entry.fields().get('label', 'Blog')
        }
        carousel_cards.append(card)
    
    carousel_data = {
        'title': 'Latest Blog Posts' if locale == 'en' else 'Últimas Entradas',
        'cards': carousel_cards
    }
    
    return carousel_data
```

**Output:** Saved to `_data/blog-carousel-{locale}.yml`

---

### 4.3 Rich Text to Markdown Conversion

Contentful rich text format must be converted to Jekyll-compatible Markdown.

**Supported Contentful Node Types:**
- `heading-2` → `## Heading`
- `heading-3` → `### Heading`
- `heading-4` → `#### Heading`
- `paragraph` → Plain text
- `ordered-list` → `1. Item`
- `unordered-list` → `- Item`
- `blockquote` → `> Quote`
- `hyperlink` → `[text](url)`
- `embedded-asset-block` → `![alt](image-url)`
- `embedded-entry-block` → Custom handling (e.g., quote component)

**Implementation:** Use `rich-text-renderer` library or custom recursive parser.

---

## 5. Jekyll Implementation

### 5.1 Site Structure

```
github-page/
├── _config.yml                # Jekyll configuration
├── _data/
│   ├── navigation.yml         # Site navigation (from Contentful Header)
│   ├── profile-en.yml         # Profile data (English)
│   ├── profile-es.yml         # Profile data (Spanish)
│   ├── blog-carousel-en.yml   # Blog carousel (English)
│   ├── blog-carousel-es.yml   # Blog carousel (Spanish)
│   └── i18n.yml               # Localization strings
├── _includes/
│   ├── header.html
│   ├── footer.html
│   ├── blog-carousel.html     # Blog carousel component
│   ├── profile-section.html   # Profile component
│   └── card.html              # Reusable card component
├── _layouts/
│   ├── default.html           # Base layout
│   ├── homepage.html          # Homepage layout
│   ├── post.html              # Blog post layout
│   └── page.html              # Generic page layout
├── _posts/
│   ├── en/
│   │   └── 2026-01-18-my-post.md
│   └── es/
│       └── 2026-01-18-mi-post.md
├── _pages/
│   ├── en/
│   │   ├── index.md           # English homepage
│   │   └── about.md
│   └── es/
│       ├── index.md           # Spanish homepage
│       └── about.md
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
├── scripts/
│   └── contentful_to_jekyll.py
└── README.md
```

### 5.2 Jekyll Configuration (`_config.yml`)

```yaml
# Site Settings
title: "Simon Salazar"
description: "Researcher, Developer, Writer"
url: "https://simon-salazar.github.io"
baseurl: ""

# Build Settings
markdown: kramdown
permalink: /:categories/:title/
timezone: America/New_York

# Collections
collections:
  posts:
    output: true
    permalink: /:lang/blog/:slug/

# Defaults
defaults:
  - scope:
      path: ""
      type: "posts"
    values:
      layout: "post"
      author: "Simon Salazar"
  - scope:
      path: "_pages/en"
    values:
      lang: "en"
      permalink: /:basename/
  - scope:
      path: "_pages/es"
    values:
      lang: "es"
      permalink: /es/:basename/

# Plugins
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag

# Exclude
exclude:
  - scripts/
  - README.md
  - Gemfile
  - Gemfile.lock
```

### 5.3 Homepage Layout (`_layouts/homepage.html`)

```liquid
---
layout: default
---

<!-- Hero Banner (optional) -->
{% if page.hero %}
  {% include hero-banner.html hero=page.hero %}
{% endif %}

<!-- Profile Section -->
{% assign profile_data = site.data['profile-' | append: page.lang] %}
{% include profile-section.html profile=profile_data %}

<!-- Blog Carousel (HERO ELEMENT) -->
{% assign carousel_data = site.data['blog-carousel-' | append: page.lang] %}
<section class="blog-carousel">
  <h2>{{ carousel_data.title }}</h2>
  <div class="carousel-container">
    {% for card in carousel_data.cards %}
      {% include card.html card=card %}
    {% endfor %}
  </div>
</section>

<!-- Additional Page Content -->
{{ content }}
```

### 5.4 Blog Post Layout (`_layouts/post.html`)

```liquid
---
layout: default
---

<article class="blog-post">
  <!-- Post Header -->
  <header class="post-header">
    <h1>{{ page.title }}</h1>
    <div class="post-meta">
      <span class="post-date">{{ page.date | date: "%B %d, %Y" }}</span>
      {% if page.author %}
        <span class="post-author">by {{ page.author }}</span>
      {% endif %}
      {% if page.category %}
        <span class="post-category">{{ page.category }}</span>
      {% endif %}
    </div>
    {% if page.image %}
      <img src="{{ page.image }}" alt="{{ page.title }}" class="featured-image">
    {% endif %}
  </header>

  <!-- Post Body -->
  <div class="post-content">
    {{ content }}
  </div>

  <!-- Post Footer -->
  <footer class="post-footer">
    <a href="/{{ page.lang }}/blog/" class="back-to-blog">← Back to Blog</a>
  </footer>
</article>

<!-- Related Posts (optional) -->
{% include related-posts.html %}
```

---

## 6. Localization Implementation

### 6.1 Language Switcher (Jekyll Include)

```liquid
<!-- _includes/language-switcher.html -->
<div class="language-switcher">
  <button class="lang-toggle" id="langToggle">
    <span class="current-lang">{{ page.lang | upcase }}</span>
    <svg class="icon-globe"><!-- globe icon --></svg>
  </button>
  <ul class="lang-menu" id="langMenu">
    {% if page.lang == 'en' %}
      <li><a href="/es{{ page.url | remove: '/en' }}">Español</a></li>
    {% else %}
      <li><a href="{{ page.url | remove: '/es' }}">English</a></li>
    {% endif %}
  </ul>
</div>

<script>
  // Toggle language menu
  document.getElementById('langToggle').addEventListener('click', () => {
    document.getElementById('langMenu').classList.toggle('open');
  });
  
  // Save language preference
  const lang = '{{ page.lang }}';
  localStorage.setItem('preferredLanguage', lang);
</script>
```

### 6.2 Localized Strings (`_data/i18n.yml`)

```yaml
read_more:
  en: "Read More"
  es: "Leer Más"

back_to_blog:
  en: "← Back to Blog"
  es: "← Volver al Blog"

latest_posts:
  en: "Latest Blog Posts"
  es: "Últimas Entradas"

published_on:
  en: "Published on"
  es: "Publicado el"

by_author:
  en: "by"
  es: "por"
```

**Usage in templates:**
```liquid
{{ site.data.i18n.read_more[page.lang] }}
```

---

## 7. GitHub Actions Workflow

### 7.1 Workflow File (`.github/workflows/contentful-deploy.yml`)

```yaml
name: Contentful to Jekyll Deployment

on:
  # Webhook trigger from Contentful
  repository_dispatch:
    types: [contentful-publish]
  
  # Manual trigger
  workflow_dispatch:
  
  # Scheduled daily build (backup)
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Python dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run Contentful transformation script
        env:
          CONTENTFUL_SPACE_ID: ${{ secrets.CONTENTFUL_SPACE_ID }}
          CONTENTFUL_ACCESS_TOKEN: ${{ secrets.CONTENTFUL_ACCESS_TOKEN }}
          CONTENTFUL_ENVIRONMENT: master
        run: |
          python scripts/contentful_to_jekyll.py
      
      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
      
      - name: Build Jekyll site
        run: |
          bundle exec jekyll build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
          publish_branch: gh-pages
```

### 7.2 Contentful Webhook Configuration

**Webhook URL:** `https://api.github.com/repos/USERNAME/REPO/dispatches`

**Payload:**
```json
{
  "event_type": "contentful-publish"
}
```

**Headers:**
```
Authorization: Bearer <GITHUB_PAT>
Content-Type: application/json
```

**Triggers:**
- Entry Published (any content type)
- Entry Unpublished
- Asset Published

---

## 8. Security & Environment Variables

### 8.1 Required Secrets (GitHub Repository Settings)

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `CONTENTFUL_SPACE_ID` | Contentful space ID | `abc123xyz456` |
| `CONTENTFUL_ACCESS_TOKEN` | Delivery API access token | `CFPAT-...` |
| `CONTENTFUL_PREVIEW_TOKEN` | (Optional) Preview API token | `CFPAT-...` |
| `GITHUB_PAT` | (Optional) Personal access token for webhooks | `ghp_...` |

### 8.2 Environment Configuration

**Development (`scripts/config.py`):**
```python
import os

CONTENTFUL_SPACE_ID = os.getenv('CONTENTFUL_SPACE_ID')
CONTENTFUL_ACCESS_TOKEN = os.getenv('CONTENTFUL_ACCESS_TOKEN')
CONTENTFUL_ENVIRONMENT = os.getenv('CONTENTFUL_ENVIRONMENT', 'master')

# Validation
if not CONTENTFUL_SPACE_ID or not CONTENTFUL_ACCESS_TOKEN:
    raise ValueError("Contentful credentials not configured")

# Locales
PRIMARY_LOCALE = 'en'
SUPPORTED_LOCALES = ['en', 'es']

# Paths
POSTS_DIR = '_posts'
PAGES_DIR = '_pages'
DATA_DIR = '_data'

# Content limits
MAX_BLOG_POSTS_IN_CAROUSEL = 10
```

---

## 9. Error Handling & Logging

### 9.1 Python Script Error Handling

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def transform_content():
    try:
        # Fetch content from Contentful
        entries = fetch_blog_posts()
        
        if not entries:
            logger.warning("No blog posts found in Contentful")
            return
        
        for entry in entries:
            try:
                transform_blog_post(entry)
                logger.info(f"Transformed blog post: {entry.id}")
            except Exception as e:
                logger.error(f"Failed to transform post {entry.id}: {e}")
                # Continue with other posts
        
        logger.info("Transformation complete")
    
    except Exception as e:
        logger.critical(f"Transformation failed: {e}")
        raise  # Fail the build
```

### 9.2 Build Failure Notifications

**GitHub Actions:** Configure notifications for build failures
- Email notifications (default)
- Slack integration (optional)
- Status badges in README

---

## 10. Performance Optimization

### 10.1 Image Optimization

**Strategy:**
1. Python script downloads images from Contentful
2. Resizes to appropriate dimensions:
   - Featured images: 1200x630px
   - Thumbnails: 400x300px
3. Compresses with Pillow (quality=85)
4. Saves to `assets/images/`
5. Generates srcset for responsive images

**Code:**
```python
from PIL import Image
import requests
from io import BytesIO

def optimize_image(image_url, output_path, max_width=1200):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    
    # Resize if needed
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)
    
    # Save with compression
    img.save(output_path, optimize=True, quality=85)
    logger.info(f"Optimized image: {output_path}")
```

### 10.2 Lazy Loading (Jekyll)

```liquid
<img 
  src="{{ image_url }}" 
  alt="{{ alt_text }}" 
  loading="lazy"
  decoding="async"
  width="1200"
  height="630"
>
```

### 10.3 CSS & JS Minification

**Jekyll Plugin:** `jekyll-minifier` (optional, for production)

```yaml
# _config.yml
minifier:
  uglifier_args:
    harmony: true
```

---

## 11. Testing Strategy

### 11.1 Python Unit Tests (`pytest`)

**Test Coverage:**
- Blog post transformation
- Profile data transformation
- Carousel generation
- Rich text → Markdown conversion
- Image URL resolution
- Localization handling

**Example Test:**
```python
def test_blog_post_transformation():
    # Mock Contentful entry
    mock_entry = create_mock_blog_post()
    
    # Transform
    file_path, content = transform_blog_post(mock_entry, locale='en')
    
    # Assertions
    assert file_path.startswith('_posts/en/')
    assert 'layout: post' in content
    assert mock_entry.title in content
    assert len(content) > 100  # Has content
```

### 11.2 Jekyll Build Testing

**Local Testing:**
```bash
# Run transformation
python scripts/contentful_to_jekyll.py

# Build Jekyll site
bundle exec jekyll serve

# Visit http://localhost:4000
```

**CI Testing:**
- GitHub Actions runs full build on every push
- Build must succeed before merge

### 11.3 Content Validation

**Pre-build Checks:**
- All required fields present
- Image URLs valid
- Slugs unique
- Dates valid
- Rich text parseable

---

## 12. Deployment & Rollback

### 12.1 Deployment Process

1. Content creator publishes in Contentful
2. Webhook triggers GitHub Actions
3. Python script transforms content
4. Jekyll builds static site
5. GitHub Pages deploys to `gh-pages` branch
6. Site live within 3-5 minutes

### 12.2 Rollback Strategy

**If bad content is published:**

**Option 1: Unpublish in Contentful**
- Unpublish the problematic entry
- Webhook triggers rebuild
- Site reverts to previous state

**Option 2: Manual Rollback (Git)**
```bash
# Revert to previous commit
git revert HEAD
git push origin main

# Triggers rebuild without bad content
```

**Option 3: Emergency Manual Build**
- Disable Contentful webhook temporarily
- Fix content locally
- Push to repository
- Re-enable webhook

---

## 13. Monitoring & Analytics

### 13.1 Build Monitoring

**GitHub Actions:**
- View build logs in Actions tab
- Email notifications on failure
- Status badge in README

**Metrics to Track:**
- Build success rate (target: > 95%)
- Build time (target: < 5 minutes)
- Deployment frequency

### 13.2 Site Analytics

**Google Analytics 4:**
- Page views (especially blog posts)
- Time on page
- Bounce rate
- User flow (homepage → blog post)
- Language preference distribution

**Key Questions:**
- Which blog posts are most popular?
- Are visitors clicking the blog carousel?
- What's the homepage → blog conversion rate?
- Which language is more popular?

---

## 14. Future Technical Enhancements

### Phase 2 Considerations

**Search Functionality:**
- Algolia integration OR
- Lunr.js client-side search
- Search index generated during build

**Comments System:**
- utterances (GitHub Issues-based)
- Disqus (traditional)
- Giscus (GitHub Discussions-based)

**Performance:**
- Service worker for offline support
- WebP image format with fallbacks
- Critical CSS inlining

**Content Features:**
- RSS feed for blog
- JSON feed for API consumption
- Reading time calculation
- Series/taxonomy for multi-part posts

---

## 15. Appendices

### Appendix A: Contentful API Reference

**Delivery API Base URL:** `https://cdn.contentful.com`

**Fetch Blog Posts:**
```http
GET /spaces/{space_id}/environments/{environment}/entries
  ?access_token={token}
  &content_type=blogTemplate
  &locale=en
  &order=-fields.publishDate
  &limit=10
```

**Resolve Includes (References):**
```http
GET /spaces/{space_id}/environments/{environment}/entries/{entry_id}
  ?access_token={token}
  &include=2
```

### Appendix B: Jekyll Liquid Filters

**Date Formatting:**
```liquid
{{ page.date | date: "%B %d, %Y" }}  # January 18, 2026
{{ page.date | date_to_xmlschema }}  # 2026-01-18T00:00:00Z
```

**Truncate Text:**
```liquid
{{ page.excerpt | truncate: 150 }}
```

**Slugify:**
```liquid
{{ page.title | slugify }}
```

---

## 16. Success Metrics (Technical)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Build Success Rate** | > 95% | GitHub Actions logs |
| **Build Time** | < 5 min | GitHub Actions duration |
| **Page Load Time (Desktop)** | < 3 sec | Lighthouse |
| **Page Load Time (Mobile)** | < 5 sec | Lighthouse |
| **Lighthouse Performance** | > 85 | Automated audit |
| **Lighthouse SEO** | > 90 | Automated audit |
| **Lighthouse Accessibility** | > 90 | Automated audit |
| **Test Coverage** | > 80% | pytest-cov |

---

## 17. Glossary

- **SDD (Spec-Driven Development)**: Development methodology where specifications precede implementation
- **Contentful Delivery API**: Read-only API for fetching published content
- **Contentful Preview API**: API for fetching draft/unpublished content
- **Jekyll Frontmatter**: YAML metadata at the top of Markdown files
- **Liquid**: Jekyll's templating language
- **GitHub Actions**: CI/CD automation platform
- **Webhook**: HTTP callback triggered by events (e.g., content publish)

---

**Document Status:** Active  
**Next Review:** 2026-02-18  
**Maintained By:** Simon Salazar

---

*This specification is a living document and will evolve with the project.*
