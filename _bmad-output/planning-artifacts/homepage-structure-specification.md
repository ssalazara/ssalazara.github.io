# Homepage Structure Specification
**Project:** github-page Portfolio  
**Purpose:** Detailed specification for blog-first homepage layout  
**Date:** 2026-01-18  
**Status:** Design Ready

---

## 1. Overview

This document specifies the homepage structure for the github-page portfolio, implementing a **blog-first strategy** where blog content is the primary driver of visitor engagement. The homepage serves as a warm, friendly introduction to the author while immediately showcasing their latest blog entries.

### 1.1 Design Philosophy

**Core Principles:**
- **Blog entries are the hero** - Featured prominently, not buried
- **Warm & friendly** - Approachable, personal, kind tone
- **Efficient navigation** - Visitors reach blog content in < 10 seconds
- **Mobile-first** - Optimized for all device sizes
- **Performance** - Fast load times (< 3 seconds)

**Target Audience Experience:**
- **Fellows/Researchers:** Discover thought leadership and technical insights immediately
- **Recruiters:** See communication skills and expertise through blog content
- **General Visitors:** Engage with valuable content right away

---

## 2. Homepage Layout Structure

### 2.1 Visual Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                        HEADER                                │
│  Logo  |  Blog  •  About  •  Contact     [Language] [🌐]   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   HERO BANNER (Optional)                     │
│                                                              │
│         "Welcome to My Digital Space"                        │
│         Brief welcoming message (1-2 sentences)              │
│                                                              │
│         [  Explore My Writing  ]  (CTA Button)               │
│                                                              │
│         Background: Warm, friendly image                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     PROFILE SECTION                          │
│  ┌──────────┐                                               │
│  │          │  Simon Salazar                                │
│  │  Photo   │  Researcher & Developer                       │
│  │          │                                               │
│  └──────────┘  I'm passionate about [topic]. I write about │
│                [themes] and share insights on [areas].      │
│                                                              │
│                🔗 LinkedIn  •  GitHub  •  Twitter           │
│                                                              │
│                [  View Full Bio  ]  (CTA Button)            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  🎯 BLOG CAROUSEL (HERO)                     │
│                   Latest Blog Posts                          │
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │ [Image] │  │ [Image] │  │ [Image] │  │ [Image] │       │
│  │         │  │         │  │         │  │         │       │
│  │  Title  │  │  Title  │  │  Title  │  │  Title  │       │
│  │         │  │         │  │         │  │         │       │
│  │ Summary │  │ Summary │  │ Summary │  │ Summary │       │
│  │         │  │         │  │         │  │         │       │
│  │Tech • 3m│  │Life • 5m│  │Tech • 7m│  │Biz  • 4m│       │
│  │         │  │         │  │         │  │         │       │
│  │[ReadMore]  │[ReadMore]  │[ReadMore]  │[ReadMore]       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                              │
│                  [  View All Blog Posts  ]                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              OPTIONAL ADDITIONAL SECTIONS                    │
│  - Featured Projects (future phase)                         │
│  - Recent Publications (future phase)                       │
│  - Testimonials/Quotes                                      │
│  - Newsletter Signup                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        FOOTER                                │
│  About • Privacy • Contact                                   │
│  © 2026 Simon Salazar • Built with Contentful & Jekyll     │
│  🔗 LinkedIn  •  GitHub  •  Twitter  •  Email               │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Section Specifications

### 3.1 Header (Global Navigation)

**Content Source:** Contentful `orHeader`

**Elements:**
- **Logo/Brand:** Left-aligned, links to homepage
- **Main Navigation:** Center or right-aligned
  - Blog (primary link)
  - About
  - Contact
  - (Future: Projects, Publications)
- **Utility Controls:** Right-aligned
  - Language switcher (EN / ES)
  - (Future: Dark mode toggle, Search icon)

**Responsive Behavior:**
- **Desktop (>1024px):** Full horizontal menu
- **Tablet (768-1024px):** Condensed menu
- **Mobile (<768px):** Hamburger menu

