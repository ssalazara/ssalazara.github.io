---
stepsCompleted: []
inputDocuments: []
---

# UX Design Specification - GitHub Page

**Author:** simon.salazar
**Date:** January 20, 2026

---

## Executive Summary

This UX design specification transforms the GitHub Page from a blog-first experience to a **portfolio-first showcase** inspired by the clean, minimal aesthetic of the Netlify reference design. The new design prioritizes:

- **Personal branding** over content volume
- **Visual hierarchy** with generous whitespace
- **Project showcase** as the hero element
- **Skill visibility** through clear, scannable sections

**Design Philosophy:** "Less is more" - Every element serves a purpose, nothing distracts from Simon's professional story.

---

## 1. Design Goals & User Experience Vision

### Primary Goals

1. **Immediate Impact** - Visitor understands who Simon is within 3 seconds
2. **Professional Credibility** - Clean, modern design builds trust
3. **Project Discovery** - Featured work is prominently displayed
4. **Skill Recognition** - Core competencies are immediately visible
5. **Action-Oriented** - Clear CTAs guide visitors to next steps

### Target Audience

- **Hiring Managers** (40%) - Evaluating technical skills and project experience
- **Potential Clients** (30%) - Looking for freelance/contract expertise
- **Fellow Developers** (20%) - Networking and collaboration
- **Recruiters** (10%) - Scanning for keywords and experience

### User Journey

```
1. Land on homepage
   ↓
2. See "Hello, World!" hero (WHO is this person?)
   ↓
3. Scan Core Skills section (WHAT can they do?)
   ↓
4. Review Featured Projects (HOW have they applied their skills?)
   ↓
5. Click project link or navigate to About/Contact
```

**Critical Success Metrics:**
- Time to understand value proposition: **< 5 seconds**
- Scroll depth to projects section: **> 80%**
- Project card click-through rate: **> 15%**

---

## 2. Visual Design System

### Design Principles

1. **Minimalist Sophistication**
   - Clean, uncluttered layouts
   - Strategic use of whitespace (60/40 content-to-space ratio)
   - Typography-driven hierarchy

