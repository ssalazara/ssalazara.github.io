---
project_name: 'github-page'
user_name: 'Simon'
date: '2026-01-18'
sections_completed: ['technology_stack', 'architecture_decisions', 'implementation_patterns', 'critical_rules']
source_documents: ['architecture.md', 'PROJECT-UPDATE-SUMMARY.md']
status: 'complete'
---

# Project Context for AI Agents

**Project:** Personal GitHub Pages Portfolio (Blog-First Architecture)  
**Author:** Simon Salazar  
**Status:** Planning Complete - Ready for Implementation

_This file contains critical rules and patterns that AI agents MUST follow when implementing code. Focus on unobvious details that agents might otherwise miss._

---

## 🎯 Project Vision (Blog-First)

This is NOT a traditional portfolio. This is a **blog-first personal website** where:

✨ **Blog content is the hero element** - Blog carousel is the homepage centerpiece  
✨ **Easy content management** - Contentful CMS, < 5 min to publish  
✨ **Warm, kind, friendly** - Profile section humanizes the author  
✨ **Drives visitors into blog entries** - Primary CTA strategy  
✨ **Multi-language ready** - ISO 639-1 compliant (EN/ES)

**Critical User Flow:**
1. Visitor lands on homepage
2. Sees profile (who is this person?)
3. **Blog carousel (6-10 latest posts)** ← PRIMARY CTA
4. Clicks into blog post
5. Reads content
6. Discovers more posts

---

## Technology Stack & Versions

### Core Technologies (EXACT VERSIONS REQUIRED)

| Layer | Technology | Version | Critical Notes |
|-------|-----------|---------|----------------|
| **CMS** | Contentful | Cloud | Free tier: 25K records, 2 locales, Preview API included |
| **Transformation** | Python | **3.11+** | Type hints mandatory, modern syntax required |
| **Static Generator** | Jekyll | **4.x** | GitHub Pages native, Liquid templating |
| **CI/CD** | GitHub Actions | N/A | Free for public repos, 2000 min/month private |
| **Hosting** | GitHub Pages | N/A | Static only, 1GB repo limit, 100GB bandwidth/month |

### Python Dependencies (requirements.txt)

```txt
contentful==1.13.3
python-frontmatter==1.0.0
PyYAML==6.0
requests==2.31.0
pytest
python-dotenv
```

### Jekyll Dependencies (Gemfile)

```ruby
gem "jekyll", "~> 4.0"
gem "jekyll-seo-tag"
gem "jekyll-sitemap"
gem "jekyll-feed"
```

### Critical Constraints

🚨 **GitHub Pages Limitations:**
- Static files ONLY (no server-side logic, no databases, no Node.js server)
- Jekyll version dictated by GitHub Pages (currently 4.x)
- 10 builds per hour limit
- HTTPS-only (enforced)

🚨 **Contentful Free Tier:**
- 14 requests/second rate limit (both Delivery and Preview APIs)
- 2 locales included (EN, ES)
- Must use `include` parameter efficiently (max `include=2`)

🚨 **Build Time Constraint:**
- **< 5 minutes** total build time (critical user expectation)
- Python transformation + Jekyll build must complete within this window

---

## 🏗️ Architecture Overview (JAMstack)

```
┌─────────────┐  Webhook    ┌────────────────┐
│  Contentful │ ────────────▶│ GitHub Actions │
│     CMS     │              │   (CI/CD)      │
└─────────────┘              └────────────────┘
       │                              │
       │ Delivery/Preview API         │ Trigger Build
       ▼                              ▼
┌──────────────┐            ┌──────────────────┐
│    Python    │───────────▶│      Jekyll      │
│ Transformer  │  Markdown  │   Static Gen     │
└──────────────┘   + YAML   └──────────────────┘
                                     │
                                     │ Deploy
                                     ▼
                            ┌──────────────────┐
                            │   GitHub Pages   │
                            │   (CDN + SSL)    │
                            └──────────────────┘
```

