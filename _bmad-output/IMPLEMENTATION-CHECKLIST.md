# Implementation Checklist: UX & Content Model Optimization
**Project:** GitHub Pages Portfolio  
**Date Started:** _________  
**Developer:** _________  
**Estimated Total Time:** 36-50 hours

---

## 📋 Pre-Implementation

### Planning & Setup
- [ ] Review full proposal (`UX-CONTENT-MODEL-OPTIMIZATION-PROPOSAL.md`)
- [ ] Review executive summary (`PROPOSAL-EXECUTIVE-SUMMARY.md`)
- [ ] Get stakeholder approval (Product Owner, Tech Lead, Content Manager)
- [ ] Schedule 1-week sprint for Phase 1+2
- [ ] Backup Contentful space (export all content types)
- [ ] Create feature branch: `feature/content-model-optimization`
- [ ] Set up preview environment for testing

### Prerequisites
- [ ] Contentful CLI installed (`npm install -g contentful-cli`)
- [ ] Access to Contentful space (admin permissions)
- [ ] Local development environment running
- [ ] Storybook running (`npm run storybook`)
- [ ] Jekyll development server running

---

## 🚀 Phase 1: Field-Level Enhancements

**Goal:** Add design variants to existing components  
**Time Estimate:** 8-12 hours  
**Priority:** CRITICAL (must complete)

### Task 1.1: Update Hero Banner Schema
**File:** `contentful-schemas/hero-banner.json`

- [ ] Add `theme` field (Symbol with options: light, dark, gradient, primary)
- [ ] Add `spacing` field (Symbol with options: tight, normal, loose, none)
- [ ] Add `layout` field (Symbol with options: centered, split, minimal)
- [ ] Add `imagePosition` field (Symbol with options: background, inline, decorative)
- [ ] Add `enableParallax` field (Boolean, default: false)
- [ ] Update field help text for each new field
- [ ] Test schema validation in Contentful UI

**Validation:**
```bash
node scripts/validate-schema.js contentful-schemas/hero-banner.json
```

### Task 1.2: Update Projects Grid Schema
**File:** `contentful-schemas/component-projects-grid.json`

- [ ] Add `theme` field (Symbol with 6 options)
- [ ] Add `spacing` field (Symbol with 5 options)
- [ ] Add `columns` field (Integer, min: 1, max: 4, default: 2)
- [ ] Add `cardStyle` field (Symbol with options: elevated, bordered, flat, glass)
- [ ] Update help text
- [ ] Test in Contentful UI

### Task 1.3: Update Skills List Schema
**File:** `contentful-schemas/component-skills-list.json`

- [ ] Add `theme` field
- [ ] Add `spacing` field
- [ ] Add `style` field (Symbol with options: pills, cards, minimal, animated)
- [ ] Add `iconSet` field (Boolean, default: false)
- [ ] Update help text

### Task 1.4: Push Schema Updates to Contentful

- [ ] Run `./push-contentful-schemas.sh` in preview environment
- [ ] Verify all fields appear in Contentful UI
- [ ] Test creating/editing existing entries
- [ ] Check default values populate correctly

### Task 1.5: Update Storybook Stories

**Files to update:**
- `stories/components/Hero.stories.js`
- `stories/components/FeaturedProjects.stories.js`
- `stories/components/CoreSkills.stories.js`

**Hero.stories.js additions:**
- [ ] Add `DarkTheme` story
- [ ] Add `GradientTheme` story
- [ ] Add `SplitLayout` story
- [ ] Add `MinimalLayout` story
- [ ] Add `TightSpacing` story
- [ ] Add `LooseSpacing` story

**FeaturedProjects.stories.js additions:**
- [ ] Add `ThreeColumns` story
- [ ] Add `FourColumns` story
- [ ] Add `BorderedCards` story
- [ ] Add `GlassCards` story

**CoreSkills.stories.js additions:**
- [ ] Add `CardStyle` story
- [ ] Add `MinimalStyle` story
- [ ] Add `WithIcons` story

