---
stepsCompleted: ['step-01-init', 'step-02-content-model', 'step-03-blog-first-update']
inputDocuments: 
  - "_bmad-output/planning-artifacts/product-brief-github-page-20260117.md"
  - "_bmad-output/planning-artifacts/brainstorming-summary-20260118.md"
  - "_bmad-output/planning-artifacts/technical-specification-20260118.md"
  - "_bmad-output/planning-artifacts/content-model-schema-20260118.md"
  - "_bmad-output/planning-artifacts/integration-architecture-20260118.md"
briefCount: 1
researchCount: 3
brainstormingCount: 1
projectDocsCount: 0
workflowType: 'prd'
lastUpdated: '2026-01-18'
---

# Product Requirements Document - github-page

**Project Name:** Personal GitHub Pages Portfolio  
**Author:** Simon Salazar  
**Date:** 2026-01-18  
**Version:** 2.0 (Blog-First Revision)  
**Status:** Active Development

---

## Executive Summary

This project transforms a static Jekyll portfolio into a **blog-first, dynamic, localized personal website** that is easy to manage and provides a warm, friendly experience for visitors. The primary audience consists of **fellows (peers/researchers) and recruiters**. The main goal is to drive visitors to **blog entries as the hero content**, while maintaining a structured, approachable digital presence.

### Key Differentiators
- **Blog-first architecture**: Blog entries are the primary content, featured prominently on the homepage
- **Easy content management**: Contentful CMS enables updates without code changes
- **Warm & friendly UX**: Kind, approachable design that reflects the author's personality
- **ISO-compliant localization**: Multi-language support with ISO 639-1 standards
- **Python-powered automation**: Contentful → Jekyll transformation pipeline

---

## 1. Product Vision

### 1.1 The "Why"

**Primary Impact:** Ease of updates for the content creator (Simon)

**Current Pain Points:**
- al-folio's static workflow requires technical knowledge for every update
- Manual rebuilds and Git commits create friction
- Difficult to maintain multi-language content
- Blog content buried in traditional portfolio structure

**Desired Outcome:**
- Publish new blog posts in < 5 minutes without touching code
- Automatic site rebuilds on content changes
- Blog entries drive the visitor experience
- Warm, friendly digital-print that showcases personality **and** content

### 1.2 Target Audience

**Primary Personas:**

1. **Fellow Researchers** (40% of traffic)
   - Looking for thought leadership and technical insights
   - Interested in blog content, research findings
   - Value depth and authenticity

2. **Recruiters** (40% of traffic)
   - Evaluating technical skills and communication ability
   - Need quick access to portfolio highlights
   - Look for evidence of expertise (blog posts!)

3. **General Visitors** (20% of traffic)
   - Discover content through search or social media
   - Blog posts are the primary draw
   - May not know the author beforehand

### 1.3 Success Criteria

**Content Management:**
- ✅ New blog post published in < 5 minutes
- ✅ Zero code required for content updates
- ✅ Multi-language content managed in one place

**Visitor Experience:**
- ✅ Blog entries immediately visible on homepage
- ✅ Clear, warm introduction to the author
- ✅ Easy navigation to blog content
- ✅ Mobile-friendly, fast loading

**Technical:**
- ✅ Automated deployment pipeline
- ✅ SEO-optimized for blog discoverability
- ✅ ISO-compliant localization
- ✅ < 3 second page load time

---

## 2. Product Strategy

### 2.1 Core Strategy: Blog-First Architecture

Unlike traditional portfolios that bury blog content under "Publications" or "Writing," this site **leads with blog entries**.

**Homepage Hierarchy:**
1. **Hero Section** (optional): Warm welcome message
2. **Profile Summary**: Name + photo + 2-3 sentence bio
3. **🎯 Blog Carousel**: Latest 6-10 blog posts as cards (THE HERO)
4. **Supporting Content** (optional): Additional sections

**Why Blog-First?**
- Blog posts demonstrate expertise more effectively than static bios
- Fresh content encourages repeat visits
- Recruiters value communication skills (shown through writing)
- Fellows discover valuable insights immediately
- Drives engagement and time-on-site

