# 🔗 GitHub Pages URL Routing Guide

**Date:** 2026-01-19  
**Issue:** Understanding URL structure for `ssalazara.github.io` vs repository name

---

## 🚨 **Current Problem**

You mentioned creating a repository named **"simon"**, but your desired URL is `https://ssalazara.github.io/` (root domain). There's a mismatch that needs to be resolved.

---

## 📋 **GitHub Pages URL Rules**

### **Rule 1: User/Organization Site (Root Domain)**
- **Repository Name:** MUST be `{username}.github.io`
- **Deployed URL:** `https://{username}.github.io/`
- **Example:** Repository `ssalazara.github.io` → `https://ssalazara.github.io/`

### **Rule 2: Project Site (Subdirectory)**
- **Repository Name:** Any other name (e.g., `simon`, `portfolio`, `blog`)
- **Deployed URL:** `https://{username}.github.io/{repository-name}/`
- **Example:** Repository `simon` → `https://ssalazara.github.io/simon/`

---

## 🎯 **Your Current Configuration**

### **What You Have:**

**In `_config.yml`:**
```yaml
baseurl: ""  # Empty = expects root domain
url: "https://ssalazara.github.io"  # Root domain URL
```

**In `index.html`:**
```yaml
permalink: /  # Homepage at root
```

**In `blog/index.html`:**
```yaml
permalink: /en/blog/  # Blog at /en/blog/
```

**In Contentful (`homepage-en.yml`):**
```yaml
url: /simon  # ⚠️ This is WRONG if you want root domain!
```

### **What This Configuration Expects:**
- ✅ Repository name: `ssalazara.github.io`
- ✅ Homepage URL: `https://ssalazara.github.io/`
- ✅ Blog URL: `https://ssalazara.github.io/en/blog/`
- ❌ Contentful homepage URL should be `/` not `/simon`

---

## 🔧 **Two Scenarios & Solutions**

### **Scenario A: Root Domain Deployment (Recommended)**

**If you want:** `https://ssalazara.github.io/`

**Requirements:**
1. ✅ Repository name: `ssalazara.github.io` (NOT "simon")
2. ✅ `_config.yml` stays as-is (baseurl: "")
3. ❌ Fix Contentful homepage entry: Change URL from `/simon` to `/`

**URL Structure:**
```
Homepage:     https://ssalazara.github.io/
Blog Archive: https://ssalazara.github.io/en/blog/
Blog Post:    https://ssalazara.github.io/en/blog/my-first-post/
Spanish Home: https://ssalazara.github.io/es/
Spanish Blog: https://ssalazara.github.io/es/blog/
```

**Action Required:**
```bash
# 1. Rename your GitHub repository to: ssalazara.github.io

# 2. Update Contentful homepage entry:
# Login to Contentful → Homepage entry → Change "url" field from "/simon" to "/"

# 3. Re-run transformation:
cd /path/to/project
source venv/bin/activate
PYTHONPATH=$(pwd) python scripts/contentful_to_jekyll.py

# 4. Rebuild Jekyll:
bundle exec jekyll build
```

---

### **Scenario B: Project Site Deployment**

**If you want:** `https://ssalazara.github.io/simon/`

**Requirements:**
1. ✅ Repository name: `simon` (or keep current name)
2. ❌ Update `_config.yml`: Change `baseurl: "/simon"`
3. ✅ Contentful homepage URL `/simon` is correct

**Update `_config.yml`:**
```yaml
baseurl: "/simon"  # Must match repository name!
url: "https://ssalazara.github.io"
```

**URL Structure:**
```
Homepage:     https://ssalazara.github.io/simon/
Blog Archive: https://ssalazara.github.io/simon/en/blog/
Blog Post:    https://ssalazara.github.io/simon/en/blog/my-first-post/
Spanish Home: https://ssalazara.github.io/simon/es/
Spanish Blog: https://ssalazara.github.io/simon/es/blog/
```

**Action Required:**
```bash
# 1. Update _config.yml (add baseurl)

# 2. Update all internal links in layouts to use {{ site.baseurl }}

# 3. Rebuild:
bundle exec jekyll build

# 4. GitHub Pages will automatically deploy to /simon/
```

---

## ✅ **Recommended Solution: Scenario A (Root Domain)**

**Why?**
- ✅ Cleaner URLs (`ssalazara.github.io` vs `ssalazara.github.io/simon`)
- ✅ Better for SEO (root domain has more authority)
- ✅ Simpler configuration (no baseurl needed)
- ✅ Standard practice for personal portfolios

**Steps to Fix:**

### **Step 1: Rename GitHub Repository**
1. Go to GitHub: `https://github.com/{your-username}/simon/settings`
2. Scroll to "Repository name"
3. Change from `simon` to `ssalazara.github.io`
4. Click "Rename"

### **Step 2: Update Contentful Homepage Entry**
1. Login to Contentful: `https://app.contentful.com`
2. Navigate to Content → Homepage entry
3. Change `url` field from `/simon` to `/`
4. Publish the entry

### **Step 3: Re-Run Transformation**
```bash
cd /Users/simon.salazar/Documents/Apply\ Digital/github-page
source venv/bin/activate
PYTHONPATH=$(pwd) python scripts/contentful_to_jekyll.py
```

