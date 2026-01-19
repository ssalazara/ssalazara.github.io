---
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics']
inputDocuments:
  - "_bmad-output/planning-artifacts/prd.md"
  - "_bmad-output/planning-artifacts/architecture.md"
  - "_bmad-output/planning-artifacts/integration-architecture-20260118.md"
  - "_bmad-output/project-context.md"
  - "_bmad-output/planning-artifacts/content-model-schema-20260118.md"
  - "_bmad-output/planning-artifacts/localization-routing-strategy.md"
---

# github-page - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for github-page, decomposing the requirements from the PRD, Architecture, and supporting documents into implementable stories.

## Requirements Inventory

### Functional Requirements

**FR1: Blog Post Management via Contentful**
- Content creator can publish new blog posts entirely through Contentful CMS
- Blog posts include: title, slug, body (rich text), publish date, author, excerpt, featured image
- Draft → Published workflow supported
- Localized fields for multi-language posts (EN/ES)
- Python script fetches and transforms blog posts to Jekyll markdown
- Blog posts appear at `/{locale}/blog/{slug}/` within 5 minutes of publishing

**FR2: Profile Management via Contentful**
- Site owner can update bio, photo, title, and contact info through Contentful
- Profile content type follows singleton pattern (only 1 instance)
- Localized bio field (500 chars max) and professional title
- Social media links management (LinkedIn, GitHub, Twitter, etc.)
- Optional CTA button configuration
- Profile renders on homepage and about page

**FR3: Homepage Blog Carousel (Latest Posts Preview)**
- Carousel component displays 6-10 LATEST blog posts as hero element on homepage
- Each card shows: featured image, title, summary, publish date, category
- "Read More" CTA on each card
- Responsive design (3 cols desktop, 2 cols tablet, 1 col mobile)
- Cards sorted by publish date (latest first)
- "View All Blog Posts →" link below carousel (goes to /blog page)
- Carousel auto-updates when new posts published
- Respects current language context

**FR4: Homepage Profile Section**
- Profile section appears above blog carousel
- Displays: name, photo, title, 2-3 sentence bio
- CTA button (e.g., "View Full Bio", "Download CV")
- Social media icons with links
- Warm, friendly visual design

**FR5: Blog Post Detail Page**
- Clean typography with optimal line length (60-75 chars)
- Proper heading hierarchy (H1 title, H2-H4 for sections)
- Code syntax highlighting for technical posts
- Image captions and alt text
- Estimated reading time
- Author byline with photo
- Publish date and category badge display

**FR6: Blog Archive Page**
- Dedicated blog listing page at `/{locale}/blog/`
- Displays ALL blog posts (not just latest 6-10)
- Same card design as homepage carousel
- Paginated if > 20 posts
- Optional: Filter by category/tags
- Each card links to individual blog post
- SEO-optimized for blog discoverability

**FR7: Related Posts**
- "Related Posts" section at bottom of individual blog post (3-4 posts)
- Related by category or tags
- Same card design as homepage carousel
- "Back to Blog Archive" navigation link (goes to /blog page)

**FR8: Multi-Language Support (ISO 639-1)**
- ISO 639-1 language codes (en, es)
- Language switcher in header/footer
- Localized URLs: `/{locale}/{content-type}/{slug}/`
- Fallback to English for untranslated content
- Language preference stored in localStorage
- All UI elements localized (buttons, labels, navigation)
- Hreflang tags for SEO

**FR9: Navigation & Footer Management**
- Header content type with logo, menu items, utility controls
- Footer content type with branding, navigation, social links
- Menu items managed through Contentful (no code changes)
- Localized navigation labels via referenced menu items

**FR10: SEO Metadata**
- Meta titles and descriptions for all pages
- Open Graph tags for social sharing
- Canonical URLs
- XML sitemap generated automatically
- robots.txt configuration
- Schema.org structured data (BlogPosting)
- Alt text required for all images

**FR11: Content Preview (Draft Review)**
- Draft content preview via Contentful Preview API
- Pre-publish review workflow for content editors
- Preview environment accessible via unique URLs
- Dual-mode Python script (Delivery API for production, Preview API for drafts)

### Non-Functional Requirements

**NFR1: Publishing Speed**
- **Target:** < 5 minutes (content published in Contentful → live on site)
- **Driver:** Critical user expectation, drives CI/CD architecture
- **Implementation:** Efficient API calls, optimized builds, webhook automation

**NFR2: Page Load Performance**
- **Target:** < 3 seconds (desktop), < 5 seconds (mobile)
- **Implementation:** Static generation, image optimization, lazy loading, CDN

**NFR3: Build Success Rate**
- **Target:** > 95% successful builds
- **Implementation:** Error handling, retry logic, graceful degradation

**NFR4: Lighthouse Scores**
- **Performance:** > 85
- **SEO:** > 90
- **Accessibility:** > 90
- **Driver:** Code quality, best practices, accessibility standards

**NFR5: Scalability**
- **Target:** < 100 blog posts (year 1), < 10K visitors/month
- **Constraint:** Sufficient for GitHub Pages limits, no premium hosting needed

**NFR6: Accessibility (WCAG 2.1 AA Compliance)**
- Semantic HTML5 elements
- ARIA labels where needed
- Alt text required for all images
- Keyboard navigation for all interactive elements
- Color contrast ratios meeting standards
- Screen reader friendly

