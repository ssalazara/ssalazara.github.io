---
title: 'Python Backend for Contentful-to-Jekyll Transformation with CI/CD'
slug: 'python-contentful-jekyll-backend'
created: '2026-01-19'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4]
tech_stack:
  - Python 3.11+
  - Contentful SDK (contentful==1.13.3)
  - Contentful CLI (npm install -g contentful-cli)
  - Jekyll 4.3.3
  - GitHub Actions
  - pytest
  - python-frontmatter
  - PyYAML
  - python-dotenv
files_to_modify:
  - README.md (add backend setup instructions)
  - .gitignore (add Python patterns)
code_patterns:
  - snake_case for Python functions and YAML frontmatter
  - PascalCase for Python classes
  - Type hints mandatory for all functions
  - Structured logging with emoji markers
  - Graceful degradation (continue on single failure)
  - SEO validation before transformation
  - ISO 8601 date preservation (no transformation)
  - Direct Contentful CDN URLs (never download images)
test_patterns:
  - pytest with AAA pattern (Arrange, Act, Assert)
  - test_{module}.py naming convention
  - Mock Contentful Entry objects (no real API calls)
  - > 80% coverage target
---

# Tech-Spec: Python Backend for Contentful-to-Jekyll Transformation with CI/CD

**Created:** 2026-01-19

## Overview

### Problem Statement

Simon has a complete Jekyll frontend (Epics 4-7 complete) but no way to get content from Contentful CMS into Jekyll. Content creators need to publish blog posts, profile updates, and navigation changes through Contentful and have them automatically transformed into Jekyll markdown/YAML files and deployed to GitHub Pages within 5 minutes.

Currently:
- Frontend is production-ready (layouts, components, Sass all built)
- 15 Contentful content types are defined in JSON schemas
- No Python transformation layer exists (zero `.py` files)
- No CI/CD automation exists (no GitHub Actions workflows)
- Content cannot flow from Contentful → Jekyll → GitHub Pages

### Solution

Build a complete Python transformation layer with dual-mode support (production + preview) and CI/CD automation:

1. **Contentful Setup:** Import content model (15 types) via Contentful CLI
2. **Python Transformation Layer:** Fetch content from Contentful APIs → Transform JSON to Jekyll files
3. **Dual-Mode Support:** Production (Delivery API) + Preview (Preview API) from day one
4. **CI/CD Automation:** GitHub Actions with 3 trigger types (webhook, manual, push)
5. **Quality Assurance:** Unit tests (> 80% coverage), SEO validation, graceful error handling

### Scope

**In Scope:**

✅ **Epic 1: Content Publishing Foundation**
- Python 3.11+ environment setup (`requirements.txt`, virtual env)
- Contentful CLI setup + content model import script (15 content types)
- Dual-mode Contentful client (Delivery API + Preview API)
- Blog post transformer with SEO validation
- Rich text → Markdown converter
- File writer with locale folder structure (`_posts/en/`, `_posts/es/`)
- Graceful error handling (continue on single failure)
- Structured logging (emoji markers: ✅ ❌ ⚠️ 📊)
- Unit tests (> 80% coverage, mocked Contentful responses)

✅ **Epic 2: Supporting Content & Basic SEO**
- Profile transformer → `_data/profile-en.yml`, `_data/profile-es.yml`
- Header transformer → `_data/header-en.yml`, `_data/header-es.yml`
- Footer transformer → `_data/footer-en.yml`, `_data/footer-es.yml`
- SEO validation before transformation (fail fast if missing)

✅ **Epic 3: CI/CD Automation**
- GitHub Actions workflows:
  - **Production workflow:** Delivery API + Contentful webhook trigger
  - **Preview workflow:** Preview API + manual dispatch trigger
  - **Code changes workflow:** Push to main branch trigger
- Dependency caching (pip + Jekyll gems)
- Build time monitoring (< 5 min target, warn if > 2 min for Python phase)
- Error logging to GitHub Actions
- Automated GitHub Pages deployment

✅ **Preview Mode (from Epic 7):**
- Dual-mode Python script (`CONTENTFUL_MODE` environment variable)
- Preview workflow for draft content review before publishing

**Out of Scope:**

❌ Frontend changes (already complete in Epics 4-7)
❌ Performance optimization beyond dependency caching (Epic 7)
❌ Lighthouse CI integration (Epic 7)
❌ Image optimization (Epic 7)
❌ Advanced monitoring/alerting (email, Slack webhooks)
❌ Content model modifications (use existing 15 types as-is)
❌ Multi-environment support beyond Master (only Master environment)

## Context for Development

### Contentful Credentials

**Space Configuration:**
- **Space Name:** ssa-personal
- **Space ID:** co4wdyhrijid
- **Environment:** Master
- **Delivery API Token:** `<your-delivery-api-token>` (obtain from Contentful: Settings > API keys > Content Delivery API)
- **Preview API Token:** `<your-preview-api-token>` (obtain from Contentful: Settings > API keys > Content Preview API)

**⚠️ SECURITY NOTE:**
- **NEVER commit actual tokens to git or documentation**
- **Local development:** Store tokens in `.env` file (gitignored)
- **CI/CD:** Store tokens as GitHub Secrets
- **Rotate tokens immediately if exposed**
- After obtaining new tokens, store them in password manager and configure in GitHub Secrets before running workflows

**Content Model Status:**
- Empty space (no content yet)
- Content model must be imported via CLI from `contentful-schemas/` directory
- 15 content types defined: blogTemplate, profile, orHeader, orFooter, seo, componentCard, componentCarousel, mlMenuItem, componentSocialLink, componentImage, componentQuote, componentRichText, textWithImage, heroBanner, pageTemplate

### Critical Implementation Rules (from project-context.md)

**Python Layer:**
1. **ALWAYS use type hints** - `def transform_single(self, entry: Entry) -> Dict[str, Any]:`
2. **ALWAYS use snake_case** - Python functions, YAML frontmatter fields
3. **NEVER transform dates** - Pass through ISO 8601 as-is (Liquid handles formatting)
4. **NEVER download images** - Use direct Contentful CDN URLs
5. **ALWAYS implement graceful degradation** - Continue processing if single post fails
6. **ALWAYS validate SEO first** - Fail fast before transformation
7. **ALWAYS use structured logging** - Emoji markers + `key=value` format

**Jekyll Layer:**
8. **ALWAYS use kebab-case** - Jekyll layout files, include files, Sass files
9. **ALWAYS use locale folders for posts** - `_posts/en/YYYY-MM-DD-slug.md`
10. **ALWAYS use type-locale pattern for data** - `profile-en.yml`, not `en/profile.yml`

