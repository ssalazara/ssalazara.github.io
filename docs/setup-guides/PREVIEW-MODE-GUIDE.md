# Preview Mode Guide - Draft Content Review

**Date:** 2026-01-20  
**Repository:** ssalazara/ssalazara.github.io  
**Purpose:** Preview draft content before publishing to production

---

## 🎯 What is Preview Mode?

**Preview Mode** lets you see how draft (unpublished) content will look on your live site BEFORE you hit publish.

**Use Cases:**
- ✍️ Review blog post formatting before going live
- 🎨 Check images and layout with real data
- 📝 Proofread content in production environment
- 👥 Share draft with colleagues for feedback
- 🐛 Test content changes without affecting live site

---

## 🔄 Production vs Preview Mode

| Feature | Production Mode | Preview Mode |
|---------|----------------|--------------|
| **API** | Delivery API | Preview API |
| **Content** | Published only | Published + Drafts |
| **Trigger** | Automatic (webhook/push) | Manual dispatch |
| **Use Case** | Live site updates | Draft review |
| **URL** | Same (ssalazara.github.io) | Same (temporarily) |
| **Duration** | Permanent | Until next deploy |

⚠️ **Important:** Preview mode temporarily overwrites your live site. This is a simplified MVP approach suitable for low-traffic personal blogs.

---

## 🚀 How to Use Preview Mode

### Step 1: Create Draft Content in Contentful

1. **Go to Contentful:**
   - Visit: https://app.contentful.com
   - Space: ssa-personal

2. **Create or Edit Entry:**
   - Content → Entries → Add entry (or edit existing)
   - Content Type: Blog Post (blogPage)

3. **Fill in Fields:**
   - Title, slug, description, author, publishDate
   - Featured image
   - Body content (rich text)
   - SEO metadata

4. **Save as Draft:**
   - Click: **Save** (top right)
   - **DO NOT click Publish yet!**
   - Status shows: **Draft** or **Changed** (yellow indicator)

### Step 2: Trigger Preview Workflow

**Option A: Via GitHub UI (Easiest)**

1. **Go to GitHub Actions:**
   - Visit: https://github.com/ssalazara/ssalazara.github.io/actions

2. **Select Preview Workflow:**
   - Left sidebar → Click: **"Preview Deploy"**

3. **Run Workflow:**
   - Click: **"Run workflow"** (button on right)
   - Branch: `main` (default)
   - Locale: `all` (or select `en` / `es`)
   - Click: **"Run workflow"** (green button)

4. **Monitor Progress:**
   - Workflow appears in list (yellow dot = running)
   - Click workflow run to see live logs
   - Takes ~3-5 minutes

**Option B: Via GitHub CLI (Advanced)**

```bash
# Install GitHub CLI (if not installed)
brew install gh  # macOS
# or: https://cli.github.com/

# Authenticate
gh auth login

# Trigger preview workflow
gh workflow run "Preview Deploy" \
  --repo ssalazara/ssalazara.github.io \
  --ref main \
  --field locale=all

# Watch workflow run
gh run watch
```

### Step 3: View Preview

1. **Wait for Deployment:**
   - GitHub Actions workflow completes (green checkmark)
   - GitHub Pages deployment finishes (~1 min after workflow)

2. **Visit Your Site:**
   - URL: https://ssalazara.github.io
   - Your draft content is now visible!

3. **Review Content:**
   - Check formatting, images, layout
   - Test on mobile/tablet/desktop
   - Proofread text
   - Verify links work

### Step 4: Publish or Revert

**If Content Looks Good:**

1. **Go back to Contentful**
2. **Open your draft entry**
3. **Click: Publish** (top right)
4. **Webhook auto-triggers production deploy**
5. **Production content replaces preview** (~3-5 min)

**If You Want to Revert Preview:**

1. **Trigger production workflow manually:**
   - GitHub Actions → Production Deploy → Run workflow
2. **Or:** Just wait - next content publish will overwrite preview
3. **Or:** Push any code change to main branch (triggers production deploy)

---

## 🔧 How Preview Mode Works Technically

### Architecture:

```
Preview Workflow:
1. Fetch from Contentful Preview API (drafts + published)
2. Transform content to Jekyll files
3. Build Jekyll site
4. Deploy to GitHub Pages (same branch as production)
5. Preview content temporarily live
```

### Environment Variables:

**Production Mode:**
```bash
CONTENTFUL_MODE=production
CONTENTFUL_ACCESS_TOKEN=<delivery-api-token>
```

**Preview Mode:**
```bash
CONTENTFUL_MODE=preview
CONTENTFUL_PREVIEW_TOKEN=<preview-api-token>
```

### Code Implementation:

The Python script (`scripts/contentful_to_jekyll.py`) checks `CONTENTFUL_MODE`:

```python
# In scripts/contentful_client/client.py
if mode == 'preview':
    self.client = contentful.Client(
        space_id,
        preview_token,
        api_url='preview.contentful.com'  # Preview API
    )
else:
    self.client = contentful.Client(
        space_id,
        access_token  # Delivery API (published only)
    )
```

---

## 📋 Preview Workflow Configuration

**File:** `.github/workflows/preview-deploy.yml`

**Key Differences from Production:**

```yaml
# Trigger: Manual only (no webhook)
on:
  workflow_dispatch:
    inputs:
      locale:
        description: 'Locale to preview'
        type: choice
        options: [all, en, es]

# Environment: Preview mode
env:
  CONTENTFUL_MODE: preview
  CONTENTFUL_PREVIEW_TOKEN: ${{ secrets.CONTENTFUL_PREVIEW_TOKEN }}
```