**NFR7: Localization Standards**
- ISO 639-1 standard (two-letter language codes)
- Field-level localization in Contentful
- URL routing per language
- Fallback strategy (ES → EN)
- Hreflang implementation

**NFR8: API Rate Limits**
- Contentful free tier: 14 requests/second (Delivery & Preview APIs)
- Request batching required
- Include parameter optimization (max include=2)
- In-memory caching for API responses

**NFR9: Security & Secrets Management**
- Contentful API keys stored as GitHub Secrets
- No exposed credentials in code or logs
- HTTPS-only (GitHub Pages enforced)
- Environment variables for all sensitive data
- Read-only API tokens (Delivery/Preview, not Management)

**NFR10: Maintainability**
- Documented code with inline comments
- Version control for all code (Git)
- Modular architecture (changes isolated to components)
- Unit tests for Python transformation logic (> 80% coverage)
- Type hints required for all Python functions

### Additional Requirements

**Architecture & Technical Implementation:**

1. **No Starter Template** - Build from scratch
   - Repository initialization required
   - Complete Python script development
   - Jekyll site structure setup
   - GitHub Actions workflow configuration

2. **Python 3.11+ with Type Hints**
   - Type hints mandatory for all functions
   - Modern Python syntax required
   - PEP 8 style guide compliance

3. **Snake_case Naming Convention (Python & Frontmatter)**
   - Python: snake_case for functions/variables, PascalCase for classes
   - Jekyll frontmatter: snake_case for all fields
   - NEVER use camelCase or kebab-case in Python/YAML

4. **Kebab-case Naming Convention (Jekyll Files)**
   - All Jekyll layout files: home-page.html, post-layout.html
   - All Jekyll includes: blog-carousel.html, profile-card.html
   - All Sass files: _home-page.scss, _post-layout.scss

5. **ISO 8601 Date Preservation**
   - NEVER transform dates in Python
   - Pass through ISO 8601 from Contentful as-is
   - Liquid date filter handles formatting in templates

6. **Direct Contentful CDN Links (NEVER Download Images)**
   - Use direct CDN URLs for all images
   - No image downloads during build (critical for < 5 min build time)
   - Contentful CDN is globally distributed and optimized

7. **Graceful Degradation (NEVER Abort on Single Failure)**
   - Continue processing if single blog post fails transformation
   - Log errors with structured logging
   - Mark build as failed but deploy working content

8. **SEO Validation Before Transformation**
   - Validate SEO entry exists (fail fast)
   - Validate required SEO fields (title, description)
   - Enforce SEO best practices from day one

9. **Structured Logging with Visual Markers**
   - Emoji markers: ✅ ❌ ⚠️ 📊
   - Structured fields: `key=value key=value`
   - Always include: entry_id, locale, content_type

10. **Locale Folder Structure for Posts**
    - `_posts/en/YYYY-MM-DD-slug.md`
    - `_posts/es/YYYY-MM-DD-slug.md`
    - Filename format: `YYYY-MM-DD-{slug}.md`

11. **Type-Locale Pattern for Data Files**
    - `_data/profile-en.yml`, `_data/profile-es.yml`
    - Type-first, locale suffix (not locale folders)

12. **Dual-Mode Python Script**
    - Mode switching via environment variable (`CONTENTFUL_MODE`)
    - Production mode: Delivery API
    - Preview mode: Preview API
    - Single codebase supports both

13. **GitHub Actions Dependency Caching**
    - Cache Python dependencies (~/.cache/pip)
    - Cache Jekyll gems (vendor/bundle)
    - Saves 30-60 seconds per build

14. **Content Model Implementation (15 Content Types)**
    - Atomic Design hierarchy (Atoms → Molecules → Organisms → Templates)
    - Blog Post (blogTemplate) - PRIMARY CONTENT TYPE
    - Profile (profile) - Singleton pattern
    - Header (orHeader), Footer (orFooter)
    - SEO (seo) - REQUIRED for all blog posts
    - Card (componentCard), Carousel (componentCarousel)
    - Menu Item (mlMenuItem), Social Link (componentSocialLink)
    - Image (componentImage), Quote (componentQuote)
    - Rich Text Block (componentRichText), Text with Image (textWithImage)
    - Hero Banner (heroBanner), Homepage (pageTemplate)

15. **Localization Implementation Details**
    - Language switcher component in header
    - Localized UI strings in `_data/i18n.yml`
    - Hreflang tags in `<head>`
    - Localized XML sitemaps
    - Language preference persistence (localStorage)
    - Browser language detection on first visit

16. **Build Time Constraint**
    - Total build time MUST be < 5 minutes
    - Python transformation: < 2 minutes
    - Jekyll build: < 2 minutes
    - Critical for user satisfaction

17. **Project Structure (Strict Boundaries)**
    - Python layer (`scripts/`) ↔ Jekyll layer (everything else) - NEVER mix
    - Contentful API ↔ Python - JSON communication
    - Python ↔ Jekyll - File system communication (Markdown + YAML)
    - Jekyll ↔ GitHub Pages - Static HTML deployment

### FR Coverage Map

**FR1:** Epic 1 - Blog Post Management via Contentful (blog posts only)  
**FR2:** Epic 2 - Profile Management via Contentful  
**FR3:** Epic 4 - Homepage Blog Carousel (Latest Posts)  
**FR4:** Epic 4 - Homepage Profile Section  
**FR5:** Epic 5 - Blog Post Detail Page  
**FR6:** Epic 4 - Blog Archive Page (`/blog/`)  
**FR7:** Epic 5 - Related Posts  
**FR8:** Epic 6 - Multi-Language UI (foundation in Epic 1)  
**FR9:** Epic 2 - Navigation & Footer Management  
**FR10:** Epic 2 - Basic SEO Metadata (enhanced in Epic 7)  
**FR11:** Epic 7 - Content Preview (Draft Review)