### Task 1.6: Update Frontend Templates

**Jekyll Liquid Templates to update:**

**`_includes/components/hero-banner.html`:**
- [ ] Add theme class logic: `{% if include.theme == 'dark' %}theme-dark{% endif %}`
- [ ] Add spacing class logic
- [ ] Add layout variant conditionals
- [ ] Add parallax initialization if `enableParallax == true`
- [ ] Test rendering with different variants

**`_includes/components/featured-projects.html`:**
- [ ] Add theme background classes
- [ ] Add spacing utility classes
- [ ] Implement grid column logic: `grid-cols-{{ include.columns }}`
- [ ] Add card style variants (elevated/bordered/flat/glass)

**`_includes/components/core-skills.html`:**
- [ ] Add theme classes
- [ ] Add spacing classes
- [ ] Implement style variants (pills/cards/minimal/animated)
- [ ] Add icon rendering logic (if `iconSet == true`)

### Task 1.7: Update SCSS Styling

**Files to create/update:**
- `_sass/components/_hero-banner.scss`
- `_sass/components/_featured-projects.scss`
- `_sass/components/_core-skills.scss`

**Add theme variant styles:**
```scss
.hero-banner {
  &.theme-light { background: $color-neutral-0; }
  &.theme-dark { background: $color-neutral-900; color: $color-neutral-0; }
  &.theme-gradient { background: linear-gradient(135deg, $color-primary-500, $color-primary-700); }
  &.theme-primary { background: $color-primary-50; }
}
```

**Add spacing utility classes:**
```scss
.spacing-tight { padding: $spacing-8 0; }
.spacing-normal { padding: $spacing-16 0; }
.spacing-loose { padding: $spacing-24 0; }
.spacing-none { padding: 0; }
```

- [ ] Implement all theme styles
- [ ] Implement all spacing utilities
- [ ] Add layout variants (split/centered/minimal)
- [ ] Add card style variants
- [ ] Test responsive behavior

### Task 1.8: Testing

- [ ] Test hero with all theme combinations
- [ ] Test hero with all layout combinations
- [ ] Test projects grid with 1/2/3/4 columns
- [ ] Test projects with all card styles
- [ ] Test skills with all display styles
- [ ] Mobile responsive testing (iPhone, iPad)
- [ ] Desktop testing (1280px, 1920px)
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Accessibility audit (WAVE, Lighthouse)

### Task 1.9: Create Test Content

**In Contentful:**
- [ ] Create "Hero - Dark Theme" test entry
- [ ] Create "Hero - Split Layout" test entry
- [ ] Create "Projects - 3 Columns" test entry
- [ ] Create "Skills - Card Style" test entry
- [ ] Create test page using all variants
- [ ] Verify preview mode rendering

### Task 1.10: Documentation

- [ ] Update `CONTENTFUL-BLOG-POST-GUIDE.md` with new fields
- [ ] Document theme options for editors
- [ ] Document spacing guidelines
- [ ] Add screenshots to docs
- [ ] Update Storybook documentation strings

---

## 🎯 Phase 2: New Content Types (Section + Button)

**Goal:** Add flexible layout container and standardized CTA  
**Time Estimate:** 16-20 hours  
**Priority:** HIGH (strongly recommended)

### Task 2.1: Create Section Container Content Type

**File:** `contentful-schemas/comp-section.json`

- [ ] Create new schema file with all fields (see proposal Part 3)
- [ ] Add `name` field (Symbol, required)
- [ ] Add `anchorId` field (Symbol, optional, regex validation)
- [ ] Add `theme` field (Symbol with 6 options)
- [ ] Add `spacing` field (Symbol with 5 options)
- [ ] Add `containerWidth` field (Symbol: full/wide/standard/narrow)
- [ ] Add `content` field (Array of Entry links)
- [ ] Add `enableDivider` field (Boolean)
- [ ] Set `linkContentType` validation on content array
- [ ] Add comprehensive help text for all fields

### Task 2.2: Create Button Component Content Type