2. **Professional Blue & Gray Palette**
   - Primary: Cool, trustworthy blue (#0ea5e9)
   - Neutrals: Sophisticated gray scale
   - Accents: Vibrant for CTAs and highlights

3. **Responsive-First**
   - Mobile-optimized from the start
   - Fluid typography and spacing
   - Touch-friendly interactions (44px minimum)

4. **Accessibility by Default**
   - WCAG 2.1 AA compliance
   - Color contrast ratios > 4.5:1
   - Keyboard navigation support

### Color Palette (Aligned with Design System)

**Primary Colors:**
- `primary-500`: #0ea5e9 (Brand blue, CTAs, links)
- `primary-600`: #0284c7 (Hover states)
- `primary-50`: #f0f9ff (Subtle backgrounds)

**Neutral Colors:**
- `neutral-0`: #ffffff (Page background)
- `neutral-50`: #fafafa (Section backgrounds)
- `neutral-100`: #f5f5f5 (Card backgrounds)
- `neutral-600`: #525252 (Body text)
- `neutral-900`: #171717 (Headings)

**Semantic Colors:**
- Success: #22c55e
- Info: #3b82f6
- Subtle borders: #e5e5e5

### Typography Scale

**Font Families:**
- **Headings:** Merriweather (serif, editorial)
- **UI/Body:** Inter (sans-serif, clean)
- **Code:** JetBrains Mono (monospace)

**Key Sizes:**
- Hero Title: 48-72px (clamp, responsive)
- Section Headings: 30-36px
- Body Text: 16-18px
- Small Text: 14px

**Hierarchy:**
- H1: Hero statement only
- H2: Section titles
- H3: Card titles
- Body: 16px, line-height 1.625

---

## 3. Layout Architecture

### Homepage Structure (New Portfolio-First Design)

```
┌─────────────────────────────────────┐
│         NAVIGATION HEADER           │
│   Logo | About | Projects | Blog    │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         HERO SECTION                │
│                                     │
│   Hello, World!                     │
│   Personal website intended as      │
│   a learning project.               │
│                                     │
│   [Decorative Image - Jellyfish]    │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│      CORE SKILLS SECTION            │
│                                     │
│       Core Skills (centered)        │
│                                     │
│   [Problem Solving] [Content        │
│    Strategy] [Data Science]         │
│          [Headless CMS]             │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│    FEATURED PROJECTS SECTION        │
│                                     │
│      Featured Projects (centered)   │
│                                     │
│  ┌─────────────┐  ┌──────────────┐ │
│  │  Project 1  │  │  Project 2   │ │
│  │  Image      │  │  Image       │ │
│  │  Title      │  │  Title       │ │
│  │  Desc       │  │  Desc        │ │
│  │  [View →]   │  │  [View →]    │ │
│  └─────────────┘  └──────────────┘ │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│           FOOTER                    │
│   © 2025 Simon Salazar              │
└─────────────────────────────────────┘
```

### Responsive Breakpoints

- **Mobile** (< 640px): Single column, stacked
- **Tablet** (640-1024px): 2-column projects grid
- **Desktop** (> 1024px): 2-column projects grid, wider spacing

### Spacing System (8px Grid)

- **Page margins:** 16px (mobile) → 32px (tablet) → 64px (desktop)
- **Section padding:** 48px (mobile) → 80px (desktop)
- **Component gaps:** 24px cards, 16px between elements
- **Container max-width:** 1200px

---

## 4. Component Specifications

### Component 1: Hero Section

**Purpose:** Immediate introduction, sets tone

**Layout:**
- Centered content (max-width: 640px)
- Vertical stack: Title → Subtitle → Image
- Large padding: 80px (mobile) → 120px (desktop)

**Elements:**
1. **Main Heading** ("Hello, World!")
   - Font: 48px (mobile) → 72px (desktop)
   - Weight: 700 (bold)
   - Color: neutral-900
   - Center-aligned

2. **Subtitle** ("Personal website intended as a learning project.")
   - Font: 18px (mobile) → 20px (desktop)
   - Color: neutral-600
   - Center-aligned
   - Margin-top: 16px

3. **Decorative Image**
   - Rounded corners (12px)
   - Max-width: 420px
   - Aspect ratio: 16:9 or organic
   - Margin-top: 48px
   - Box shadow: medium elevation

**Interactions:**
- Image: Subtle hover scale (1.02x)
- No CTA buttons (keep it clean)

**Accessibility:**
- Semantic H1 for heading
- Alt text for image
- Sufficient color contrast

---

### Component 2: Core Skills Section

**Purpose:** Quick scan of capabilities

**Layout:**
- Centered content (max-width: 800px)
- Vertical stack: Heading → Pill Grid
- Padding: 64px (mobile) → 96px (desktop)
- Background: neutral-50 (subtle contrast)

**Elements:**
1. **Section Heading** ("Core Skills")
   - Font: 30px (mobile) → 36px (desktop)
   - Weight: 700
   - Color: neutral-900
   - Center-aligned
   - Margin-bottom: 32px

2. **Skill Pills** (Horizontal centered flex)
   - Display: Flex wrap, centered
   - Gap: 16px between pills
   - Pills: Rounded (full radius), padding 12px 24px
   - Background: white or neutral-100
   - Border: 1px solid neutral-200
   - Font: 16px, medium weight
   - Color: neutral-700

**Skill List:**
- Problem Solving
- Content Strategy
- Data Science
- Headless CMS

**Interactions:**
- Hover: Background → primary-50, Border → primary-500
- Transition: 150ms ease

**Accessibility:**
- Semantic list markup
- Keyboard focusable
- Proper color contrast

---

### Component 3: Featured Projects Section

**Purpose:** Showcase 2-3 key projects

**Layout:**
- Centered content (max-width: 1200px)
- Vertical stack: Heading → 2-column grid
- Padding: 64px (mobile) → 96px (desktop)
- Background: white

**Elements:**
1. **Section Heading** ("Featured Projects")
   - Font: 30px (mobile) → 36px (desktop)
   - Weight: 700
   - Color: neutral-900
   - Center-aligned
   - Margin-bottom: 48px

2. **Project Cards** (2-column grid)
   - Grid: 1 col (mobile) → 2 cols (desktop)
   - Gap: 32px
   - Card structure:
     - Image (aspect-ratio 16:9, rounded corners)
     - Title (H3, 20px, bold)
     - Description (16px, 3 lines max)
     - CTA link ("View Project →")

**Project Card Anatomy:**
```
┌─────────────────────────────┐
│                             │
│     Project Image           │
│     (16:9 ratio)            │
│                             │
├─────────────────────────────┤
│  Project Title (H3)         │
│                             │
│  Short description text     │
│  that explains the project  │
│  in 2-3 lines maximum.      │
│                             │
│  [View Project →]           │
└─────────────────────────────┘
```

**Card Styling:**
- Background: white
- Border: 1px solid neutral-200
- Border-radius: 12px
- Padding: 24px (content area)
- Box shadow: Small elevation
- Hover: Lift effect (translateY -4px, shadow-md)

**Interactions:**
- Card hover: Elevation increase, slight lift
- CTA link: Color change to primary-600
- Smooth transitions: 200ms ease-out

**Accessibility:**
- Semantic article/card markup
- Descriptive alt text for images
- Keyboard accessible
- Focus indicators on CTAs

---

### Component 4: Navigation Header (Updated)

**Purpose:** Site-wide navigation

**Layout:**
- Horizontal flex layout
- Max-width: 1200px, centered
- Padding: 16px 24px
- Sticky position (optional)

**Elements:**
1. **Logo/Brand** (Left)
   - Text: "SSA" or "Simon Salazar"
   - Font: 20px, bold
   - Color: neutral-900

2. **Navigation Links** (Right)
   - Links: About | Projects | Contact
   - Font: 16px, medium weight
   - Color: neutral-700
   - Hover: Color → primary-600
   - Gap: 32px between links

**Mobile Behavior:**
- Hamburger menu (< 768px)
- Full-screen overlay menu

**Accessibility:**
- Semantic nav element
- Skip to content link
- Keyboard navigation

---

### Component 5: Footer (Simplified)

**Purpose:** Copyright and minimal links

**Layout:**
- Centered content
- Single row: Copyright text
- Padding: 32px
- Background: neutral-900 or white

**Elements:**
- Copyright: "© 2025 Simon Salazar. All rights reserved."
- Font: 14px
- Color: neutral-500
- Center-aligned

**Optional:**
- Social icons (LinkedIn, GitHub, Twitter)
- Small, monochrome
- Horizontal centered row

---

## 5. Interaction Design

### Hover States

**Links & Buttons:**
- Color shift: neutral → primary-600
- Transition: 150ms ease-out

**Cards:**
- Elevation increase: shadow-sm → shadow-md
- Lift: translateY(-4px)
- Transition: 200ms ease-out

**Skill Pills:**
- Background: white → primary-50
- Border: neutral-200 → primary-500

### Focus States (Keyboard Navigation)

- All interactive elements: 3px solid outline, primary-500
- Offset: 2px
- Visible on keyboard focus only (not mouse click)

### Loading States

- Skeleton screens for images
- Fade-in animation for content (300ms)

### Scroll Behavior

- Smooth scroll for anchor links
- Subtle parallax for hero image (optional)

---

## 6. Content Strategy

### Hero Section

**Heading:** "Hello, World!"
- **Why:** Developer-friendly, welcoming, playful
- **Tone:** Approachable, technical

**Subtitle:** "Personal website intended as a learning project."
- **Why:** Honest, relatable, shows growth mindset
- **Tone:** Humble, transparent

### Core Skills

**Selection Criteria:**
- Top 4 most marketable skills
- Broad enough to attract diverse opportunities
- Specific enough to demonstrate expertise

**Recommended Skills:**
1. Problem Solving (universal appeal)
2. Content Strategy (shows product thinking)
3. Data Science (technical depth)
4. Headless CMS (modern tech stack)

### Featured Projects

**Selection Criteria:**
- 2 projects maximum (quality over quantity)
- Mix of technical depth + business impact
- Recent work (within 2 years)
- Completed projects with live demos

**Project 1: My Personal Profile**
- **Title:** "My Personal Profile"
- **Description:** "Self-taught project based on using a free tech-stack for a personal website. In short: Astro + Sanity + Netlify"
- **Image:** Screenshot or abstract tech visual
- **CTA:** "View Project" → links to live site

**Project 2: Rosetta Bridge**
- **Title:** "Rosetta Bridge"
- **Description:** "Part of the winning team at the Apply Digital hackathon in July 2025. Rosetta Bridge is an agent-based solution that utilizes a JSON object to generate user-friendly documentation."
- **Image:** Hackathon visual or product screenshot
- **CTA:** "View Project" → links to repo or demo

---

## 7. Responsive Design

### Mobile (< 640px)

**Hero:**
- Title: 36px
- Image: Full width
- Padding: 48px 16px

**Skills:**
- Pills: Stack vertically or wrap
- Padding: 48px 16px

**Projects:**
- Single column
- Cards: Full width
- Padding: 48px 16px

### Tablet (640-1024px)

**Hero:**
- Title: 56px
- Image: Max 420px
- Padding: 64px 32px

**Skills:**
- Pills: Horizontal wrap, centered
- Padding: 64px 32px

**Projects:**
- 2-column grid
- Cards: Equal width
- Padding: 64px 32px

### Desktop (> 1024px)

**Hero:**
- Title: 72px
- Image: Max 420px
- Padding: 120px 64px

**Skills:**
- Pills: Horizontal centered
- Padding: 96px 64px

**Projects:**
- 2-column grid
- Cards: Max 540px each
- Padding: 96px 64px

---

## 8. Accessibility Requirements

### WCAG 2.1 AA Compliance

**Color Contrast:**
- Body text: 4.5:1 minimum (neutral-600 on white = 7.9:1 ✓)
- Headings: 4.5:1 minimum (neutral-900 on white = 15:1 ✓)
- Links: 4.5:1 + underline or bold

**Focus Indicators:**
- Visible on all interactive elements
- 3px solid outline, primary-500
- Never remove focus styles

**Touch Targets:**
- Minimum 44×44px for all interactive elements
- Adequate spacing between clickable items

**Semantic HTML:**
- Proper heading hierarchy (H1 → H2 → H3)
- Landmark regions (header, main, footer, nav, section)
- ARIA labels for icon-only buttons

**Keyboard Navigation:**
- All interactive elements focusable via Tab
- Logical tab order
- Skip to content link
- Escape key closes mobile menu

**Screen Reader Support:**
- Alt text for all images
- ARIA labels where needed
- Descriptive link text (no "click here")

**Motion Preferences:**
- Respect prefers-reduced-motion
- Disable animations for users who prefer it

---

## 9. Performance Considerations

### Image Optimization

- **Hero image:** WebP format, < 200KB
- **Project images:** WebP format, < 150KB each
- **Lazy loading:** For below-fold images
- **Responsive images:** Serve appropriate sizes

### CSS Strategy

- **Critical CSS:** Inline above-the-fold styles
- **CSS bundle:** < 50KB (gzipped)
- **No unused CSS:** Purge during build

### JavaScript

- **Minimal JS:** Only for mobile menu toggle
- **Vanilla JS:** No heavy frameworks needed
- **Defer non-critical scripts**

### Font Loading

- **System fonts fallback:** Arial, Helvetica, sans-serif
- **Web fonts:** Subset, woff2 format
- **Font-display:** swap

### Performance Targets

- **Lighthouse Performance:** > 90
- **First Contentful Paint:** < 1.5s
- **Largest Contentful Paint:** < 2.5s
- **Total Blocking Time:** < 200ms
- **Cumulative Layout Shift:** < 0.1

---

## 10. Implementation Roadmap

### Phase 1: Storybook Components ✅ (Current Phase)

**Deliverables:**
- Hero section story
- Core skills story  
- Featured projects story
- Updated navigation story

**Timeline:** 2-4 hours

---

### Phase 2: SCSS Implementation

**Deliverables:**
- `_sass/components/_hero-section.scss`
- `_sass/components/_core-skills.scss`
- `_sass/components/_featured-projects.scss`
- Update `_sass/pages/_home-page.scss`

**Timeline:** 2-3 hours

---

### Phase 3: Jekyll Layouts

**Deliverables:**
- `_includes/components/hero-section.html`
- `_includes/components/core-skills.html`
- `_includes/components/featured-projects.html`
- Update `_layouts/home-page.html`

**Timeline:** 2-3 hours

---

### Phase 4: Content Integration

**Deliverables:**
- Update `_data/homepage-en.yml`
- Update `_data/homepage-es.yml`
- Add project data structures
- Add skill lists

**Timeline:** 1-2 hours

---

### Phase 5: Testing & QA

**Deliverables:**
- Cross-browser testing (Chrome, Safari, Firefox)
- Responsive testing (mobile, tablet, desktop)
- Accessibility audit (WAVE, axe)
- Performance testing (Lighthouse)
- Keyboard navigation testing

**Timeline:** 2-3 hours

---

## 11. Success Metrics

### User Experience Metrics

- **Bounce rate:** < 40% (homepage)
- **Average time on page:** > 45 seconds
- **Scroll depth:** > 80% reach projects section
- **Click-through rate:** > 15% on project CTAs

### Technical Metrics

- **Lighthouse Performance:** > 90
- **Lighthouse Accessibility:** > 95
- **Lighthouse SEO:** > 90
- **Core Web Vitals:** All "Good" ratings

### Design Quality Metrics

- **Whitespace ratio:** 60/40 (space to content)
- **Color contrast:** All text > 4.5:1
- **Touch targets:** All interactive elements > 44px
- **Font size:** No text < 14px

---

## 12. Design Rationale

### Why Portfolio-First Over Blog-First?

**Blog-First (Previous):**
- ❌ Buries personal brand under content
- ❌ Assumes visitor wants to read immediately
- ❌ Complex navigation and cognitive load
- ❌ Doesn't showcase technical skills visually

**Portfolio-First (New):**
- ✅ Immediate personal connection
- ✅ Skills and projects front and center
- ✅ Simple, scannable layout
- ✅ Professional, modern aesthetic
- ✅ Better conversion for hiring/networking goals

### Why "Hello, World!"?

- **Technical credibility:** Recognizable developer phrase
- **Welcoming tone:** Approachable, friendly
- **Memorable:** Stands out from typical portfolio intros
- **Conversation starter:** Invites curiosity

### Why Only 2 Featured Projects?

- **Quality over quantity:** Shows best work only
- **Reduces decision paralysis:** Visitor doesn't feel overwhelmed
- **Faster scanning:** Can evaluate both in < 30 seconds
- **Encourages deeper engagement:** Visitor more likely to click

### Why 4 Core Skills?

- **Cognitive load:** Human brain processes 3-4 items easily
- **Scannability:** Can read all in < 5 seconds
- **Specificity:** Each skill tells a story
- **Positioning:** Shows technical + strategic balance

---

## 13. Wireframes & Mockups

### Desktop Wireframe (1280px)

```
┌────────────────────────────────────────────────────────────┐
│  [Logo]                    [About] [Projects] [Contact]    │
└────────────────────────────────────────────────────────────┘

                    Hello, World!
                    
          Personal website intended as a
              learning project.
              
              [Decorative Image]
              


════════════════════════════════════════════════════════════

                    Core Skills
                    
    [Problem Solving] [Content Strategy]
    [Data Science] [Headless CMS]
    

════════════════════════════════════════════════════════════

                 Featured Projects
                 
┌──────────────────────┐    ┌──────────────────────┐
│                      │    │                      │
│   Project Image      │    │   Project Image      │
│                      │    │                      │
├──────────────────────┤    ├──────────────────────┤
│ My Personal Profile  │    │ Rosetta Bridge       │
│                      │    │                      │
│ Self-taught project  │    │ Winning hackathon    │
│ using free tech...   │    │ team solution...     │
│                      │    │                      │
│ [View Project →]     │    │ [View Project →]     │
└──────────────────────┘    └──────────────────────┘


════════════════════════════════════════════════════════════

          © 2025 Simon Salazar. All rights reserved.
```

### Mobile Wireframe (375px)

```
┌──────────────────────┐
│ [☰]        [Logo]    │
└──────────────────────┘

   Hello, World!
   
Personal website
intended as a
learning project.

  [Decorative Image]


══════════════════════

   Core Skills
   
[Problem Solving]
[Content Strategy]
[Data Science]
[Headless CMS]


══════════════════════

 Featured Projects
 
┌────────────────────┐
│                    │
│  Project Image     │
│                    │
├────────────────────┤
│ My Personal        │
│ Profile            │
│                    │
│ Self-taught        │
│ project using...   │
│                    │
│ [View Project →]   │
└────────────────────┘

┌────────────────────┐
│                    │
│  Project Image     │
│                    │
├────────────────────┤
│ Rosetta Bridge     │
│                    │
│ Winning hackathon  │
│ team solution...   │
│                    │
│ [View Project →]   │
└────────────────────┘


══════════════════════

© 2025 Simon Salazar
```

---

## 14. Design Handoff Checklist

### For Developers

- [x] Color palette documented (using design system tokens)
- [x] Typography scale defined (fluid responsive values)
- [x] Spacing system specified (8px grid)
- [x] Component specifications complete
- [x] Interaction states defined (hover, focus, active)
- [x] Responsive breakpoints documented
- [x] Accessibility requirements listed
- [x] Performance targets set

### For Content Editors

- [ ] Content structure defined
- [ ] Character limits specified
- [ ] Image specifications documented
- [ ] Alt text guidelines provided
- [ ] Localization strategy outlined

### For QA

- [ ] Browser support matrix
- [ ] Device testing list
- [ ] Accessibility checklist
- [ ] Performance benchmarks
- [ ] User flow test cases

---

## 15. Appendices

### A. Design System Alignment

This UX design fully leverages the existing design system documented in:
- `_bmad-output/DESIGN-SYSTEM-COMPLETE.md`
- `_bmad-output/DESIGN-SYSTEM-IMPLEMENTATION-COMPLETE.md`

**Reused Components:**
- Button system (primary, secondary, ghost)
- Card component (adapted for projects)
- Typography system (fluid scaling)
- Color palette (blue & gray)
- Spacing tokens (8px grid)

**New Components:**
- Hero section (unique to homepage)
- Core skills pills (new pattern)
- Featured projects grid (variant of existing cards)

### B. Content Model Changes

**New Data Structures Needed:**

`_data/homepage-en.yml`:
```yaml
hero:
  title: "Hello, World!"
  subtitle: "Personal website intended as a learning project."
  image_url: "https://images.ctfassets.net/..."
  
skills:
  - "Problem Solving"
  - "Content Strategy"
  - "Data Science"
  - "Headless CMS"
  
featured_projects:
  - title: "My Personal Profile"
    description: "Self-taught project based on using a free tech-stack for a personal website. In short: Astro + Sanity + Netlify"
    image_url: "https://images.ctfassets.net/..."
    link_url: "https://simonsalazar.netlify.app/"
    link_text: "View Project"
  - title: "Rosetta Bridge"
    description: "Part of the winning team at the Apply Digital hackathon in July 2025. Rosetta Bridge is an agent-based solution that utilizes a JSON object to generate user-friendly documentation."
    image_url: "https://images.ctfassets.net/..."
    link_url: "#"
    link_text: "View Project"
```

### C. References

**Design Inspiration:**
- Netlify Portfolio: https://simonsalazar.netlify.app/
- Minimal portfolio patterns
- Developer portfolio best practices

**Technical References:**
- Existing design system documentation
- WCAG 2.1 AA guidelines
- Core Web Vitals documentation

---

**Document Status:** ✅ Complete - Ready for Implementation  
**Last Updated:** January 20, 2026  
**Author:** Sally (UX Designer Agent)  
**Approved By:** Simon Salazar

---

**Next Steps:**
1. ✅ Create Storybook components
2. Implement SCSS stylesheets
3. Build Jekyll layouts
4. Integrate with content model
5. Test and iterate