**NFR1:** Epic 3 - Publishing Speed (< 5 min via CI/CD)  
**NFR2:** Epic 7 - Page Load Performance  
**NFR3:** Epic 3 - Build Success Rate  
**NFR4:** Epic 7 - Lighthouse Scores

✅ **All 11 FRs + 4 NFRs covered across 7 epics (revised structure)**

## Epic List

### Epic 1: Content Publishing Foundation (Blog Posts Only)
**Goal:** Content creator can publish blog posts from Contentful that transform into Jekyll markdown files with locale support

**User Outcome:** Simon can create blog posts in Contentful and have them automatically transformed into properly formatted Jekyll markdown with frontmatter, supporting future localization from day one.

**FRs Covered:** FR1 (blog posts only)

**Implementation Notes:**
- Repository initialization with strict boundaries (Python layer ↔ Jekyll layer)
- Python 3.11+ environment + dependencies (requirements.txt)
- Contentful client with in-memory caching (performance requirement)
- Blog post transformer ONLY (JSON → Markdown + frontmatter)
  - Type hints mandatory
  - Snake_case naming (Python & frontmatter)
  - ISO 8601 date preservation (no transformation)
  - Direct CDN links (never download images)
  - Graceful error handling (continue on failure)
  - Structured logging with visual markers (✅ ❌ ⚠️)
- Locale folder structure from day one (`_posts/en/`, `_posts/es/`)
- Unit test framework + transformer tests (> 80% coverage target)
- Build time monitoring/logging
- SEO validation before transformation (fail fast)

**Architectural Decisions:**
- Performance architecture is foundational (caching, monitoring)
- Quality patterns established early (type hints, tests, logging)
- Localization foundation prevents retrofit pain
- Focus on ONE content type done RIGHT

---

### Epic 2: Supporting Content & Basic SEO
**Goal:** Content creator can manage profile, navigation, and footer; visitors have basic SEO for discoverability

**User Outcome:** Simon can update profile/navigation through Contentful, and all published content has proper meta tags for search engines and social sharing.

**FRs Covered:** FR2, FR9, FR10 (basic SEO only)

**Implementation Notes:**
- Profile transformer → localized YAML data files (`_data/profile-en.yml`, `_data/profile-es.yml`)
- Navigation/Footer transformers → localized YAML data files
- Type-locale pattern for data files (profile-en.yml, not en/profile.yml)
- Basic SEO metadata generation (title, description, Open Graph tags)
- Jekyll SEO plugin integration (jekyll-seo-tag)
- Contentful SEO validation (required fields)

**Why After Epic 1:**
- Builds on transformer patterns from Epic 1
- Adds supporting content types (profile, navigation, footer)
- Ensures discoverability from day one (basic SEO)

---

### Epic 3: CI/CD Automation (MOVED UP)
**Goal:** Published content goes live automatically within 5 minutes via GitHub Actions

**User Outcome:** Simon publishes in Contentful, webhook triggers build, and site updates automatically within < 5 minutes without manual intervention.

**FRs Covered:** NFR1 (Publishing Speed), NFR3 (Build Success Rate)

**Implementation Notes:**
- GitHub Actions workflow (production mode)
- Contentful webhook configuration (content.publish event)
- Dependency caching (Python pip, Jekyll gems - saves 30-60 seconds)
- Build time tracking and alerts (< 5 min constraint)
- Error notifications (build failures)
- Jekyll build optimization
- GitHub Pages deployment

**Why Moved Up:**
- Enables automated testing of Epic 4-7
- < 5 min constraint is CRITICAL (NFR1)
- Automation should enable remaining epics, not come last
- Prevents manual deployment bottleneck

---

### Epic 4: Homepage & Blog Discovery
**Goal:** Visitors land on homepage and immediately see profile + latest blog posts, with access to full blog archive

**User Outcome:** Recruiters and visitors see who Simon is (profile section) and discover latest blog content (6-10 posts carousel), with clear "View All" path to complete archive.

**FRs Covered:** FR3, FR4, FR6

**Implementation Notes:**
- Jekyll homepage layout (home-page.html, kebab-case naming)
- Profile card component (_includes/components/profile-card.html)
- Blog carousel component (_includes/components/blog-carousel.html)
- Blog archive page layout (all posts at `/{locale}/blog/`)
- Post card component (reusable)
- "View All Blog Posts →" link below carousel
- Responsive design (3 cols desktop, 2 cols tablet, 1 col mobile)
- Mobile-first approach

**Why After Epic 3:**
- CI/CD enables rapid iteration on layouts
- Automated testing of responsive design
- Can deploy and test homepage immediately

---

### Epic 5: Blog Reading Experience
**Goal:** Visitors read full blog posts in clean, distraction-free layouts with related content recommendations

**User Outcome:** Readers enjoy well-formatted blog posts with optimal typography, code highlighting, related posts, and easy navigation back to archive.

**FRs Covered:** FR5, FR7