**Technical Implementation:**
```liquid
<!-- _includes/header.html -->
{% assign nav_data = site.data.navigation %}
<header class="site-header">
  <div class="container">
    <a href="/{{ page.lang }}/" class="logo">
      <img src="{{ nav_data.logo }}" alt="Simon Salazar">
    </a>
    
    <nav class="main-nav">
      {% for item in nav_data.menu_items %}
        <a href="{{ item.url }}" class="nav-link">
          {{ item.label[page.lang] }}
        </a>
      {% endfor %}
    </nav>
    
    {% include language-switcher.html %}
  </div>
</header>
```

---

### 3.2 Hero Banner (Optional, Warm Welcome)

**Content Source:** Contentful `heroBanner` (optional on homepage)

**Purpose:** Set a warm, inviting tone immediately

**Elements:**
- **Background Image:** Full-width, warm/friendly aesthetic
- **Headline:** 1-2 sentence welcome message (localized)
  - Example (EN): "Welcome to My Digital Space"
  - Example (ES): "Bienvenido a Mi Espacio Digital"
- **Subheading:** Brief context (optional, max 250 chars)
  - Example: "Exploring technology, research, and personal growth"
- **CTA Button:** Soft call-to-action (localized)
  - Example: "Explore My Writing" → Scrolls to blog carousel
  - Example: "Learn More" → Links to About page

**Design Guidelines:**
- **Height:** 50vh (half-screen) on desktop, 40vh on mobile
- **Overlay:** Semi-transparent overlay for text readability
- **Typography:** Large, friendly font (48-60px headline, 18-20px subheading)
- **Colors:** Warm tones (soft blues, greens, earth tones)

**Optional:** This section can be omitted for a more minimal design, jumping straight to Profile Section.

---

### 3.3 Profile Section (About the Author)

**Content Source:** Contentful `profile`

**Purpose:** Introduce the author before showcasing their work

**Elements:**
- **Profile Photo:** 
  - Circular or rounded square
  - 200-300px diameter
  - High-quality, friendly, approachable
  - Left-aligned or centered (mobile)
  
- **Name:** Full name (e.g., "Simon Salazar")
  - Font size: 32-36px
  - Bold, readable
  
- **Title/Tagline:** Professional title (localized)
  - Font size: 18-20px
  - Example (EN): "Researcher & Developer"
  - Example (ES): "Investigador y Desarrollador"
  
- **Bio Summary:** 2-4 sentences (localized, max 500 chars)
  - Warm, friendly tone
  - Mentions key interests/expertise
  - Provides context for blog content
  - Example: "I'm a researcher passionate about making technology accessible. I write about [topics] and share insights from my work in [field]."
  
- **Social Links:** Icon row
  - LinkedIn, GitHub, Twitter, Email, etc.
  - Max 8 links
  - Icons only or icon + label
  - Open in new tab
  
- **CTA Button:** Optional (localized)
  - Example: "View Full Bio" → Links to About page
  - Example: "Download CV" → Links to resume PDF

**Layout:**
- **Desktop:** Two-column (photo left, text right) or centered
- **Tablet:** Two-column or stacked
- **Mobile:** Stacked (photo top, text below)

**Design Guidelines:**
- **Background:** Subtle, light background (slightly different from page bg)
- **Spacing:** Generous padding (60-80px vertical)
- **Width:** Max 1000px content width, centered

**Technical Implementation:**
```liquid
<!-- _includes/profile-section.html -->
{% assign profile = site.data['profile-' | append: page.lang] %}
<section class="profile-section">
  <div class="container">
    <div class="profile-content">
      <img src="{{ profile.profileImage }}" alt="{{ profile.fullName }}" class="profile-photo">
      
      <div class="profile-text">
        <h2>{{ profile.fullName }}</h2>
        <p class="profile-title">{{ profile.title }}</p>
        <p class="profile-bio">{{ profile.bio }}</p>
        
        <div class="social-links">
          {% for link in profile.socialLinks %}
            <a href="{{ link.url }}" target="_blank" rel="noopener" class="social-link">
              <i class="icon-{{ link.icon }}"></i>
              <span>{{ link.platform }}</span>
            </a>
          {% endfor %}
        </div>
        
        {% if profile.ctaLabel %}
          <a href="{{ profile.ctaUrl }}" class="btn btn-primary">
            {{ profile.ctaLabel }}
          </a>
        {% endif %}
      </div>
    </div>
  </div>
</section>
```

