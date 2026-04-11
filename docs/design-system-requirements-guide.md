# Design System Requirements Guide
## ssalazara.github.io — Alineación, Correcciones y Estrategia Futura

**Versión:** 1.0  
**Fecha:** Abril 2026  
**Propósito:** Guía ejecutable para Claude. Cada sección describe el problema, su causa raíz y las acciones exactas a tomar, en orden de prioridad.

---

## DIAGNÓSTICO GENERAL

El sitio tiene un sistema de diseño sólido y bien definido en `_sass/_variables.scss` (tokens completos: colores, tipografía, espaciado, sombras, breakpoints). El problema NO son los tokens — el problema es que hay **componentes HTML que existen pero carecen de sus SCSS correspondientes**, y hay **páginas que no consumen el sistema de diseño porque no están conectadas a Contentful**.

Tres grandes brechas identificadas:

| Brecha | Causa | Impacto |
|--------|-------|---------|
| `.post-byline` no tiene SCSS | `_post-byline.scss` no existe y no está importado en `style.scss` | Íconos SVG gigantes en post individual |
| `.breadcrumb` no tiene SCSS | `_breadcrumb.scss` no existe | Breadcrumb renderiza como "1. 2." |
| `/blog/` no tiene identidad visual | La página es estática, sin hero, sin conexión a Contentful | Página pobre que rompe la consistencia |
| Post layout no usa hero-banner para imagen destacada | `post-layout.html` renderiza la imagen inline como `<figure>` después del header | El post carece del impacto visual de la homepage |
| `heroBanner` del schema de blog post no se procesa | `blog_post_transformer.py` ignora el campo `heroBanner` del content type | El campo existe en Contentful pero nunca llega al Jekyll |

---

## FASE 1 — CORRECCIONES CRÍTICAS (Sin tocar Contentful)

### REQ-001: Crear `_sass/components/_post-byline.scss`

**Problema:** El componente `_includes/components/post-byline.html` usa clases `.post-byline`, `.post-byline__item`, `.post-byline__icon`, `.post-byline__author`, `.post-byline__date`, `.post-byline__category`, y `.badge`. Ninguna de estas tiene estilos definidos. Los íconos SVG sin dimensiones fijas heredan el tamaño de su contenedor y se renderizan como bloques negros grandes.

**Archivo a crear:** `_sass/components/_post-byline.scss`

**Contenido exacto:**

```scss
// ============================================================================
// POST BYLINE COMPONENT
// Design System v1.0 — Author, date, reading time, and category metadata
// ============================================================================

.post-byline {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: $spacing-4;
  margin-bottom: $spacing-6;

  @include md {
    gap: $spacing-6;
  }

  &__item {
    display: inline-flex;
    align-items: center;
    gap: $spacing-2;
    font-size: $font-size-sm;
    color: $color-text-tertiary;
    font-family: $font-family-base;
  }

  &__icon {
    flex-shrink: 0;
    width: $icon-size-sm;   // 16px
    height: $icon-size-sm;  // 16px
    color: $color-text-tertiary;
  }

  &__author {
    font-weight: $font-weight-medium;
    color: $color-text-secondary;
  }

  &__category {
    font-weight: $font-weight-medium;
  }
}

// Badge component (used for category labels)
.badge {
  display: inline-block;
  padding: $spacing-1 $spacing-3;
  font-size: $font-size-xs;
  font-weight: $font-weight-semibold;
  border-radius: $radius-full;
  text-transform: uppercase;
  letter-spacing: $letter-spacing-wide;
  background-color: $color-bg-secondary;
  color: $color-text-secondary;

  // Category variants
  &--technology {
    background-color: $color-primary-50;
    color: $color-primary-700;
  }

  &--design {
    background-color: #fdf4ff;
    color: #7e22ce;
  }

  &--business {
    background-color: $color-success-50;
    color: $color-success-600;
  }

  &--lifestyle {
    background-color: $color-warning-50;
    color: $color-warning-600;
  }

  &--updates {
    background-color: $color-info-50;
    color: $color-info-600;
  }

  &--news {
    background-color: $color-error-50;
    color: $color-error-600;
  }
}
```