**Implementation Notes:**
- Individual blog post layout (post-layout.html)
- Typography optimization (60-75 char line length)
- Code syntax highlighting (for technical posts)
- Related posts algorithm (by category/tags, 3-4 posts)
- "Back to Blog Archive" navigation link
- Reading time estimation
- Author byline with photo
- Publish date and category badge

**Why After Epic 4:**
- Builds on card component from Epic 4 (related posts)
- Completes blog content consumption flow
- Homepage discovery → Archive browsing → Individual reading

---

### Epic 6: Multi-Language UI (RENAMED)
**Goal:** International visitors can switch languages and see localized UI elements

**User Outcome:** Spanish-speaking visitors can toggle to Spanish via language switcher, seeing localized navigation, buttons, and labels (foundation already established in Epic 1).

**FRs Covered:** FR8

**Implementation Notes:**
- Language switcher component (_includes/language-switcher.html)
- i18n UI strings (_data/i18n.yml)
- Language preference persistence (localStorage)
- Hreflang tags for SEO
- Browser language detection (first visit)
- Localized Jekyll permalinks configuration

**Why Foundation in Epic 1:**
- Locale folder structure (`_posts/en/`, `_posts/es/`) already exists
- Data files already use type-locale pattern
- Epic 6 adds UI layer only, not architectural retrofit

---

### Epic 7: Content Preview & Performance
**Goal:** Content creator can preview drafts before publishing; visitors experience fast page loads and optimal Lighthouse scores

**User Outcome:** Simon can review blog posts in preview environment before going live. All visitors experience < 3s page loads with excellent Lighthouse scores.

**FRs Covered:** FR11, NFR2, NFR4

**Implementation Notes:**
- Dual-mode Python script (CONTENTFUL_MODE environment variable)
- Preview API integration (preview.contentful.com)
- Preview workflow in GitHub Actions
- Image lazy loading
- CSS/JS minification
- XML sitemap generation
- Schema.org structured data (BlogPosting)
- Canonical URLs
- Advanced SEO (builds on Epic 2 basic SEO)
- Lighthouse CI integration
- Performance monitoring

**Why Last:**
- Preview mode is nice-to-have (not MVP blocker)
- Performance optimization after content flows work
- Lighthouse targets verified after all features complete

---

## Epic 1: Content Publishing Foundation (Blog Posts Only)

**Goal:** Content creator can publish blog posts from Contentful that transform into Jekyll markdown files with locale support

### Story 1.1: Repository Structure & Python Environment

As a **developer**,
I want **a properly initialized repository with Python 3.11+ environment and dependencies**,
So that **I have a clean foundation to build the content transformation pipeline**.

**Acceptance Criteria:**

**Given** a new project
**When** repository is initialized
**Then** project structure includes: `scripts/`, `tests/`, `_posts/`, `_data/`, `.github/workflows/`, `_layouts/`, `_includes/`, `_sass/`, `assets/`
**And** `.gitignore` excludes: `.env`, `__pycache__/`, `*.py[cod]`, `venv/`, `_site/`, `.jekyll-cache/`, `_posts/`, `_data/`
**And** `requirements.txt` includes: `contentful==1.13.3`, `python-frontmatter==1.0.0`, `PyYAML==6.0`, `requests==2.31.0`, `pytest`, `python-dotenv`
**And** `.env.example` documents required environment variables: `CONTENTFUL_SPACE_ID`, `CONTENTFUL_ACCESS_TOKEN`
**And** Python 3.11+ virtual environment can be created successfully
**And** All dependencies install without errors

### Story 1.2: Contentful Client with Caching

As a **developer**,
I want **a Contentful API client with in-memory caching**,
So that **I can fetch blog posts efficiently without hitting rate limits**.

**Acceptance Criteria:**

**Given** valid Contentful credentials in environment variables
**When** client fetches blog posts
**Then** uses Contentful Delivery API with `include=2` parameter (optimize references)
**And** implements in-memory cache with TTL (5 minutes)
**And** subsequent requests within TTL window return cached data
**And** client handles rate limit errors gracefully (14 req/sec limit)
**And** supports locale parameter for future multi-language support
**And** uses type hints for all public methods
**And** raises clear exceptions for missing credentials
**And** logs API calls with structured format: `✅ API_CALL endpoint=entries.blog_post locale=en cached=false`

### Story 1.3: Blog Post Transformer (Core Logic)

As a **content creator**,
I want **blog posts from Contentful transformed into Jekyll markdown with frontmatter**,
So that **Jekyll can generate static blog post pages**.

**Acceptance Criteria:**

**Given** a Contentful blog post entry
**When** transformer processes the entry
**Then** generates markdown file with YAML frontmatter using snake_case for all fields
**And** preserves ISO 8601 dates without transformation (e.g., `publish_date: '2026-01-18T10:30:00Z'`)
**And** extracts featured image as direct Contentful CDN URL (no download)
**And** transforms rich text body to markdown
**And** validates SEO entry exists (fail fast if missing)
**And** validates required fields: title, slug, body, publish_date
**And** supports locale parameter (defaults to 'en')
**And** uses type hints: `def transform_single(self, entry: Entry) -> Dict[str, Any]`
**And** logs transformation: `✅ TRANSFORM_SUCCESS entry_id={id} locale={locale} slug={slug}`

### Story 1.4: Locale Folder Structure & File Writer

As a **content creator**,
I want **blog posts written to locale-specific folders**,
So that **multi-language support can be added without architectural changes**.

**Acceptance Criteria:**