**Build Constraints:**
- **Total build time:** < 5 minutes (critical user expectation)
- **Python transformation:** < 2 minutes target
- **Jekyll build:** < 2 minutes target

### Codebase Patterns

**Status: Clean Slate Confirmed** ✅

No Python code exists in the repository. The entire `scripts/` directory structure must be created from scratch. This is a greenfield implementation with no legacy constraints.

**Existing Codebase (Frontend Complete):**
- ✅ Jekyll 4.3.3 configured with plugins (seo-tag, sitemap, feed)
- ✅ 4 layouts: `default.html`, `home-page.html`, `post-layout.html`, `blog-archive.html`
- ✅ 8 components in `_includes/components/`
- ✅ Complete Sass architecture (60+ files, 4000+ lines)
- ✅ Locale support configured (en/es permalinks, collection paths)
- ✅ 15 Contentful content type schemas ready to import

**Key Architecture Decisions:**
1. **Permalink Structure:** `/:lang/blog/:slug/` (configured in `_config.yml`)
2. **Locale Folders:** Posts go in `_posts/en/`, `_posts/es/` (Jekyll collections)
3. **Data Files:** Type-locale pattern: `profile-en.yml`, `header-en.yml` (not `en/profile.yml`)
4. **Frontmatter Fields:** snake_case (Jekyll expects `publish_date`, `featured_image`, etc.)
5. **Contentful Fields:** camelCase (API returns `publishDate`, `featuredImage`, etc.)

**Critical Field Mappings (Contentful → Jekyll):**

**Blog Post (blogTemplate):**
```
Contentful Field       → Jekyll Frontmatter
-----------------        -------------------
name                   → (internal only, not in frontmatter)
url                    → slug
title                  → title
description            → excerpt
label                  → category
publishDate            → publish_date (ISO 8601, no transformation)
author                 → author
text (RichText)        → (converted to Markdown body)
image (Asset)          → featured_image (CDN URL)
seo (Link to seo)      → seo_title, seo_description, seo_keywords, og_image
```

**Profile (profile) → `_data/profile-{locale}.yml`:**
```
fullName               → name
title                  → title (localized)
bio                    → bio (localized)
profileImage (Asset)   → photo_url (CDN URL)
email                  → email
socialLinks (Array)    → social_links (array of platform/url)
ctaLabel               → cta_button.text (localized)
ctaUrl                 → cta_button.url
```

**Header (orHeader) → `_data/header-{locale}.yml`:**
```
name                   → (internal only)
brandUrl               → brand_url
brandImage (Asset)     → brand_logo_url (CDN URL)
menuItems (Array)      → menu_items (array, resolve mlMenuItem references)
```

**Footer (orFooter) → `_data/footer-{locale}.yml`:**
```
name                   → (internal only)
brandImage (Asset)     → brand_logo_url (CDN URL)
brandUrl               → brand_url
description            → description
copyright              → copyright
menuItems (Array)      → menu_items (resolve mlMenuItem references)
socialLinks (Array)    → social_links (resolve componentSocialLink references)
```

**SEO (seo) - Merged into blog post frontmatter:**
```
title                  → seo_title (localized)
description            → seo_description (localized)
keywords (Array)       → seo_keywords (localized array)
ogImage (Asset)        → og_image (CDN URL)
noIndex                → no_index (boolean)
canonicalUrl           → canonical_url
```

### Files to Reference

| File | Purpose | Lines |
| ---- | ------- | ----- |
| `_bmad-output/project-context.md` | Complete implementation rules, patterns, anti-patterns | 1010 |
| `_bmad-output/planning-artifacts/epics.md` | Detailed epic breakdown with acceptance criteria | 1057 |
| `_bmad-output/planning-artifacts/architecture.md` | Complete architecture decisions | 2510 |
| `contentful-schemas/blogpage.json` | Blog post content type (PRIMARY) | 210 |
| `contentful-schemas/profile.json` | Profile content type (singleton) | 195 |
| `contentful-schemas/or-header.json` | Header navigation content type | 172 |
| `contentful-schemas/footer.json` | Footer content type | 164 |
| `contentful-schemas/seo.json` | SEO metadata (required for blog posts) | 140 |
| `contentful-schemas/menu-item.json` | Navigation menu item (referenced by header/footer) | - |
| `contentful-schemas/social-link.json` | Social media link component | - |
| `_config.yml` | Jekyll configuration (permalinks, collections, locales) | 82 |
| `Gemfile` | Jekyll dependencies (4.3.3 + plugins) | 26 |
| `_layouts/post-layout.html` | Blog post layout (expects specific frontmatter) | 111 |
| `_includes/components/profile-card.html` | Profile component (expects YAML data structure) | 117 |
| `_data/profile-en.yml.example` | Expected profile YAML structure | 22 |
| `_data/header-en.yml.example` | Expected header YAML structure | 15 |

### Technical Decisions

**Decision 1: Dual-Mode from Day One**
- **Rationale:** Preview mode is essential for content iteration post-launch. Retrofitting is painful.
- **Implementation:** Single codebase with `CONTENTFUL_MODE` env var switching between Delivery/Preview APIs
- **Investigation:** Confirmed Contentful Python SDK supports both `api_url='preview.contentful.com'` and default delivery API

**Decision 2: Graceful Degradation Over Strict Validation**
- **Rationale:** One broken blog post shouldn't prevent entire site deployment
- **Implementation:** Try-catch around each entry transformation, log errors, continue processing, exit code 1 if any failures
- **Investigation:** Jekyll will still build successfully even if some posts are missing, so failed transformations should not block deployment

**Decision 3: SEO Validation Before Transformation**
- **Rationale:** Enforce SEO best practices from day one, give content editors immediate feedback
- **Implementation:** Validate SEO entry exists and has required fields before starting transformation
- **Investigation:** Contentful schema marks `seo` field as `required: true` for blogTemplate, but validation at Python layer provides better error messages

**Decision 4: Direct CDN Links (No Image Downloads)**
- **Rationale:** Build time constraint (< 5 min). Downloading images adds 2-5 minutes.
- **Implementation:** Store Contentful CDN URLs directly in frontmatter, let Contentful CDN serve images
- **Investigation:** Jekyll templates already use Contentful URLs with query params (`?w=1200&fm=webp&q=85`) for optimization

**Decision 5: Three Trigger Types for CI/CD**
- **Rationale:** Flexibility for different workflows (content publish, draft preview, code changes)
- **Implementation:**
  - Contentful webhook → Production workflow (normal publish flow)
  - Manual dispatch → Preview workflow (review drafts)
  - Push to main → Production workflow (code updates)
- **Investigation:** GitHub Actions supports `on: [push, workflow_dispatch, repository_dispatch]` for flexible triggering