**Luego agregar la importación en `assets/css/style.scss`**, después de `@import 'components/hero-banner';`:

```scss
@import 'components/post-byline';
```

---

### REQ-002: Crear `_sass/components/_breadcrumb.scss`

**Problema:** `blog-archive.html` usa `<nav class="breadcrumb">` → `<ol class="breadcrumb__list">` → `<li class="breadcrumb__item">`. No existe `_breadcrumb.scss`, entonces el `<ol>` renderiza con numeración por defecto del browser ("1." "2.").

**Archivo a crear:** `_sass/components/_breadcrumb.scss`

**Contenido exacto:**

```scss
// ============================================================================
// BREADCRUMB COMPONENT
// Design System v1.0 — Navigation breadcrumb
// ============================================================================

.breadcrumb {
  margin-bottom: $spacing-4;

  &__list {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: $spacing-2;
    list-style: none;
    margin: 0;
    padding: 0;
  }

  &__item {
    display: inline-flex;
    align-items: center;
    gap: $spacing-2;
    font-size: $font-size-sm;
    color: $color-text-tertiary;

    // Separator between items
    &:not(:last-child)::after {
      content: '/';
      color: $color-neutral-300;
      font-weight: $font-weight-normal;
    }

    &--active {
      color: $color-text-secondary;
      font-weight: $font-weight-medium;
    }
  }

  &__link {
    color: $color-text-tertiary;
    text-decoration: none;
    transition: $transition-colors;

    @include hover {
      color: $color-text-link;
    }
  }
}
```

**Agregar importación en `assets/css/style.scss`**, después de `@import 'components/post-byline';`:

```scss
@import 'components/breadcrumb';
```

---

### REQ-003: Rediseñar el header de la Blog Archive page

**Problema:** `_layouts/blog-archive.html` tiene un header estático y minimalista que no sigue el sistema de diseño. La página `/blog/` carece de hero visual, descripción y jerarquía.

**Estrategia:** No conectar a Contentful en esta fase. Usar datos YAML estáticos para el hero de la página de blog.

**Paso 1 — Crear archivo de datos YAML para la blog page:**

Crear `_data/blog-page-en.yml`:

```yaml
# Blog listing page data (English)
# Edit this file to update the blog page hero content
hero:
  title: "Blog"
  description: "Notes, experiments, and deep dives into web development, product design, and the technologies shaping how we build the web."
  image_url: ""  # Optional: add a Contentful image URL here if desired
```

Crear `_data/blog-page-es.yml`:

```yaml
# Datos de la página de blog (Español)
hero:
  title: "Blog"
  description: "Notas, experimentos y análisis sobre desarrollo web, diseño de producto y las tecnologías que están cambiando cómo construimos la web."
  image_url: ""
```

**Paso 2 — Actualizar `_layouts/blog-archive.html`:**

Reemplazar el bloque `<header class="blog-archive__header">` completo por:

```liquid
{% assign blog_page_data = site.data["blog-page-" | append: current_locale] | default: site.data["blog-page-en"] %}

{% if blog_page_data.hero %}
  <section class="blog-archive__hero">
    {% if blog_page_data.hero.image_url and blog_page_data.hero.image_url != "" %}
      {% include components/hero-banner.html hero=blog_page_data.hero %}
    {% else %}
      <div class="blog-archive__hero-minimal">
        <div class="container">
          {% include components/breadcrumb-nav.html %}
          <h1 class="blog-archive__title">{{ blog_page_data.hero.title | default: "Blog" }}</h1>
          {% if blog_page_data.hero.description %}
            <p class="blog-archive__description">{{ blog_page_data.hero.description }}</p>
          {% endif %}
          {% if locale_posts.size > 0 %}
            <p class="blog-archive__subtitle">
              {{ locale_posts.size }} {% if current_locale == 'es' %}{% if locale_posts.size == 1 %}artículo{% else %}artículos{% endif %}{% else %}{% if locale_posts.size == 1 %}post{% else %}posts{% endif %}{% endif %} published
            </p>
          {% endif %}
        </div>
      </div>
    {% endif %}
  </section>
{% endif %}
```