---

### 3.4 Blog Carousel (THE HERO ELEMENT) 🎯

**Content Source:** Auto-generated from latest blog posts (`_data/blog-carousel-{locale}.yml`)

**Purpose:** Drive visitors to blog content immediately

**Elements:**
- **Section Heading:** Clear, prominent (localized)
  - Example (EN): "Latest Blog Posts"
  - Example (ES): "Últimas Entradas del Blog"
  - Font size: 36-42px
  - Center or left-aligned
  
- **Blog Cards:** 6-10 latest posts displayed as cards
  - Each card contains:
    - **Featured Image:** Top of card, consistent aspect ratio (16:9 or 4:3)
    - **Title:** Blog post title (max 60 chars, truncated with ellipsis)
    - **Summary:** Brief description (max 120-150 chars, truncated)
    - **Metadata:** Category badge + estimated reading time
    - **CTA Button:** "Read More" (localized)
  
- **Navigation:** 
  - Arrow buttons (prev/next) on desktop
  - Swipe gestures on mobile/tablet
  - Dots indicator (current position)
  
- **View All Link:** Below carousel
  - "View All Blog Posts" → Links to `/blog/` archive page

**Card Design:**
- **Shadow:** Subtle box-shadow for depth
- **Hover Effect:** Slight lift and shadow increase
- **Border Radius:** Rounded corners (8-12px)
- **Background:** White or light card background
- **Spacing:** 20-30px gap between cards

**Responsive Grid:**
- **Desktop (>1024px):** 3-4 cards visible
- **Tablet (768-1024px):** 2 cards visible
- **Mobile (<768px):** 1 card visible, swipe to navigate

**Performance:**
- **Lazy Loading:** Images load only when card enters viewport
- **Smooth Animations:** CSS transitions for hover/scroll effects

**Technical Implementation:**
```liquid
<!-- _includes/blog-carousel.html -->
{% assign carousel = site.data['blog-carousel-' | append: page.lang] %}
<section class="blog-carousel">
  <div class="container">
    <h2 class="section-heading">{{ carousel.title }}</h2>
    
    <div class="carousel-container">
      {% for card in carousel.cards %}
        {% include card.html card=card %}
      {% endfor %}
    </div>
    
    <div class="carousel-controls">
      <button class="carousel-prev" aria-label="Previous">‹</button>
      <div class="carousel-dots"></div>
      <button class="carousel-next" aria-label="Next">›</button>
    </div>
    
    <div class="text-center">
      <a href="/{{ page.lang }}/blog/" class="btn btn-outline">
        {{ site.data.i18n.view_all_posts[page.lang] }}
      </a>
    </div>
  </div>
</section>
```

**Card Component:**
```liquid
<!-- _includes/card.html -->
<article class="blog-card">
  <a href="{{ card.url }}" class="card-link">
    <div class="card-image">
      <img src="{{ card.image }}" alt="{{ card.title }}" loading="lazy">
      <span class="card-category">{{ card.category }}</span>
    </div>
    
    <div class="card-content">
      <h3 class="card-title">{{ card.title | truncate: 60 }}</h3>
      <p class="card-description">{{ card.description | truncate: 120 }}</p>
      
      <div class="card-meta">
        <span class="card-date">{{ card.date | date: "%b %d, %Y" }}</span>
        <span class="card-reading-time">• 5 min read</span>
      </div>
      
      <span class="card-cta">
        {{ site.data.i18n.read_more[page.lang] }} →
      </span>
    </div>
  </a>
</article>
```

---