**Given** transformed blog post data with locale='en'
**When** file writer saves the post
**Then** creates file at `_posts/en/YYYY-MM-DD-{slug}.md`
**And** filename format follows: `{publish_date}-{slug}.md` (date prefix, kebab-case slug)
**And** creates locale folder if it doesn't exist (`_posts/en/`, `_posts/es/`)
**And** writes YAML frontmatter with `---` delimiters
**And** appends markdown body after frontmatter
**And** handles file write errors gracefully (permissions, disk space)
**And** logs: `✅ FILE_WRITTEN path=_posts/en/2026-01-18-my-post.md`
**And** locale folder structure is ready for Spanish posts in future epic

### Story 1.5: Graceful Error Handling & Structured Logging

As a **developer**,
I want **graceful error handling that continues processing if single post fails**,
So that **one broken blog post doesn't prevent entire site deployment**.

**Acceptance Criteria:**

**Given** 10 blog posts where 1 has missing SEO entry
**When** transformation script runs
**Then** successfully transforms 9 valid posts
**And** logs error for broken post: `❌ TRANSFORM_FAILED entry_id={id} error='SEO_MISSING'` with stack trace
**And** continues processing remaining posts (does not abort)
**And** exits with code 1 if any failures occurred (mark build as failed)
**And** exits with code 0 if all posts succeeded
**And** logs summary: `📊 TRANSFORM_COMPLETE total=10 success=9 failed=1`
**And** all logs use visual markers: ✅ (success), ❌ (error), ⚠️ (warning), 📊 (summary)
**And** all logs include structured fields: `key=value key=value`

### Story 1.6: Build Time Monitoring

As a **developer**,
I want **build time monitoring and logging**,
So that **I can ensure < 5 minute total build time constraint is met**.

**Acceptance Criteria:**

**Given** transformation script starts
**When** script executes
**Then** logs start time: `🚀 BUILD_START timestamp={iso8601}`
**And** logs each major phase: FETCH, TRANSFORM, WRITE
**And** logs end time: `✅ BUILD_COMPLETE duration={seconds}s`
**And** warns if duration > 120 seconds (2 minute target for Python phase): `⚠️ BUILD_SLOW duration={seconds}s target=120s`
**And** includes performance breakdown: `fetch={x}s transform={y}s write={z}s`
**And** logs entry count processed: `entries_processed={count}`

### Story 1.7: Unit Tests for Transformer

As a **developer**,
I want **comprehensive unit tests for blog post transformer**,
So that **I can refactor safely and prevent regressions**.

**Acceptance Criteria:**

**Given** pytest framework installed
**When** tests run with `pytest tests/`
**Then** test file exists: `tests/test_blog_post_transformer.py`
**And** tests cover: successful transformation, missing SEO validation, missing required fields, ISO 8601 date preservation, CDN URL handling, graceful error handling
**And** uses mock Contentful entries (no real API calls)
**And** test coverage > 80% for transformer module
**And** all tests pass
**And** tests follow AAA pattern (Arrange, Act, Assert)
**And** test names are descriptive: `test_blog_post_transformer_preserves_iso8601_dates()`

---

## Epic 4: Homepage & Blog Discovery

**Goal:** Visitors land on homepage and immediately see profile + latest blog posts, with access to full blog archive

### Story 4.1: Jekyll Homepage Layout Structure

As a **visitor**,
I want **a well-structured homepage with clear visual hierarchy**,
So that **I can immediately understand who Simon is and discover his latest blog content**.

**Acceptance Criteria:**

**Given** Jekyll site is configured
**When** visitor navigates to `/` or `/en/`
**Then** homepage layout renders with semantic HTML5 structure
**And** layout file exists: `_layouts/home-page.html` (kebab-case naming)
**And** layout uses `default.html` as base layout
**And** includes clear sections: `<header>`, `<main>`, `<footer>`
**And** main content area includes: profile section (first), blog carousel section (second)
**And** uses mobile-first responsive CSS (breakpoints: 768px tablet, 1024px desktop)
**And** follows accessibility best practices (ARIA landmarks, semantic HTML)
**And** `index.html` in project root uses `layout: home-page` frontmatter
**And** page title from frontmatter: `title: "Home | Simon Salazar"`

### Story 4.2: Profile Card Component

As a **recruiter or visitor**,
I want **to see Simon's profile prominently on the homepage**,
So that **I can quickly learn who he is and connect with him**.

**Acceptance Criteria:**

**Given** profile data exists in `_data/profile-en.yml`
**When** homepage renders profile section
**Then** profile component file exists: `_includes/components/profile-card.html`
**And** displays profile photo as circular avatar (150px × 150px on mobile, 200px × 200px on desktop)
**And** displays name as `<h1>` (from `profile.name`)
**And** displays professional title as `<p class="profile-title">` (from `profile.title`)
**And** displays bio text as `<p class="profile-bio">` (from `profile.bio`, max 500 chars)
**And** renders social media links as icon buttons (LinkedIn, GitHub, Twitter)
**And** social links open in new tab with `rel="noopener noreferrer"`
**And** displays optional CTA button (e.g., "View Full Bio", "Download CV") if configured
**And** uses warm, friendly color palette (per design spec)
**And** all images have proper alt text for accessibility
**And** component is locale-aware (pulls from `profile-{locale}.yml`)

### Story 4.3: Post Card Component (Reusable)

As a **developer**,
I want **a reusable blog post card component**,
So that **I can display blog posts consistently across homepage carousel, archive page, and related posts**.