---

## 🎨 Advanced: Preview-Specific Features

### Locale Selection:

When triggering preview, you can choose:
- **`all`** - Preview both EN and ES content (default)
- **`en`** - Preview only English content
- **`es`** - Preview only Spanish content

**Use Case:** If you only changed English content, preview just `en` to save build time.

### Preview with Specific Branch:

Currently preview always uses `main` branch code. To preview with code changes:

1. **Create feature branch:**
   ```bash
   git checkout -b feature/new-layout
   # Make code changes
   git push origin feature/new-layout
   ```

2. **Modify workflow trigger:**
   - Edit `.github/workflows/preview-deploy.yml`
   - Change `on.workflow_dispatch` to allow branch selection
   - Or: Manually trigger from feature branch in GitHub UI

---

## 🚨 Important Limitations

### ⚠️ Preview Overwrites Live Site

**Current Behavior:**
- Preview deploys to same GitHub Pages site as production
- Your live site temporarily shows draft content
- Lasts until next production deploy

**Why:**
- Simplified MVP approach
- No need for separate preview domain/branch
- Acceptable for personal blog with low traffic

**Mitigation:**
- Only preview during low-traffic times
- Or: Preview late at night / early morning
- Or: Warn visitors (add banner: "Preview mode active")

### 🔄 No Automatic Revert

**Current Behavior:**
- Preview stays live until you manually revert or publish

**To Revert:**
- Trigger production workflow manually
- Or: Publish content in Contentful (triggers production)
- Or: Push code to main branch

### 🌐 Single Preview at a Time

**Current Behavior:**
- Only one preview can be live at a time
- New preview overwrites previous preview

**For Multiple Previews:**
- Would need separate preview branches/domains (future enhancement)

---

## 🎯 Best Practices

### ✅ DO:
- Preview during low-traffic hours
- Review on multiple devices (mobile, tablet, desktop)
- Test all links and images
- Check SEO metadata (view page source)
- Proofread carefully before publishing

### ❌ DON'T:
- Preview during peak traffic hours (if you have significant traffic)
- Leave preview live for extended periods
- Preview sensitive/confidential content (it's publicly accessible)
- Forget to publish or revert after reviewing

---

## 🔍 Troubleshooting

### Preview Workflow Not Running:

**Check:**
- GitHub Secrets include `CONTENTFUL_PREVIEW_TOKEN`
- Workflow file exists: `.github/workflows/preview-deploy.yml`
- You have permission to trigger workflows (repo admin/write access)

### Preview Shows Old Content:

**Cause:** Jekyll cache or GitHub Pages cache

**Fix:**
1. Wait 2-3 minutes for GitHub Pages to update
2. Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
3. Clear browser cache
4. Try incognito/private window

### Preview Shows Published Content Only:

**Cause:** Using wrong token or wrong mode

**Fix:**
1. Verify GitHub Secret `CONTENTFUL_PREVIEW_TOKEN` is set
2. Check workflow logs - should show `CONTENTFUL_MODE: preview`
3. Verify token is Preview API token (not Delivery API token)

### Draft Content Not Appearing:

**Cause:** Entry not saved as draft in Contentful

**Fix:**
1. In Contentful, verify entry status is "Draft" or "Changed"
2. Ensure entry has all required fields filled
3. Check Contentful Preview API directly (test with curl)

---

## 🔐 Security Considerations

### Preview API Token:

- **Scope:** Read-only access to drafts + published content
- **Storage:** GitHub Secrets (encrypted)
- **Rotation:** Rotate every 6-12 months
- **Exposure Risk:** If exposed, drafts become publicly readable

### Public Preview:

- **Visibility:** Preview content is publicly accessible
- **SEO:** Not indexed (same URL as production, temporary)
- **Confidentiality:** Don't preview sensitive content

---

## 📊 Preview Workflow Metrics

**Expected Performance:**
- **Trigger to Start:** < 10 seconds
- **Python Transformation:** ~5-10 seconds
- **Jekyll Build:** ~30-60 seconds
- **GitHub Pages Deploy:** ~1-2 minutes
- **Total:** ~3-5 minutes

**Monitoring:**
- Check GitHub Actions logs for timing
- Python script logs build duration
- Warning if > 2 minutes for transformation

---

## 🚀 Future Enhancements (Out of Scope)

### Separate Preview Environment:

**Setup:**
1. Create `gh-pages-preview` branch
2. Configure separate GitHub Pages site
3. Point custom subdomain: `preview.ssalazara.com`
4. Update preview workflow to deploy to preview branch

**Benefits:**
- Preview doesn't affect live site
- Multiple previews possible
- Permanent preview URL

**Tradeoffs:**
- More complex setup
- Requires custom domain
- Additional DNS configuration

### Preview Comments/Annotations:

**Feature:** Add visual indicators on preview site
- Banner: "Preview Mode - Draft Content"
- Highlight draft posts with badge
- Show last preview date/time

**Implementation:**
- Add preview mode flag to Jekyll build
- Conditional rendering in layouts
- CSS styling for preview indicators

---

## 📞 Quick Reference

**Trigger Preview:**
```
GitHub → Actions → Preview Deploy → Run workflow
```

**Revert Preview:**
```
GitHub → Actions → Production Deploy → Run workflow
```

**Check Status:**
```
GitHub → Actions → [View workflow run logs]
```

**View Live Site:**
```
https://ssalazara.github.io
```

---

**Last Updated:** 2026-01-20  
**Status:** Production ready ✅  
**Limitation:** Preview overwrites live site temporarily (acceptable for MVP)
