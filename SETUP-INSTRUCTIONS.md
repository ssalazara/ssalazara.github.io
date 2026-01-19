# 🚀 Instrucciones de Configuración - Landing Page

## ❌ Problema Actual

Tu sitio https://ssalazara.github.io/ genera 404 porque:
1. ✅ **RESUELTO**: URL corregida en `_config.yml` 
2. ✅ **RESUELTO**: Ruby 3.2.2 y Jekyll instalados
3. ✅ **RESUELTO**: Python y dependencias instaladas
4. ❌ **PENDIENTE**: Contentful no tiene locales configurados (EN/ES)
5. ❌ **PENDIENTE**: No hay contenido generado en `_posts/` y `_data/`

## 🔧 Paso 1: Configurar Locales en Contentful (CRÍTICO)

### Opción A: Configurar EN/ES en Contentful (Recomendado)

1. **Ve a Contentful Dashboard**: https://app.contentful.com/spaces/co4wdyhrijid/settings/locales

2. **Agregar locale "English (United States)"**:
   - Click en "Add locale"
   - Name: `English (United States)`
   - Code: `en-US`
   - Fallback: None (es el default)
   - Click "Save"

3. **Agregar locale "Spanish (Spain)"**:
   - Click en "Add locale"
   - Name: `Spanish (Spain)` 
   - Code: `es-ES`
   - Fallback: `en-US`
   - Click "Save"

### Opción B: Usar el locale existente (Más rápido para testing)

Si Contentful ya tiene un locale configurado (por ejemplo `en-US` o solo `en`), podemos adaptar el script.

**Para verificar qué locales tienes**:
1. Ve a: https://app.contentful.com/spaces/co4wdyhrijid/settings/locales
2. Anota el código exacto del locale (ej: `en-US`, `es-ES`, etc.)

**Luego edita** `scripts/config.py` y cambia:
```python
# Línea ~20
LOCALES = ['en-US', 'es-ES']  # Usa los códigos exactos de Contentful
```

## 🔧 Paso 2: Crear Contenido en Contentful

Una vez que los locales estén configurados, necesitas crear contenido:

### 2.1 Importar Content Model (Schemas)

```bash
cd "/Users/simon.salazar/Documents/Apply Digital/github-page"

# Instalar Contentful CLI (si no lo tienes)
npm install -g contentful-cli

# Autenticarse
contentful login

# Importar schemas
./push-contentful-schemas.sh
```

### 2.2 Crear Contenido Mínimo

En Contentful, crea al menos:

1. **Profile** (Singleton - solo 1 instancia):
   - Name: Tu nombre
   - Title: Tu título profesional
   - Bio: Descripción corta
   - Photo: URL de tu foto

2. **Header** (orHeader):
   - Logo: Texto o imagen
   - Menu Items: Links de navegación

3. **Footer** (orFooter):
   - Copyright text
   - Social links

4. **Blog Post** (blogTemplate) - Al menos 1:
   - Title: Título del post
   - Slug: url-del-post
   - Body: Contenido en Rich Text
   - Publish Date: Fecha
   - SEO: Linked SEO entry (REQUERIDO)

5. **SEO** (para cada blog post):
   - Title: SEO title
   - Description: Meta description
   - Keywords: Palabras clave

## 🔧 Paso 3: Generar Contenido Localmente

Una vez que Contentful tenga contenido:

```bash
cd "/Users/simon.salazar/Documents/Apply Digital/github-page"

# Activar virtualenv
source venv/bin/activate

# Ejecutar transformación
PYTHONPATH=. python scripts/contentful_to_jekyll.py

# Deberías ver:
# ✅ TRANSFORM_SUCCESS para cada entrada
# Archivos generados en _posts/en/ y _data/
```

## 🔧 Paso 4: Probar Jekyll Localmente

```bash
# Iniciar Jekyll (en otra terminal o después de la transformación)
export SSL_CERT_FILE=/etc/ssl/cert.pem
eval "$(rbenv init - zsh)"
rbenv global 3.2.2
bundle exec jekyll serve

# Abre: http://localhost:4000
```

## 🔧 Paso 5: Desplegar a GitHub Pages