**Decision 6: Mock Responses for Unit Tests**
- **Rationale:** Fast test execution, no API rate limits, deterministic tests
- **Implementation:** Create mock Entry objects with fixtures, no real Contentful API calls in tests
- **Investigation:** Contentful SDK Entry objects are complex, will need fixtures that simulate `entry.fields()` method with locale support

**Decision 7: Contentful CLI for Content Model Import**
- **Rationale:** Bulk import of 15 content types faster than manual Contentful UI
- **Implementation:** Use `contentful space import` command with JSON files from `contentful-schemas/` directory
- **Investigation:** Confirmed 16 JSON files exist in `contentful-schemas/` (15 content types + 1 summary doc)

**Decision 8: File Writer Handles Locale Folder Creation**
- **Rationale:** Jekyll collections require specific folder structure (`_posts/en/`, `_posts/es/`)
- **Implementation:** File writer checks if locale folder exists, creates if missing, writes markdown files
- **Investigation:** `_config.yml` already configured with locale-aware defaults and permalink structure

**Decision 9: Rich Text → Markdown Conversion Required**
- **Rationale:** Contentful stores blog body as RichText JSON, Jekyll needs Markdown
- **Implementation:** Custom converter to handle Contentful's document nodes (paragraphs, headings, lists, blockquotes, embedded assets)
- **Investigation:** Contentful RichText enables: H2-H4, lists, blockquotes, hr, embedded-asset-block, embedded-entry-block, hyperlinks, marks (bold/italic/code)

**Decision 10: Referenced Entry Resolution**
- **Rationale:** Header/Footer menuItems are references to mlMenuItem entries (not inline)
- **Implementation:** Use Contentful SDK `include=2` parameter to fetch referenced entries in single API call, then resolve references in transformer
- **Investigation:** `orHeader` and `orFooter` schemas show `menuItems` and `socialLinks` are arrays of Entry references, not direct values

## Implementation Plan

### Tasks

**Phase 0: Security Setup (CRITICAL - Do First)**

