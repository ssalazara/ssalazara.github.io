# Localization & Routing Strategy
**Project:** github-page Portfolio  
**Purpose:** Multi-language implementation strategy with ISO 639-1 compliance  
**Date:** 2026-01-18  
**Status:** Implementation Ready

---

## 1. Overview

This document specifies the localization and routing strategy for the github-page portfolio, implementing **ISO 639-1 compliant multi-language support** across all content types. The strategy follows [Contentful's localization best practices](https://www.contentful.com/help/content-models/content-modeling-patterns/#localization) and provides a seamless user experience for multilingual visitors.

### 1.1 Goals

- **ISO 639-1 Compliance:** Standard two-letter language codes
- **SEO-Friendly URLs:** Language-specific routing `/en/blog/post/` vs `/es/blog/post/`
- **Fallback Strategy:** Graceful handling of missing translations
- **User Preference Persistence:** Remember language choice across sessions
- **Automatic Language Detection:** Detect browser language (optional)

---

## 2. Localization Architecture

### 2.1 Supported Languages

**Initial Launch:**
- **English (`en`)**: Primary locale, default
- **Spanish (`es`)**: Secondary locale

**Future Expansion (Phase 2):**
- French (`fr`)
- German (`de`)
- Portuguese (`pt`)
- Italian (`it`)

**Language Selection Criteria:**
- Audience demographics
- Content creator fluency
- Content volume (sufficient translations available)

---

## 3. URL Routing Strategy

### 3.1 URL Structure

**Pattern:** `/{locale}/{content-type}/{slug}/`

**Examples:**

| Content | English URL | Spanish URL |
|---------|-------------|-------------|
| Homepage | `/en/` or `/` (default) | `/es/` |
| Blog Post | `/en/blog/my-first-post/` | `/es/blog/mi-primer-post/` |
| About Page | `/en/about/` | `/es/acerca/` |
| Blog Archive | `/en/blog/` | `/es/blog/` |

### 3.2 Root URL Behavior

**Option A: Redirect to Primary Locale (Recommended)**
```
user.github.io/ → /en/ (302 redirect based on browser language)
```

**Option B: Language Selection Page**
```
user.github.io/ → Language selection page (EN | ES)
```

**Recommendation:** Option A with browser language detection for better UX.

### 3.3 Jekyll Permalink Configuration

**`_config.yml`:**
```yaml
defaults:
  - scope:
      path: "_posts/en"
      type: "posts"
    values:
      layout: "post"
      lang: "en"
      permalink: /en/blog/:slug/
  
  - scope:
      path: "_posts/es"
      type: "posts"
    values:
      layout: "post"
      lang: "es"
      permalink: /es/blog/:slug/

  - scope:
      path: "_pages/en"
    values:
      lang: "en"
      permalink: /en/:basename/
  
  - scope:
      path: "_pages/es"
    values:
      lang: "es"
      permalink: /es/:basename/
```

---

## 4. Contentful Localization Setup

### 4.1 Locale Configuration

**Primary Locale:**
- **Code:** `en-US` (Contentful) → `en` (Jekyll/URLs)
- **Name:** English (United States)
- **Fallback:** None (primary locale)

**Secondary Locale:**
- **Code:** `es` (Contentful) → `es` (Jekyll/URLs)
- **Name:** Spanish
- **Fallback:** `en-US`

**Adding New Locales in Contentful:**
1. Go to Settings → Locales
2. Click "Add locale"
3. Select language code (ISO 639-1)
4. Set fallback locale (usually primary locale)
5. Save

### 4.2 Field-Level Localization

**Localized Fields** (marked `"localized": true` in schema):
- All user-facing text (titles, descriptions, body content)
- CTA labels and button text
- SEO metadata (title, description, keywords)
- Navigation labels (menu items)
- Blog post URLs (localized slugs)

**Non-Localized Fields:**
- Internal names (editor-only)
- Assets (images, files) - shared across languages
- Dates and booleans
- Reference links between entries
- Technical IDs and slugs (base structure)

**Example: Blog Post Fields**
```json
{
  "name": "Internal Name",                // Not localized
  "url": "my-post",                       // Localized per language
  "title": "My First Post",               // Localized
  "description": "This is about...",      // Localized
  "text": "<rich text content>",          // Localized
  "publishDate": "2026-01-18",           // Not localized (same date)
  "author": "Simon Salazar",             // Not localized (same author)
  "image": "<asset reference>",          // Not localized (same image)
  "seo": "<reference to SEO entry>"      // Not localized (but SEO entry has localized fields)
}
```

### 4.3 Fallback Strategy

**Scenario:** Content exists in English but not Spanish

**Contentful Behavior:**
- Request entry in `es` locale
- If translation missing, fallback to `en-US`
- Python script receives English content

**Jekyll Handling:**
```liquid
{% assign title = page.title | default: page.title_en %}
```

**Visual Indicator (Optional):**
- Show badge: "Translated content" or "Original: English"
- Helps users understand when content is not in their language

---

## 5. Python Transformation (Localized Content)

### 5.1 Fetching Localized Entries

**Fetch Blog Posts for Each Locale:**
```python
from config import SUPPORTED_LOCALES

for locale in SUPPORTED_LOCALES:  # ['en', 'es']
    blog_posts = client.get_blog_posts(locale=locale)
    
    for post in blog_posts:
        # Extract localized fields with fallback
        fields = post.fields(locale=locale, fallback_locale='en')
        
        title = fields.get('title')  # Spanish if available, else English
        description = fields.get('description')
        body = fields.get('text')
        url_slug = fields.get('url')  # Localized slug
        
        # Generate file: _posts/es/2026-01-18-mi-primer-post.md
```

### 5.2 Handling Missing Translations

**Strategy 1: Skip Untranslated Content (Strict)**
```python
if not fields.get('title'):
    logger.warning(f"Skipping post {post.id} - no translation for {locale}")
    continue
```

**Strategy 2: Use Fallback (Lenient) - Recommended**
```python
# Contentful SDK automatically falls back to en-US
title = fields.get('title')  # Always returns something

# Mark as fallback in frontmatter
frontmatter['translation_status'] = 'fallback' if locale != 'en' else 'original'
```

### 5.3 Localized File Paths

**Blog Posts:**
```
_posts/
  en/
    2026-01-18-my-first-post.md
    2026-01-15-second-post.md
  es/
    2026-01-18-mi-primer-post.md
    2026-01-15-segundo-post.md
```

**Pages:**
```
_pages/
  en/
    index.md
    about.md
    blog.md
  es/
    index.md
    acerca.md
    blog.md
```

**Data Files:**
```
_data/
  profile-en.yml
  profile-es.yml
  blog-carousel-en.yml
  blog-carousel-es.yml
  navigation.yml  (structure only, labels localized via menu items)
```

---

## 6. Jekyll Localization Implementation

### 6.1 Language Switcher Component

**Purpose:** Allow visitors to change language

**Placement:**
- Header (top-right)
- Footer (optional redundancy)

**Design:**
- **Simple:** Dropdown or toggle (EN | ES)
- **Accessible:** ARIA labels, keyboard navigation
- **Visual:** Flag icons (optional) or text labels

**Implementation (`_includes/language-switcher.html`):**
```liquid
<div class="language-switcher">
  <button 
    class="lang-toggle" 
    id="langToggle" 
    aria-label="Change language"
    aria-haspopup="true"
    aria-expanded="false"
  >
    <span class="current-lang">{{ page.lang | upcase }}</span>
    <svg class="icon-globe" aria-hidden="true">
      <!-- Globe icon SVG -->
    </svg>
  </button>
  
  <ul class="lang-menu" id="langMenu" role="menu">
    {% assign current_url = page.url %}
    {% if page.lang == 'en' %}
      <li role="menuitem">
        <a href="/es{{ current_url | remove: '/en' }}" hreflang="es">
          🇪🇸 Español
        </a>
      </li>
    {% else %}
      <li role="menuitem">
        <a href="{{ current_url | remove: '/es' }}" hreflang="en">
          🇬🇧 English
        </a>
      </li>
    {% endif %}
  </ul>
</div>

<script>
  // Toggle menu
  document.getElementById('langToggle').addEventListener('click', () => {
    const menu = document.getElementById('langMenu');
    const isOpen = menu.classList.toggle('open');
    document.getElementById('langToggle').setAttribute('aria-expanded', isOpen);
  });
  
  // Save language preference
  const lang = '{{ page.lang }}';
  localStorage.setItem('preferredLanguage', lang);
</script>
```

### 6.2 Language Persistence (LocalStorage)

**On Page Load:**
```javascript
// Check user's preferred language
const preferredLang = localStorage.getItem('preferredLanguage');
const currentLang = '{{ page.lang }}';

// If mismatch, redirect
if (preferredLang && preferredLang !== currentLang) {
  const currentPath = window.location.pathname;
  const newPath = currentPath.replace(`/${currentLang}/`, `/${preferredLang}/`);
  window.location.href = newPath;
}
```

**Alternative: Cookie-Based (Server-Side)**
- GitHub Pages doesn't support server-side logic
- LocalStorage is client-side solution
- Works well for static sites

### 6.3 Localized UI Strings (`_data/i18n.yml`)

**Purpose:** Translate UI elements not in Contentful

**Structure:**
```yaml
# Navigation
home:
  en: "Home"
  es: "Inicio"

blog:
  en: "Blog"
  es: "Blog"

about:
  en: "About"
  es: "Acerca"

contact:
  en: "Contact"
  es: "Contacto"

# Blog UI
read_more:
  en: "Read More"
  es: "Leer Más"

back_to_blog:
  en: "← Back to Blog"
  es: "← Volver al Blog"

latest_posts:
  en: "Latest Blog Posts"
  es: "Últimas Entradas del Blog"

view_all_posts:
  en: "View All Blog Posts"
  es: "Ver Todas las Entradas"

# Metadata
published_on:
  en: "Published on"
  es: "Publicado el"

by_author:
  en: "by"
  es: "por"

reading_time:
  en: "min read"
  es: "min de lectura"

# Footer
copyright:
  en: "© 2026 Simon Salazar. All rights reserved."
  es: "© 2026 Simon Salazar. Todos los derechos reservados."

built_with:
  en: "Built with Contentful & Jekyll"
  es: "Creado con Contentful y Jekyll"
```

**Usage in Templates:**
```liquid
<a href="{{ post.url }}" class="read-more">
  {{ site.data.i18n.read_more[page.lang] }}
</a>
```

### 6.4 Date Localization

**Jekyll Date Formatting:**
```liquid
<!-- English: January 18, 2026 -->
{{ page.date | date: "%B %d, %Y" }}

<!-- Spanish: 18 de enero de 2026 -->
{% if page.lang == 'es' %}
  {{ page.date | date: "%d de %B de %Y" }}
{% else %}
  {{ page.date | date: "%B %d, %Y" }}
{% endif %}
```

**Month Names Translation:**
```liquid
{% assign months_es = "enero,febrero,marzo,abril,mayo,junio,julio,agosto,septiembre,octubre,noviembre,diciembre" | split: "," %}
{% assign month_index = page.date | date: "%m" | minus: 1 %}
{% assign month_name = months_es[month_index] %}

{{ page.date | date: "%d" }} de {{ month_name }} de {{ page.date | date: "%Y" }}
```

---

## 7. SEO & Hreflang Implementation

### 7.1 Hreflang Tags

**Purpose:** Tell search engines about language variations of a page

**Implementation (`_includes/head.html`):**
```liquid
<!-- Current page -->
<link rel="canonical" href="{{ site.url }}{{ page.url }}" />

<!-- Alternate language versions -->
{% if page.lang == 'en' %}
  <link rel="alternate" hreflang="es" href="{{ site.url }}/es{{ page.url | remove: '/en' }}" />
  <link rel="alternate" hreflang="x-default" href="{{ site.url }}{{ page.url }}" />
{% elsif page.lang == 'es' %}
  <link rel="alternate" hreflang="en" href="{{ site.url }}{{ page.url | remove: '/es' }}" />
  <link rel="alternate" hreflang="x-default" href="{{ site.url }}{{ page.url | remove: '/es' }}" />
{% endif %}
```

### 7.2 XML Sitemap (Localized)

**Generate Separate Sitemaps:**
```xml
<!-- sitemap_en.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  
  {% for post in site.posts %}
    {% if post.lang == 'en' %}
    <url>
      <loc>{{ site.url }}{{ post.url }}</loc>
      <lastmod>{{ post.date | date_to_xmlschema }}</lastmod>
      
      <!-- Alternate language links -->
      <xhtml:link rel="alternate" hreflang="es" 
                  href="{{ site.url }}/es{{ post.url | remove: '/en' }}" />
    </url>
    {% endif %}
  {% endfor %}
  
</urlset>
```

**Or Combined Sitemap with hreflang:**
```xml
<url>
  <loc>https://user.github.io/en/blog/my-post/</loc>
  <xhtml:link rel="alternate" hreflang="en" href="https://user.github.io/en/blog/my-post/" />
  <xhtml:link rel="alternate" hreflang="es" href="https://user.github.io/es/blog/mi-post/" />
  <xhtml:link rel="alternate" hreflang="x-default" href="https://user.github.io/en/blog/my-post/" />
</url>
```

### 7.3 Language Meta Tags

**Per Page:**
```liquid
<html lang="{{ page.lang }}">
<head>
  <meta charset="UTF-8">
  <meta name="language" content="{{ page.lang | upcase }}">
  
  <!-- Open Graph -->
  <meta property="og:locale" content="{{ page.lang }}_{% if page.lang == 'en' %}US{% elsif page.lang == 'es' %}ES{% endif %}" />
  
  {% if page.lang == 'en' %}
    <meta property="og:locale:alternate" content="es_ES" />
  {% elsif page.lang == 'es' %}
    <meta property="og:locale:alternate" content="en_US" />
  {% endif %}
</head>
```

---

## 8. Content Management Workflow

### 8.1 Creating Localized Content in Contentful

**Step-by-Step:**

1. **Create Entry (Primary Language):**
   - Create blog post in English (`en-US`)
   - Fill all required fields
   - Publish

2. **Add Translation:**
   - Switch to Spanish locale in Contentful UI (top-right dropdown)
   - Fill localized fields (title, description, body, url)
   - Non-localized fields (date, author, image) auto-populate
   - Publish

3. **Automatic Build:**
   - Contentful webhook triggers GitHub Actions
   - Python script generates both `/en/` and `/es/` versions
   - Jekyll builds site
   - Both languages live within 5 minutes

### 8.2 Translation Workflow

**Who Translates?**
- **Option A:** Content creator (if bilingual)
- **Option B:** Professional translator
- **Option C:** Translation service (DeepL, Google Translate, then human review)

**Quality Assurance:**
- Preview translations in Contentful
- Review Jekyll output locally
- Check for cultural appropriateness (not just literal translation)

### 8.3 Managing Partially Translated Content

**Strategy 1: Hide Untranslated Posts**
- Don't generate Spanish version if key fields missing
- Only show fully translated content

**Strategy 2: Show with Disclaimer (Recommended)**
- Generate Spanish version using English fallback
- Display banner: "This content is not yet available in Spanish. Showing English version."

**Implementation:**
```liquid
{% if page.translation_status == 'fallback' %}
  <div class="translation-notice">
    <p>{{ site.data.i18n.translation_notice[page.lang] }}</p>
  </div>
{% endif %}
```

---

## 9. User Experience Considerations

### 9.1 First Visit (No Preference Set)

**Option A: Browser Language Detection (Recommended)**
```javascript
// On root page load (/)
const browserLang = navigator.language.substring(0, 2); // 'en', 'es', etc.
const supportedLangs = ['en', 'es'];

const targetLang = supportedLangs.includes(browserLang) ? browserLang : 'en';
window.location.href = `/${targetLang}/`;
```

**Option B: Show Language Selection**
- Simple page: "Welcome! Choose your language: English | Español"
- Redirects to `/{chosen-lang}/`

### 9.2 Language Switching Within Content

**Preserve Context:**
- If reading `/en/blog/my-post/`, switching to Spanish goes to `/es/blog/mi-post/`
- If Spanish translation doesn't exist, go to `/es/` (homepage) with notice

**Smooth Transition:**
- No page flash or jarring redirect
- Maintain scroll position if possible (same content layout)

### 9.3 Search Engine Crawlers

**Googlebot Handling:**
- Crawls all localized URLs independently
- Respects hreflang tags
- Shows English results to English searches, Spanish to Spanish searches

**Sitemap Submission:**
- Submit sitemap to Google Search Console
- Verify both language versions indexed

---

## 10. Testing & Validation

### 10.1 Localization Testing Checklist

**Content:**
- [ ] All blog posts have English versions
- [ ] Spanish translations are complete (or fallback works)
- [ ] Dates format correctly per language
- [ ] Currency/numbers format correctly (if applicable)

**Navigation:**
- [ ] Language switcher visible on all pages
- [ ] Switching languages goes to correct URL
- [ ] Language preference persists across pages
- [ ] Breadcrumbs show correct language

**SEO:**
- [ ] Hreflang tags present and correct
- [ ] Sitemap includes all localized URLs
- [ ] Meta tags have correct `lang` attribute
- [ ] Open Graph locale tags present

**Accessibility:**
- [ ] HTML `lang` attribute set correctly
- [ ] Screen readers announce language changes
- [ ] Language switcher keyboard accessible

### 10.2 Cross-Language Consistency

**Verify:**
- Same blog post exists in both languages (or fallback handled)
- Navigation structure identical across languages
- Image alt text localized (if applicable)
- Links within content point to correct language version

### 10.3 Tools for Testing

**Browser Testing:**
- Chrome DevTools → Sensors → Location/Language override
- Firefox → about:config → intl.accept_languages

**SEO Testing:**
- Google Search Console → International Targeting
- Hreflang validator tools (e.g., Aleyda Solis's tool)
- Screaming Frog SEO Spider (crawl localized URLs)

**Accessibility Testing:**
- NVDA/JAWS screen readers (Windows)
- VoiceOver (macOS/iOS)
- Verify language announcements

---

## 11. Performance Considerations

### 11.1 Duplicate Content Concerns

**Not an Issue:** Hreflang tags tell search engines this is legitimate multilingual content, not duplicate content.

### 11.2 Site Size

**Impact:** Each additional language roughly doubles content size

**Current:** 20 blog posts × 2 languages = 40 markdown files

**Optimization:**
- Jekyll pagination (if blog grows large)
- Incremental builds
- Asset sharing (images not duplicated)

---

## 12. Future Enhancements

### Phase 2 (3+ Languages)

**Dynamic Language Selector:**
- Dropdown with all languages (3+)
- Flag icons for visual recognition

**Translation Management:**
- Contentful Translation API integration
- Workflow for professional translators

**Regional Variations:**
- `en-US` vs `en-GB` (color vs colour)
- `es-ES` vs `es-MX` (vosotros vs ustedes)

**Machine Translation:**
- Auto-translate with DeepL API
- Human review before publish

---

## 13. Troubleshooting Common Issues

### Issue 1: Language Switcher Doesn't Work

**Symptoms:** Clicking language toggle does nothing

**Causes:**
- JavaScript not loaded
- URL structure mismatch

**Fix:**
```javascript
// Debug: Log current URL
console.log('Current URL:', window.location.pathname);
console.log('Target URL:', targetUrl);
```

### Issue 2: Wrong Language Shows

**Symptoms:** Visiting `/es/blog/post/` but content in English

**Causes:**
- Translation missing (fallback to English)
- Python script not fetching Spanish locale

**Fix:**
- Check Contentful: Is content published in Spanish?
- Check Python logs: Did Spanish fetch succeed?
- Verify frontmatter has `lang: es`

### Issue 3: Google Shows Wrong Language

**Symptoms:** English content appears in Spanish Google searches

**Causes:**
- Hreflang tags incorrect
- Sitemap not submitted

**Fix:**
- Validate hreflang with tools
- Submit sitemap to Google Search Console
- Wait 1-2 weeks for re-crawl

---

## 14. Success Metrics

### 14.1 Language Distribution

**Track:**
- % of visitors per language (English vs Spanish)
- % of content translated (English-only vs bilingual)
- Language switcher usage rate

**Target:**
- Spanish visitors: 20-30% (if targeting Spanish audience)
- Content translation: 80%+ of blog posts
- Language switcher usage: 10-15% of visitors

### 14.2 SEO Performance

**Per Language:**
- Google Search impressions (English vs Spanish)
- Organic traffic by language
- Keyword rankings per language

**Tools:**
- Google Search Console (filter by country/language)
- Google Analytics (segment by language)

---

## Appendix: Quick Reference

### Key Files for Localization

| File | Purpose |
|------|---------|
| `_config.yml` | Jekyll locale configuration, permalinks |
| `_data/i18n.yml` | Localized UI strings |
| `_includes/language-switcher.html` | Language toggle component |
| `_includes/head.html` | Hreflang and meta tags |
| `scripts/contentful_to_jekyll.py` | Fetch localized content |
| `sitemap.xml` | Localized sitemap with hreflang |

### Contentful Locale Codes

| Language | Contentful Code | Jekyll/URL Code |
|----------|----------------|-----------------|
| English | `en-US` | `en` |
| Spanish | `es` | `es` |
| French | `fr` | `fr` |
| German | `de` | `de` |

### Common Liquid Filters for Localization

```liquid
{{ page.lang }}                           # Current language
{{ page.lang | upcase }}                  # EN, ES
{{ site.data.i18n.key[page.lang] }}      # Localized string
{{ page.url | remove: '/en' }}           # Remove language prefix
{{ page.date | date: "%B %d, %Y" }}      # Localized date
```

---

**Document Status:** Implementation Ready  
**Next Steps:** Configure Contentful locales, implement language switcher  
**Maintained By:** Simon Salazar