**Paso 3 — Agregar estilos para el hero minimal en `_sass/pages/_blog-archive.scss`:**

Agregar al final del archivo, dentro de `.blog-archive`:

```scss
  // Hero section variants
  &__hero-minimal {
    background: linear-gradient(
      180deg,
      $color-bg-secondary 0%,
      $color-bg-page 100%
    );
    padding: $spacing-16 0 $spacing-12;
    text-align: center;
    border-bottom: 1px solid $color-border-light;

    @include md {
      padding: $spacing-20 0 $spacing-16;
    }
  }

  &__description {
    font-size: $font-size-lg;
    line-height: $line-height-relaxed;
    color: $color-text-secondary;
    max-width: 640px;
    margin: 0 auto $spacing-6;

    @include md {
      font-size: $font-size-xl;
    }
  }

  &__subtitle {
    display: inline-block;
    padding: $spacing-2 $spacing-4;
    font-size: $font-size-sm;
    font-weight: $font-weight-medium;
    color: $color-text-tertiary;
    background-color: $color-bg-surface;
    border: 1px solid $color-border-light;
    border-radius: $radius-full;
    margin-top: $spacing-4;
  }
```

---

### REQ-004: Rediseñar el header del Post Layout

**Problema:** En `_layouts/post-layout.html`, el header muestra solo título + byline sobre fondo blanco liso, seguido de la imagen destacada como `<figure>` inline. Esto produce la secuencia visual: [título texto] → [íconos rotos] → [imagen grande] → [contenido]. Es inconsistente con la homepage donde los bloques tienen identidad visual fuerte.

**Solución:** Invertir el orden — colocar la imagen destacada ANTES del título, como hero full-width, y dejar el título centrado sobre la imagen con overlay.

**Actualizar `_layouts/post-layout.html`:**

Reemplazar el contenido actual entre `<article class="post-layout"...>` y `<!-- Post Content -->` con:

```liquid
<article class="post-layout" itemscope itemtype="https://schema.org/BlogPosting">

  <!-- Post Hero: Featured Image Full Width -->
  {% if page.featured_image %}
  <div class="post-layout__hero">
    <div class="post-layout__hero-image"
         style="background-image: url('{{ page.featured_image }}?w=1400&fm=webp&q=85');"
         role="img"
         aria-label="{{ page.featured_image_alt | default: page.title | escape }}">
    </div>
    <div class="post-layout__hero-overlay">
      <div class="container container--narrow">
        {% if page.label %}
        <span class="badge badge--{{ page.label | slugify }} post-layout__label">{{ page.label }}</span>
        {% endif %}
        <h1 class="post-layout__title" itemprop="headline">{{ page.title | escape }}</h1>
        {% include components/post-byline.html %}
      </div>
    </div>
  </div>
  {% else %}
  <!-- No image: minimal centered header -->
  <header class="post-layout__header">
    <div class="container container--narrow">
      {% if page.label %}
      <span class="badge badge--{{ page.label | slugify }} post-layout__label">{{ page.label }}</span>
      {% endif %}
      <h1 class="post-layout__title" itemprop="headline">{{ page.title | escape }}</h1>
      {% include components/post-byline.html %}
    </div>
  </header>
  {% endif %}
```

**Agregar SCSS al `_sass/pages/_post-layout.scss`**, reemplazando el bloque `&__featured-image` existente y agregando los nuevos elementos `&__hero`:

```scss
  // Hero con imagen de fondo (cuando existe featured_image)
  &__hero {
    position: relative;
    width: 100%;
    min-height: 480px;
    overflow: hidden;
    background-color: $color-neutral-900;
    margin-bottom: $spacing-12;

    @include md {
      min-height: 560px;
    }

    @include lg {
      min-height: 640px;
    }
  }

  &__hero-image {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    z-index: 1;

    &::after {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(
        to top,
        rgba(0, 0, 0, 0.85) 0%,
        rgba(0, 0, 0, 0.4) 50%,
        rgba(0, 0, 0, 0.15) 100%
      );
      z-index: 2;
    }
  }

  &__hero-overlay {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: flex-end;
    min-height: inherit;
    padding: $spacing-12 $spacing-4 $spacing-10;

    @include md {
      padding: $spacing-16 $spacing-6 $spacing-12;
    }

    .container--narrow {
      text-align: center;
    }

    // Override title and byline colors when over image
    .post-layout__title {
      color: $color-text-inverse;
      text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }

    .post-byline {
      color: $color-neutral-200;
    }

    .post-byline__item,
    .post-byline__icon {
      color: $color-neutral-300;
    }
  }

  // Label badge positioning
  &__label {
    display: inline-block;
    margin-bottom: $spacing-4;
  }

  // Remove old featured-image block (replaced by hero)
  &__featured-image {
    display: none;
  }
```

---

## FASE 2 — ALINEACIÓN ESTRATÉGICA CON CONTENTFUL

### REQ-005: Procesar campo `heroBanner` en `blog_post_transformer.py`

**Contexto:** El schema `contentful-schemas/blogpage.json` ya define el campo `heroBanner` (link a content type `heroBanner`) para blog posts. Sin embargo, `blog_post_transformer.py` no extrae este campo — solo procesa `image` (featured image).

**Propósito:** Permitir que un editor en Contentful asigne un hero personalizado a un post (diferente imagen, título y CTA propio), o que el hero use la imagen destacada como fallback automático.

**Actualizar `scripts/transformers/blog_post_transformer.py`** en el método `transform_single`:

Después de la línea que extrae `featured_image`, agregar:

```python
# Extract hero banner reference (optional field)
hero_banner_data = {}
hero_banner_ref = self.resolve_reference(entry, 'hero_banner')
if hero_banner_ref:
    try:
        hb_fields = hero_banner_ref.fields()
        hb_image_url = ''
        hb_image = hb_fields.get('image')
        if hb_image:
            hb_image_url = self.get_asset_url(hb_image)
        
        hero_banner_data = {
            'title': hb_fields.get('title', title),
            'description': hb_fields.get('description', ''),
            'cta_label': hb_fields.get('cta_label', ''),
            'cta_url': hb_fields.get('cta_url', ''),
            'image_url': hb_image_url or featured_image
        }
        logger.info(f"✅ HERO_BANNER_RESOLVED entry_id={entry.id}")
    except Exception as e:
        logger.warning(f"⚠️ HERO_BANNER_FAILED entry_id={entry.id} error={str(e)}")
else:
    # Fallback: use featured image as hero background (no text overlay from hero)
    if featured_image:
        hero_banner_data = {
            'image_url': featured_image
        }
```

Agregar `hero_banner` al diccionario `frontmatter`:

```python
frontmatter = {
    ...existing fields...,
    'hero_banner': hero_banner_data,  # ADD THIS
    ...
}
```

**Actualizar `_layouts/post-layout.html`** para usar `page.hero_banner` en lugar del bloque de imagen directo. El hero debe leer `page.hero_banner` primero, con fallback a `page.featured_image`:

```liquid
{% assign post_hero = page.hero_banner | default: nil %}
{% if post_hero %}
  {% include components/hero-banner.html hero=post_hero %}
{% elsif page.featured_image %}
  <div class="post-layout__hero">
    <!-- el bloque hero definido en REQ-004 -->
  </div>
{% endif %}
```

---

### REQ-006: Crear Content Type `blogListingPage` en Contentful

**Propósito:** Permitir que la página `/blog/` tenga su propio hero, descripción SEO y metadatos, gestionados desde Contentful. Esto mantiene la coherencia: tanto la homepage como la blog page son entradas de Contentful.

**Schema del nuevo Content Type:**