**File:** `contentful-schemas/ui-button.json`

- [ ] Create new schema file
- [ ] Add `label` field (Symbol, required, localized, max 25 chars)
- [ ] Add `url` field (Symbol, required, regex validation)
- [ ] Add `variant` field (Symbol: primary/secondary/outline/ghost/link)
- [ ] Add `size` field (Symbol: small/medium/large)
- [ ] Add `icon` field (Symbol: none/arrow-right/external-link/download/chevron-right)
- [ ] Add `openInNewTab` field (Boolean)
- [ ] Add help text and examples

### Task 2.3: Update Homepage Schema

**File:** `contentful-schemas/homepage.json`

**Modify `blocks` field:**
- [ ] Add `compSection` to allowed content types array
- [ ] Update help text to mention Section containers
- [ ] Keep backward compatibility (existing types still work)

### Task 2.4: Refactor Hero Banner for Button Component

**File:** `contentful-schemas/hero-banner.json`

**Option A (Recommended - Non-Breaking):**
- [ ] Add new `cta` field (Link to Entry, linkContentType: uiButton)
- [ ] Mark `ctaLabel` and `ctaUrl` as deprecated (help text: "Use 'CTA' field instead")
- [ ] Keep old fields for backward compatibility

**Option B (Breaking Change):**
- [ ] Remove `ctaLabel` and `ctaUrl` fields
- [ ] Add `cta` field
- [ ] Migrate all existing hero entries

### Task 2.5: Push New Schemas to Contentful

```bash
# Preview environment
./push-contentful-schemas.sh --environment preview

# Verify in Contentful UI
# Create test entries for comp.Section and ui.Button

# Production deployment (after testing)
./push-contentful-schemas.sh --environment master
```

- [ ] Push to preview environment
- [ ] Test creating Section entries
- [ ] Test creating Button entries
- [ ] Test linking Button to Hero
- [ ] Push to production

### Task 2.6: Create Section Component Template

**New file:** `_includes/components/section.html`

```liquid
{% assign theme_class = include.theme | default: 'white' %}
{% assign spacing_class = include.spacing | default: 'normal' %}
{% assign width_class = include.containerWidth | default: 'standard' %}

<section 
  class="section theme-{{ theme_class }} spacing-{{ spacing_class }}"
  {% if include.anchorId %}id="{{ include.anchorId }}"{% endif %}
>
  <div class="container width-{{ width_class }}">
    {% for component in include.content %}
      <!-- Render component based on type -->
    {% endfor %}
  </div>
  
  {% if include.enableDivider %}
    <hr class="section-divider">
  {% endif %}
</section>
```

- [ ] Create template file
- [ ] Implement theme classes
- [ ] Implement spacing classes
- [ ] Implement container width logic
- [ ] Add component rendering loop
- [ ] Test with multiple content types

### Task 2.7: Create Button Component Template

**New file:** `_includes/components/button.html`

```liquid
{% assign variant = include.variant | default: 'primary' %}
{% assign size = include.size | default: 'medium' %}
{% assign icon = include.icon | default: 'none' %}

<a 
  href="{{ include.url }}" 
  class="btn btn-{{ variant }} btn-{{ size }}"
  {% if include.openInNewTab %}target="_blank" rel="noopener noreferrer"{% endif %}
>
  {{ include.label }}
  {% if icon != 'none' %}
    {% include icons/{{ icon }}.svg %}
  {% endif %}
</a>
```

- [ ] Create template file
- [ ] Implement all variant styles
- [ ] Implement all size options
- [ ] Add icon rendering
- [ ] Add accessibility attributes
- [ ] Test with all combinations

### Task 2.8: Create Button SCSS Styles

**New file:** `_sass/components/_button.scss`