**Data Flow:**
1. Content editor publishes in Contentful
2. Contentful webhook triggers GitHub Actions
3. Python script fetches content via API
4. Python transforms JSON → Markdown + YAML
5. Jekyll generates static HTML
6. GitHub Pages deploys site
7. **Total time: < 5 minutes**

---

## 📋 Content Model (15 Content Types)

### Atomic Design Hierarchy

```
📄 Templates (2)
├── Homepage (pageTemplate) - Profile + Blog Carousel
└── Blog Post (blogTemplate) - PRIMARY CONTENT TYPE

🦠 Organisms (3)
├── Header (orHeader) - uses mlMenuItem
├── Footer (orFooter) - uses mlMenuItem
└── Hero Banner (heroBanner) - optional

🧩 Molecules (3)
├── Carousel (componentCarousel) - for blog cards
├── Text with Image (textWithImage)
└── Rich Text Block (componentRichText)

🧬 Atoms (5)
├── Card (componentCard) - blog post cards
├── Menu Item (mlMenuItem) - navigation links
├── Social Link (componentSocialLink)
├── Image (componentImage)
└── Quote (componentQuote)

⚙️ Utilities (2)
├── SEO (seo) - REQUIRED for all blog posts
└── Profile (profile) - Singleton (only 1 instance)
```

### Blog-First Content Types (Priority Order)

1. **Blog Post (blogTemplate)** - P0 (Critical)
   - Fields: title, slug, body (rich text), publishDate, author, excerpt, featuredImage, SEO (linked)
   - **All text fields localized** (EN/ES)
   - **SEO entry REQUIRED** (build fails if missing)

2. **Profile (profile)** - P0 (Critical, Singleton)
   - Fields: name, title, bio, photo, socialLinks, CTA
   - **Bio and title localized**
   - Only ONE instance allowed

3. **Header (orHeader)** - P0 (Critical)
   - Fields: logo, menuItems (mlMenuItem references)
   - Global navigation

4. **Footer (orFooter)** - P0 (Critical)
   - Fields: menuItems, socialLinks, copyright
   - Global footer

5. **SEO (seo)** - P0 (Critical)
   - Fields: title, description, keywords, ogImage, canonicalUrl
   - **Title, description, keywords localized**
   - REQUIRED for all blog posts

---

## 🔥 Critical Implementation Rules

### Python Transformation Layer

#### 1. ALWAYS Use Type Hints

```python
# ✅ CORRECT
from typing import Dict, List, Optional
from contentful import Entry

def transform_single(self, entry: Entry) -> Dict[str, Any]:
    """Transform Contentful entry to Jekyll frontmatter."""
    pass

# ❌ WRONG
def transform_single(self, entry):  # No type hints
    pass
```

#### 2. ALWAYS Use snake_case (Python & Frontmatter)

```python
# ✅ CORRECT
class BlogPostTransformer:  # PascalCase for classes
    def transform_single(self, entry: Entry):  # snake_case for functions
        frontmatter = {
            'publish_date': entry.fields().get('publishDate'),  # snake_case
            'featured_image': image_url,                        # snake_case
            'seo_title': seo_title                             # snake_case
        }

# ❌ WRONG
class blogPostTransformer:  # Wrong case
    def transformSingle(self, entry):  # camelCase (wrong for Python)
        frontmatter = {
            'publishDate': date,     # camelCase (wrong for frontmatter)
            'featured-image': url    # kebab-case (wrong for YAML)
        }
```

#### 3. ALWAYS Preserve ISO 8601 Dates (No Transformation)

```python
# ✅ CORRECT - Pass through as-is
frontmatter['publish_date'] = entry.fields().get('publishDate')
# Contentful returns: '2026-01-18T10:30:00Z'
# Jekyll frontmatter stores: '2026-01-18T10:30:00Z'
# Liquid template displays: {{ post.publish_date | date: "%B %d, %Y" }}

# ❌ WRONG - Never convert dates in Python
from datetime import datetime
date_obj = datetime.fromisoformat(publish_date)
frontmatter['publish_date'] = date_obj.strftime('%Y-%m-%d')  # ❌ Loses timezone
```

