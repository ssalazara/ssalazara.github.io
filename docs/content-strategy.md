# Content Strategy — ssalazara.github.io

> **Objetivo:** Página personal como activo de carrera — job-hunting, freelance/consulting lead-gen, credibilidad peer.  
> **Stack:** Contentful CMS → Python → Jekyll → GitHub Pages  
> **Idiomas:** Bilingual (EN + ES) — paridad obligatoria en todo contenido nuevo.

---

## Propuesta de Valor

> Simon Salazar — Ingeniero de software con enfoque en producto.  
> Escribo sobre IA aplicada, estrategia de producto digital y el oficio de construir cosas que importan.

---

## Audiencia Objetivo

| Segmento | Qué busca en el sitio | Contenido prioritario |
|----------|----------------------|----------------------|
| Reclutadores / Hiring managers | Validar experiencia y capacidad de comunicación | Perfil, CV, 2-3 posts técnicos recientes |
| Peers (engineers, PMs) | Perspectivas originales, aprendizajes | Blog — posts técnicos y de reflexión |
| Clientes potenciales (freelance) | Evidencia de trabajo, forma de pensar | Portfolio, CV, posts de proyecto |
| Juniors / estudiantes | Referencia y orientación | Posts de carrera y metodología |

---

## Tipos de Contenido

### 1. Blog Posts (`blogTemplate`) — ✅ Activo
- **Frecuencia:** 2 posts/mes (objetivo sostenible)
- **Extensión:** 600–1500 palabras
- **Categorías:** `ai` · `product` · `engineering` · `career` · `meta`
- **Flujo:** borrador Contentful → preview local → publicar → deploy automático (<5 min)

### 2. Perfil Profesional (`profile`) — ✅ Activo
- **Frecuencia:** Actualización cada 6 meses o tras cambio relevante
- **Campos clave:** bio (corta + larga), foto, título, social links, tecnologías principales

### 3. CV Interactivo (`cvPage`) — 🚧 Por implementar
- **Prioridad:** Alta — máximo impacto para reclutadores
- **Contenido:** experiencia (`experienceItem`), educación (`educationItem`), habilidades (`skillsGroup`)
- **URL:** `/cv/` y `/es/cv/`
- **Ver:** [contentful-schemas/cv-page.json](../contentful-schemas/cv-page.json)

### 4. Portfolio de Proyectos (`componentProjectCard`) — 🚧 Por implementar
- **Prioridad:** Media
- **URL:** `/projects/` y `/es/projects/`

---

## Guía de Voz Editorial

- **Tono:** Directo, reflexivo, con opinión propia. No corporativo.
- **Persona:** Primera persona. "Aprendí", "decidí", "recomiendo" — no "se puede", "se debe".
- **EN:** Escribir en el idioma en que se pensó originalmente el post. Traducir después.
- **ES:** Priorizar si la audiencia principal del post es latinoamericana.
- **Evitar:** Listas de bullet sin contexto, posts sin conclusión accionable, contenido evergreen genérico.

---

## Workflow de Publicación

```
1. Crear borrador en Contentful (modo Preview)
2. Preview local:
     CONTENTFUL_MODE=preview python scripts/contentful_to_jekyll.py
     bundle exec jekyll serve --livereload
3. Revisar en http://localhost:4000
4. Publicar en Contentful
5. Webhook → production-deploy.yml → < 5 min a producción
6. Verificar en https://ssalazara.github.io
```

---

## Plan Editorial Q4 2026

| # | Título tentativo | Categoría | Idioma orig. | Estado | Fecha target |
|---|-----------------|-----------|-------------|--------|-------------|
| 1 | "Mi experiencia con el método BMAD" *(ya publicado — revisar vigencia)* | `meta` | ES | Publicado | 2026-01-21 |
| 2 | "Cómo estructuré mi sitio personal con Jekyll + Contentful + IA" | `engineering` | ES | Borrador | Nov 2026 |
| 3 | "Mi stack de herramientas con IA en 2026: lo que uso, lo que descarté" | `ai` | ES | Idea | Nov 2026 |
| 4 | "Decisiones de arquitectura que tomaría diferente" | `engineering` | EN | Idea | Dic 2026 |

---

## Checklist de Calidad por Post

Antes de publicar en Contentful, verificar:

- [ ] Título claro y específico (no genérico)
- [ ] Excerpt ≤150 chars (se usa en cards y meta description)
- [ ] Cover image cargada en Contentful (assets)
- [ ] Categoría asignada
- [ ] Tags relevantes (3–5 máx)
- [ ] Versión EN + ES ambas escritas
- [ ] Preview verificado localmente antes de publicar
- [ ] Hreflang funciona correctamente (EN ↔ ES)

---

## Sitemap y SEO

- `jekyll-sitemap` plugin activo → genera `/sitemap.xml` en cada build
- `robots.txt` apunta correctamente a `https://ssalazara.github.io/sitemap.xml`
- Registrar sitemap en Google Search Console: https://search.google.com/search-console
- `jekyll-seo-tag` genera Open Graph + Twitter Cards automáticamente desde front matter

---

## Referencias

- [Contentful Schemas](../contentful-schemas/README.md) — estado de implementación de content types
- [Architecture](architecture.md) — pipeline técnico completo
- [Setup Guide](setup-guides/SETUP-INSTRUCTIONS.md) — instrucciones de configuración