### 2.2 Content Strategy

**Primary Content Type:** Blog Posts
- Technology insights
- Research findings
- Personal reflections
- Professional growth

**Supporting Content:**
- Profile/About (contextualizes the author)
- Projects (future phase)
- Publications (future phase)

**Update Frequency:**
- Blog posts: 1-2 per month (target)
- Profile updates: Quarterly
- Design/structure: As needed

### 2.3 Technical Strategy

**The Python Bridge:**
- Contentful (headless CMS) ↔ Python script ↔ Jekyll (static site)
- Automated via GitHub Actions
- Triggered by Contentful webhooks

**Why This Stack?**
1. **Contentful**: Best-in-class CMS with excellent localization
2. **Python**: Flexible transformation logic, official Contentful SDK
3. **Jekyll**: Free hosting on GitHub Pages, fast static sites
4. **GitHub Actions**: Free CI/CD, integrated with GitHub Pages

---

## 3. Functional Requirements

### 3.1 Content Management (P0 - Critical)

#### 3.1.1 Blog Post Management
**User Story:** As a content creator, I can publish a new blog post entirely through Contentful, and it appears on my site within 5 minutes.

**Requirements:**
- [ ] Contentful blog post content type with all necessary fields
- [ ] Localized fields for multi-language posts
- [ ] Rich text editor with formatting options (H2-H4, lists, links, images)
- [ ] Featured image upload with preview
- [ ] Category/tag selection
- [ ] Publish date scheduling
- [ ] Draft → Published workflow
- [ ] Python script fetches and transforms blog posts
- [ ] Jekyll generates blog post pages with proper routing
- [ ] Contentful webhook triggers automatic rebuild

**Acceptance Criteria:**
- Creating a new blog post in Contentful triggers site rebuild
- Post appears at `/{locale}/blog/{slug}/` within 5 minutes
- All localized versions render correctly
- Featured image displays on listing and detail pages
- SEO metadata auto-generated from post data

---

#### 3.1.2 Profile Management
**User Story:** As the site owner, I can update my bio, photo, and contact info through Contentful without code changes.

**Requirements:**
- [ ] Profile content type (singleton pattern)
- [ ] Localized bio field (500 chars max)
- [ ] Profile photo upload with preview
- [ ] Social media links management
- [ ] Professional title (localized)
- [ ] Optional CTA button configuration
- [ ] Python script fetches profile data
- [ ] Jekyll renders profile on homepage and about page

**Acceptance Criteria:**
- Profile updates appear on homepage within 5 minutes
- Localized bios display correctly per language
- Profile photo optimized for web display
- Social links open in new tabs with proper icons

---

### 3.2 Homepage Experience (P0 - Critical)

#### 3.2.1 Blog Carousel
**User Story:** As a visitor, I immediately see the latest blog entries on the homepage, presented as visually appealing cards.

**Requirements:**
- [ ] Carousel component displays 6-10 latest blog posts
- [ ] Each card shows: featured image, title, summary, publish date, category
- [ ] "Read More" CTA on each card
- [ ] Responsive design (3 cols desktop, 2 cols tablet, 1 col mobile)
- [ ] Cards link to full blog post
- [ ] Carousel auto-updates when new posts published
- [ ] Smooth animations/transitions

**Acceptance Criteria:**
- Latest posts appear first (sorted by publish date)
- Cards have consistent sizing and spacing
- Images load efficiently (lazy loading)
- Clicking card navigates to full post
- Carousel respects current language context

---

#### 3.2.2 Profile Section
**User Story:** As a visitor, I can quickly understand who the author is before diving into blog content.

**Requirements:**
- [ ] Profile section appears above blog carousel
- [ ] Displays: name, photo, title, 2-3 sentence bio
- [ ] CTA button (e.g., "View Full Bio", "Download CV")
- [ ] Social media icons with links
- [ ] Warm, friendly visual design
- [ ] Responsive layout

**Acceptance Criteria:**
- Profile loads with homepage (no separate fetch)
- Photo is high-quality but optimized for web
- Bio is concise and engaging
- CTA button has clear action
- Social icons match site theme

---