**Why:** Liquid's `date` filter handles ISO 8601 natively. No transformation = no timezone bugs.

#### 4. ALWAYS Use Direct Contentful CDN Links (NEVER Download Images)

```python
# ✅ CORRECT
def get_featured_image(self, entry: Entry) -> Optional[str]:
    """Get Contentful CDN URL (no download)."""
    image = entry.fields().get('featuredImage')
    if image:
        return image.url()  # Direct CDN link
    return None

# ❌ WRONG - NEVER do this
import requests
def download_image(self, url: str, local_path: str):
    response = requests.get(url)
    with open(local_path, 'wb') as f:
        f.write(response.content)  # ❌ Adds minutes to build time
```

**Why:** Contentful CDN is globally distributed, optimized, and adds ZERO build time.

#### 5. ALWAYS Implement Graceful Degradation (NEVER Abort on Single Failure)

```python
# ✅ CORRECT
def transform_all(self) -> List[Dict[str, Any]]:
    entries = self.client.get_blog_posts(locale=self.locale)
    transformed = []
    failed_count = 0
    
    for entry in entries:
        try:
            post_data = self.transform_single(entry)
            transformed.append(post_data)
            logger.info(f"✅ TRANSFORM_SUCCESS entry_id={entry.id}")
        except Exception as e:
            logger.error(f"❌ TRANSFORM_FAILED entry_id={entry.id} error={str(e)}", exc_info=True)
            failed_count += 1
            # ✅ Continue with next entry
    
    if failed_count > 0:
        sys.exit(1)  # Mark build as failed but deploy working content
    
    return transformed

# ❌ WRONG
def transform_all(self):
    entries = self.client.get_blog_posts()
    transformed = []
    for entry in entries:
        post_data = self.transform_single(entry)  # ❌ Crashes on first failure
        transformed.append(post_data)
```

**Why:** Single broken post shouldn't prevent entire site from deploying.

#### 6. ALWAYS Validate SEO Before Transformation

```python
# ✅ CORRECT
def transform_single(self, entry: Entry) -> Dict[str, Any]:
    # Validate FIRST (fail fast)
    self.validate_seo(entry)
    self.validate_required_fields(entry)
    
    # THEN transform
    return self.build_frontmatter(entry)

def validate_seo(self, entry: Entry) -> None:
    seo_entry = entry.fields().get('seo')
    if not seo_entry:
        raise ValueError(
            f"❌ SEO_MISSING entry_id={entry.id} "
            f"message='Blog post requires linked SEO entry'"
        )
    
    seo_fields = seo_entry.fields(locale=self.locale)
    if not seo_fields.get('title') or not seo_fields.get('description'):
        raise ValueError(f"❌ SEO_FIELD_MISSING entry_id={entry.id}")

# ❌ WRONG
def transform_single(self, entry):
    # Transform first, validate later (too late if build already generated files)
    frontmatter = self.build_frontmatter(entry)
    if not frontmatter.get('seo_title'):  # ❌ Should fail earlier
        logger.warning("Missing SEO")
```

**Why:** Enforce SEO best practices from day one. Content editor gets immediate feedback.

#### 7. ALWAYS Use Structured Logging

```python
# ✅ CORRECT
import logging
logger = logging.getLogger(__name__)

logger.info(
    f"✅ TRANSFORM_SUCCESS "      # Visual marker
    f"entry_id={entry.id} "       # Structured field
    f"locale={self.locale} "      # Context
    f"slug={slug}"                # Identifier
)

logger.error(
    f"❌ TRANSFORM_FAILED "
    f"entry_id={entry.id} "
    f"locale={self.locale} "
    f"error={str(e)}",
    exc_info=True  # Include stack trace
)

# ❌ WRONG
print("Transformed blog post")  # No logger, no context
logger.info(f"Processing {entry.id}")  # No visual marker, minimal info
logger.error("Failed")  # No structured fields, no entry ID
```