- [ ] Task 0: Rotate Contentful API tokens (security remediation)
  - Action: Log into Contentful dashboard (https://app.contentful.com)
  - Navigate to: Settings > API keys
  - **Revoke old tokens:**
    - Delete existing Delivery API token
    - Delete existing Preview API token
  - **Generate new tokens:**
    - Create new Content Delivery API token (for production)
    - Create new Content Preview API token (for draft preview)
  - **Store securely:**
    - Save new tokens in password manager (1Password, LastPass, etc.)
    - Add tokens to GitHub Secrets (repository Settings > Secrets and variables > Actions)
    - Create `.env` file locally with new tokens (DO NOT commit)
  - **Verify:**
    - Test new tokens work with simple API call: `curl https://cdn.contentful.com/spaces/co4wdyhrijid/entries?access_token=<NEW_TOKEN>`
  - Notes: This remediates the security incident from exposed tokens in initial spec version

**Phase 1: Foundation Setup**

- [ ] Task 1: Initialize Python project structure
  - File: Create directory structure: `scripts/`, `scripts/contentful_client/`, `scripts/transformers/`, `scripts/converters/`, `scripts/writers/`, `tests/`
  - File: `scripts/requirements.txt`
  - Action: Create with dependencies: `contentful==1.13.3`, `python-frontmatter==1.0.0`, `PyYAML==6.0`, `requests==2.31.0`, `pytest`, `python-dotenv`
  - File: `.env.example`
  - Action: Document required environment variables: `CONTENTFUL_SPACE_ID`, `CONTENTFUL_ACCESS_TOKEN`, `CONTENTFUL_PREVIEW_TOKEN`, `CONTENTFUL_MODE`
  - File: `.gitignore`
  - Action: Add Python patterns: `.env`, `__pycache__/`, `*.py[cod]`, `venv/`, `_posts/`, `_data/*.yml` (exclude examples)
  - Notes: Clean slate - no existing Python code

- [ ] Task 2: Import Contentful content model via CLI
  - File: `scripts/import_content_model.sh` (bash script)
  - Action: Create script that imports all 15 content types from `contentful-schemas/*.json` using `contentful space import`
  - **Prerequisites:**
    - Install Contentful CLI: `npm install -g contentful-cli`
    - Obtain Management API token: Contentful dashboard > Settings > API keys > Content management tokens > Generate personal token
    - Note: This is DIFFERENT from Delivery/Preview tokens - Management tokens have write access for schema changes
  - Command: `contentful space import --space-id co4wdyhrijid --management-token <YOUR_MANAGEMENT_TOKEN> --content-file contentful-schemas/`
  - Alternative: Use existing `push-contentful-schemas.sh` if it already handles imports correctly (verify first)
  - Notes: Must authenticate with Contentful CLI first (`contentful login`), use Master environment, Management token is NEVER stored in GitHub Secrets (local use only)

**Phase 2: Core Infrastructure**

- [ ] Task 3: Create Contentful dual-mode client
  - File: `scripts/contentful_client/client.py`
  - Action: Implement `ContentfulClient` class with:
    - Constructor accepts `space_id`, `access_token`, `mode` ('production' or 'preview')
    - Dual-mode API switching (`api_url='preview.contentful.com'` for preview mode)
    - In-memory cache with TTL (5 minutes) using `dict` and timestamps
    - Method `get_entries(content_type, locale='en', include=2)` with caching
    - Method `clear_cache()` for testing
    - Type hints: `def get_entries(self, content_type: str, locale: str = 'en') -> List[Entry]:`
    - Structured logging: `logger.info(f"✅ API_CALL content_type={content_type} locale={locale} cached={from_cache}")`
  - Notes: Must handle 14 req/sec rate limit gracefully

- [ ] Task 4: Create configuration module
  - File: `scripts/config.py`
  - Action: Implement configuration loading:
    - Load environment variables using `python-dotenv`
    - Validate required variables exist (raise `EnvironmentError` if missing)
    - Export constants: `CONTENTFUL_SPACE_ID`, `CONTENTFUL_ACCESS_TOKEN`, `CONTENTFUL_PREVIEW_TOKEN`, `CONTENTFUL_MODE`
    - Setup structured logging with emoji markers
    - Type hints for all functions
  - Notes: Never log sensitive values (tokens)

**Phase 3: Content Transformers**

- [ ] Task 5: Create base transformer class
  - File: `scripts/transformers/base_transformer.py`
  - Action: Implement `BaseTransformer` abstract class with:
    - Constructor accepts `ContentfulClient` and `locale`
    - Abstract method `transform_single(entry: Entry) -> Dict[str, Any]`
    - Abstract method `transform_all() -> List[Dict[str, Any]]`
    - Common validation methods: `validate_required_fields(entry, fields: List[str])`
    - Error handling wrapper with graceful degradation
    - Structured logging methods
  - Notes: All transformers inherit from this base class

- [ ] Task 6: Implement Rich Text → Markdown converter
  - File: `scripts/converters/markdown_converter.py`
  - Action: Implement `RichTextConverter` class to handle Contentful RichText JSON:
    - Method `convert(rich_text_document: dict) -> str` returns Markdown string
    - Handle known node types: paragraph, heading-2, heading-3, heading-4, unordered-list, ordered-list, blockquote, hr, hyperlink
    - Handle known marks: bold (`**text**`), italic (`*text*`), code (`` `text` ``), underline (use `<u>` HTML)
    - Handle embedded-asset-block: convert to `![alt](cdn_url)` Markdown image syntax
    - Handle embedded-entry-block: skip with warning log (not implemented in MVP)
    - **Unknown node type handling:** If encounter unrecognized `nodeType`, log warning with `logger.warning(f"⚠️ UNKNOWN_NODE_TYPE node_type={node_type} - skipping")` and continue processing (graceful degradation)
    - **Unknown mark handling:** If encounter unrecognized mark, log warning and render as plain text
    - Preserve line breaks and paragraph spacing
    - Type hints: `def convert(self, document: Dict[str, Any]) -> str:`
  - Notes: Contentful RichText structure is nested JSON with `nodeType`, `content`, `marks`. Future-proof against Contentful API additions by logging unknowns rather than crashing

- [ ] Task 7: Implement blog post transformer
  - File: `scripts/transformers/blog_post_transformer.py`
  - Action: Implement `BlogPostTransformer(BaseTransformer)` with:
    - Method `validate_seo(entry: Entry) -> None`: Check SEO entry exists and has required fields (title, description), raise `ValueError` if missing
    - Method `transform_single(entry: Entry) -> Dict[str, Any]`:
      - Call `validate_seo()` FIRST (fail fast)
      - Extract Contentful fields using `entry.fields(locale=self.locale, fallback_locale='en')`
      - Map fields: `url` → `slug`, `title` → `title`, `description` → `excerpt`, `publishDate` → `publish_date` (ISO 8601, no transformation), `label` → `category`, `author` → `author`
      - Convert `text` (RichText) → Markdown body using `RichTextConverter`
      - Extract `image` asset → `featured_image` (direct CDN URL via `asset.url()`)
      - Extract SEO fields: `seo.title` → `seo_title`, `seo.description` → `seo_description`, `seo.keywords` → `seo_keywords`, `seo.ogImage` → `og_image`
      - Return dict with `frontmatter` (dict) and `body` (Markdown string)
      - Use snake_case for ALL frontmatter keys
      - Type hints: `def transform_single(self, entry: Entry) -> Dict[str, Any]:`
    - Method `transform_all() -> List[Dict[str, Any]]`: Fetch all blog posts, transform with graceful degradation, log errors, return list
  - Notes: Primary transformer - gets built first, most complex

- [ ] Task 8: Implement profile transformer
  - File: `scripts/transformers/profile_transformer.py`
  - Action: Implement `ProfileTransformer(BaseTransformer)`:
    - Method `transform_single(entry: Entry) -> Dict[str, Any]`:
      - Map fields: `fullName` → `name`, `title` → `title` (localized), `bio` → `bio` (localized), `profileImage` → `photo_url` (CDN URL), `email` → `email`
      - Resolve `socialLinks` array (Entry references to componentSocialLink): extract `platform` and `url`, create list of dicts
      - Map CTA: `ctaLabel` → `cta_button.text` (localized), `ctaUrl` → `cta_button.url`, `ctaUrl` starts with 'http' → `external: true`
      - Return YAML-ready dict (no frontmatter/body split, pure data)
    - Method `transform_all()`: Fetch profile entries (should be singleton), return first entry only
  - Notes: Outputs to `_data/profile-{locale}.yml`, not `_posts/`

- [ ] Task 9: Implement header transformer
  - File: `scripts/transformers/header_transformer.py`
  - Action: Implement `HeaderTransformer(BaseTransformer)`:
    - Method `transform_single(entry: Entry) -> Dict[str, Any]`:
      - Map fields: `brandUrl` → `brand_url`, `brandImage` → `brand_logo_url` (CDN URL)
      - Resolve `menuItems` array (Entry references to mlMenuItem): extract `label` (localized) and `url`, create list of dicts with `label`, `url`, `external` (bool)
      - **Circular reference protection:** Track visited entry IDs in set during reference resolution, skip entries already seen (log warning if detected)
      - Resolve `topLinks` array (same as menuItems with circular protection)
      - Return YAML-ready dict
    - Method `transform_all()`: Fetch header entries, return first (singleton)
  - Notes: Referenced Entry resolution critical here (`include=2` in API call). Contentful's `include` parameter limits depth to 2 levels, which provides natural protection, but add explicit visited-set guard as defense-in-depth

- [ ] Task 10: Implement footer transformer
  - File: `scripts/transformers/footer_transformer.py`
  - Action: Implement `FooterTransformer(BaseTransformer)`:
    - Method `transform_single(entry: Entry) -> Dict[str, Any]`:
      - Map fields: `brandImage` → `brand_logo_url`, `brandUrl` → `brand_url`, `description` → `description`, `copyright` → `copyright`
      - Resolve `menuItems` array (mlMenuItem references): extract `label`, `url`, create list
      - Resolve `socialLinks` array (componentSocialLink references): extract `platform`, `url`, create list
      - Return YAML-ready dict
  - Notes: Similar to header transformer, handles referenced entries

**Phase 4: File Writers**

- [ ] Task 11: Implement file writer for blog posts
  - File: `scripts/writers/file_writer.py`
  - Action: Implement `FileWriter` class:
    - Method `write_blog_post(post_data: Dict[str, Any], locale: str) -> None`:
      - Extract `slug` and `publish_date` from `post_data['frontmatter']`
      - **Validate publish_date format:**
        - Parse ISO 8601 date to extract YYYY-MM-DD portion: `date_str = publish_date[:10]`
        - Validate format matches YYYY-MM-DD using regex or datetime parsing
        - If invalid or missing, use current date: `date_str = datetime.now().strftime('%Y-%m-%d')` and log warning
      - Generate filename: `{date_str}-{slug}.md` (format: `YYYY-MM-DD-slug.md`)
      - **Validate slug format:** Ensure slug is kebab-case (lowercase, hyphens only), sanitize if needed
      - Create locale folder if not exists: `_posts/{locale}/`
      - Use `frontmatter` library to serialize: `frontmatter.dumps(Post(body, **frontmatter_dict))`
      - Write to `_posts/{locale}/{filename}`
      - Handle write errors gracefully, log with `logger.error(f"❌ WRITE_FAILED path={path} error={e}")`
      - Type hints: `def write_blog_post(self, post_data: Dict[str, Any], locale: str) -> None:`
  - Notes: YAML frontmatter with `---` delimiters, Markdown body below. Date/slug validation prevents filesystem errors from malformed data

- [ ] Task 12: Implement data writer for YAML files
  - File: `scripts/writers/data_writer.py`
  - Action: Implement `DataWriter` class:
    - Method `write_data_file(data: Dict[str, Any], content_type: str, locale: str) -> None`:
      - Generate filename: `_data/{content_type}-{locale}.yml` (e.g., `profile-en.yml`)
      - Serialize dict to YAML using `yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)`
      - Add header comment: `# {content_type} data for {locale} locale\n# Generated by scripts/transformers/\n# DO NOT EDIT MANUALLY`
      - Write to `_data/{filename}`
      - Handle write errors gracefully
      - Type hints: `def write_data_file(self, data: Dict[str, Any], content_type: str, locale: str) -> None:`
  - Notes: Type-locale pattern, not locale folders

**Phase 5: Main Entry Point**

- [ ] Task 13: Create main orchestration script
  - File: `scripts/contentful_to_jekyll.py`
  - Action: Implement main script:
    - Load config, initialize `ContentfulClient` with dual-mode support
    - Initialize transformers: `BlogPostTransformer`, `ProfileTransformer`, `HeaderTransformer`, `FooterTransformer`
    - Initialize writers: `FileWriter`, `DataWriter`
    - For each locale ('en', 'es'):
      - Transform blog posts → write to `_posts/{locale}/`
      - Transform profile → write to `_data/profile-{locale}.yml`
      - Transform header → write to `_data/header-{locale}.yml`
      - Transform footer → write to `_data/footer-{locale}.yml`
    - Track build time (start/end timestamps)
    - Log summary: `logger.info(f"📊 BUILD_COMPLETE duration={duration}s total_posts={count} locales=['en', 'es']")`
    - **Build time monitoring:**
      - If duration > 120 seconds: Log `⚠️ BUILD_SLOW duration={duration}s target=120s` (warning only, continue)
      - If duration > 240 seconds (4 min - critical threshold): Log `❌ BUILD_CRITICAL duration={duration}s - approaching 5min limit, investigate caching/API calls`
      - Script always completes regardless of duration (no timeouts), but warnings help identify performance degradation
    - **Failure threshold logic (graceful degradation with limits):**
      - Track: `total_entries`, `successful_transformations`, `failed_transformations`
      - Calculate failure rate: `failure_rate = failed / total`
      - If `failure_rate < 0.10` (< 10%): Log warning, exit code 0, deploy partial content
      - If `failure_rate >= 0.10` (≥ 10%): Log error, exit code 1, abort deployment
      - If `total_entries == 0`: Log warning "no content found", exit code 0 (empty site is valid)
    - Exit with code 1 if failure threshold exceeded, code 0 if within acceptable limits
  - Notes: Entry point for CI/CD, can run locally with `.env` file. If builds consistently exceed 2 min, investigate: API response times, number of posts, network latency, consider pagination for large post volumes (>100 posts)

**Phase 6: Unit Tests**

- [ ] Task 14: Create test fixtures for Contentful Entry mocks
  - File: `tests/fixtures.py`
  - Action: Create mock Entry objects that simulate Contentful SDK:
    - **Mock Entry class structure:**
      - `entry.id` property returns string entry ID
      - `entry.fields(locale='en', fallback_locale='en')` method returns dict of fields for requested locale
      - **Locale fallback logic:** If field not available in requested locale, return value from fallback_locale
      - **Linked entries:** Mock referenced entries (e.g., SEO entry) with same Entry interface
      - **Assets:** Mock Asset objects with `.url()` method returning CDN URL string
    - Factory functions:
      - `create_mock_blog_post(locale='en', with_seo=True, **overrides)` returns mock Entry with all blogTemplate fields populated
      - `create_mock_profile(locale='en', **overrides)` returns mock Entry with profile fields
      - `create_mock_seo(locale='en', **overrides)` returns mock SEO Entry
      - `create_mock_menu_item(label='Home', url='/', locale='en')` returns mock mlMenuItem Entry
      - Accept `**overrides` to customize specific fields per test (e.g., `create_mock_blog_post(title='Custom Title')`)
    - **Example implementation:**
      ```python
      from unittest.mock import Mock
      
      def create_mock_blog_post(locale='en', with_seo=True, **overrides):
          mock_entry = Mock()
          mock_entry.id = 'blog-123'
          
          fields_data = {
              'title': 'Test Blog Post',
              'url': 'test-blog-post',
              'description': 'Test excerpt',
              # ... more fields
          }
          fields_data.update(overrides)
          
          mock_entry.fields.return_value = fields_data
          return mock_entry
      ```
    - Notes: Use `unittest.mock.Mock` with explicit return_value configuration for methods

- [ ] Task 15: Write unit tests for blog post transformer
  - File: `tests/test_blog_post_transformer.py`
  - Action: Implement tests:
    - `test_transform_single_success()`: Happy path, verify all fields mapped correctly, snake_case keys
    - `test_transform_single_seo_missing()`: Verify raises `ValueError` when SEO entry missing
    - `test_transform_single_seo_fields_missing()`: Verify raises `ValueError` when SEO missing title/description
    - `test_iso8601_date_preserved()`: Verify `publishDate` passed through unchanged
    - `test_featured_image_cdn_url()`: Verify image is CDN URL, not downloaded
    - `test_rich_text_conversion()`: Verify RichText converts to Markdown correctly
    - `test_transform_all_graceful_degradation()`: Verify continues on single failure, returns partial results
  - Notes: Use AAA pattern, mock Contentful client

- [ ] Task 16: Write unit tests for profile/header/footer transformers
  - File: `tests/test_profile_transformer.py`, `tests/test_header_transformer.py`, `tests/test_footer_transformer.py`
  - Action: Test each transformer:
    - Happy path (all fields present)
    - Missing optional fields (graceful handling)
    - Referenced entry resolution (socialLinks, menuItems)
    - Locale handling (localized fields)
  - Notes: Similar structure to blog post tests

- [ ] Task 17: Write unit tests for Rich Text converter
  - File: `tests/test_markdown_converter.py`
  - Action: Test node types:
    - Paragraphs, headings (H2-H4), lists (ordered/unordered), blockquotes
    - Marks (bold, italic, code)
    - Embedded assets (images)
    - Hyperlinks
  - Notes: Use real Contentful RichText JSON structures as fixtures

- [ ] Task 18: Write unit tests for file writers
  - File: `tests/test_file_writer.py`, `tests/test_data_writer.py`
  - Action: Test file writing:
    - Filename generation (date prefix, slug format)
    - Locale folder creation
    - YAML frontmatter serialization
    - Error handling (permissions, disk space)
  - Notes: Use temporary directory for test file writes

**Phase 7: CI/CD Automation**

- [ ] Task 19: Create production deployment workflow
  - File: `.github/workflows/production-deploy.yml`
  - Action: Implement GitHub Actions workflow:
    - Triggers: `push` (branch: main), `workflow_dispatch` (manual), `repository_dispatch` (Contentful webhook)
    - Jobs:
      - Checkout code
      - Setup Python 3.11
      - Cache pip dependencies (`~/.cache/pip`, key based on `requirements.txt` hash)
      - Install Python dependencies: `pip install -r scripts/requirements.txt`
      - Run transformation script with production mode: `CONTENTFUL_MODE=production python scripts/contentful_to_jekyll.py`
      - Setup Ruby
      - Cache Jekyll gems (`vendor/bundle`, key based on `Gemfile.lock` hash)
      - Install Jekyll dependencies: `bundle install`
      - Build Jekyll site: `bundle exec jekyll build`
      - Deploy to GitHub Pages: `actions/deploy-pages@v2`
    - Environment variables from GitHub Secrets: `CONTENTFUL_SPACE_ID`, `CONTENTFUL_ACCESS_TOKEN`
    - Track build time, log if > 5 minutes
  - Notes: Default workflow for content publishes

- [ ] Task 20: Create preview deployment workflow
  - File: `.github/workflows/preview-deploy.yml`
  - Action: Implement preview workflow (similar to production):
    - Trigger: `workflow_dispatch` only (manual dispatch for draft preview)
    - Same steps as production BUT:
      - Use `CONTENTFUL_MODE=preview` environment variable
      - Use `CONTENTFUL_PREVIEW_TOKEN` secret
      - **Preview deployment strategy (SIMPLIFIED):** Deploy to same branch (main) but with different build mode
        - Preview builds fetch draft content, transform, commit to main branch
        - GitHub Pages serves the updated content (preview is live on main site briefly)
        - **Trade-off:** Preview content goes live temporarily (acceptable for low-traffic personal blog)
        - **Alternative (future enhancement):** Deploy to `gh-pages-preview` branch with separate domain, requires custom domain setup
    - Add workflow input parameter for locale selection (optional)
  - Notes: For reviewing draft content before publishing. Simplified approach deploys to main branch temporarily. For true isolated preview, set up separate GitHub Pages branch with custom domain (out of scope for MVP)

- [ ] Task 21: Configure Contentful webhook
  - File: Documentation in `README.md`
  - Action: Document steps to configure Contentful webhook:
    - Webhook URL: `https://api.github.com/repos/{owner}/{repo}/dispatches`
    - Event: `Entry.publish` for `blogTemplate`, `profile`, `orHeader`, `orFooter` content types
    - Headers: `Authorization: Bearer {GITHUB_TOKEN}`, `Accept: application/vnd.github+json`
    - Payload: `{"event_type": "contentful-publish"}`
    - **Retry Configuration (in Contentful webhook settings):**
      - Enable automatic retries (Contentful retries failed webhooks up to 3 times)
      - Timeout: 10 seconds (Contentful default)
      - If webhook consistently fails: Check GitHub API status, verify PAT is valid, check repo permissions
    - **Monitoring:**
      - Contentful webhook logs show delivery status (Settings > Webhooks > Activity log)
      - GitHub Actions shows workflow runs (Actions tab in repo)
      - If webhook fails silently, manually trigger workflow: Actions > Production Deploy > Run workflow
  - Notes: Requires GitHub Personal Access Token with `repo` scope, stored in Contentful webhook settings. Webhook failures are logged in Contentful dashboard for debugging

**Phase 8: Documentation & Final Setup**

- [ ] Task 22: Update README with backend setup instructions
  - File: `README.md`
  - Action: Add sections:
    - Prerequisites (Python 3.11+, Contentful CLI, Node.js for CLI)
    - Backend setup instructions (virtual env, install dependencies)
    - Contentful content model import steps
    - Environment variables configuration (`.env` file for local development)
    - **Local development workflow** (instant iteration - see Task 24)
    - CI/CD architecture diagram
    - Build time expectations (< 5 min via CI/CD, < 10 sec local)
  - Notes: Clear onboarding for future developers

- [ ] Task 23: Create Python package structure files
  - File: `scripts/__init__.py`, `scripts/contentful_client/__init__.py`, `scripts/transformers/__init__.py`, `scripts/converters/__init__.py`, `scripts/writers/__init__.py`
  - Action: Create empty `__init__.py` files to make directories Python packages
  - Notes: Required for proper imports

- [ ] Task 24: Document local development workflow for rapid iteration
  - File: `README.md` (new section: "Local Development for Rapid Preview")
  - Action: Document local development workflow:
    - **Setup:** Create `.env` file with Contentful credentials (copy from `.env.example`)
    - **Workflow:**
      1. Edit content in Contentful (use Preview mode to see drafts)
      2. Run `python scripts/contentful_to_jekyll.py` locally (fetches + transforms: ~5-10 sec)
      3. Start Jekyll with live reload: `bundle exec jekyll serve --livereload --incremental`
      4. View at `http://localhost:4000` (auto-refreshes on file changes)
      5. Iterate rapidly (edit in Contentful → re-run script → Jekyll rebuilds changed files)
      6. When satisfied, publish in Contentful → CI/CD deploys to production (~5 min)
    - **Expected Timing:**
      - Python transformation: ~5-10 seconds (depends on network, number of posts)
      - Jekyll incremental rebuild: ~3-15 seconds (faster for single file changes, slower for Sass/layout changes)
      - **Total iteration cycle: ~10-25 seconds** (still much faster than 5-min CI/CD)
      - First Jekyll build (full): ~30-60 seconds (compiles all Sass, processes all posts)
    - **Performance Tips:**
      - Use `--incremental` flag for faster Jekyll rebuilds (only rebuilds changed files)
      - If Jekyll rebuild is slow, check: post count, Sass complexity, number of includes
      - For very rapid iteration, consider: `CONTENTFUL_MODE=preview` to avoid re-fetching unchanged content
    - **Environment Variables:** Use `CONTENTFUL_MODE=preview` for draft content, `CONTENTFUL_MODE=production` for published content
    - **Use Cases:**
      - Daily editing with multiple iterations: Use local mode (~10-25 sec cycle)
      - Final publish after edits complete: Use Contentful publish + CI/CD (5 min, automated)
  - Notes: Local development significantly faster than CI/CD (~80% faster), but not instant due to Jekyll rebuild overhead

### Acceptance Criteria

**AC1: Environment Setup**
- [ ] Given Python 3.11+ is installed, when `pip install -r scripts/requirements.txt` is run, then all dependencies install successfully without errors

**AC2: Content Model Import**
- [ ] Given Contentful CLI is authenticated, when `scripts/import_content_model.sh` is executed, then all 15 content types are imported to space `co4wdyhrijid` in Master environment

**AC3: Dual-Mode Client**
- [ ] Given `CONTENTFUL_MODE=production` environment variable, when `ContentfulClient` is initialized, then it connects to Delivery API (`cdn.contentful.com`)
- [ ] Given `CONTENTFUL_MODE=preview` environment variable, when `ContentfulClient` is initialized, then it connects to Preview API (`preview.contentful.com`)
- [ ] Given Contentful client fetches entries twice within 5 minutes, when second request is made, then cached data is returned (no API call)

**AC4: Blog Post Transformation**
- [ ] Given a valid blog post with linked SEO entry, when `BlogPostTransformer.transform_single()` is called, then frontmatter dict contains all fields in snake_case: `slug`, `title`, `excerpt`, `publish_date`, `category`, `author`, `featured_image`, `seo_title`, `seo_description`, `seo_keywords`, `og_image`
- [ ] Given a blog post with missing SEO entry, when `BlogPostTransformer.transform_single()` is called, then `ValueError` is raised with message containing "SEO_MISSING"
- [ ] Given a blog post with `publishDate` field, when transformed, then `publish_date` frontmatter field contains unchanged ISO 8601 string (e.g., "2026-01-19T10:30:00Z")
- [ ] Given a blog post with RichText `text` field, when transformed, then body contains valid Markdown with headings, lists, bold/italic text preserved

**AC5: Profile/Header/Footer Transformation**
- [ ] Given a profile entry with localized `title` and `bio`, when `ProfileTransformer.transform_single()` is called with `locale='es'`, then returned dict contains Spanish values for `title` and `bio`
- [ ] Given a header entry with 3 `menuItems` references, when `HeaderTransformer.transform_single()` is called, then `menu_items` array contains 3 dicts with resolved `label` and `url` values
- [ ] Given a footer entry with 5 `socialLinks` references, when `FooterTransformer.transform_single()` is called, then `social_links` array contains 5 dicts with `platform` and `url`

**AC6: File Writing**
- [ ] Given transformed blog post data with `slug='my-first-post'` and `publish_date='2026-01-19'`, when `FileWriter.write_blog_post()` is called with `locale='en'`, then file is created at `_posts/en/2026-01-19-my-first-post.md` with YAML frontmatter and Markdown body
- [ ] Given `_posts/en/` folder does not exist, when `FileWriter.write_blog_post()` is called, then folder is created automatically
- [ ] Given transformed profile data, when `DataWriter.write_data_file()` is called with `content_type='profile'` and `locale='en'`, then file is created at `_data/profile-en.yml` with valid YAML

**AC7: Graceful Degradation with Failure Threshold**
- [ ] Given 10 blog posts where 1 has missing SEO entry, when `BlogPostTransformer.transform_all()` is called, then 9 posts are successfully transformed and returned, 1 failure is logged with `❌ TRANSFORM_FAILED` message
- [ ] Given transformation script processes entries with < 10% failure rate (e.g., 1 failed out of 10), when script completes, then exit code is 0 (success), warning logged, and all valid content is deployed
- [ ] Given transformation script processes entries with ≥ 10% failure rate (e.g., 3 failed out of 10), when script completes, then exit code is 1 (failure), error logged, and CI/CD pipeline halts (no deployment)
- [ ] Given 100% of blog posts fail transformation (e.g., API down, bad credentials), when script completes, then exit code is 1, no deployment occurs, alerting in CI/CD logs

**AC8: Main Script Orchestration**
- [ ] Given valid Contentful credentials, when `scripts/contentful_to_jekyll.py` is executed, then blog posts are written to `_posts/en/` and `_posts/es/`, profile data to `_data/profile-en.yml` and `_data/profile-es.yml`, header/footer to corresponding YAML files
- [ ] Given transformation script runs, when completed, then summary log is output: `📊 BUILD_COMPLETE duration={seconds}s total_posts={count} locales=['en', 'es']`
- [ ] Given transformation takes > 120 seconds, when script completes, then warning log is output: `⚠️ BUILD_SLOW duration={seconds}s target=120s`

**AC9: Unit Test Coverage**
- [ ] Given test suite is run with `pytest tests/ --cov=scripts`, when coverage report is generated, then transformer and converter modules have > 80% coverage
- [ ] Given unit tests use mock Contentful entries, when tests run, then zero real Contentful API calls are made (tests run offline)

**AC10: Production CI/CD**
- [ ] Given production workflow is triggered (push to main or Contentful webhook), when workflow runs, then Python transformation completes successfully, Jekyll builds site, and deploys to GitHub Pages
- [ ] Given GitHub Actions workflow runs, when pip cache is used, then dependency installation completes in < 30 seconds (vs ~90 seconds without cache)
- [ ] Given workflow runs with valid content, when completed, then total workflow duration is < 5 minutes

**AC11: Preview CI/CD**
- [ ] Given preview workflow is manually dispatched, when workflow runs with `CONTENTFUL_MODE=preview`, then draft (unpublished) blog posts are fetched and transformed
- [ ] Given preview workflow deploys, when preview site is accessed, then draft content is visible for review

**AC12: Contentful Webhook Integration**
- [ ] Given Contentful webhook is configured, when content editor publishes blog post in Contentful, then GitHub Actions production workflow is triggered within 30 seconds
- [ ] Given webhook triggers workflow, when workflow completes successfully, then new blog post is live on GitHub Pages within 5 minutes of Contentful publish

**AC13: Build Time Monitoring**
- [ ] Given transformation script tracks timestamps, when script runs with 50 blog posts, then Python transformation phase completes in < 2 minutes
- [ ] Given Jekyll build runs after transformation, when site is built, then Jekyll build completes in < 2 minutes (total < 5 min end-to-end)

**AC14: Error Handling**
- [ ] Given Contentful API returns rate limit error (429), when client retries request, then request succeeds after retry with exponential backoff
- [ ] Given transformation fails due to missing environment variable, when script runs, then clear error message is output: `EnvironmentError: CONTENTFUL_SPACE_ID not set`
- [ ] Given file write fails due to permissions, when error occurs, then error is logged with `❌ WRITE_FAILED path={path} error={message}` and script continues processing remaining files

**AC15: Local Development Workflow**
- [ ] Given `.env` file exists with valid Contentful credentials, when `python scripts/contentful_to_jekyll.py` is run locally, then content is fetched, transformed, and written to Jekyll files in ~5-10 seconds (network dependent)
- [ ] Given Jekyll is running with live reload and incremental builds (`bundle exec jekyll serve --livereload --incremental`), when Python script writes new markdown files to `_posts/`, then Jekyll auto-rebuilds changed files (~3-15 sec) and browser refreshes automatically
- [ ] Given `CONTENTFUL_MODE=preview` in `.env`, when script runs locally, then draft (unpublished) content is fetched from Preview API and transformed
- [ ] Given user iterates on content (edit in Contentful → run script → view in browser), when workflow is repeated 5 times, then each iteration completes in ~10-25 seconds total (Python + Jekyll rebuild), which is 80% faster than 5-min CI/CD cycle
- [ ] Given first Jekyll build (full site compile), when `bundle exec jekyll serve` runs initially, then build completes in ~30-60 seconds (compiles all Sass, processes all posts)

## Additional Context

### Dependencies

**Python (requirements.txt):**
```txt
contentful==1.13.3
python-frontmatter==1.0.0
PyYAML==6.0
requests==2.31.0
pytest
pytest-cov
python-dotenv
```

**Ruby (Gemfile - already installed):**
```ruby
gem "jekyll", "~> 4.3.3"
gem "jekyll-seo-tag", "~> 2.8"
gem "jekyll-sitemap", "~> 1.4"
gem "jekyll-feed", "~> 0.12"
```

**Contentful CLI:**
```bash
npm install -g contentful-cli
```

**GitHub Secrets Required:**
- `CONTENTFUL_SPACE_ID`: co4wdyhrijid
- `CONTENTFUL_ACCESS_TOKEN`: `<your-delivery-api-token>` (generate fresh token from Contentful)
- `CONTENTFUL_PREVIEW_TOKEN`: `<your-preview-api-token>` (generate fresh token from Contentful)
- `GITHUB_TOKEN`: (automatically provided by GitHub Actions)

**How to Configure GitHub Secrets:**
1. Go to GitHub repository > Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Add each secret with name and value from your newly generated Contentful tokens

**Contentful Space Configuration:**
- Space Name: ssa-personal
- Environment: Master
- Content Types: 15 (to be imported via CLI)

### Testing Strategy

**Unit Tests (pytest):**
- Test file naming: `test_{module}.py`
- Coverage target: > 80% for transformers and converters
- Use mocked Contentful Entry objects (no real API calls)
- Test structure: AAA pattern (Arrange, Act, Assert)
- Run with: `pytest tests/ --cov=scripts --cov-report=term-missing`

**Test Coverage Areas:**
1. **Contentful client** (`test_contentful_client.py`):
   - Dual-mode switching (production vs preview API)
   - In-memory caching with TTL
   - Rate limit handling
   - Error handling for missing credentials

2. **Blog post transformer** (`test_blog_post_transformer.py`):
   - Successful transformation (happy path)
   - SEO validation (missing entry, missing fields)
   - ISO 8601 date preservation
   - Rich text → Markdown conversion
   - Featured image CDN URL extraction
   - Graceful degradation (continue on failure)

3. **Profile/Header/Footer transformers** (`test_profile_transformer.py`, etc.):
   - YAML data structure generation
   - Locale handling (localized vs non-localized fields)
   - Referenced entry resolution (menuItems, socialLinks)
   - Fallback locale handling (es → en)

4. **Rich text converter** (`test_markdown_converter.py`):
   - Node types: paragraphs, headings, lists, blockquotes, hr
   - Marks: bold, italic, code, underline
   - Embedded assets (images)
   - Hyperlinks
   - Nested structures

5. **File writers** (`test_file_writer.py`, `test_data_writer.py`):
   - Filename generation (date prefix, slug format)
   - Locale folder creation
   - YAML frontmatter serialization
   - Data YAML serialization
   - Error handling (permissions, disk space)

**Manual Testing (via preview workflow):**
- Trigger preview workflow manually
- Review draft content in preview environment
- Verify transformations correct before publishing

**Integration Testing:**
- Not in scope for this phase (covered by manual testing via CI/CD workflows)

### Notes

**Project Context:**
- Frontend is 100% complete (Epics 4-7) - 60+ files, 4000+ lines of code
- Project follows blog-first architecture (blog carousel is homepage hero element)
- Jekyll expects specific data structures (verified via `.example` files)
- All critical rules documented in `project-context.md` (1010 lines)

**Contentful Constraints:**
- Free tier: 14 req/sec rate limit → use `include=2` for efficient reference fetching
- Cache API responses to minimize calls
- Space is currently empty (content model must be imported first)

**GitHub Pages Constraints:**
- 10 builds per hour limit (shouldn't hit with typical blog publishing cadence)
- 1GB repository limit (mainly text files, well under limit)
- Static files only (no server-side logic)
- HTTPS enforced automatically

**Build Time Targets:**
- **Total:** < 5 minutes (critical user expectation)
- **Python transformation:** < 2 minutes (target)
- **Jekyll build:** < 2 minutes (target)
- **Deployment:** < 1 minute (GitHub Pages)

**High-Risk Items (Pre-Mortem):**
1. **Rich Text → Markdown conversion complexity**: Contentful RichText has nested structure, edge cases may exist
   - Mitigation: Comprehensive unit tests, handle unknown node types gracefully
2. **Referenced entry resolution**: menuItems and socialLinks are Entry references requiring `include` parameter
   - Mitigation: Use `include=2`, test with real Contentful data structure
3. **Build time exceeding 5 minutes**: Large number of blog posts could slow transformation
   - Mitigation: Monitor build time, optimize API calls with caching, consider pagination
4. **Contentful rate limits**: Fetching multiple content types across 2 locales could hit 14 req/sec limit
   - Mitigation: Sequential requests with short delays if needed, cache responses
5. **Contentful webhook configuration**: Requires GitHub PAT with repo scope, potential auth issues
   - Mitigation: Clear documentation, test webhook manually with Postman first

**Known Limitations:**
- Embedded entry blocks in RichText not fully supported (only asset blocks for images)
- No support for multi-level menu items (flat navigation only)
- Preview workflow deploys to same branch (not separate preview environment)
- No automated rollback on failed deployment

**Future Considerations (Out of Scope):**
- Content model versioning and migration scripts
- Multi-environment support (staging, production)
- Advanced monitoring (Datadog, Sentry)
- Performance optimization beyond caching (CDN, image optimization)
- Support for additional content types (case studies, portfolio items)
- Admin dashboard for content management
- Analytics integration