### 3.3 Blog Post Detail Page (P0 - Critical)

#### 3.3.1 Reading Experience
**User Story:** As a visitor, I can read blog posts in a clean, distraction-free layout optimized for reading.

**Requirements:**
- [ ] Clean typography with optimal line length (60-75 chars)
- [ ] Proper heading hierarchy (H1 title, H2-H4 for sections)
- [ ] Code syntax highlighting (if technical posts)
- [ ] Image captions and alt text
- [ ] Table of contents for long posts (optional)
- [ ] Estimated reading time
- [ ] Author byline with photo
- [ ] Publish date display
- [ ] Category badge

**Acceptance Criteria:**
- Readable on all device sizes
- Images don't break layout
- Code blocks properly formatted
- Internal links work correctly
- Print-friendly styling

---

#### 3.3.2 Related Content
**User Story:** As a visitor, after reading a blog post, I can discover other related content.

**Requirements:**
- [ ] "Related Posts" section at bottom (3-4 posts)
- [ ] Related by category or tags
- [ ] Same card design as homepage carousel
- [ ] "Back to Blog" navigation link

**Acceptance Criteria:**
- Related posts actually relevant (same category)
- Related section doesn't slow page load
- Navigation is intuitive

---

### 3.4 Localization (P1 - Important)

#### 3.4.1 Multi-Language Support
**User Story:** As a non-English visitor, I can view the site in my preferred language.

**Requirements:**
- [ ] ISO 639-1 language codes (`en`, `es`, etc.)
- [ ] Language switcher in header/footer
- [ ] Localized URLs: `/{locale}/blog/{slug}/`
- [ ] Fallback to English for untranslated content
- [ ] Language preference stored in localStorage
- [ ] All UI elements localized (buttons, labels, navigation)

**Acceptance Criteria:**
- Switching languages updates entire site
- URLs reflect current language
- Missing translations show English gracefully
- Language preference persists across sessions

---

### 3.5 SEO & Discoverability (P1 - Important)

#### 3.5.1 Search Engine Optimization
**User Story:** As the site owner, I want blog posts to rank well in search engines.

**Requirements:**
- [ ] Meta titles and descriptions for all pages
- [ ] Open Graph tags for social sharing
- [ ] Canonical URLs
- [ ] XML sitemap generated automatically
- [ ] robots.txt configuration
- [ ] Schema.org structured data (BlogPosting)
- [ ] Alt text required for all images

**Acceptance Criteria:**
- Google Search Console shows no errors
- Social shares display correct image and text
- Site appears in search results within 2 weeks
- Lighthouse SEO score > 90

---

### 3.6 Performance (P1 - Important)

#### 3.6.1 Fast Loading
**User Story:** As a visitor, pages load quickly so I can access content without waiting.

**Requirements:**
- [ ] Page load time < 3 seconds (desktop)
- [ ] Page load time < 5 seconds (mobile)
- [ ] Images optimized and lazy-loaded
- [ ] Minimal JavaScript (static site advantage)
- [ ] CSS minification
- [ ] CDN for asset delivery (GitHub Pages default)

**Acceptance Criteria:**
- Lighthouse Performance score > 85
- First Contentful Paint < 1.5 seconds
- No render-blocking resources
- Smooth scrolling and animations

---

## 4. Non-Functional Requirements

### 4.1 Usability (Content Editor)
- **Help Text**: Every Contentful field has clear guidance
- **Validations**: Prevent common errors (character limits, required fields)
- **Preview**: See changes before publishing
- **Intuitive UI**: No training required to publish a post

### 4.2 Accessibility
- **WCAG 2.1 AA Compliance**: Minimum standard
- **Alt Text**: Required for all images
- **Keyboard Navigation**: All interactive elements accessible
- **Screen Reader Friendly**: Proper semantic HTML

### 4.3 Security
- **Contentful API Keys**: Stored as GitHub Secrets
- **No Exposed Credentials**: All sensitive data in environment variables
- **HTTPS Only**: GitHub Pages enforces SSL

### 4.4 Maintainability
- **Documented Code**: Python script well-commented
- **Version Control**: All code in Git
- **Modular Architecture**: Changes isolated to components
- **Testing**: Unit tests for Python transformation logic