**Log Format:**
- Emoji markers: ✅ ❌ ⚠️ 📊 (for quick scanning)
- Structured fields: `key=value key=value`
- Always include: `entry_id`, `locale`, `content_type`

---

### Jekyll Implementation Layer

#### 8. ALWAYS Use kebab-case for Jekyll Files

```bash
# ✅ CORRECT
_layouts/
  default.html
  home-page.html          # kebab-case
  post-layout.html        # kebab-case
  archive-page.html

_includes/
  components/
    blog-carousel.html    # kebab-case
    profile-card.html     # kebab-case
    post-card.html

_sass/
  layouts/
    _home-page.scss       # kebab-case
    _post-layout.scss

# ❌ WRONG
_layouts/
  homePage.html           # camelCase
  post_layout.html        # snake_case
  ArchivePage.html        # PascalCase
```

#### 9. ALWAYS Use Locale Folders for Posts

```bash
# ✅ CORRECT
_posts/
  en/
    2026-01-18-my-first-blog-post.md       # Date prefix, kebab-case slug
    2026-01-19-web-performance-tips.md
  es/
    2026-01-18-mi-primera-publicacion.md   # Spanish translation
    2026-01-19-consejos-rendimiento-web.md

# ❌ WRONG
_posts/
  my-first-blog-post.md                    # ❌ No locale folder
  my-first-blog-post.en.md                 # ❌ Locale suffix instead of folder
  en-my-first-blog-post.md                 # ❌ Locale prefix
  2026-01-18_my_first_blog_post.md         # ❌ Underscore separator
```

**Filename Format:** `YYYY-MM-DD-{slug}.md`

**Why:** Jekyll collections use folder structure for URL routing (`/en/blog/slug/`).

#### 10. ALWAYS Use Type-Locale Pattern for Data Files

```bash
# ✅ CORRECT
_data/
  profile-en.yml          # Type-first, locale suffix
  profile-es.yml
  navigation-en.yml
  navigation-es.yml
  footer-en.yml
  footer-es.yml

# Jekyll access: {{ site.data.profile-en.name }}

# ❌ WRONG
_data/
  en/
    profile.yml           # ❌ Locale folder (wrong for data files)
  profile.yml             # ❌ No locale specified
  profile_en.yml          # ❌ Underscore separator
  en-profile.yml          # ❌ Locale-first
```

**Why:** Jekyll's `site.data` structure maps to filename. `profile-en` is intuitive.

#### 11. ALWAYS Use Single Includes with i18n Logic

```liquid
<!-- ✅ CORRECT - Single file with i18n logic -->
<!-- _includes/navigation.html -->
{% assign nav_data = site.data.navigation-en %}
{% if page.locale == 'es' %}
  {% assign nav_data = site.data.navigation-es %}
{% endif %}

<nav>
  {% for item in nav_data.items %}
    <a href="{{ item.url }}">{{ item.label }}</a>
  {% endfor %}
</nav>

<!-- ❌ WRONG - Separate files per locale -->
_includes/
  navigation-en.html      # ❌ Duplication
  navigation-es.html      # ❌ Hard to maintain
```

**Why:** Avoids template duplication. Logic stays DRY.

---

### Localization Rules (ISO 639-1)

#### 12. ALWAYS Use Two-Letter Language Codes

```yaml
# ✅ CORRECT
locales:
  - en    # English
  - es    # Spanish

# URLs
/en/blog/my-first-post/
/es/blog/mi-primer-post/

# Data files
profile-en.yml
profile-es.yml

# ❌ WRONG
locales:
  - english          # ❌ Full word
  - EN               # ❌ Uppercase
  - en-US            # ❌ Region code (use only 'en')
  - spa              # ❌ Three-letter code
```

**Standard:** ISO 639-1 (two-letter codes only)

#### 13. ALWAYS Implement ES → EN Fallback

```python
# ✅ CORRECT
fields = entry.fields(locale=self.locale, fallback_locale='en')

# If Spanish translation missing, automatically use English

# ❌ WRONG
fields = entry.fields(locale=self.locale)  # ❌ No fallback, returns None
```