```scss
.btn {
  // Base styles
  display: inline-flex;
  align-items: center;
  gap: $spacing-2;
  font-family: $font-family-base;
  font-weight: $font-weight-semibold;
  text-decoration: none;
  border-radius: $radius-lg;
  transition: $transition-colors;
  cursor: pointer;
  
  // Variants
  &.btn-primary {
    background: $color-primary-600;
    color: $color-neutral-0;
    &:hover { background: $color-primary-700; }
  }
  
  &.btn-secondary {
    background: $color-neutral-200;
    color: $color-neutral-900;
    &:hover { background: $color-neutral-300; }
  }
  
  &.btn-outline {
    background: transparent;
    border: 2px solid $color-primary-600;
    color: $color-primary-600;
    &:hover { background: $color-primary-50; }
  }
  
  &.btn-ghost {
    background: transparent;
    color: $color-primary-600;
    &:hover { background: $color-primary-50; }
  }
  
  &.btn-link {
    background: none;
    color: $color-primary-600;
    text-decoration: underline;
    &:hover { color: $color-primary-700; }
  }
  
  // Sizes
  &.btn-small {
    height: $button-height-sm;
    padding: 0 $button-padding-x-sm;
    font-size: $font-size-sm;
  }
  
  &.btn-medium {
    height: $button-height-md;
    padding: 0 $button-padding-x-md;
    font-size: $font-size-base;
  }
  
  &.btn-large {
    height: $button-height-lg;
    padding: 0 $button-padding-x-lg;
    font-size: $font-size-lg;
  }
}
```

- [ ] Create SCSS file
- [ ] Implement all variants
- [ ] Implement all sizes
- [ ] Add hover/focus states
- [ ] Add icon spacing
- [ ] Test all combinations
- [ ] Accessibility testing (focus rings, contrast)

### Task 2.9: Create Section SCSS Styles

**New file:** `_sass/components/_section.scss`

- [ ] Create base section styles
- [ ] Implement 6 theme variants
- [ ] Implement 5 spacing options
- [ ] Implement 4 container widths
- [ ] Add divider styles
- [ ] Test responsive behavior

### Task 2.10: Create Storybook Stories

**New file:** `stories/layout/Section.stories.js`

- [ ] Create Section component story
- [ ] Add "Light Background" variant
- [ ] Add "Dark Background" variant
- [ ] Add "Primary Background" variant
- [ ] Add "With Multiple Components" story
- [ ] Add "With Divider" story
- [ ] Add "Full Width" story
- [ ] Add "Narrow Width" story

**Update:** `stories/components/Button.stories.js`

- [ ] Add all 5 variant stories
- [ ] Add all 3 size stories
- [ ] Add icon combinations
- [ ] Add "Button Group" story
- [ ] Add responsive example

### Task 2.11: Update Hero to Use Button Component

**File:** `_includes/components/hero-banner.html`

- [ ] Check if `include.cta` exists (new field)
- [ ] If yes, render Button component
- [ ] If no, fall back to old `ctaLabel` + `ctaUrl` (backward compatibility)
- [ ] Test both paths

### Task 2.12: Testing Phase 2

**Section Container:**
- [ ] Create test page with 3 sections
- [ ] Test all theme combinations
- [ ] Test all spacing options
- [ ] Test all container widths
- [ ] Test nested components render correctly
- [ ] Test anchor links work
- [ ] Mobile responsive check

**Button Component:**
- [ ] Test all 5 variants render correctly
- [ ] Test all 3 sizes
- [ ] Test all icon options
- [ ] Test external links open in new tab
- [ ] Test hover states
- [ ] Test focus states (keyboard navigation)
- [ ] Accessibility audit (contrast ratios)

**Integration Testing:**
- [ ] Create homepage with Sections containing Buttons
- [ ] Create Hero with Button CTA
- [ ] Test existing content still renders
- [ ] Performance testing (Lighthouse score)

### Task 2.13: Content Migration (Optional)

**If choosing breaking change approach:**
- [ ] Export all Hero entries with CTAs
- [ ] Create Button entries for each CTA
- [ ] Update Hero entries to reference Buttons
- [ ] Delete old CTA fields
- [ ] Verify all pages still work

### Task 2.14: Documentation Updates