---

## 5. User Flows

### 5.1 Content Creator: Publishing a Blog Post

```
1. Log in to Contentful
2. Click "Add Entry" → Select "Blog Post"
3. Fill in required fields:
   - Internal name (e.g., "My First Post - Jan 2026")
   - URL slug (e.g., "my-first-post")
   - Title (English): "My First Post"
   - Title (Spanish): "Mi Primer Post"
   - Description (English): "This is my first post..."
   - Description (Spanish): "Este es mi primer post..."
   - Category: "Technology"
   - Publish Date: 2026-01-18
   - Author: "Simon Salazar"
   - Body content (rich text, English and Spanish)
   - Featured image (upload)
4. Link to SEO entry (create if needed):
   - Meta title (English/Spanish)
   - Meta description (English/Spanish)
   - Keywords
5. Click "Publish"
6. Contentful webhook triggers GitHub Action
7. GitHub Action runs Python script:
   - Fetches new blog post from Contentful
   - Generates markdown files: `_posts/en/2026-01-18-my-first-post.md`
   - Generates markdown files: `_posts/es/2026-01-18-mi-primer-post.md`
   - Updates blog carousel data
8. Jekyll builds site
9. GitHub Pages deploys
10. Post live at `/en/blog/my-first-post/` within 5 minutes
```

**Total Time:** < 5 minutes (including content writing)

---

### 5.2 Visitor: Discovering Blog Content

```
1. Visitor lands on homepage (user.github.io)
2. Sees hero banner (optional warm welcome)
3. Sees profile section:
   - Photo + name
   - "Researcher & Developer"
   - Brief bio (2-3 sentences)
   - Social links (LinkedIn, GitHub, etc.)
4. Scrolls to blog carousel:
   - 6-10 blog post cards displayed
   - Each card: image, title, summary, date, category
5. Clicks on interesting blog post card
6. Navigates to full blog post page
7. Reads article
8. Sees "Related Posts" at bottom
9. Clicks related post or "Back to Blog"
10. Continues exploring content
```

**Key Metric:** Time from homepage to blog post < 10 seconds

---

### 5.3 Visitor: Changing Language

```
1. Visitor on English homepage
2. Clicks language switcher (top-right toggle)
3. Selects "Español"
4. Page reloads with Spanish content:
   - URL changes to `/es/`
   - Profile bio in Spanish
   - Blog post titles/summaries in Spanish
   - UI elements in Spanish ("Leer Más", etc.)
5. Language preference saved in localStorage
6. Next visit automatically loads Spanish version
```

---

## 6. Technical Architecture

### 6.1 System Overview

```
┌─────────────┐     Webhook      ┌──────────────┐
│  Contentful │ ───────────────> │GitHub Actions│
│     CMS     │                   │              │
└─────────────┘                   └──────┬───────┘
                                         │
                                         │ Runs
                                         ▼
                                  ┌─────────────┐
                                  │   Python    │
                                  │   Script    │
                                  └──────┬──────┘
                                         │
                                         │ Generates
                                         ▼
                                  ┌─────────────┐
                                  │   Jekyll    │
                                  │  Markdown   │
                                  └──────┬──────┘
                                         │
                                         │ Builds
                                         ▼
                                  ┌─────────────┐
                                  │GitHub Pages │
                                  │   (Static)  │
                                  └─────────────┘
                                         │
                                         │ Serves
                                         ▼
                                    Visitors
```

### 6.2 Data Flow

**Content Creation Flow:**
1. Content creator publishes in Contentful
2. Contentful triggers webhook → GitHub Actions
3. GitHub Actions runs Python script:
   - Fetches entries via Contentful Delivery API
   - Resolves references (SEO, images, author)
   - Transforms JSON → Jekyll frontmatter + Markdown
   - Writes files to `_posts/`, `_pages/`, `_data/`
4. Jekyll builds static site
5. GitHub Pages deploys

