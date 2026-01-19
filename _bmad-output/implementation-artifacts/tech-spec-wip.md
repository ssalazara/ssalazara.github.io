---
title: 'Homepage & Hero Banner Transformers + Sample Blog Content'
slug: 'homepage-hero-banner-transformers'
created: '2026-01-19'
status: 'completed'
stepsCompleted: [1, 2, 3]
tech_stack: ['Python 3.11+', 'Contentful SDK', 'Jekyll 4.x', 'YAML', 'Liquid templating']
files_modified: ['scripts/transformers/homepage_transformer.py', 'scripts/contentful_to_jekyll.py', '_includes/components/hero-banner.html', '_layouts/home-page.html', '_sass/components/_hero-banner.scss', 'assets/css/style.scss', 'CONTENTFUL-BLOG-POST-GUIDE.md']
code_patterns: ['BaseTransformer inheritance', 'singleton pattern', 'snake_case YAML', 'type hints', 'structured logging', 'reference resolution']
test_patterns: ['Manual validation', 'Jekyll build test', 'Visual QA']
---

# Tech-Spec: Homepage & Hero Banner Transformers + Sample Blog Content

**Created:** 2026-01-19

## Overview

### Problem Statement

Homepage content exists in Contentful (Entry ID: 4a0t1j30SNBh2mSCeJB69N with heroBanner block) but isn't being transformed or rendered. The hero banner component doesn't exist. There are no blog posts in Contentful to test the blog carousel functionality. The homepage layout is hardcoded rather than dynamic.

### Solution

Build three components following existing transformer patterns:

1. **Homepage Transformer** - Python script that fetches homepage entries from Contentful and transforms them to `_data/homepage-{locale}.yml` (follows header/footer pattern)
2. **Hero Banner Component** - Jekyll include at `_includes/components/hero-banner.html` that renders hero content
3. **Blog Post Creation Guide** - Documentation for manually creating sample blog posts in Contentful UI

Update the homepage layout to dynamically render blocks from the homepage data file instead of hardcoded profile/carousel sections.

### Scope

**In Scope:**
- Homepage transformer (`scripts/transformers/homepage_transformer.py`)
- Hero banner Jekyll component (`_includes/components/hero-banner.html`)
- Homepage layout updates for dynamic block rendering
- Blog post creation guide/documentation
- Integration with main orchestration script (`contentful_to_jekyll.py`)

**Out of Scope:**
- Other block types (carousel, text-with-image, rich-text-block, etc.) - future work
- Contentful Management API integration for automated content creation
- CI/CD pipeline updates (comes in separate epic)
- Profile and blog carousel components (already exist)

## Context for Development

### Codebase Patterns

**Transformer Pattern (from HeaderTransformer):**
```python
class HomepageTransformer(BaseTransformer):
    def __init__(self, client, locale: str = 'en'):
        super().__init__(client, locale)
        self.content_type = CONTENT_TYPE_HOMEPAGE
    
    def transform_single(self, entry: Entry) -> Dict[str, Any]:
        fields = entry.fields()
        # Extract fields, resolve references
        # Return snake_case dict
    
    def transform_all(self) -> List[Dict[str, Any]]:
        # Fetch entries with include=2
        # Transform first entry only (singleton)
        # Return list with single dict
```

**Key Methods from BaseTransformer:**
- `resolve_reference(entry, 'seo')` - Get single reference
- `resolve_reference_array(entry, 'blocks')` - Get array of references  
- `get_asset_url(asset)` - Extract CDN URL with HTTPS
- `log_transform_success(entry, extra_info)` - Structured logging

**YAML Data Writer Pattern:**
```python
data_writer.write_data_file(homepage_data, 'homepage', jekyll_locale)
# Outputs: _data/homepage-en.yml with header comment
```

**Jekyll Component Pattern:**
```liquid
{% assign homepage = site.data.homepage_en %}
{% for block in homepage.blocks %}
  {% if block.type == 'heroBanner' %}
    {% include components/hero-banner.html hero=block %}
  {% endif %}
{% endfor %}
```

**Critical Patterns:**
- Contentful camelCase → snake_case YAML (brandUrl → brand_url)
- ISO 8601 dates preserved as-is
- Direct CDN URLs (never download)
- Singleton content: transform first entry only, warn if multiple
- Structured logging: `✅ TRANSFORM_SUCCESS entry_id={id}`
- Type hints mandatory for all functions
- Graceful error handling (continue on failure)

### Files to Reference