### 3.5 Optional Additional Sections

**Flexible Content Blocks** (from Contentful `pageTemplate.blocks`)

**Potential Sections (Future Phases):**
1. **Featured Projects:** Grid of 2-4 portfolio projects
2. **Recent Publications:** List of research papers/publications
3. **Testimonials/Quotes:** Social proof from colleagues/clients
4. **Newsletter Signup:** Email capture for blog updates
5. **Stats/Achievements:** Key numbers (publications, projects, etc.)

**Current Recommendation:** **Keep minimal for launch**. Focus on Profile + Blog Carousel. Add supporting sections based on user feedback and content availability.

---

### 3.6 Footer (Global)

**Content Source:** Contentful `orFooter`

**Elements:**
- **Footer Navigation:** Links to key pages
  - About, Privacy Policy, Contact, etc.
- **Copyright Notice:** "© 2026 Simon Salazar"
- **Site Credit:** "Built with Contentful & Jekyll" (optional)
- **Social Links:** Repeat of profile social links
- **Newsletter Signup:** (Future, optional)

**Design Guidelines:**
- **Background:** Dark or contrasting background color
- **Text:** Light text for contrast
- **Layout:** 3-column on desktop, stacked on mobile
- **Spacing:** 60-80px padding

---

## 4. Content Strategy

### 4.1 Homepage Content Priorities

**Priority Order:**
1. **Blog Carousel** (Primary CTA: Read blog posts)
2. **Profile Section** (Context: Who is the author?)
3. **Header Navigation** (Secondary CTAs: About, Contact)
4. **Hero Banner** (Tertiary, optional: Set tone/mood)

**Why Blog-First?**
- Blog posts demonstrate expertise better than static bios
- Fresh content encourages return visits
- Recruiters value writing/communication skills
- Fellows/researchers discover valuable insights immediately

### 4.2 Call-to-Action (CTA) Strategy

**Primary CTA:** "Read More" on blog cards (leads to blog posts)

**Secondary CTAs:**
- "View Full Bio" (profile section → about page)
- "View All Blog Posts" (below carousel → blog archive)
- Hero banner button (if present → scroll to carousel or about page)

**CTA Design:**
- **Primary:** Solid button, brand color, high contrast
- **Secondary:** Outline button, less prominent
- **Hover State:** Slight color shift, subtle animation

---

## 5. Responsive Design Specifications

### 5.1 Breakpoints

| Device | Width | Layout Changes |
|--------|-------|----------------|
| **Mobile** | < 768px | Stacked sections, 1 blog card visible, hamburger menu |
| **Tablet** | 768-1024px | 2-column profile, 2 blog cards visible, condensed menu |
| **Desktop** | > 1024px | Full layout, 3-4 blog cards visible, horizontal menu |
| **Large Desktop** | > 1440px | Max content width 1400px, centered |

### 5.2 Mobile-First Optimizations

**Touch Targets:**
- Minimum 44x44px for all interactive elements
- Adequate spacing between cards (20px minimum)

**Typography Scaling:**
- Mobile: 16px base font size
- Desktop: 18px base font size
- Headings scale proportionally

**Image Optimization:**
- Serve responsive images (srcset)
- Lazy loading for below-fold images
- WebP with JPEG fallback

**Performance:**
- Critical CSS inlined in `<head>`
- Minimal JavaScript (carousel only)
- Font loading optimized (font-display: swap)

---

## 6. Accessibility (WCAG 2.1 AA)

### 6.1 Requirements

**Semantic HTML:**
- Proper heading hierarchy (H1 → H2 → H3)
- `<nav>`, `<main>`, `<section>`, `<article>` landmarks
- ARIA labels for carousel controls

**Keyboard Navigation:**
- All interactive elements accessible via Tab
- Carousel navigation via arrow keys
- Skip to main content link

**Screen Reader Support:**
- Alt text for all images (required in Contentful)
- Descriptive link text (not "click here")
- ARIA-live regions for carousel updates