**Visitor Request Flow:**
1. Visitor requests `user.github.io/en/blog/my-post/`
2. GitHub Pages serves pre-built HTML
3. Browser renders page
4. JavaScript (minimal) handles:
   - Language switcher
   - Dark mode toggle (future)
   - Analytics tracking

### 6.3 Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **CMS** | Contentful | Best-in-class localization, great API, generous free tier |
| **Transformation** | Python 3.11+ | Official Contentful SDK, flexible data manipulation |
| **Static Site Generator** | Jekyll 4.x | GitHub Pages native support, Ruby-based, mature ecosystem |
| **Hosting** | GitHub Pages | Free, fast, integrated with GitHub Actions |
| **CI/CD** | GitHub Actions | Free for public repos, tight GitHub integration |
| **Styling** | TBD (CSS framework) | Warm, friendly design system |
| **Monitoring** | Google Analytics 4 | Free, comprehensive visitor insights |

---

## 7. Content Model

*For detailed content model, see `content-model-schema-20260118.md`*

**Key Content Types:**
1. **Blog Post** (`blogTemplate`) - Primary content type
2. **Profile** (`profile`) - Singleton for author info
3. **Card** (`componentCard`) - Reusable blog/project cards
4. **Carousel** (`componentCarousel`) - Blog carousel on homepage
5. **Hero Banner** (`heroBanner`) - Optional homepage hero
6. **SEO Metadata** (`seo`) - Search engine optimization
7. **Menu Item** (`mlMenuItem`) - Navigation links
8. **Header/Footer** (`orHeader`, `orFooter`) - Global components

**Localization:**
- Localized: Titles, descriptions, body text, CTA labels, SEO metadata
- Non-localized: Internal names, dates, asset references, URLs (except slugs)

---

## 8. Design Requirements

### 8.1 Design Principles

1. **Warm & Friendly**: Not corporate, approachable and human
2. **Content-First**: Typography and readability prioritized
3. **Clean & Simple**: No clutter, focus on content
4. **Professional**: Still appropriate for recruiters
5. **Accessible**: WCAG AA compliant, readable fonts

### 8.2 Visual Design

**Typography:**
- Headings: Serif or friendly sans-serif (e.g., Merriweather, Inter)
- Body: Highly readable (e.g., Georgia, System UI)
- Code: Monospace (e.g., Fira Code, JetBrains Mono)

**Color Palette:**
- Primary: Warm, inviting (e.g., soft blues, greens)
- Accent: Energetic but not aggressive
- Background: Light, airy (white or off-white)
- Text: High contrast for readability

**Components:**
- **Cards**: Rounded corners, subtle shadows
- **Buttons**: Clear CTAs, hover states
- **Images**: Rounded corners, optimized sizes
- **Navigation**: Sticky header, clear hierarchy

### 8.3 Responsive Design

**Breakpoints:**
- Mobile: < 768px (1 column)
- Tablet: 768-1024px (2 columns)
- Desktop: > 1024px (3 columns)

**Blog Carousel:**
- Mobile: 1 card visible, swipe to navigate
- Tablet: 2 cards visible
- Desktop: 3-4 cards visible

---

## 9. Development Phases

### Phase 1: Foundation (Week 1-2)
**Goal:** Basic blog-first site live with English content

**Deliverables:**
- [ ] Contentful space set up with all content types
- [ ] Python script fetches and transforms blog posts
- [ ] Jekyll site structure with homepage + blog posts
- [ ] Blog carousel displays on homepage
- [ ] Profile section renders correctly
- [ ] Basic styling (mobile-responsive)
- [ ] GitHub Actions workflow configured
- [ ] 3-5 initial blog posts published

**Definition of Done:**
- New blog post in Contentful appears on site within 5 minutes
- Homepage shows profile + blog carousel
- Blog posts readable and well-formatted
- Site loads in < 3 seconds

---

### Phase 2: Localization (Week 3)
**Goal:** Multi-language support operational

**Deliverables:**
- [ ] Contentful locales configured (en, es, etc.)
- [ ] Python script handles localized content
- [ ] Jekyll generates localized pages (`/en/`, `/es/`)
- [ ] Language switcher UI implemented
- [ ] Localized blog posts tested
- [ ] Language preference persistence (localStorage)