Crear `contentful-schemas/blog-listing-page.json`:

```json
{
  "name": "📋 Blog Listing Page",
  "description": "Configuration for the /blog/ archive page. Hero, SEO metadata, and introductory text.",
  "displayField": "name",
  "sys": { "id": "blogListingPage" },
  "fields": [
    {
      "id": "name",
      "name": "Internal Name",
      "type": "Symbol",
      "localized": false,
      "required": true,
      "helpText": "For editors only. E.g. 'Blog Listing Page'"
    },
    {
      "id": "seo",
      "name": "SEO Metadata",
      "type": "Link",
      "linkType": "Entry",
      "localized": false,
      "required": true,
      "validations": [{ "linkContentType": ["seo"] }],
      "helpText": "SEO title, description, and OG image for the /blog/ URL"
    },
    {
      "id": "hero",
      "name": "Hero Banner",
      "type": "Link",
      "linkType": "Entry",
      "localized": false,
      "required": false,
      "validations": [{ "linkContentType": ["heroBanner"] }],
      "helpText": "Optional hero. If omitted, renders a minimal header with title and description."
    },
    {
      "id": "title",
      "name": "Page Title",
      "type": "Symbol",
      "localized": true,
      "required": true,
      "helpText": "H1 for the blog listing page. E.g. 'Blog' or 'Articles'"
    },
    {
      "id": "description",
      "name": "Page Description",
      "type": "Text",
      "localized": true,
      "required": false,
      "helpText": "Subtitle shown below title. Describe what readers will find."
    }
  ]
}
```

**Crear `scripts/transformers/blog_listing_page_transformer.py`:**

```python
"""
Blog listing page transformer for Contentful blogListingPage content type.
Outputs to _data/blog-page-{locale}.yml
"""
from typing import Dict, Any, List
from contentful.entry import Entry
from scripts.transformers.base_transformer import BaseTransformer
from scripts.config import logger

CONTENT_TYPE_BLOG_LISTING = 'blogListingPage'

class BlogListingPageTransformer(BaseTransformer):
    def __init__(self, client, locale: str = 'en') -> None:
        super().__init__(client, locale)
        self.content_type = CONTENT_TYPE_BLOG_LISTING

    def transform_single(self, entry: Entry) -> Dict[str, Any]:
        fields = entry.fields()
        
        # Extract hero banner if linked
        hero_data = {}
        hero_ref = self.resolve_reference(entry, 'hero')
        if hero_ref:
            hb_fields = hero_ref.fields()
            image_url = ''
            if hb_fields.get('image'):
                image_url = self.get_asset_url(hb_fields['image'])
            hero_data = {
                'title': hb_fields.get('title', ''),
                'description': hb_fields.get('description', ''),
                'cta_label': hb_fields.get('cta_label', ''),
                'cta_url': hb_fields.get('cta_url', ''),
                'image_url': image_url
            }
            hero_data = {k: v for k, v in hero_data.items() if v}
        
        # Extract SEO
        seo_data = {}
        seo_ref = self.resolve_reference(entry, 'seo')
        if seo_ref:
            seo_fields = seo_ref.fields()
            og_image = ''
            if seo_fields.get('og_image'):
                og_image = self.get_asset_url(seo_fields['og_image'])
            seo_data = {
                'title': seo_fields.get('title', ''),
                'description': seo_fields.get('description', ''),
                'og_image': og_image
            }
        
        return {
            'title': fields.get('title', 'Blog'),
            'description': fields.get('description', ''),
            'hero': hero_data,
            'seo': seo_data
        }

    def transform_all(self) -> List[Dict[str, Any]]:
        try:
            entries = self.client.get_entries(
                content_type=self.content_type,
                locale=self.locale,
                include=3
            )
            if not entries:
                logger.warning(f"⚠️ NO_BLOG_LISTING_PAGE locale={self.locale}")
                return []
            return [self.transform_single(entries[0])]
        except Exception as e:
            logger.error(f"❌ BLOG_LISTING_TRANSFORM_FAILED error={str(e)}")
            return []
```