**Color Contrast:**
- Minimum 4.5:1 for body text
- Minimum 3:1 for large text (18px+)
- Test all color combinations

**Focus Indicators:**
- Visible focus outline on all interactive elements
- Never remove outline without custom replacement

---

## 7. Performance Targets

### 7.1 Lighthouse Scores (Target)

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Performance** | > 85 | Fast page load, good UX |
| **Accessibility** | > 90 | WCAG AA compliance |
| **Best Practices** | > 90 | Security, modern standards |
| **SEO** | > 90 | Discoverability |

### 7.2 Core Web Vitals

| Metric | Target | Strategy |
|--------|--------|----------|
| **LCP (Largest Contentful Paint)** | < 2.5s | Optimize blog card images, critical CSS |
| **FID (First Input Delay)** | < 100ms | Minimal JavaScript |
| **CLS (Cumulative Layout Shift)** | < 0.1 | Fixed image dimensions, no layout shifts |

### 7.3 Load Time Budget

- **Homepage HTML:** < 50 KB (gzipped)
- **CSS:** < 30 KB (gzipped)
- **JavaScript:** < 20 KB (gzipped, carousel only)
- **Images (above-fold):** < 200 KB total
- **Total Page Size:** < 500 KB (initial load)

---

## 8. Visual Design Guidelines

### 8.1 Color Palette (Suggested)

**Primary Colors:**
- **Brand Blue:** `#4A90E2` (links, primary buttons)
- **Accent Green:** `#7ED321` (success, highlights)
- **Warm Gray:** `#F5F5F7` (backgrounds)

**Neutral Colors:**
- **Text Black:** `#333333` (body text)
- **Text Gray:** `#666666` (metadata, secondary text)
- **Border Gray:** `#E0E0E0` (dividers, card borders)
- **White:** `#FFFFFF` (cards, sections)

**Category Badges:**
- Technology: Blue `#4A90E2`
- Lifestyle: Green `#7ED321`
- Business: Orange `#F5A623`
- Design: Purple `#9013FE`

### 8.2 Typography

**Font Families:**
- **Headings:** "Inter" or "Merriweather" (serif for warmth)
- **Body:** "System UI" stack or "Georgia" (readability)
- **Code:** "Fira Code" or "JetBrains Mono"

**Font Sizes:**
- H1 (Homepage Hero): 48-60px
- H2 (Section Headings): 36-42px
- H3 (Card Titles): 20-24px
- Body: 16-18px
- Small (Metadata): 14px

**Line Height:**
- Headings: 1.2
- Body: 1.6 (optimal readability)

### 8.3 Spacing System

**Base Unit:** 8px

**Common Spacing:**
- `xs`: 8px
- `sm`: 16px
- `md`: 24px
- `lg`: 32px
- `xl`: 48px
- `xxl`: 64px

**Section Padding:**
- Mobile: 32px vertical
- Desktop: 64-80px vertical

---

## 9. Content Guidelines (For Contentful Editors)

### 9.1 Profile Bio Writing Guidelines

**Length:** 2-4 sentences (300-500 chars)

**Structure:**
1. Who you are (name + role)
2. What you're passionate about
3. What you write about

**Tone:**
- Warm, friendly, approachable
- Professional but not stuffy
- First-person ("I am..." not "Simon is...")

**Example (Good):**
> "I'm a researcher and developer passionate about making technology accessible. I write about software development, research methodologies, and personal growth. My goal is to share insights that help others learn and grow."

**Example (Avoid):**
> "Simon Salazar is an experienced professional in the field of technology with expertise in various domains including software engineering, research, and development."

### 9.2 Blog Card Guidelines

**Title:** 
- Max 60 chars
- Clear, descriptive, engaging
- Avoid clickbait

**Summary:**
- Max 150 chars
- Complete sentence or compelling fragment
- Hook reader without spoiling content

**Featured Image:**
- Min 800x600px (1200x630 recommended)
- Relevant to post content
- High quality, not pixelated
- Avoid text-heavy images