- [ ] Document Section Container usage for editors
- [ ] Document Button component variants
- [ ] Add visual examples to docs
- [ ] Update `CONTENTFUL-AUTHORING-GUIDE.md`
- [ ] Create video tutorial (optional)

---

## 🔧 Phase 3: Global Settings (Optional)

**Goal:** Singleton for site-wide configuration  
**Time Estimate:** 8-12 hours  
**Priority:** MEDIUM (nice to have)

### Task 3.1: Create Site Settings Content Type

**File:** `contentful-schemas/sys-site-settings.json`

- [ ] Create schema with all fields (see proposal)
- [ ] Add `name` field (unique)
- [ ] Add `defaultHeader` field (Link to orHeader)
- [ ] Add `defaultFooter` field (Link to orFooter)
- [ ] Add `mainNavigation` field (Array of mlMenuItem)
- [ ] Add `analyticsId` field (Symbol)
- [ ] Add `maintenanceMode` field (Boolean)
- [ ] Push to Contentful

### Task 3.2: Update Page Template Schema

**File:** `contentful-schemas/homepage.json`

- [ ] Make `header` field optional (change `required: false`)
- [ ] Make `footer` field optional
- [ ] Update help text: "Leave empty to use Site Settings defaults"
- [ ] Push schema update

### Task 3.3: Update Page Rendering Logic

**Files:** `_layouts/home-page.html`, `_layouts/default.html`

Add fallback logic:
```liquid
{% if page.header %}
  {% assign header = page.header %}
{% else %}
  {% assign header = site.settings.defaultHeader %}
{% endif %}

{% include components/header.html header=header %}
```

- [ ] Implement header fallback
- [ ] Implement footer fallback
- [ ] Test with page-specific header
- [ ] Test with global header

### Task 3.4: Create Site Settings Entry

**In Contentful:**
- [ ] Create single "Main Site Settings" entry
- [ ] Link default header
- [ ] Link default footer
- [ ] Add main navigation menu items
- [ ] Add analytics ID
- [ ] Publish entry

### Task 3.5: Fetch Site Settings in Build

**File:** `scripts/contentful_to_jekyll.py` or build script

- [ ] Add query for sysSiteSettings
- [ ] Store as `_data/site-settings.yml`
- [ ] Ensure available to all templates
- [ ] Test build process

### Task 3.6: Testing

- [ ] Create new page without header/footer fields
- [ ] Verify global settings used
- [ ] Update global header
- [ ] Verify change appears on all pages
- [ ] Test page-specific override still works

---

## 🎬 Phase 4: Media Block (Optional)

**Goal:** Rich media support (images, videos, embeds)  
**Time Estimate:** 4-6 hours  
**Priority:** LOW (future enhancement)

### Task 4.1: Create Media Block Content Type

**File:** `contentful-schemas/comp-media-block.json`

- [ ] Create schema (see proposal Part 3)
- [ ] Add all fields (mediaType, image, video, embedUrl, etc.)
- [ ] Add validations
- [ ] Push to Contentful

### Task 4.2: Create Media Block Template

**File:** `_includes/components/media-block.html`

- [ ] Implement image rendering
- [ ] Implement video player (HTML5 video tag)
- [ ] Implement YouTube embed
- [ ] Implement Vimeo embed
- [ ] Add aspect ratio logic
- [ ] Add effects (rounded, shadow, etc.)

### Task 4.3: Add Media Block Styles

- [ ] Create `_sass/components/_media-block.scss`
- [ ] Implement aspect ratio containers
- [ ] Add visual effect styles
- [ ] Add responsive video wrapper

### Task 4.4: Testing

- [ ] Test image display
- [ ] Test video playback
- [ ] Test YouTube embed
- [ ] Test Vimeo embed
- [ ] Test all aspect ratios
- [ ] Mobile testing

---

## ✅ Post-Implementation

### Quality Assurance

