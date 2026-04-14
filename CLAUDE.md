# Project Context

This is a Jekyll-based GitHub Pages personal portfolio and blog for Simon Salazar Albornoz.

- **Live site:** https://ssalazara.github.io
- **Framework:** Jekyll with Minima theme
- **Languages:** English and Spanish (bilingual)
- **Styling:** SASS (`_sass/`), compressed output in production
- **Design system:** Storybook (HTML + Vite) via `npm run storybook`
- **CMS:** Contentful (schemas in `contentful-schemas/`, sync via `push-contentful-schemas.sh`)
- **Markdown:** kramdown with Rouge syntax highlighting

## Working Directory

When I refer to "the project" or "my site", this refers to this directory (`~/Documents/Apply Digital/github-page`).

## Project Structure

```
_config.yml          — Main Jekyll config (plugins, defaults, permalink rules)
_posts/en/           — English blog posts
_posts/es/           — Spanish blog posts
_layouts/            — Page layout templates (default, home-page, post-layout, blog-archive)
_includes/           — Reusable partials (components/, helpers/, seo/)
_sass/               — Sass stylesheets
assets/              — Static assets (images, JS, CSS output)
_data/               — Site data files (YAML)
scripts/             — Utility scripts (excluded from Jekyll build)
tests/               — Test files (excluded from Jekyll build)
contentful-schemas/  — Contentful content type schemas
stories/             — Storybook component stories
```

## Content Organization

- Posts use front matter with `lang:`, `layout: post-layout`, and slug-based permalinks
- English posts → `/blog/:slug/`
- Spanish posts → `/es/blog/:slug/`
- Both `_posts/en/` and `_posts/es/` currently have one post each

## Key Commands

```bash
bundle exec jekyll serve     # Local dev server
bundle exec jekyll build     # Build the site to _site/
npm run storybook            # Run Storybook design system (port 6006)
npm run build-storybook      # Build Storybook static output
```

## Plugins

- `jekyll-feed` — RSS feed generation
- `jekyll-seo-tag` — SEO meta tags
- `jekyll-sitemap` — Sitemap generation

## Interaction Preferences

- If I type a single short word or something that looks like a stray command, ask for clarification instead of treating it as a full request.
- Skip re-exploring the directory structure unless something has changed — jump straight to the task.
- When making content changes, always validate with `bundle exec jekyll build` and report any errors before finishing.