**Definition of Done:**
- Switching languages updates entire site
- Localized blog posts display correctly
- URLs reflect language (`/es/blog/mi-post/`)
- No broken links between languages

---

### Phase 3: Polish & SEO (Week 4)
**Goal:** Production-ready site optimized for search

**Deliverables:**
- [ ] SEO metadata on all pages
- [ ] Open Graph tags for social sharing
- [ ] XML sitemap generated
- [ ] Schema.org structured data
- [ ] Performance optimization (images, CSS)
- [ ] Accessibility audit and fixes
- [ ] Google Search Console setup
- [ ] Analytics integration

**Definition of Done:**
- Lighthouse scores: Performance > 85, SEO > 90, Accessibility > 90
- Social shares show correct preview
- Site indexed by Google
- No accessibility violations

---

### Phase 4: Future Enhancements (Month 2+)
**Optional features based on user feedback:**

- [ ] Projects portfolio section
- [ ] Publications/research papers section
- [ ] Dark mode toggle
- [ ] Search functionality (Algolia/Lunr.js)
- [ ] Comments system (Disqus/utterances)
- [ ] Newsletter subscription
- [ ] Related posts algorithm (ML-based)
- [ ] Content recommendations
- [ ] Reading progress indicator

---

## 10. Success Metrics & KPIs

### 10.1 Content Management Efficiency

| Metric | Current (al-folio) | Target (New System) |
|--------|-------------------|---------------------|
| Time to publish new post | 30+ minutes | < 5 minutes |
| Technical knowledge required | High (Git, Markdown, YAML) | None (CMS only) |
| Localization effort | Manual file duplication | Contentful UI |
| Update frequency | 1-2 posts/quarter | 1-2 posts/month |

---

### 10.2 Visitor Engagement

**Primary KPIs:**
- **Blog Post Views**: > 100 views/month (within 3 months)
- **Time on Site**: > 2 minutes average
- **Pages per Session**: > 2 pages
- **Bounce Rate**: < 60%
- **Returning Visitors**: > 20%

**Secondary KPIs:**
- Blog carousel click-through rate > 30%
- Profile CTA click rate > 10%
- Social link click rate > 5%

---

### 10.3 Technical Performance

| Metric | Target |
|--------|--------|
| Page Load Time (Desktop) | < 3 seconds |
| Page Load Time (Mobile) | < 5 seconds |
| Lighthouse Performance | > 85 |
| Lighthouse SEO | > 90 |
| Lighthouse Accessibility | > 90 |
| Build Time (GitHub Actions) | < 5 minutes |
| Uptime | > 99.5% |

---

### 10.4 SEO Performance (3-month targets)

- Google Search Console impressions: > 500/month
- Organic search clicks: > 50/month
- Average position: Top 30 for target keywords
- Indexed pages: 100% of published content

---

## 11. Risks & Mitigations

### 11.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Contentful API rate limits** | Low | Medium | Implement caching, optimize queries |
| **GitHub Actions build failures** | Medium | High | Error handling, notifications, fallback manual trigger |
| **Jekyll build time increases** | Medium | Medium | Incremental builds, pagination for large blogs |
| **Localization complexity** | Medium | Medium | Start with 2 languages, expand gradually |
| **Mobile performance** | Low | High | Image optimization, lazy loading, CDN |

### 11.2 Content Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Abandoned blog (no new posts)** | Medium | High | Set realistic publishing goals (1-2/month), not daily |
| **Inconsistent localization** | Medium | Medium | Fallback to English, clear translation workflow |
| **Poor content quality** | Low | High | Editorial guidelines, peer review optional |

### 11.3 User Experience Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Blog carousel ignored** | Medium | High | A/B test placement, eye-tracking studies, analytics monitoring |
| **Confusing navigation** | Low | Medium | User testing with 5-10 people, iterate based on feedback |
| **Mobile usability issues** | Low | High | Mobile-first design, test on real devices |

---

## 12. Dependencies & Assumptions

### 12.1 External Dependencies

- **Contentful**: Service availability and API stability
- **GitHub Pages**: Hosting reliability
- **GitHub Actions**: Build pipeline availability
- **Python libraries**: `contentful.py`, `PyYAML`, `Pillow` (for image processing)

