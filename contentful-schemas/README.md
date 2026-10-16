# Contentful Schemas — Status Registry

> ⚠️ **Free tier cap:** Contentful free plans allow up to 25 content types per space.  
> This directory has 27 schema files. Verify live count in Contentful → Settings → Content model.

## Schema Status

| Schema file | Content type ID | Status | Used in site |
|-------------|----------------|--------|-------------|
| `blogpage.json` | `blogTemplate` | ✅ **Active** | `/blog/:slug/`, `/es/blog/:slug/` |
| `profile.json` | `profile` | ✅ **Active** | Homepage profile card |
| `or-header.json` | `orHeader` | ✅ **Active** | Site navigation header |
| `footer.json` | `orFooter` | ✅ **Active** | Site footer |
| `seo.json` | `seo` | ✅ **Active** | SEO meta fields on posts |
| `homepage.json` | `homepage` | ✅ **Active** | Homepage data |
| `blog-listing-page.json` | `blogListingPage` | ✅ **Active** | Blog archive pages |
| `menu-item.json` | `menuItem` | ✅ **Active** | Navigation menu items |
| `social-link.json` | `socialLink` | ✅ **Active** | Profile social links |
| `component-image.json` | `componentImage` | ✅ **Active** | Post cover images |
| `rich-text-block.json` | `richTextBlock` | ✅ **Active** | Rich text content blocks |
| `cv-page.json` | `cvPage` | 🚧 **Defined, not implemented** | — (future `/cv/` page) |
| `component-project-card.json` | `componentProjectCard` | 🚧 **Defined, not implemented** | — (future `/projects/` page) |
| `component-projects-grid.json` | `componentProjectsGrid` | 🚧 **Defined, not implemented** | — (future `/projects/` page) |
| `education-item.json` | `educationItem` | 🚧 **Defined, not implemented** | — (future `/cv/` page) |
| `experience-item.json` | `experienceItem` | 🚧 **Defined, not implemented** | — (future `/cv/` page) |
| `contact-section.json` | `contactSection` | 🚧 **Defined, not implemented** | — (future contact section) |
| `hero-banner.json` | `heroBanner` | 🚧 **Defined, not implemented** | — (future homepage hero) |
| `timeline.json` | `timeline` | 🚧 **Defined, not implemented** | — (future `/cv/` timeline) |
| `skills-group.json` | `skillsGroup` | 🚧 **Defined, not implemented** | — (future skills section) |
| `skill-tag.json` | `skillTag` | 🚧 **Defined, not implemented** | — (future skills section) |
| `component-skills-list.json` | `componentSkillsList` | 🚧 **Defined, not implemented** | — (future skills section) |
| `component-card.json` | `componentCard` | 🚧 **Defined, not implemented** | — |
| `component-carousel.json` | `componentCarousel` | 🚧 **Defined, not implemented** | — |
| `component-quote.json` | `componentQuote` | 🚧 **Defined, not implemented** | — (future post enrichment) |
| `text-with-image.json` | `textWithImage` | 🚧 **Defined, not implemented** | — |

> **Note on status accuracy:** Content type IDs above are inferred from schema file naming conventions.  
> Run `contentful space list-content-types --space-id $CONTENTFUL_SPACE_ID` to get the authoritative live list.

## Pushing Schemas to Contentful

```bash
./push-contentful-schemas.sh
```

## Roadmap for Unimplemented Schemas

See [docs/content-strategy.md](../docs/content-strategy.md) for the content implementation plan.  
Priority order: `cv-page` → `component-project-card` → `skills-group` → `hero-banner`