| File | Purpose | Key Details |
| ---- | ------- | ----------- |
| `scripts/transformers/header_transformer.py` | Reference pattern for singleton content type | Lines 82-130: transform_single(), lines 132-176: transform_all() with singleton handling |
| `scripts/transformers/base_transformer.py` | Base class with common methods | resolve_reference(), resolve_reference_array(), get_asset_url(), logging methods |
| `scripts/writers/data_writer.py` | YAML writer | write_data_file(data, content_type, locale) → _data/{type}-{locale}.yml |
| `scripts/contentful_to_jekyll.py` | Main orchestration | Lines 178-181: Need to add homepage transformer |
| `scripts/config.py` | Config constants | Lines 36-40: Add CONTENT_TYPE_HOMEPAGE = 'homePage' |
| `_layouts/home-page.html` | Homepage layout | Currently hardcoded profile+carousel, needs dynamic block rendering from site.data |
| `contentful-schemas/homepage.json` | Homepage schema | Fields: name, url, seo (ref), header (ref), blocks (array), footer (ref) |
| `contentful-schemas/hero-banner.json` | Hero Banner schema | Fields: name, title (localized), description (localized), ctaLabel, ctaUrl, image (asset) |

### Technical Decisions

**Decision 1: Homepage as YAML Data File (Confirmed)**
- **Pattern:** Same as header/footer transformers  
- **Output:** `_data/homepage-en.yml`, `_data/homepage-es.yml`
- **Rationale:** Consistent with existing architecture, allows dynamic rendering
- **Alternative rejected:** Static `index.html` generation (less flexible, breaks pattern)

**Decision 2: Block Type Field for Dynamic Rendering**
- **Implementation:** Add `type: 'heroBanner'` field to each transformed block
- **Rationale:** Jekyll needs to know which component include to use
- **Pattern:** `{% if block.type == 'heroBanner' %}{% include components/hero-banner.html %}{% endif %}`

**Decision 3: Hero Banner Component Structure**
- **File:** `_includes/components/hero-banner.html`
- **Parameters:** Receives `hero` object with title, description, cta_label, cta_url, image_url
- **Styling:** Reuse existing Sass variables from design system
- **Pattern:** Match existing components (profile-card, blog-carousel)

**Decision 4: Homepage Content Type ID**
- **Actual ID:** `homePage` (confirmed from Contentful entry test)
- **Config constant:** `CONTENT_TYPE_HOMEPAGE = 'homePage'`
- **Note:** Schema file says `pageTemplate` but actual entry uses `homePage`

**Decision 5: Blog Post Creation - Manual Guide**
- **Format:** Markdown documentation with step-by-step Contentful UI instructions
- **Includes:** Required fields, SEO setup, sample content suggestions
- **Rationale:** No Management API needed, aligns with content editor workflow

## Implementation Plan

### Tasks

**Task 1: Config Setup**
- Add `CONTENT_TYPE_HOMEPAGE = 'homePage'` to `scripts/config.py`
- **Estimated Effort:** 1 min
- **Files:** `scripts/config.py`

**Task 2: Homepage Transformer**
- Create `scripts/transformers/homepage_transformer.py`
- Inherit from `BaseTransformer`
- Implement `transform_single()`:
  - Extract `name`, `url` fields
  - Resolve `seo` reference (optional - just store ID for now)
  - Resolve `header` reference (just store ID)
  - Resolve `blocks` array → transform each block with type detection
  - Resolve `footer` reference (just store ID)
- Implement `transform_all()` with singleton pattern
- Add block type detection logic (inspect entry content_type)
- **Estimated Effort:** 20 min
- **Files:** `scripts/transformers/homepage_transformer.py`

**Task 3: Block Transformer Helper**
- Create `_transform_block(block_entry)` method in HomepageTransformer
- Detect content type via `block_entry.sys.get('content_type', {}).get('sys', {}).get('id')`
- Switch on type:
  - `heroBanner` → extract title, description, ctaLabel, ctaUrl, image
  - Other types → return placeholder with `type: 'unsupported'`
- Return dict with `type` field + transformed data
- **Estimated Effort:** 10 min
- **Files:** `scripts/transformers/homepage_transformer.py`

**Task 4: Hero Banner Jekyll Component**
- Create `_includes/components/hero-banner.html`
- Structure:
  ```liquid
  <section class="hero-banner">
    <div class="hero-content">
      <h1>{{ include.hero.title }}</h1>
      <p>{{ include.hero.description }}</p>
      {% if include.hero.cta_label %}
        <a href="{{ include.hero.cta_url }}" class="btn-primary">{{ include.hero.cta_label }}</a>
      {% endif %}
    </div>
    <div class="hero-image" style="background-image: url('{{ include.hero.image_url }}')"></div>
  </section>
  ```
- **Estimated Effort:** 10 min
- **Files:** `_includes/components/hero-banner.html`

**Task 5: Hero Banner Sass Styles**
- Create `_sass/components/_hero-banner.scss`
- Import in `assets/css/style.scss`
- Mobile-first responsive design (flexbox/grid)
- Use design tokens from `_variables.scss`
- **Estimated Effort:** 15 min
- **Files:** `_sass/components/_hero-banner.scss`, `assets/css/style.scss`

**Task 6: Update Homepage Layout**
- Modify `_layouts/home-page.html`
- Load homepage data: `{% assign homepage = site.data.homepage_en %}`
- Replace hardcoded profile/carousel with dynamic block loop:
  ```liquid
  {% for block in homepage.blocks %}
    {% if block.type == 'heroBanner' %}
      {% include components/hero-banner.html hero=block %}
    {% endif %}
  {% endfor %}
  ```