**Acceptance Criteria:**

**Given** blog post data (title, slug, excerpt, featured_image, publish_date, category)
**When** card component renders
**Then** component file exists: `_includes/components/post-card.html`
**And** displays featured image with aspect ratio 16:9 (lazy loading enabled)
**And** displays post title as `<h3>` (linked to post URL)
**And** displays excerpt text (150 chars max with "..." truncation)
**And** displays publish date formatted as "Jan 18, 2026" (Liquid date filter)
**And** displays category badge (e.g., `<span class="badge">Technical</span>`)
**And** includes "Read More →" CTA link
**And** card has hover state (subtle shadow elevation)
**And** card is fully clickable (entire card is link target)
**And** image has proper alt text from post metadata
**And** component accepts parameters: `{% include components/post-card.html post=post %}`
**And** responsive design: fills container width on mobile, max 350px on desktop

### Story 4.4: Blog Carousel Component (Latest Posts)

As a **visitor**,
I want **to see the latest 6-10 blog posts in a carousel on the homepage**,
So that **I can discover Simon's most recent content immediately**.

**Acceptance Criteria:**

**Given** blog posts exist in `_posts/en/` folder
**When** homepage carousel section renders
**Then** carousel component file exists: `_includes/components/blog-carousel.html`
**And** displays section heading: `<h2>Latest Blog Posts</h2>`
**And** fetches latest 6-10 posts sorted by `publish_date` descending
**And** uses Liquid logic: `{% assign latest_posts = site.posts | where: "lang", page.lang | slice: 0, 10 %}`
**And** renders each post using `post-card.html` component
**And** responsive grid layout: 1 column (mobile), 2 columns (tablet), 3 columns (desktop)
**And** includes "View All Blog Posts →" link below carousel (links to `/en/blog/`)
**And** carousel respects current language context (`page.lang`)
**And** if < 6 posts exist, displays all available posts (no minimum)
**And** if 0 posts exist, shows placeholder: "No blog posts yet. Check back soon!"

### Story 4.5: Blog Archive Page Layout

As a **visitor**,
I want **a dedicated page listing ALL blog posts**,
So that **I can browse Simon's complete blog archive beyond just the latest posts**.

**Acceptance Criteria:**

**Given** blog posts exist in `_posts/en/` folder
**When** visitor navigates to `/en/blog/`
**Then** archive page file exists: `blog/index.html` with frontmatter:
```yaml
---
layout: home-page
title: "Blog Archive | Simon Salazar"
permalink: /en/blog/
lang: en
---
```
**And** page displays heading: `<h1>Blog Archive</h1>`
**And** displays ALL blog posts (not just latest 10) sorted by `publish_date` descending
**And** uses same `post-card.html` component for consistency
**And** same responsive grid layout as homepage carousel (1/2/3 columns)
**And** if > 20 posts, implements pagination with Jekyll paginate plugin
**And** includes breadcrumb navigation: "Home > Blog Archive"
**And** page has proper SEO metadata (title, description, canonical URL)
**And** locale-aware: `/en/blog/` for English, `/es/blog/` for Spanish (future)

### Story 4.6: Responsive CSS & Mobile-First Design

As a **mobile visitor**,
I want **the homepage to look beautiful and function perfectly on my phone**,
So that **I can read and navigate easily on any device**.

**Acceptance Criteria:**

**Given** homepage with profile and carousel sections
**When** viewed on mobile device (< 768px)
**Then** Sass file exists: `_sass/pages/_home-page.scss` (kebab-case, snake_case for variables)
**And** mobile layout: single column, profile photo centered, social icons row layout
**And** carousel displays 1 post per row (stacked)
**And** touch-friendly tap targets (minimum 44px × 44px)
**And** text is readable without zooming (min 16px font size)
**And** images scale responsively (max-width: 100%, height: auto)
**When** viewed on tablet (768px - 1023px)
**Then** carousel displays 2 posts per row
**And** profile section uses side-by-side layout (photo left, bio right)
**When** viewed on desktop (≥ 1024px)
**Then** carousel displays 3 posts per row
**And** max content width: 1200px (centered)
**And** generous whitespace and padding
**And** all layouts tested on Chrome, Firefox, Safari, Edge

### Story 4.7: Homepage Navigation & Footer Integration

As a **visitor**,
I want **clear navigation and footer on the homepage**,
So that **I can easily explore other sections of the site**.

**Acceptance Criteria:**

**Given** navigation data exists in `_data/header-en.yml` and footer data in `_data/footer-en.yml`
**When** homepage renders
**Then** header component included: `{% include components/header.html %}`
**And** header displays: logo/name (left), navigation menu (center), language switcher (right)
**And** navigation menu items: "Home", "Blog", "About" (from `header-en.yml`)
**And** current page highlighted in nav ("Home" active on homepage)
**And** footer component included: `{% include components/footer.html %}`
**And** footer displays: copyright notice, social links, sitemap links
**And** header is sticky on scroll (desktop only)
**And** mobile menu uses hamburger icon (< 768px) with slide-out drawer
**And** all navigation links work correctly
**And** keyboard navigation supported (Tab, Enter, Escape for mobile menu)

---

## Epic 5: Blog Reading Experience

**Goal:** Visitors read full blog posts in clean, distraction-free layouts with related content recommendations

### Story 5.1: Individual Blog Post Layout

As a **reader**,
I want **to read blog posts in a clean, distraction-free layout**,
So that **I can focus on the content without distractions**.