**Why:** Prevents broken pages when translations incomplete.

#### 14. ALWAYS Localize These Content Fields

**Must be localized:**
- Blog post: `title`, `slug`, `body`, `excerpt`
- SEO: `title`, `description`, `keywords`
- Profile: `bio`, `title`, `ctaLabel`
- Navigation: `label`
- Hero banner: `headline`, `subheading`, `ctaLabel`

**Never localize:**
- Dates (ISO 8601 is universal)
- Image URLs (Contentful CDN serves globally)
- Canonical URLs (single URL per piece of content)
- Author names (proper nouns)

---

### Security & Secrets Management

#### 15. NEVER Commit Secrets to Git

```gitignore
# ✅ MUST be in .gitignore
.env
.env.local
.env.*.local
*.pem
*.key

# Python
__pycache__/
*.py[cod]
venv/

# Jekyll
_site/
.jekyll-cache/

# Generated content (optional)
_posts/
_data/
```

#### 16. ALWAYS Use Environment Variables

```python
# ✅ CORRECT
import os
from dotenv import load_dotenv

load_dotenv()

CONTENTFUL_SPACE_ID = os.getenv('CONTENTFUL_SPACE_ID')
CONTENTFUL_ACCESS_TOKEN = os.getenv('CONTENTFUL_ACCESS_TOKEN')

if not CONTENTFUL_SPACE_ID:
    raise EnvironmentError("CONTENTFUL_SPACE_ID not set")

# ❌ NEVER log secrets
logger.info(f"🔧 Configuration loaded: mode={CONTENTFUL_MODE}")
# ❌ DO NOT: logger.info(f"Token: {CONTENTFUL_ACCESS_TOKEN}")

# ❌ WRONG
CONTENTFUL_ACCESS_TOKEN = "abc123xyz789"  # ❌ Hardcoded secret
```

#### 17. ALWAYS Use Read-Only API Tokens

**Correct Token Types:**
- ✅ **Delivery API Token** (production builds) - Read published content only
- ✅ **Preview API Token** (preview builds) - Read draft content only
- ❌ **NEVER Management API Token** in CI/CD - Full read/write access (admin only)

**GitHub Secrets Required:**
- `CONTENTFUL_SPACE_ID`
- `CONTENTFUL_ACCESS_TOKEN` (Delivery API)
- `CONTENTFUL_PREVIEW_TOKEN` (Preview API)
- `GITHUB_TOKEN` (automatic)

---

### GitHub Actions CI/CD

#### 18. ALWAYS Use Dependency Caching

```yaml
# ✅ CORRECT
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

- name: Cache Jekyll gems
  uses: actions/cache@v3
  with:
    path: vendor/bundle
    key: ${{ runner.os }}-gems-${{ hashFiles('**/Gemfile.lock') }}

# Saves 30-60 seconds per build
```

#### 19. ALWAYS Implement Dual-Mode Python Script

```python
# ✅ CORRECT - Mode switching via environment variable
CONTENTFUL_MODE = os.getenv('CONTENTFUL_MODE', 'production')

if CONTENTFUL_MODE == 'preview':
    # Use Preview API
    client = Client(SPACE_ID, PREVIEW_TOKEN, api_url='preview.contentful.com')
else:
    # Use Delivery API
    client = Client(SPACE_ID, ACCESS_TOKEN)
```

```yaml
# Production workflow
env:
  CONTENTFUL_MODE: production
  CONTENTFUL_ACCESS_TOKEN: ${{ secrets.CONTENTFUL_ACCESS_TOKEN }}

# Preview workflow
env:
  CONTENTFUL_MODE: preview
  CONTENTFUL_PREVIEW_TOKEN: ${{ secrets.CONTENTFUL_PREVIEW_TOKEN }}
```

---

## 📁 Project Structure (Critical Boundaries)