- [ ] Full site regression testing
- [ ] Performance audit (Lighthouse score > 90)
- [ ] Accessibility audit (WAVE, aXe)
- [ ] Cross-browser testing
- [ ] Mobile responsiveness check
- [ ] SEO validation (structured data, meta tags)

### Content Editor Training

- [ ] Schedule training session
- [ ] Create editor cheat sheet
- [ ] Record tutorial video
- [ ] Update internal docs
- [ ] Q&A session

### Deployment

- [ ] Merge feature branch to main
- [ ] Deploy to staging
- [ ] Smoke testing on staging
- [ ] Deploy to production
- [ ] Monitor for errors
- [ ] Update CHANGELOG.md

### Documentation

- [ ] Update README.md
- [ ] Update SETUP-INSTRUCTIONS.md
- [ ] Update CONTENTFUL-AUTHORING-GUIDE.md
- [ ] Add screenshots to docs
- [ ] Document new workflows

### Monitoring & Metrics

**Week 1 Post-Launch:**
- [ ] Monitor error logs
- [ ] Track page load times
- [ ] Survey editor satisfaction
- [ ] Count dev support requests

**Week 2-4 Post-Launch:**
- [ ] Measure page creation time
- [ ] Track content reuse patterns
- [ ] Assess design consistency
- [ ] Gather feedback

---

## 🚨 Troubleshooting Guide

### Common Issues

**Schema Push Fails:**
```bash
# Check Contentful CLI authentication
contentful space list

# Validate JSON syntax
jsonlint contentful-schemas/comp-section.json

# Check for field ID conflicts
```

**Storybook Not Updating:**
```bash
# Clear cache and rebuild
rm -rf node_modules/.cache
npm run storybook
```

**Jekyll Not Rendering New Fields:**
```bash
# Clear Jekyll cache
bundle exec jekyll clean

# Rebuild site
bundle exec jekyll serve --livereload
```

**Contentful Preview Not Showing Changes:**
- Clear browser cache
- Check webhook configuration
- Verify preview URL settings
- Check contentful_to_jekyll.py script

---

## 📊 Success Criteria

### Phase 1 Complete When:
- [ ] All 3 schemas updated with new fields
- [ ] All fields have default values
- [ ] Storybook shows all variants
- [ ] Frontend templates handle all options
- [ ] 5+ test pages created successfully
- [ ] Mobile responsive on all devices
- [ ] Lighthouse score remains > 90

### Phase 2 Complete When:
- [ ] Section and Button content types exist
- [ ] Homepage accepts Section blocks
- [ ] Button component works in 5 contexts
- [ ] All variants render correctly
- [ ] Storybook 100% coverage
- [ ] Editors can create pages without dev help
- [ ] Backward compatibility maintained

### Phase 3 Complete When:
- [ ] Site Settings singleton exists
- [ ] All pages use global defaults
- [ ] Override mechanism works
- [ ] Single-point updates verified
- [ ] Migration complete (if applicable)

### Phase 4 Complete When:
- [ ] MediaBlock type exists
- [ ] Images, videos, embeds all work
- [ ] Responsive on all devices
- [ ] Performance maintained

---

## 📞 Support & Resources

**Contentful Documentation:**
- [Content Modeling Guide](https://www.contentful.com/developers/docs/concepts/data-model/)
- [Content Type API](https://www.contentful.com/developers/docs/references/content-management-api/#/reference/content-types)
- [Migration Guide](https://www.contentful.com/developers/docs/tutorials/cli/import-and-export/)

**Project Documentation:**
- Full Proposal: `UX-CONTENT-MODEL-OPTIMIZATION-PROPOSAL.md`
- Executive Summary: `PROPOSAL-EXECUTIVE-SUMMARY.md`
- Current Schemas: `/contentful-schemas/`
- Design System: `_sass/_variables.scss`

**Need Help?**
- Check full proposal Part 8 (Migration Path)
- Review Contentful CLI docs
- Contact: [Your team Slack channel]

---

**Checklist Version:** 1.0  
**Last Updated:** January 20, 2026  
**Estimated Completion:** 1-3 weeks (depending on phases)