**Acceptance Criteria:**

**Given** a published blog post exists
**When** reader navigates to `/en/blog/{slug}/`
**Then** post layout file exists: `_layouts/post-layout.html` (kebab-case naming)
**And** layout uses `default.html` as base layout
**And** displays post title as `<h1>` with proper heading hierarchy
**And** displays featured image with caption (if provided)
**And** displays publish date formatted as "January 18, 2026"
**And** displays category badge
**And** displays author byline with name (from site config)
**And** displays estimated reading time (calculated from word count)
**And** renders post content with proper spacing and typography
**And** content area has max-width for optimal readability (60-75 chars line length ~700px)
**And** uses semantic HTML (`<article>`, `<header>`, `<time>`, `<footer>`)
**And** includes Schema.org BlogPosting structured data
**And** post frontmatter specifies `layout: post-layout`

### Story 5.2: Typography Optimization for Reading

As a **reader**,
I want **text that is easy to read with proper spacing and hierarchy**,
So that **I can comfortably read long-form content**.

**Acceptance Criteria:**

**Given** blog post content renders
**When** reader views the post
**Then** Sass file exists: `_sass/pages/_post-layout.scss`
**And** body text uses optimal line length: max-width 700px (approximately 60-75 characters)
**And** body text font size: 18px (slightly larger than base for readability)
**And** body text line height: 1.75 (relaxed for long-form reading)
**And** paragraphs have generous spacing: margin-bottom 1.5rem
**And** headings (H2-H4) have clear visual hierarchy with proper spacing
**And** H2 headings: 1.75rem (28px), margin-top 3rem, margin-bottom 1rem
**And** H3 headings: 1.5rem (24px), margin-top 2rem, margin-bottom 0.75rem
**And** blockquotes styled with left border, italic text, gray background
**And** lists (ul, ol) have proper indentation and spacing
**And** links within content are underlined and use primary color
**And** images within content are full-width within content area, centered
**And** image captions styled in smaller, gray text below images

### Story 5.3: Code Syntax Highlighting

As a **technical reader**,
I want **code blocks to have syntax highlighting**,
So that **I can easily understand code examples**.

**Acceptance Criteria:**

**Given** blog post contains code blocks (fenced code blocks in markdown)
**When** post renders
**Then** Jekyll syntax highlighter configured in `_config.yml`: `highlighter: rouge`
**And** Syntax highlighting Sass file exists: `_sass/components/_syntax-highlighting.scss`
**And** Code blocks have dark background with light text (accessible contrast)
**And** Syntax colors distinguish between: keywords, strings, comments, functions, variables
**And** Inline code (`backticks`) styled with monospace font and light gray background
**And** Code blocks have horizontal scroll on mobile (no line wrapping)
**And** Code blocks include language indicator in top-right corner (optional enhancement)
**And** Line numbers optional (can be enabled per code block)
**And** "Copy code" button optional (future enhancement)

### Story 5.4: Related Posts Section

As a **reader**,
I want **to discover related blog posts after finishing an article**,
So that **I can continue reading relevant content**.

**Acceptance Criteria:**

**Given** reader finishes reading a blog post
**When** post layout renders
**Then** related posts component file exists: `_includes/components/related-posts.html`
**And** component displays section heading: "Related Posts" or "You May Also Like"
**And** shows 3-4 related posts (not including current post)
**And** related posts filtered by same category as current post
**And** if < 3 posts in same category, fills with recent posts from other categories
**And** uses same `post-card.html` component for consistency
**And** related posts displayed in responsive grid: 1 column (mobile), 2 columns (tablet), 3 columns (desktop)
**And** section appears after post content and before comments section (if future)
**And** "Back to Blog Archive" link included below related posts
**And** related posts respect current locale (only show posts in same language)

### Story 5.5: Post Metadata & Byline

As a **reader**,
I want **to see who wrote the post and when it was published**,
So that **I can assess the content's recency and authority**.

**Acceptance Criteria:**

**Given** blog post displays
**When** post header renders
**Then** byline component file exists: `_includes/components/post-byline.html`
**And** displays author name (from site config or post frontmatter)
**And** displays publish date in human-readable format: "Published on January 18, 2026"
**And** displays estimated reading time: "5 min read" (calculated from word count: words ÷ 200)
**And** displays category badge (same style as post cards)
**And** byline appears below post title and above featured image
**And** byline uses smaller, secondary text color
**And** includes Schema.org metadata: `datePublished`, `author`, `wordCount`
**And** optional: displays last updated date if post was modified

### Story 5.6: Post Footer & Navigation

As a **reader**,
I want **clear navigation options after reading a post**,
So that **I can easily navigate to other content or return to the archive**.

**Acceptance Criteria:**

**Given** reader finishes reading blog post
**When** post footer renders
**Then** post footer section appears after content and related posts
**And** includes "Back to Blog Archive" prominent button/link
**And** includes previous/next post navigation (optional: "← Older" / "Newer →")
**And** includes social sharing buttons (optional future enhancement)
**And** footer uses clear visual separation (border-top or background color)
**And** all navigation elements are touch-friendly (44px minimum tap target)
**And** keyboard navigation supported (Tab, Enter)

---

## Epic 6: Multi-Language UI

**Goal:** International visitors can switch languages and see localized UI elements

### Story 6.1: i18n UI Strings Data File

As a **developer**,
I want **centralized UI string translations**,
So that **all interface text can be easily localized without code changes**.