```
github-page/
├── scripts/                           # Python transformation layer
│   ├── contentful_to_jekyll.py        # Main entry point
│   ├── config.py                      # Configuration (mode switching)
│   ├── requirements.txt               # Python dependencies
│   │
│   ├── contentful_client/
│   │   └── client.py                  # Dual-mode API client
│   │
│   ├── transformers/
│   │   ├── base_transformer.py        # Base class
│   │   ├── blog_post_transformer.py   # Blog → Markdown + frontmatter
│   │   ├── profile_transformer.py     # Profile → YAML data
│   │   ├── navigation_transformer.py  # Navigation → YAML
│   │   └── footer_transformer.py      # Footer → YAML
│   │
│   ├── converters/
│   │   ├── markdown_converter.py      # Rich text → Markdown
│   │   └── asset_resolver.py          # CDN URL resolution
│   │
│   └── writers/
│       ├── file_writer.py             # Write Markdown files
│       └── data_writer.py             # Write YAML files
│
├── _config.yml                        # Jekyll configuration
├── Gemfile                            # Ruby dependencies
│
├── _layouts/                          # Jekyll layout templates
│   ├── default.html                   # Base layout (HTML structure)
│   ├── home-page.html                 # Homepage (blog-first)
│   ├── post-layout.html               # Blog post layout
│   └── archive-page.html              # Blog archive
│
├── _includes/                         # Jekyll reusable components
│   ├── head.html                      # <head> section (SEO, meta)
│   ├── navigation.html                # Top navigation
│   ├── footer.html                    # Footer section
│   └── components/
│       ├── blog-carousel.html         # Homepage blog carousel (HERO)
│       ├── profile-card.html          # Profile section
│       ├── post-card.html             # Blog post preview card
│       ├── social-links.html          # Social media links
│       └── language-switcher.html     # EN/ES toggle
│
├── _posts/                            # Generated blog posts (Markdown)
│   ├── en/
│   │   └── 2026-01-18-my-first-blog-post.md
│   └── es/
│       └── 2026-01-18-mi-primera-publicacion.md
│
├── _data/                             # Generated data files (YAML)
│   ├── profile-en.yml                 # English profile data
│   ├── profile-es.yml                 # Spanish profile data
│   ├── navigation-en.yml              # English navigation
│   ├── navigation-es.yml              # Spanish navigation
│   ├── footer-en.yml                  # English footer
│   └── footer-es.yml                  # Spanish footer
│
├── _sass/                             # Sass stylesheets
│   ├── main.scss
│   ├── base/
│   │   ├── _typography.scss
│   │   ├── _colors.scss
│   │   └── _variables.scss
│   ├── components/
│   │   ├── _blog-card.scss
│   │   ├── _profile-section.scss
│   │   └── _navigation.scss
│   └── layouts/
│       ├── _home-page.scss
│       └── _post-layout.scss
│
├── assets/                            # Static assets
│   ├── css/
│   ├── js/
│   │   ├── main.js
│   │   └── language-switcher.js
│   └── images/
│
├── .github/
│   └── workflows/
│       ├── production-deploy.yml      # Production (Delivery API)
│       └── preview-deploy.yml         # Preview (Preview API)
│
├── .env.example                       # Safe template
├── .gitignore                         # Secrets excluded
└── README.md
```

**Critical Boundaries:**
1. **Python layer** (`scripts/`) ↔ **Jekyll layer** (everything else) - NEVER mix
2. **Contentful API** ↔ **Python** - JSON communication
3. **Python** ↔ **Jekyll** - File system communication (Markdown + YAML)
4. **Jekyll** ↔ **GitHub Pages** - Static HTML deployment

---

## 🚫 Anti-Patterns (NEVER Do These)

### 1. NEVER Download Images During Build

```python
# ❌ WRONG - Adds 2-5 minutes to build time
for post in posts:
    image_url = post['featured_image']
    local_path = f"assets/images/{post['slug']}.jpg"
    download_image(image_url, local_path)  # ❌ NEVER

# ✅ CORRECT - Use CDN URLs directly
frontmatter['featured_image'] = image.url()  # Direct Contentful CDN link
```