**Registrar el transformer en `scripts/contentful_to_jekyll.py`:** Agregar import y llamada al transformer, escribiendo el resultado a `_data/blog-page-{locale}.yml`.

**Una vez que el transformer esté activo, el archivo `blog/index.html` puede simplificarse** porque el layout `blog-archive.html` ya leerá el YAML dinámico. El hero en `blog-archive.html` (de REQ-003) ya está diseñado para leer `site.data["blog-page-en"]` o `site.data["blog-page-es"]`.

---

## FASE 3 — DESIGN SYSTEM: REGLAS OBLIGATORIAS PARA FUTURAS ENTRADAS

### REQ-007: Definición de la estructura visual por página

Toda página del sitio debe seguir exactamente una de las siguientes estructuras:

**Estructura A — Página con Hero de Contenido (Homepage, páginas de landing):**
```
[Header global]
[Hero Banner — full viewport width, min 480px, imagen + texto overlay]
[Bloques de contenido: quote, textWithImage, carousel, etc.]
[Footer global]
```

**Estructura B — Blog Archive (`/blog/`):**
```
[Header global]
[Hero minimal — gradiente gris claro, sin imagen, título + descripción centrada]
[Grid de post cards — 1 col mobile, 2 col tablet, 3 col desktop]
[Footer global]
```

**Estructura C — Blog Post individual:**
```
[Header global]
[Post Hero — full width, imagen como fondo, texto overlay (título + byline)]
[Contenido del artículo — container narrow, max-width 720px]
[Post footer — tags + back to archive]
[Related posts — fondo gris, grid de 3]
[Footer global]
```

Ninguna página debe existir con solo texto plano sin hero visual. Si no hay imagen disponible, el hero minimal del gradiente es el mínimo aceptable.

---

### REQ-008: Reglas para nuevas entradas de blog en Contentful

Cada nuevo blog post que se cree en Contentful debe cumplir:

1. **Campo `image` (Featured Image) — OBLIGATORIO.** Mínimo 1200x630px. Esta imagen se usa como fondo del hero en la vista del post Y como thumbnail en el blog listing.

2. **Campo `seo` (SEO entry) — OBLIGATORIO.** Debe tener `title` y `description`. Sin estos campos el transformer rechaza la entrada.

3. **Campo `text` (Article Body) — OBLIGATORIO.** El cuerpo del artículo debe tener contenido sustancial. Un post con solo 3 bullets se verá vacío con el layout actual.

4. **Campo `heroBanner` — OPCIONAL.** Solo usar cuando el post necesita un hero con título y CTA diferentes al título del post mismo. En la mayoría de casos NO es necesario — el `featured_image` ya funciona como hero automáticamente.

5. **Campo `label` (Category) — RECOMENDADO.** Permite aplicar el badge de categoría en el hero y en el post card. Usar los valores definidos: `Technology`, `Design`, `Business`, `Lifestyle`, `Updates`, `News`.

6. **Localización:** Todo nuevo post debe tener sus versiones en inglés (locale `en-US`) y español (locale `es`) si el sitio es bilingüe. El slug puede variar por locale.

---

### REQ-009: Tokens de diseño — Uso obligatorio

Estas son las reglas de uso de tokens que DEBEN respetarse en cualquier nuevo componente o modificación:

**Colores:**
- Fondo de página principal: siempre `$color-bg-page` (`#fafafa`)
- Fondo de tarjetas/superficies elevadas: `$color-bg-surface` (`#ffffff`)
- Fondo de secciones alternadas: `$color-bg-secondary` (`#f5f5f5`)
- Texto principal: `$color-text-primary` (`#171717`)
- Texto secundario: `$color-text-secondary` (`#525252`)
- Texto muted/metadatos: `$color-text-tertiary` (`#737373`)
- Links: `$color-text-link` (`$color-primary-600`)
- Nunca usar valores hex directos para colores. Siempre usar variables.