### 12.2 Assumptions

1. **Content Volume**: < 100 blog posts in first year (realistic for GitHub Pages)
2. **Traffic**: < 10,000 visitors/month (within GitHub Pages limits)
3. **Languages**: Start with 2 (English + Spanish), expand if needed
4. **Image Sizes**: Editor uploads reasonably-sized images (< 5MB)
5. **Browser Support**: Modern evergreen browsers (Chrome, Firefox, Safari, Edge)

---

## 13. Acceptance Criteria (Launch Checklist)

### 13.1 Minimum Viable Product (MVP)

**Content Management:**
- [ ] Can publish new blog post in < 5 minutes
- [ ] All Contentful fields have help text
- [ ] Validations prevent common errors
- [ ] Preview before publish works

**Homepage:**
- [ ] Profile section displays name, photo, bio, socials
- [ ] Blog carousel shows latest 6-10 posts
- [ ] Cards are visually appealing and clickable
- [ ] Responsive on mobile, tablet, desktop

**Blog Posts:**
- [ ] Clean, readable typography
- [ ] Featured image displays correctly
- [ ] Rich text formatting works (headings, lists, links, images)
- [ ] Author and date display
- [ ] Category badge shows

**Navigation:**
- [ ] Header with logo and menu
- [ ] Footer with links and social icons
- [ ] "Back to Blog" link from post detail
- [ ] All internal links work

**Performance:**
- [ ] Page load < 3 seconds (desktop)
- [ ] Lighthouse Performance > 80
- [ ] Images optimized and lazy-loaded

**SEO:**
- [ ] Meta tags on all pages
- [ ] Open Graph tags for social sharing
- [ ] XML sitemap generated
- [ ] robots.txt present

**Deployment:**
- [ ] GitHub Actions workflow runs successfully
- [ ] Contentful webhook triggers rebuild
- [ ] Site deploys to GitHub Pages
- [ ] Custom domain configured (if applicable)

---

## 14. Out of Scope (For Initial Launch)

The following features are explicitly **not** included in the initial launch and may be considered for future phases:

- ❌ Dark mode toggle
- ❌ Search functionality
- ❌ Comments system
- ❌ Newsletter subscription
- ❌ Projects portfolio section
- ❌ Publications/research papers section
- ❌ User accounts or authentication
- ❌ E-commerce or payments
- ❌ Real-time features (WebSockets, live updates)
- ❌ Mobile app
- ❌ Advanced analytics dashboard

---

## 15. Glossary

- **Blog-First**: Design strategy where blog content is the primary focus and driver of site traffic
- **ISO 639-1**: International standard for language codes (e.g., `en`, `es`, `fr`)
- **Contentful**: Headless CMS platform for content management
- **Jekyll**: Ruby-based static site generator
- **GitHub Pages**: Free static site hosting by GitHub
- **GitHub Actions**: CI/CD automation platform
- **Atomic Design**: Design methodology organizing UI into atoms, molecules, organisms, templates
- **Localization**: Adapting content for different languages and regions
- **Frontmatter**: YAML metadata at the top of Markdown files

---

## 16. Appendices

### Appendix A: Related Documents
- `technical-specification-20260118.md` - Detailed technical implementation
- `content-model-schema-20260118.md` - Complete Contentful schema
- `integration-architecture-20260118.md` - Python-Jekyll integration details
- `homepage-structure-specification.md` - Homepage layout specification
- `brainstorming-summary-20260118.md` - Initial brainstorming session notes

### Appendix B: Reference Links
- Contentful Content Modeling Patterns: https://www.contentful.com/help/content-models/content-modeling-patterns/
- Jekyll Documentation: https://jekyllrb.com/docs/
- GitHub Pages Documentation: https://docs.github.com/pages
- ISO 639-1 Language Codes: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

---

**Document Status:** Active  
**Next Review Date:** 2026-02-18  
**Maintained By:** Simon Salazar  
**Contact:** [Contact information]

---

*This PRD is a living document and will be updated as the project evolves.*