- **Estimated Effort:** 5 min
- **Files:** `_layouts/home-page.html`

**Task 7: Integrate into Main Script**
- Modify `scripts/contentful_to_jekyll.py`
- Import `HomepageTransformer`
- Add to `TRANSFORMERS` dict: `'homepage': HomepageTransformer`
- Add to `DATA_WRITERS` dict: `'homepage': data_writer`
- **Estimated Effort:** 3 min
- **Files:** `scripts/contentful_to_jekyll.py`

**Task 8: Blog Post Creation Guide**
- Create `CONTENTFUL-BLOG-POST-GUIDE.md`
- Include: Required fields, SEO setup, sample content suggestions, screenshot placeholders
- Store in root directory
- **Estimated Effort:** 10 min
- **Files:** `CONTENTFUL-BLOG-POST-GUIDE.md`

**Total Estimated Effort:** ~74 minutes

### Acceptance Criteria

**Homepage Transformer:**
- ✅ Creates `_data/homepage-en.yml` file
- ✅ Contains `name`, `url` fields
- ✅ Contains `blocks` array with at least hero banner
- ✅ Hero banner has `type: 'heroBanner'`, `title`, `description`, `image_url`
- ✅ Logs structured success messages
- ✅ Warns if multiple homepage entries found (singleton)

**Hero Banner Component:**
- ✅ Renders title, description, image
- ✅ Shows CTA button only if `cta_label` exists
- ✅ Responsive on mobile, tablet, desktop
- ✅ Image loads via CDN URL
- ✅ Follows design system (colors, typography, spacing)

**Jekyll Build:**
- ✅ `bundle exec jekyll build` succeeds without errors
- ✅ Homepage renders at `/` and `/en/` paths
- ✅ Hero banner visible on homepage
- ✅ No Liquid template errors in output

**Blog Post Guide:**
- ✅ Step-by-step instructions for creating blog post in Contentful UI
- ✅ Lists all required fields (title, slug, publishDate, author, featuredImage, body, seo)
- ✅ Explains SEO setup
- ✅ Provides sample content suggestions

## Additional Context

### Dependencies

**Python Dependencies (already installed):**
- `contentful==1.13.3` - Contentful SDK
- `PyYAML>=6.0` - YAML serialization
- `python-dotenv>=1.0.0` - Environment variables

**Jekyll Dependencies (already installed):**
- `jekyll ~> 4.3.2` - Static site generator
- `sass` - CSS preprocessing

**External Dependencies:**
- Contentful CMS entry ID: `4a0t1j30SNBh2mSCeJB69N` (Homepage with hero banner)
- Contentful Space/Access Token in `.env`

**No New Dependencies Required**

### Testing Strategy

**Phase 1: Unit Testing (Python)**
1. Run transformation script: `python scripts/contentful_to_jekyll.py`
2. Verify `_data/homepage-en.yml` created
3. Inspect YAML structure manually
4. Check logs for success messages

**Phase 2: Integration Testing (Jekyll)**
1. Run Jekyll build: `bundle exec jekyll build`
2. Check for compilation errors
3. Verify `_site/index.html` exists
4. Inspect generated HTML structure

**Phase 3: Visual QA (Browser)**
1. Serve site locally: `bundle exec jekyll serve`
2. Open `http://localhost:4000`
3. Verify hero banner renders correctly
4. Test responsive breakpoints (mobile, tablet, desktop)
5. Check image loading from Contentful CDN
6. Test CTA button link (if present)

**Phase 4: Error Handling**
1. Test with missing homepage entry (should log warning, not crash)
2. Test with hero banner missing required field (should skip, log error)
3. Verify graceful degradation

### Notes

**Content Type ID Clarification:**
- Schema file says `sys.id = pageTemplate`
- But actual Contentful entry uses content type `homePage`
- MUST use `homePage` in config - confirmed by previous API tests

**Block Types:**
- Initial implementation: Only `heroBanner` supported
- Future blocks: `componentRichText`, `textWithImage`, `componentCarousel`, `componentQuote`
- Unsupported blocks logged as warnings, skipped gracefully

**Locale Handling:**
- Homepage: Non-localized (singleton per locale)
- Hero Banner: Title and description are localized fields
- CTA label: Localized
- URL slug: Non-localized (same across locales)

**Performance Considerations:**
- Use `include=2` to minimize API calls (fetch references in single request)
- Hero banner images loaded directly from Contentful CDN (no local storage)
- YAML files cached by Jekyll (no rebuild needed if unchanged)

**SEO Note:**
- Homepage SEO handled separately by existing SEO transformer
- Hero banner does not affect SEO metadata
- URL slug from homepage used for canonical URL

**Current State:**
- Homepage entry already exists in Contentful with 1 heroBanner block
- Current homepage layout shows profile + blog carousel (hardcoded)
- Blog posts content type is `blogPage` (not `blogTemplate`)
- All blockers from Implementation Status Audit are now fixed
