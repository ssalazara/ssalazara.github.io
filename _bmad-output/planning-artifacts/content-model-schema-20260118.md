# Content Model Schema Blueprint: github-page
**Version:** 2.0  
**Target Platform:** Contentful  
**Last Updated:** 2026-01-18  
**Approach:** Atomic Design + Blog-First Strategy

---

## 1. Overview

This schema maps a **blog-first, warm, and friendly personal portfolio** to structured content types in Contentful. The content model follows [Contentful's best practices](https://www.contentful.com/help/content-models/content-modeling-patterns/) using:

- **Topics and Assemblies Pattern**: Reusable components (topics) composed into page structures (assemblies)
- **Localization Pattern**: ISO 639-1 multi-language support with field-level localization
- **Multichannel Pattern**: Component-based design for maximum reusability

### Design Philosophy

The site is designed with **blog entries as the hero content**, featuring:
- A warm, approachable homepage with profile + blog carousel
- Easy content management for the site owner
- Structured, localized content for fellows and recruiters

---

## 2. Atomic Design Hierarchy

Following atomic design principles with Contentful modeling patterns:

```
⚙️ Utilities (SEO, Profile)
│
📄 Templates (Homepage, Blog Post)
│   ├── 🦠 Organisms (Header, Footer, Hero Banner)
│   │   ├── 🧩 Molecules (Carousel, Text with Image, Rich Text Block)
│   │   │   └── 🧬 Atoms (Card, Quote, Image, Social Link, Menu Item)
│   │   └── 🧬 Atoms
│   └── ⚙️ Utilities (SEO, Profile)
```

---

## 3. Content Types

### 3.1 🧬 Atomic Components (Building Blocks)

#### Menu Item (`mlMenuItem`)
**Purpose:** Single navigation link for headers and footers  
**Localized:** Labels only

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| label | Symbol | Yes | Yes | Display text (max 30 chars) |
| url | Symbol | No | Yes | Relative or absolute URL |
| openInNewTab | Boolean | No | No | Default: false |
| icon | Symbol | No | No | Optional icon identifier |

---

#### Social Link (`componentSocialLink`)
**Purpose:** Social media platform links with icons  
**Used in:** Footer, Header, Profile

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| platform | Symbol | No | Yes | Platform name (e.g., "LinkedIn") |
| url | Symbol | No | Yes | Profile/page URL |
| icon | Symbol | No | No | Icon identifier |

---

#### Card (`componentCard`)
**Purpose:** Reusable content card with image, title, description  
**Used in:** Carousels, blog listings, grid layouts  
**Localized:** Title, description, CTA label

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| title | Symbol | Yes | Yes | Max 60 chars |
| description | Text | Yes | No | Max 150 chars |
| image | Asset | No | Yes | Min 400x300px |
| url | Symbol | No | No | Optional link destination |
| urlLabel | Symbol | Yes | No | CTA button text (max 25 chars) |

**Key Feature:** Can represent blog posts, projects, or any card-based content.

---

#### Image Component (`componentImage`)
**Purpose:** Accessible image wrapper with alt text and captions  
**Used in:** Various content blocks

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| image | Asset | No | Yes | The image file |
| altText | Symbol | Yes | Yes | Accessibility description |
| caption | Text | Yes | No | Optional caption |

---

#### Quote / Testimonial (`componentQuote`)
**Purpose:** Quote display with author attribution  
**Used in:** Page content blocks

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| quoteText | Text | Yes | Yes | Max 500 chars |
| author | Symbol | No | No | Person quoted |
| authorTitle | Symbol | Yes | No | Person's title/role |
| authorPhoto | Asset | No | No | Optional photo (200x200px) |

---

### 3.2 🧩 Molecular Components (Simple Groups)

#### Carousel (`componentCarousel`)
**Purpose:** Sliding container for multiple Card components  
**Primary Use Case:** Blog entry carousel on homepage

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| title | Symbol | Yes | No | Section heading (max 80 chars) |
| cards | Array[Card] | No | Yes | 2-12 cards for optimal UX |

**Blog Strategy:** Auto-generate cards from latest blog posts via Python script.

---

#### Text with Image (`textWithImage`)
**Purpose:** Two-column layout with rich text and image  
**Localized:** All text content

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| heading | Symbol | Yes | No | Section title |
| text | RichText | Yes | Yes | Main content |
| image | Asset | No | Yes | Supporting image |
| imagePosition | Symbol | No | No | "left" or "right" |

---

#### Rich Text Block (`componentRichText`)
**Purpose:** Long-form content with full rich text capabilities  
**Localized:** All content

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| content | RichText | Yes | Yes | Full formatting (H2-H6, no H1) |

**SEO Note:** H1 disabled to maintain one H1 per page.

---

### 3.3 🦠 Organism Components (Complex Sections)

#### Hero Banner (`heroBanner`)
**Purpose:** Full-width hero section with headline, CTA, and background  
**Localized:** Headline, subheading, CTA label

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| title | Symbol | Yes | Yes | Main headline (max 80 chars) |
| description | Text | Yes | No | Subheading (max 250 chars) |
| ctaLabel | Symbol | Yes | No | Button text (max 25 chars) |
| ctaUrl | Symbol | No | No | Button destination |
| image | Asset | No | Yes | Background (1920x1080px, max 2MB) |

---

#### Header (`orHeader`)
**Purpose:** Global navigation with logo, menu, and utility controls  
**Localized:** Menu items via reference

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| brandUrl | Symbol | No | Yes | Logo link destination |
| brandImage | Asset | No | Yes | Logo (max 400x100px) |
| menuItems | Array[MenuItem] | No | Yes | 1-8 main nav items |
| topLinks | Array[MenuItem] | No | No | Max 5 utility links |
| enableSearch | Boolean | No | No | Toggle search bar |
| enableBasket | Boolean | No | No | Toggle shopping cart |
| stickBarContent | RichText | No | No | Announcement bar |

**Note:** Language toggle will be implemented in Jekyll frontend, not in Contentful.

---

#### Footer (`orFooter`)
**Purpose:** Global footer with branding, navigation, social links  
**Localized:** Via menu item references

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| brandImage | Asset | No | No | Optional footer logo |
| brandUrl | Symbol | No | No | Logo link |
| description | Text | No | No | About text (max 300 chars) |
| copyright | Symbol | No | No | Copyright notice |
| menuItems | Array[MenuItem] | No | No | Max 12 footer links |
| socialTitle | Symbol | No | No | Social section heading |
| socialLinks | Array[SocialLink] | No | No | Max 8 platforms |
| enableNewsletter | Boolean | No | No | Toggle newsletter form |

---

### 3.4 📄 Templates (Complete Pages)

#### Homepage (`pageTemplate`)
**Purpose:** Main landing page with flexible content blocks  
**Blog Strategy:** Profile + Blog Carousel as primary content

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Page identifier |
| url | Symbol | No | Yes | URL slug (use "/" for homepage) |
| seo | Link[SEO] | No | Yes | SEO metadata |
| header | Link[Header] | No | Yes | Header configuration |
| blocks | Array[Components] | No | No | Max 20 content blocks |
| footer | Link[Footer] | No | Yes | Footer configuration |

**Accepted Block Types:**
- `heroBanner`
- `componentRichText`
- `textWithImage`
- `componentCarousel` ← **Blog carousel goes here**
- `componentQuote`

**Homepage Structure:**
1. Hero Banner (optional, with profile image)
2. Profile Section (from Profile content type)
3. **Blog Carousel** (featured blog entries)
4. Additional flexible blocks

---

#### Blog Post (`blogTemplate`)
**Purpose:** Individual blog article page  
**Localized:** Title, description, body content  
**Primary Content Type:** This is the hero of the site!

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| url | Symbol | Yes | Yes | URL slug per language |
| seo | Link[SEO] | No | Yes | SEO metadata |
| title | Symbol | Yes | Yes | Article title (H1, max 100 chars) |
| description | Text | Yes | Yes | Summary (max 300 chars) |
| label | Symbol | No | No | Category badge |
| publishDate | Date | No | No | Publication date |
| author | Symbol | No | No | Author name |
| heroBanner | Link[HeroBanner] | No | No | Optional hero |
| text | RichText | Yes | Yes | Main article body (H2-H4) |
| image | Asset | No | Yes | Featured image (min 800x600px) |

**Categories:** Technology, Lifestyle, Business, Design, Updates, News

---

### 3.5 ⚙️ Utility Components

#### SEO Metadata (`seo`)
**Purpose:** Search engine and social media optimization  
**Localized:** Title, description, keywords

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| title | Symbol | Yes | Yes | Meta title (30-60 chars) |
| description | Text | Yes | Yes | Meta description (120-160 chars) |
| keywords | Array[Symbol] | Yes | No | 5-10 focus keywords |
| ogImage | Asset | No | No | Social share image (1200x630px) |
| noIndex | Boolean | No | No | Hide from search engines |
| canonicalUrl | Symbol | No | No | Preferred URL |

---

#### Profile (`profile`)
**Purpose:** Personal profile information for homepage  
**Singleton:** Only one instance should exist  
**Localized:** Title, bio, CTA label

| Field | Type | Localized | Required | Notes |
|-------|------|-----------|----------|-------|
| name | Symbol | No | Yes | Internal identifier |
| fullName | Symbol | No | Yes | Display name |
| title | Symbol | Yes | Yes | Professional title (max 150 chars) |
| bio | Text | Yes | Yes | About summary (max 500 chars) |
| profileImage | Asset | No | Yes | Photo (min 400x400px, square) |
| email | Symbol | No | No | Contact email |
| socialLinks | Array[SocialLink] | No | No | Max 8 social profiles |
| ctaLabel | Symbol | Yes | No | Button text (max 30 chars) |
| ctaUrl | Symbol | No | No | Button destination |
| resumeFile | Asset | No | No | Downloadable CV/resume (PDF) |

**Homepage Integration:** Rendered as a dedicated profile section above the blog carousel.

---

## 4. Localization Strategy

### 4.1 ISO 639-1 Language Codes

**Primary Locale:** `en` (English)  
**Secondary Locales:** To be defined (e.g., `es`, `fr`, `de`)

### 4.2 Localized vs. Non-Localized Fields

**Localized Fields:**
- All user-facing text content (titles, descriptions, body text)
- CTA labels and button text
- SEO metadata (title, description, keywords)
- Menu item labels
- Blog post URLs (for language-specific slugs)

**Non-Localized Fields:**
- Internal names (editor-only)
- Assets (images, files)
- Dates and booleans
- Reference links between entries
- Base URLs and technical IDs

### 4.3 URL Strategy

**Pattern:** `/{locale}/{content-type}/{slug}/`

**Examples:**
- English: `/en/blog/my-first-post/`
- Spanish: `/es/blog/mi-primer-post/`
- Homepage: `/en/` or `/es/`

**Implementation:** Python script generates localized markdown files in Jekyll structure.

---

## 5. Blog-First Content Strategy

### 5.1 Content Hierarchy

1. **Blog Posts** (Primary content)
2. Profile (About the author)
3. Supporting pages (optional)

### 5.2 Homepage Flow

```
Homepage (user.github.io)
├── Hero Banner (optional, warm welcome)
├── Profile Section (image + bio + CTA)
├── 🎯 Blog Carousel (latest 6-10 posts as cards)
└── Optional additional blocks
```

### 5.3 Blog Card Auto-Generation

**Strategy:** Python script creates Card entries automatically from blog posts:

```python
# Pseudo-code
for blog_post in contentful.get_blog_posts(limit=10):
    card = {
        'title': blog_post.title,
        'description': blog_post.description,
        'image': blog_post.image,
        'url': f'/blog/{blog_post.url}/',
        'urlLabel': 'Read More'
    }
    add_to_carousel(card)
```

**Benefit:** Content editors only manage blog posts; cards update automatically.

---

## 6. Validations & Constraints

### 6.1 Character Limits (Contentful Best Practices)

| Field Type | Optimal Range | Max | Rationale |
|------------|--------------|-----|-----------|
| Meta Title | 30-60 chars | 60 | Search engine display |
| Meta Description | 120-160 chars | 160 | Snippet length |
| Hero Headline | - | 80 | Mobile readability |
| Card Title | 40-50 chars | 60 | Consistent card sizing |
| Card Description | 100-120 chars | 150 | Quick scanning |
| CTA Button | 15-20 chars | 25-30 | Button space |
| Blog Summary | - | 300 | Above-fold preview |

### 6.2 Image Specifications

| Component | Recommended Size | Max File Size |
|-----------|-----------------|---------------|
| Hero Background | 1920x1080px | 2MB |
| Blog Featured Image | 1200x630px | - |
| Profile Photo | 500x500px (square) | - |
| Card Thumbnail | 400x300px min | - |
| Logo | 400x100px max | - |
| Social Icon | 48x48px | - |

### 6.3 Content Limits

- Homepage blocks: Max 20
- Carousel cards: 2-12 (optimal UX)
- Menu items: 1-8 (main nav), max 5 (utility)
- Social links: Max 8

---

## 7. Integration with Python & Jekyll

### 7.1 Python Transformation Layer

**Role:** Fetch Contentful data → Transform to Jekyll-compatible Markdown

**Key Responsibilities:**
1. Fetch blog posts with localized fields
2. Generate frontmatter with SEO metadata
3. Resolve references (SEO, images, related content)
4. Create localized file structure: `_posts/en/`, `_posts/es/`
5. Auto-generate blog carousel data

### 7.2 Jekyll Collections

**Proposed Structure:**
```
_posts/
  en/
    2026-01-18-my-first-post.md
  es/
    2026-01-18-mi-primer-post.md
_pages/
  en/
    index.md (homepage)
  es/
    index.md (homepage)
_data/
  profile.yml (from Profile content type)
  blog-carousel.yml (auto-generated from latest posts)
```

### 7.3 Contentful → Jekyll Field Mapping

| Contentful Field | Jekyll Frontmatter | Notes |
|------------------|-------------------|-------|
| `blogTemplate.title` | `title:` | H1 heading |
| `blogTemplate.description` | `excerpt:` | Summary |
| `blogTemplate.publishDate` | `date:` | ISO format |
| `blogTemplate.author` | `author:` | Byline |
| `blogTemplate.label` | `category:` | Badge |
| `blogTemplate.url` | `permalink:` | Custom slug |
| `blogTemplate.image` | `image:` | Featured image URL |
| `seo.title` | `seo_title:` | Meta title |
| `seo.description` | `seo_description:` | Meta description |

---

## 8. Contentful Best Practices Implemented

### ✅ **Topics and Assemblies Pattern**
- **Topics** = Atomic components (Card, Menu Item, etc.)
- **Assemblies** = Page templates that compose topics
- Enables maximum content reuse

### ✅ **Localization Pattern**
- Field-level localization for text content
- ISO 639-1 standard codes
- Fallback to English for missing translations

### ✅ **Multichannel Pattern**
- Component-based structure
- Same Card component works in carousels, grids, listings
- Future-proof for additional channels (mobile app, API)

### ✅ **Navigation Pattern**
- Menu Items control site navigation
- Editors can update nav without code changes
- Supports both header and footer menus

### ✅ **Microcopy Pattern**
- Short, concise text with character limits
- CTA labels, button text, form hints
- Non-developers manage UX copy

---

## 9. Migration & Deployment

### 9.1 Contentful Setup

1. Create new Contentful space (or use existing)
2. Import all 15 content type schemas:
   - 5 Atomic components
   - 3 Molecular components
   - 3 Organism components
   - 2 Templates
   - 2 Utilities
3. Configure locales: Add `en` as primary, additional locales as needed
4. Set up API keys (Delivery API and Preview API)

### 9.2 Initial Content

**Required for Launch:**
1. 1x Profile entry (singleton)
2. 1x Header configuration
3. 1x Footer configuration
4. 1x Homepage entry
5. 3-5 Blog posts (to populate carousel)
6. SEO entries for each page/post

### 9.3 Python Script Deployment

- GitHub Actions workflow triggered on:
  - Contentful webhook (content.publish)
  - Manual trigger
  - Scheduled daily build
- Script fetches latest content and rebuilds Jekyll site
- Deploys to GitHub Pages

---

## 10. Success Metrics

### Content Editor Experience
- ✅ Can publish new blog post in < 5 minutes
- ✅ No code required for content updates
- ✅ Clear help text guides every field
- ✅ Validations prevent common errors

### Site Visitor Experience
- ✅ Warm, friendly, blog-first interface
- ✅ Latest content always featured on homepage
- ✅ Multi-language support for global audience
- ✅ Fast load times (static site generation)

### Technical Quality
- ✅ SEO-optimized (meta tags, structured data)
- ✅ Accessible (alt text, semantic HTML)
- ✅ Mobile-responsive (character limits, image specs)
- ✅ Maintainable (modular, documented)

---

## 11. Future Enhancements

### Phase 2 Considerations
- **Publications content type** (research papers)
- **Projects content type** (portfolio items)
- **Comments system** (via third-party integration)
- **Search functionality** (Algolia or Lunr.js)
- **Newsletter integration** (Mailchimp, ConvertKit)
- **Analytics dashboard** (track popular blog posts)

---

## Conclusion

This content model provides:
- **Blog-first strategy** with carousel as hero element
- **Warm, friendly UX** with profile-driven homepage
- **ISO-compliant localization** for global reach
- **Contentful best practices** for scalability
- **Atomic design** for component reuse
- **Easy content management** for non-technical editors

All schemas are production-ready and follow the [Contentful content modeling patterns](https://www.contentful.com/help/content-models/content-modeling-patterns/) for long-term success.

---

**For implementation details, see:**
- `technical-specification-20260118.md`
- `integration-architecture-20260118.md`
- `homepage-structure-specification.md`