### **Step 4: Verify & Deploy**
```bash
# Check homepage URL is now "/"
cat _data/homepage-en.yml | grep "url:"
# Should show: url: /

# Rebuild Jekyll
bundle exec jekyll build

# Push to GitHub
git add .
git commit -m "Fix: Update homepage URL to root"
git push origin main
```

### **Step 5: Configure GitHub Pages**
1. Go to repository Settings → Pages
2. Source: Deploy from branch `main` (or `gh-pages`)
3. Folder: `/ (root)` or custom folder if using Actions
4. Wait 1-2 minutes for deployment
5. Visit `https://ssalazara.github.io/`

---

## 📊 **How Blog URLs Work**

### **With Contentful Content Model:**

**Blog Posts are generated dynamically:**
- **Source:** Contentful `blogPage` content type
- **Transformation:** `scripts/contentful_to_jekyll.py` → `_posts/en/*.md`
- **Jekyll Processing:** Posts → HTML at `/{lang}/blog/{slug}/`
- **URL Pattern:** Defined in `_config.yml` → `permalink: /:lang/blog/:slug/`

**Example Flow:**
```
1. Create blog post in Contentful:
   - Title: "My First Post"
   - Slug: "my-first-post"
   - Locale: en-US

2. Run transformation script:
   → Generates: _posts/en/2026-01-19-my-first-post.md

3. Jekyll builds:
   → Generates: _site/en/blog/my-first-post/index.html

4. Final URL:
   → https://ssalazara.github.io/en/blog/my-first-post/
```

### **Blog Archive Page:**
- **File:** `blog/index.html`
- **Permalink:** `/en/blog/`
- **URL:** `https://ssalazara.github.io/en/blog/`
- **Content:** Lists all blog posts (generated by `blog-archive` layout)

---

## 🎨 **Can You Create `/blog/` with Content Model?**

**Short Answer:** Partially, but NOT recommended.

**Current Setup (Recommended):**
- ✅ Blog **posts** created in Contentful (`blogPage` content type)
- ✅ Blog **archive page** is a Jekyll layout (`blog/index.html`)
- ✅ Jekyll automatically lists all posts on archive page

**Alternative (Not Recommended):**
- Create a Contentful `blogArchivePage` content type
- Add fields for title, description, filters, etc.
- Transform to Jekyll data file
- Render archive page dynamically

**Why Current Approach is Better:**
1. ✅ Blog archive is mostly static layout (doesn't need frequent changes)
2. ✅ Jekyll automatically handles post listing, pagination, filtering
3. ✅ Less complexity in Contentful content model
4. ✅ Faster builds (no extra API calls)

**What IS in Contentful:**
- ✅ Blog post content (title, body, images, metadata)
- ✅ SEO metadata
- ✅ Author information
- ✅ Featured images

**What is NOT in Contentful:**
- ❌ Blog archive page structure (hardcoded in Jekyll)
- ❌ Post listing logic (handled by Jekyll)
- ❌ Pagination (handled by Jekyll plugins)

---

## 🔍 **Testing Your URLs**

### **Local Testing:**
```bash
# Start Jekyll server
bundle exec jekyll serve

# Test URLs:
http://localhost:4000/              # Homepage (with hero banner)
http://localhost:4000/en/blog/      # Blog archive
http://localhost:4000/es/           # Spanish homepage
http://localhost:4000/es/blog/      # Spanish blog
```

### **Production Testing (After Deploy):**
```bash
# Check if site is live:
curl -I https://ssalazara.github.io/

# Expected response:
# HTTP/2 200
# content-type: text/html
```

---

## 📝 **Summary & Recommendation**

### **Current Issue:**
- ❌ Repository name might be "simon" (deploys to `/simon/`)
- ❌ Contentful homepage has `url: /simon`
- ✅ Jekyll config expects root domain (`baseurl: ""`)
- **Result:** Mismatch between expected and actual URLs

### **Recommended Fix:**
1. ✅ Rename repository to `ssalazara.github.io`
2. ✅ Update Contentful homepage URL from `/simon` to `/`
3. ✅ Re-run transformation script
4. ✅ Deploy to GitHub Pages

### **Result:**
```
✅ Homepage:     https://ssalazara.github.io/
✅ Blog Archive: https://ssalazara.github.io/en/blog/
✅ Blog Posts:   https://ssalazara.github.io/en/blog/{slug}/
✅ Spanish Site: https://ssalazara.github.io/es/
```

---

## ❓ **Questions to Answer**

Before proceeding, please confirm:

1. **What is your actual GitHub repository name?**
   - [ ] `ssalazara.github.io` (root domain)
   - [ ] `simon` (project site)
   - [ ] Something else: _______

2. **Which URL do you prefer?**
   - [ ] `https://ssalazara.github.io/` (Recommended - cleaner)
   - [ ] `https://ssalazara.github.io/simon/` (Works but longer)

3. **Are you okay with renaming the repository?**
   - [ ] Yes, rename to `ssalazara.github.io`
   - [ ] No, keep current name and adjust config

---

**Once you answer these questions, I'll proceed with:**
1. Fixing the URL configuration
2. Continuing with the next epic/story implementation

Let me know your preference! 🚀
