# Contentful Authoring Experience Guide

**Purpose:** Manage all website content through Contentful CMS without touching code  
**Last Updated:** January 20, 2026  
**Status:** Production Ready

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Homepage Setup](#homepage-setup)
3. [Content Types Overview](#content-types-overview)
4. [Step-by-Step: Creating Homepage Content](#step-by-step-creating-homepage-content)
5. [Publishing Workflow](#publishing-workflow)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### The Content Flow

```
┌──────────────┐
│  Contentful  │ ← You create/edit content here
│     CMS      │
└──────┬───────┘
       │
       │ Publish
       ▼
┌──────────────┐
│    GitHub    │ ← Webhook triggers automatic build
│   Actions    │
└──────┬───────┘
       │
       │ < 5 minutes
       ▼
┌──────────────┐
│ GitHub Pages │ ← Live website updates!
│   (Live)     │
└──────────────┘
```

### What You Can Control

✅ **Homepage content** (hero, skills, projects)  
✅ **Blog posts** (write, edit, publish)  
✅ **Navigation menus** (header & footer)  
✅ **SEO metadata** (titles, descriptions, social cards)  
✅ **Images and media**

❌ **What stays in code:** Design system, layouts, styling

---

## 🏠 Homepage Setup

### Portfolio-First Layout

Your homepage is built with **3 flexible content blocks**:

1. **Hero Banner** - Big headline with image  
2. **Skills List** - Your core competencies as tags  
3. **Projects Grid** - Showcase 2-4 featured projects

### Data Structure

```yaml
# In Contentful, your Homepage entry contains:
Homepage Entry
├── Name: "Homepage EN" (internal reference)
├── URL: "/" (root path)
├── SEO: Link to SEO entry
├── Header: Link to Header entry
├── Blocks: [Array of content blocks]
│   ├── Hero Banner
│   ├── Skills List
│   └── Projects Grid
└── Footer: Link to Footer entry
```

---

## 📦 Content Types Overview

### Core Components for Homepage

| Content Type | Purpose | Required Fields | Example |
|-------------|---------|-----------------|---------|
| **Homepage** | Main landing page | name, url, blocks | "Homepage EN" |
| **Hero Banner** | Large hero section | title, description, image | "Hello, World!" |
| **Skills List** | Core competencies | title, skills (array) | "Core Skills" |
| **Projects Grid** | Featured work | title, projects (array) | "Featured Projects" |
| **Project Card** | Single project | title, description, image, url | "My Portfolio" |

### Supporting Content Types

| Content Type | Purpose | Used By |
|-------------|---------|---------|
| **SEO** | Search metadata | All pages |
| **Header** | Site navigation | All pages |
| **Footer** | Site footer | All pages |
| **Blog Post** | Blog entries | Blog section |

---

## 📝 Step-by-Step: Creating Homepage Content

### Phase 1: Create Content Pieces

#### 1.1 Create Hero Banner

1. In Contentful, go to **Content**
2. Click **Add Entry** → **Hero Banner**
3. Fill in:
   ```
   Internal Name: "Homepage Hero"
   Headline: "Hello, World!"
   Subheading: "Personal website intended as a learning project."
   CTA Button Label: "Learn More" (optional)
   CTA Button URL: "/blog/" (optional)
   Background Image: Upload or select image (1920x1080px recommended)
   ```
4. **Publish**

#### 1.2 Create Skills List

1. **Add Entry** → **Skills List**
2. Fill in:
   ```
   Internal Name: "Technical Skills"
   Section Title: "Core Skills"
   Skills: (Click "Add" for each skill)
     - Problem Solving
     - Content Strategy
     - Data Science
     - Headless CMS
     - UX Design
     - Front-end Development
   ```
3. **Publish**

#### 1.3 Create Project Cards

**First, create individual project cards:**

1. **Add Entry** → **Project Card**
2. Fill in:
   ```
   Project Title: "My Personal Profile"
   Project Description: "Self-taught project based on using a free tech-stack for a personal website. In short: Astro + Sanity + Netlify"
   Project Image: Upload screenshot (800x450px recommended, 16:9 ratio)
   Project URL: "https://simonsalazar.netlify.app/"
   External Link: ✓ (checked)
   ```
3. **Publish**
4. **Repeat** for each project (recommended: 2-4 projects total)

#### 1.4 Create Projects Grid

1. **Add Entry** → **Projects Grid**
2. Fill in:
   ```
   Internal Name: "Featured Work"
   Section Title: "Featured Projects"
   Project Cards: Link to the Project Cards you created above
   ```
3. **Publish**

### Phase 2: Assemble Homepage

#### 2.1 Create Homepage Entry

1. **Add Entry** → **Homepage**
2. Fill in:
   ```
   Internal Name: "Homepage EN"
   URL Slug: "/"
   SEO Metadata: Link to your SEO entry (create if needed)
   Header Component: Link to "Main Header" (create if needed)
   Content Blocks: (Add in this order)
     1. Link to "Homepage Hero"
     2. Link to "Technical Skills"
     3. Link to "Featured Work"
   Footer Component: Link to "Main Footer" (create if needed)
   ```
3. **Publish**

### Phase 3: For Spanish Version

**Repeat the same steps but:**
- Set URL to `/es/`
- Translate all text content
- Use same images (or localized versions)
- Link to Spanish Header/Footer if separate

---

## 🔄 Publishing Workflow

### Publishing Changes

1. **Edit** content in Contentful
2. Click **Publish** (or **Update** if already published)
3. **Wait 3-5 minutes** for build to complete
4. **Refresh** your GitHub Pages site to see changes

### Content States

| State | What It Means | Visible on Site? |
|-------|---------------|------------------|
| **Draft** | Work in progress | ❌ No |
| **Changed** | Published but has unpublished edits | ⚠️ Old version |
| **Published** | Live and current | ✅ Yes |
| **Archived** | Hidden from queries | ❌ No |

### Using Preview Mode

**To see changes before publishing:**

1. Use the **Preview** button in Contentful
2. Or run locally: `python3 scripts/contentful_to_jekyll.py --mode preview`
3. Preview mode pulls draft content for testing

---

## 💡 Best Practices

### Content Creation

✅ **DO:**
- Write descriptive **Internal Names** (you'll thank yourself later)
- Keep headlines **under 80 characters** for mobile
- Use **WebP images** for faster loading
- Optimize images **before uploading** (< 1MB for projects, < 2MB for heroes)
- Write **alt text** for accessibility
- Test links before publishing

❌ **DON'T:**
- Use special characters in URL slugs
- Upload massive images (> 5MB)
- Leave required fields empty
- Publish untested content to production

### Image Guidelines

| Component | Recommended Size | Max File Size | Format |
|-----------|------------------|---------------|--------|
| Hero Banner | 1920x1080px | 2MB | WebP, JPG |
| Project Card | 800x450px (16:9) | 1MB | WebP, JPG |
| Blog Post | 1200x630px | 1MB | WebP, JPG |

### SEO Optimization

**Title Tags:** 50-60 characters  
**Meta Descriptions:** 150-160 characters  
**Social Images:** 1200x630px (required for Facebook/Twitter)

---

## 🔧 Troubleshooting

### Changes Not Showing Up?

**Wait 5 minutes** - Build takes 3-5 minutes total

**Check:**
1. Did you click **Publish** (not just Save)?
2. Check [GitHub Actions](https://github.com/YOUR_USERNAME/YOUR_REPO/actions) for build status
3. Hard refresh your browser (`Cmd/Ctrl + Shift + R`)
4. Clear cache or try incognito mode

### Build Failed?

1. Check GitHub Actions logs for error details
2. Common issues:
   - Missing required fields in Contentful
   - Broken image links
   - Invalid URL formats
   - Exceeding content limits (max 20 blocks per page)

### Content Not Appearing?

**Checklist:**
- [ ] Entry is **Published** (not draft)
- [ ] Entry is **linked** to Homepage blocks array
- [ ] Entry has all **required fields** filled
- [ ] No **validation errors** in Contentful
- [ ] Correct **locale** selected (EN vs ES)

### Need to Rollback?

**In Contentful:**
1. Go to entry → **Info** tab
2. View **Publishing history**
3. **Restore** previous version

**In GitHub:**
1. Revert last commit if needed
2. Or re-run previous successful build

---

## 📚 Content Model Reference

### Homepage Content Model

```
📄 Homepage
  ├── 🦠 Hero Banner
  │     ├── title (Symbol, max 80 chars)
  │     ├── description (Text, max 250 chars)
  │     ├── ctaLabel (Symbol, optional)
  │     ├── ctaUrl (Symbol, optional)
  │     └── image (Asset, max 2MB)
  │
  ├── 🧩 Skills List
  │     ├── title (Symbol, max 60 chars)
  │     └── skills (Array, 1-12 items)
  │
  └── 🧩 Projects Grid
        ├── title (Symbol, max 60 chars)
        └── projects (Array of Project Cards, 1-6 items)
              └── 🧬 Project Card
                    ├── title (Symbol, max 60 chars)
                    ├── description (Text, max 200 chars)
                    ├── image (Asset, max 1MB)
                    ├── url (Symbol, URL or "#")
                    └── external (Boolean)
```

---

## 🎯 Next Steps

### For First-Time Setup

1. ✅ Push Contentful schemas: `./push-contentful-schemas.sh`
2. ✅ Create SEO entry (reusable for all pages)
3. ✅ Create Header entry (site navigation)
4. ✅ Create Footer entry (site footer)
5. ✅ Create Homepage content (Hero → Skills → Projects)
6. ✅ Publish and wait for build

### For Ongoing Content Management

1. **Blog Posts:** Create new entries, publish when ready
2. **Homepage Updates:** Edit existing blocks, republish
3. **Project Additions:** Add new Project Cards, link to Projects Grid
4. **Navigation Changes:** Edit Header/Footer entries

### Monitoring

- **GitHub Actions:** Monitor builds at `github.com/YOUR_REPO/actions`
- **Analytics:** Check Google Analytics for traffic (if configured)
- **Errors:** Check build logs for warnings

---

## 🆘 Getting Help

### Resources

- **Contentful Docs:** https://www.contentful.com/developers/docs/
- **Jekyll Docs:** https://jekyllrb.com/docs/
- **Project Context:** See `_bmad-output/project-context.md`
- **Design System:** See `_bmad-output/DESIGN-SYSTEM-COMPLETE.md`

### Common Questions

**Q: Can I add more than 3 sections to the homepage?**  
A: Yes! Add more blocks to the Content Blocks array. Supported types: Hero Banner, Skills List, Projects Grid, Rich Text, Text with Image, Carousel, Quote.

**Q: How do I change the site design/colors?**  
A: Design changes require code edits in `_sass/` files. Contact a developer.

**Q: Can I schedule content to publish later?**  
A: Yes! Use Contentful's **Scheduled Publishing** feature (paid tiers only).

**Q: How many languages can I support?**  
A: Free tier supports 2 locales (EN, ES currently configured).

---

**Ready to start creating?** Head to Contentful and build your first Homepage! 🚀