**Tipografía:**
- Headings (h1–h4): `$font-family-heading` (Merriweather)
- Body, UI, metadatos: `$font-family-base` (Inter)
- Código: `$font-family-mono` (JetBrains Mono)
- Nunca hardcodear `font-family`, `font-size` o `font-weight` — siempre usar variables del sistema.

**Espaciado:**
- Toda la separación entre elementos usa la escala `$spacing-*`
- Padding interno de secciones: mínimo `$spacing-12` vertical en mobile, `$spacing-16` en desktop
- Gap entre cards del grid: `$spacing-8`

**Responsividad:**
- Siempre mobile-first: el estilo base es para mobile, usar `@include md` para tablet, `@include lg` para desktop
- Nunca usar breakpoints con valores numéricos directos. Usar `$breakpoint-md`, `@include md`, etc.

**Variables legacy:** El archivo `_variables.scss` contiene aliases de compatibilidad (`$color_primary`, `$font_size_base`, etc.) que NO deben usarse en código nuevo. Solo usar la nomenclatura con guiones: `$color-primary-500`, `$font-size-base`.

---

### REQ-010: Estructura de archivos — Convenio para nuevos componentes

Cada nuevo componente visual debe cumplir exactamente con este patrón:

```
1. _includes/components/{component-name}.html   ← HTML del componente
2. _sass/components/_{component-name}.scss       ← Estilos del componente
3. assets/css/style.scss                         ← @import del SCSS (obligatorio)
```

El componente HTML usa clases BEM: `.component-name`, `.component-name__element`, `.component-name--modifier`.

No se acepta CSS inline en templates Liquid salvo para `background-image` en heroes con imagen dinámica de Contentful (único caso justificado).

---

## VERIFICACIÓN POST-IMPLEMENTACIÓN

Después de implementar las fases 1 y 2, verificar:

**Para `/blog/`:**
- [ ] El breadcrumb muestra "Home / Blog" con separador `/` y sin numeración
- [ ] Hay un header con gradiente gris, título "Blog" y descripción
- [ ] El grid de posts muestra 1 columna en mobile, 2 en tablet, 3 en desktop
- [ ] Las post cards muestran imagen, categoría badge, título, fecha y "Read More →"

**Para `/blog/bmad-method-experience/`:**
- [ ] El hero ocupa el ancho completo con la imagen de fondo
- [ ] El título "BMad Method Experience" aparece en texto blanco sobre la imagen
- [ ] El byline (autor, fecha, tiempo de lectura, categoría) aparece en texto pequeño gris claro
- [ ] Los íconos SVG son pequeños (16px) y están alineados inline con el texto
- [ ] El contenido del artículo usa el contenedor narrow (max 720px, centrado)
- [ ] El botón "← Back to Blog Archive" aparece al final del contenido

**Para nuevas entradas:**
- [ ] Un nuevo blog post creado en Contentful sin campo `heroBanner` muestra automáticamente su `featured_image` como hero de fondo
- [ ] El badge de categoría aparece en el hero con el color correcto según su variante
- [ ] La página `/blog/` lista el nuevo post automáticamente sin cambios de código

---

## ORDEN DE EJECUCIÓN RECOMENDADO

```
1. REQ-001  Crear _post-byline.scss + importar en style.scss
2. REQ-002  Crear _breadcrumb.scss + importar en style.scss
3. REQ-003  Crear blog-page-en.yml + blog-page-es.yml + actualizar blog-archive.html
4. REQ-004  Rediseñar post-layout.html con hero de imagen de fondo
5. REQ-005  Actualizar blog_post_transformer.py para procesar heroBanner
6. REQ-006  Crear schema blogListingPage + transformer + registrar en pipeline
7. REQ-007–010  Aplicar como reglas en revisiones de código y nuevas entradas
```

Las fases 1 y 2 (REQ-001 a REQ-005) son correcciones que no requieren tocar Contentful y resuelven el 90% de los problemas visuales. REQ-006 es la mejora estructural que hace el sitio completamente headless y escalable.