**Category:**
- Choose one primary category
- Consistent across posts
- Helps visitors filter content

---

## 10. Success Metrics

### 10.1 User Engagement

**Primary Metrics:**
- **Blog Carousel CTR:** > 30% (visitors click blog card)
- **Time on Homepage:** > 30 seconds (sufficient to scan content)
- **Scroll Depth:** > 50% (reach blog carousel)
- **Bounce Rate:** < 60% (visitors explore further)

**Secondary Metrics:**
- **Profile CTA Click Rate:** > 10%
- **Social Link Click Rate:** > 5%
- **Return Visitor Rate:** > 20% (within 30 days)

### 10.2 Content Performance

**Blog Post Discovery:**
- % of visitors who land on homepage vs. direct blog post
- Average posts read per session
- Blog → About page flow (understanding author after reading)

**Device Breakdown:**
- Mobile vs. Desktop traffic
- Performance scores per device type

---

## 11. Implementation Checklist

### Phase 1: Core Structure
- [ ] Header with navigation and language switcher
- [ ] Profile section with bio and social links
- [ ] Blog carousel with latest 10 posts
- [ ] Footer with navigation and copyright
- [ ] Responsive design (mobile, tablet, desktop)

### Phase 2: Enhancement
- [ ] Hero banner (optional, warm welcome)
- [ ] Carousel navigation (arrows, dots, swipe)
- [ ] Smooth scroll animations
- [ ] Lazy loading for images
- [ ] Dark mode toggle (future)

### Phase 3: Optimization
- [ ] Performance audit (Lighthouse)
- [ ] Accessibility audit (WCAG AA)
- [ ] Cross-browser testing
- [ ] Real device testing (iOS, Android)
- [ ] Analytics integration

---

## Appendix: Wireframe ASCII Art

```
MOBILE (< 768px)
┌─────────────────┐
│  ☰  LOGO   🌐EN │
├─────────────────┤
│   HERO BANNER   │
│   (Optional)    │
├─────────────────┤
│   ┌─────────┐   │
│   │  Photo  │   │
│   └─────────┘   │
│  Name & Title   │
│  Bio (2-3 sent) │
│  🔗 Social      │
│  [ CTA Button ] │
├─────────────────┤
│ Latest Posts    │
│ ┌─────────────┐ │
│ │   [Image]   │ │
│ │   Title     │ │
│ │   Summary   │ │
│ │   [Read →]  │ │
│ └─────────────┘ │
│  (swipe for more)│
├─────────────────┤
│     FOOTER      │
└─────────────────┘

DESKTOP (> 1024px)
┌────────────────────────────────────────────┐
│  LOGO    Blog • About • Contact    EN 🌐  │
├────────────────────────────────────────────┤
│           HERO BANNER (Optional)           │
│         "Welcome to My Space"              │
│          [  Explore Writing  ]             │
├────────────────────────────────────────────┤
│  ┌────────┐  Name: Simon Salazar          │
│  │ Photo  │  Title: Researcher & Dev      │
│  │        │  Bio: 2-4 sentences about...  │
│  └────────┘  🔗 LinkedIn • GitHub         │
│              [  View Full Bio  ]           │
├────────────────────────────────────────────┤
│           Latest Blog Posts                │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  │
│  │Image │  │Image │  │Image │  │Image │  │
│  │Title │  │Title │  │Title │  │Title │  │
│  │Summ. │  │Summ. │  │Summ. │  │Summ. │  │
│  │[Read]│  │[Read]│  │[Read]│  │[Read]│  │
│  └──────┘  └──────┘  └──────┘  └──────┘  │
│       ‹  •••••  ›                          │
│       [  View All Blog Posts  ]            │
├────────────────────────────────────────────┤
│                   FOOTER                   │
│  About • Privacy • Contact                 │
│  © 2026 Simon Salazar                     │
└────────────────────────────────────────────┘
```

---

**Document Status:** Design Ready  
**Next Steps:** Visual design mockups, Jekyll template implementation  
**Maintained By:** Simon Salazar