### 2. NEVER Transform Dates

```python
# ❌ WRONG
publish_date = datetime.strptime(entry.fields().get('publishDate'), '%Y-%m-%dT%H:%M:%SZ')
frontmatter['publish_date'] = publish_date.strftime('%B %d, %Y')

# ✅ CORRECT
frontmatter['publish_date'] = entry.fields().get('publishDate')  # Pass through
```

### 3. NEVER Abort Build on Single Post Failure

```python
# ❌ WRONG
for entry in entries:
    post = self.transform_single(entry)  # Crashes entire build
    posts.append(post)

# ✅ CORRECT
for entry in entries:
    try:
        post = self.transform_single(entry)
        posts.append(post)
    except Exception as e:
        logger.error(f"❌ FAILED entry_id={entry.id}")
        # Continue with next post
```

### 4. NEVER Skip SEO Validation

```python
# ❌ WRONG
def transform_single(self, entry):
    # Transform first, validate never
    frontmatter = self.build_frontmatter(entry)
    return frontmatter

# ✅ CORRECT
def transform_single(self, entry):
    self.validate_seo(entry)  # Validate FIRST
    return self.build_frontmatter(entry)
```

### 5. NEVER Mix Naming Conventions

```python
# ❌ WRONG - Inconsistent naming
frontmatter = {
    'publishDate': date,        # camelCase
    'featured-image': url,      # kebab-case
    'seo_title': title,         # snake_case
    'TagList': tags             # PascalCase
}

# ✅ CORRECT - Consistent snake_case
frontmatter = {
    'publish_date': date,
    'featured_image': url,
    'seo_title': title,
    'tags': tags
}
```

### 6. NEVER Use Management API Tokens in CI/CD

```yaml
# ❌ WRONG
env:
  CONTENTFUL_MANAGEMENT_TOKEN: ${{ secrets.CONTENTFUL_MANAGEMENT_TOKEN }}

# ✅ CORRECT
env:
  CONTENTFUL_ACCESS_TOKEN: ${{ secrets.CONTENTFUL_ACCESS_TOKEN }}  # Read-only
```

---

## 🧪 Testing Requirements

### Python Unit Tests (pytest)

**File Naming:** `test_{module}.py`

```
tests/
├── test_transformers.py
├── test_converters.py
└── test_integration.py
```

**Test Structure:**

```python
# ✅ CORRECT
def test_blog_post_transformer_success():
    """Test successful blog post transformation."""
    # Arrange
    mock_entry = create_mock_entry()
    transformer = BlogPostTransformer(client, locale='en')
    
    # Act
    result = transformer.transform_single(mock_entry)
    
    # Assert
    assert result['frontmatter']['title'] == 'My First Post'
    assert result['frontmatter']['locale'] == 'en'
    assert 'publish_date' in result['frontmatter']

def test_seo_validation_fails_when_missing():
    """Test SEO validation fails when entry missing."""
    mock_entry = create_mock_entry(seo=None)
    transformer = BlogPostTransformer(client, locale='en')
    
    with pytest.raises(ValueError, match="SEO_MISSING"):
        transformer.validate_seo(mock_entry)
```

**Coverage Target:** > 80% for transformers and converters

---

## 📊 Performance Targets

| Metric | Target | Critical |
|--------|--------|----------|
| **Total Build Time** | < 5 min | 🔥 YES |
| **Python Transformation** | < 2 min | 🔥 YES |
| **Jekyll Build** | < 2 min | 🔥 YES |
| **Page Load (Desktop)** | < 3 sec | YES |
| **Page Load (Mobile)** | < 5 sec | YES |
| **Lighthouse Performance** | > 85 | YES |
| **Lighthouse SEO** | > 90 | YES |
| **Lighthouse Accessibility** | > 90 | YES |
| **Build Success Rate** | > 95% | 🔥 YES |

---

## 🎯 Implementation Priority Order

### Phase 1: Core Infrastructure (Week 1-2)