**Acceptance Criteria:**

**Given** UI elements need translation
**When** i18n data file is created
**Then** file exists: `_data/i18n.yml`
**And** contains translations for both locales (en, es)
**And** includes all UI strings: navigation labels, button text, form labels, empty states, error messages
**And** structured by component/section for easy maintenance
**And** accessed in templates via: `{{ site.data.i18n[current_locale].key }}`
**And** includes translations for: "Home", "Blog", "About", "Read More", "View All", "Related Posts", "Back to Archive", "No posts yet", "Published on", "min read", etc.

### Story 6.2: Hreflang Tags for SEO

As a **search engine**,
I want **hreflang tags indicating alternate language versions**,
So that **I can show users the correct language version in search results**.

**Acceptance Criteria:**

**Given** pages exist in multiple languages
**When** page header renders
**Then** hreflang component file exists: `_includes/seo/hreflang-tags.html`
**And** included in `<head>` section of `default.html` layout
**And** generates `<link rel="alternate" hreflang="en" href="..." />` for English version
**And** generates `<link rel="alternate" hreflang="es" href="..." />` for Spanish version
**And** generates `<link rel="alternate" hreflang="x-default" href="..." />` for default language
**And** URLs are absolute (include domain)
**And** hreflang tags included on: homepage, blog archive, individual blog posts

### Story 6.3: Language Preference Persistence Enhancement

As a **returning visitor**,
I want **my language preference remembered**,
So that **I don't have to select my language on every visit**.

**Acceptance Criteria:**

**Given** visitor selects a language
**When** language switcher is clicked
**Then** JavaScript stores preference in localStorage: `preferredLanguage`
**And** on subsequent visits, redirects to preferred language if on wrong locale
**And** preference persists across sessions
**And** preference can be cleared by switching language again
**And** browser language detection only runs on first visit (no stored preference)
**And** language switcher updates URL correctly for all page types (homepage, archive, posts)

### Story 6.4: Localized Date Formatting

As a **Spanish-speaking reader**,
I want **dates displayed in Spanish format**,
So that **content feels natural in my language**.

**Acceptance Criteria:**

**Given** dates are displayed (publish dates, timestamps)
**When** page renders in Spanish
**Then** dates use Spanish month names: "enero, febrero, marzo..."
**And** date format follows Spanish convention: "18 de enero de 2026"
**When** page renders in English
**Then** dates use English month names: "January, February, March..."
**And** date format follows English convention: "January 18, 2026"
**And** Jekyll date filters handle locale correctly
**And** all date displays are consistent across site (post cards, bylines, archive)

---

## Epic 7: Content Preview & Performance

**Goal:** Content creator can preview drafts before publishing; visitors experience fast page loads and optimal Lighthouse scores

### Story 7.1: SEO Meta Tags Enhancement

As a **search engine / social media platform**,
I want **complete meta tags for all pages**,
So that **I can properly index and display page previews**.

**Acceptance Criteria:**

**Given** any page on the site
**When** page header renders
**Then** includes complete Open Graph tags: og:title, og:description, og:image, og:url, og:type
**And** includes Twitter Card tags: twitter:card, twitter:title, twitter:description, twitter:image
**And** includes canonical URL tag
**And** blog posts include article-specific tags: article:published_time, article:author
**And** images use absolute URLs (include domain)
**And** descriptions are optimized length (150-160 chars)
**And** homepage has site-level OG tags
**And** blog posts inherit featured image as OG image

### Story 7.2: XML Sitemap Generation

As a **search engine**,
I want **an XML sitemap of all pages**,
So that **I can efficiently crawl and index the site**.

**Acceptance Criteria:**

**Given** Jekyll site builds
**When** sitemap generation runs
**Then** jekyll-sitemap plugin configured in `_config.yml`
**And** sitemap.xml generated at root: `/sitemap.xml`
**And** includes all pages: homepage (both locales), blog archive (both locales), all blog posts
**And** includes lastmod dates for posts
**And** includes changefreq and priority hints
**And** excludes: 404 page, admin pages, test pages
**And** sitemap accessible and valid XML format
**And** includes hreflang alternate URLs for multi-language pages

### Story 7.3: Performance Optimization

As a **visitor**,
I want **fast page loads**,
So that **I can access content quickly on any device**.

**Acceptance Criteria:**

**Given** site is deployed
**When** performance is measured
**Then** Sass compilation configured with `style: compressed` in production
**And** images use Contentful CDN with optimization params: `?w=800&fm=webp&q=80`
**And** lazy loading enabled on all images except featured post image: `loading="lazy"`
**And** critical CSS inlined in `<head>` (optional enhancement)
**And** JavaScript is minimal and deferred (already implemented in Epic 4)
**And** no render-blocking resources
**And** fonts use system font stack (no external font loading)
**And** target: < 3 seconds page load on desktop, < 5 seconds on mobile

### Story 7.4: robots.txt Configuration

As a **search engine**,
I want **crawling instructions via robots.txt**,
So that **I know which pages to index**.

**Acceptance Criteria:**

**Given** site is deployed
**When** robots.txt is requested
**Then** file exists at root: `/robots.txt`
**And** allows all user agents: `User-agent: *`
**And** allows crawling all content: `Allow: /`
**And** references sitemap: `Sitemap: https://simonsalazar.github.io/sitemap.xml`
**And** disallows: `/admin/` (if admin section exists)
**And** file is accessible and properly formatted

---