### 5.1 Verificar GitHub Repository

Tu repo actual: `https://github.com/ssalazara/simon.git`

**Importante**: Para GitHub Pages, el repositorio debe llamarse:
- `ssalazara.github.io` (para user page en https://ssalazara.github.io/)
- O usar el nombre actual `simon` (para project page en https://ssalazara.github.io/simon/)

### 5.2 Opción A: Renombrar Repositorio (Recomendado)

1. Ve a: https://github.com/ssalazara/simon/settings
2. En "Repository name", cambia `simon` a `ssalazara.github.io`
3. Click "Rename"

Esto hará que tu sitio esté en: **https://ssalazara.github.io/**

### 5.3 Opción B: Usar Project Page

Si quieres mantener el nombre `simon`, tu sitio estará en:
**https://ssalazara.github.io/simon/**

En ese caso, edita `_config.yml`:
```yaml
baseurl: "/simon"  # Cambiar de "" a "/simon"
```

### 5.4 Configurar GitHub Secrets

1. Ve a: https://github.com/ssalazara/simon/settings/secrets/actions
2. Agrega estos secrets:

```
CONTENTFUL_SPACE_ID = co4wdyhrijid
CONTENTFUL_ACCESS_TOKEN = 5WtbBRlNlDO9-rpEMs01AiKT_PQxU6j1dbPh9zeTogo
CONTENTFUL_PREVIEW_TOKEN = 9pnndUO33gOF5G3SJ3Kb7jrjB8MwUBqzs1on87XUCI0
```

### 5.5 Habilitar GitHub Pages

1. Ve a: https://github.com/ssalazara/simon/settings/pages
2. **Source**: GitHub Actions (no "Deploy from branch")
3. Guarda los cambios

### 5.6 Hacer Push y Desplegar

```bash
cd "/Users/simon.salazar/Documents/Apply Digital/github-page"

# Agregar cambios
git add _config.yml scripts/requirements.txt

# Commit
git commit -m "fix: Update URL and dependencies for deployment"

# Push a main
git push origin main
```

Esto disparará el workflow de GitHub Actions que:
1. Ejecuta el script Python (transforma Contentful → Jekyll)
2. Construye el sitio con Jekyll
3. Despliega a GitHub Pages

## 📊 Verificación Final

Después del deploy (toma ~3-5 minutos):

1. **Verifica el workflow**: https://github.com/ssalazara/simon/actions
2. **Visita tu sitio**: 
   - https://ssalazara.github.io/ (si renombraste el repo)
   - https://ssalazara.github.io/simon/ (si usaste project page)

## 🆘 Troubleshooting

### Error: "Unknown locale"
- Ve a Contentful > Settings > Locales
- Verifica que `en-US` y `es-ES` (o los que uses) estén configurados
- Actualiza `scripts/config.py` con los códigos exactos

### Error: "No content found"
- Verifica que hayas creado al menos 1 blog post en Contentful
- Verifica que el post esté **publicado** (no draft)
- Verifica que tenga un SEO entry linked

### Error: Jekyll no inicia
- Verifica que Ruby 3.2.2 esté activo: `ruby --version`
- Ejecuta: `eval "$(rbenv init - zsh)"`
- Ejecuta: `rbenv global 3.2.2`
- Ejecuta: `export SSL_CERT_FILE=/etc/ssl/cert.pem`
- Ejecuta: `bundle install`

### Sitio muestra 404
- Verifica que el nombre del repo sea `ssalazara.github.io` o que `baseurl` esté configurado
- Verifica que GitHub Pages esté habilitado en Settings > Pages
- Verifica que el workflow haya completado exitosamente

## 📚 Próximos Pasos

Una vez que el sitio funcione:

1. **Crear más contenido** en Contentful
2. **Configurar webhook** para auto-deploy en cada publicación
3. **Personalizar diseño** en `_sass/` y `_layouts/`
4. **Agregar tu foto** y personalizar el profile

---

**¿Necesitas ayuda?** Revisa los logs en:
- GitHub Actions: https://github.com/ssalazara/simon/actions
- Contentful Activity: https://app.contentful.com/spaces/co4wdyhrijid/settings/webhooks