1. **Repository Setup**
   ```bash
   mkdir -p github-page/{scripts,tests,_layouts,_includes,_sass,_posts,_data,assets,.github/workflows}
   cd github-page && git init
   ```

2. **Python Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install contentful==1.13.3 python-frontmatter==1.0.0 PyYAML==6.0 requests pytest python-dotenv
   ```

3. **Jekyll Setup**
   ```bash
   gem install bundler jekyll
   bundle init
   bundle add jekyll jekyll-seo-tag jekyll-sitemap jekyll-feed
   ```

4. **Contentful Client** (`scripts/contentful_client/client.py`)
   - Dual-mode support (Delivery/Preview API)
   - In-memory caching
   - Mode switching via environment variable

5. **Blog Post Transformer** (`scripts/transformers/blog_post_transformer.py`)
   - SEO validation (fail if missing)
   - Frontmatter generation (snake_case fields)
   - Rich text → Markdown conversion
   - Graceful degradation

### Phase 2: Jekyll Layouts (Week 2-3)

6. **Homepage Layout** (`_layouts/home-page.html`)
   - Profile section
   - Blog carousel (6-10 posts)

7. **Blog Post Layout** (`_layouts/post-layout.html`)
   - Featured image
   - Author byline
   - Publish date
   - Content body

8. **Components** (`_includes/components/`)
   - `blog-carousel.html`
   - `profile-card.html`
   - `post-card.html`
   - `language-switcher.html`

### Phase 3: CI/CD & Deployment (Week 3-4)

9. **GitHub Actions** (`.github/workflows/`)
   - `production-deploy.yml` (Delivery API)
   - `preview-deploy.yml` (Preview API)
   - Dependency caching
   - Build time tracking

10. **Contentful Webhook**
    - Configure webhook → GitHub Actions
    - Test publish flow
    - Verify < 5 min end-to-end

---

## 📚 Reference Documentation

### Architectural Decisions (ADRs)

- **ADR-001:** Hybrid caching strategy (in-memory + GitHub Actions cache)
- **ADR-002:** Graceful degradation error handling
- **ADR-003:** Dual-mode Preview API integration
- **ADR-004:** Monitor-first build optimization
- **ADR-005:** Required SEO metadata validation

### Source Documents

- **Architecture Document:** `_bmad-output/planning-artifacts/architecture.md` (2,510 lines)
- **PRD:** `_bmad-output/planning-artifacts/prd.md`
- **Technical Specification:** `_bmad-output/planning-artifacts/technical-specification-20260118.md`
- **Integration Architecture:** `_bmad-output/planning-artifacts/integration-architecture-20260118.md`
- **Content Model Schema:** `_bmad-output/planning-artifacts/content-model-schema-20260118.md`

---

## ✅ Final Checklist for AI Agents

Before implementing ANY code, ensure you:

- [ ] Read the complete architecture document
- [ ] Understand the blog-first vision (blog carousel is hero)
- [ ] Use exact versions (Python 3.11+, Jekyll 4.x, contentful.py 1.13.3)
- [ ] Apply snake_case for Python and frontmatter, kebab-case for Jekyll files
- [ ] Preserve ISO 8601 dates (no transformation)
- [ ] Use direct Contentful CDN links (never download images)
- [ ] Implement graceful degradation (continue on single failures)
- [ ] Validate SEO before transformation (fail fast)
- [ ] Use structured logging with emoji markers
- [ ] Never commit secrets (use environment variables)
- [ ] Use read-only API tokens (Delivery/Preview, not Management)
- [ ] Implement dual-mode script (production/preview)
- [ ] Follow locale folder structure (`_posts/en/`, `_posts/es/`)
- [ ] Follow data file naming (`profile-en.yml`, `profile-es.yml`)
- [ ] Target < 5 min total build time

---

**Status:** ✅ Project Context Complete - Ready for Implementation  
**Last Updated:** 2026-01-18  
**Maintained By:** Simon Salazar

_This document is the single source of truth for implementation patterns. Update it when new patterns emerge during development._
