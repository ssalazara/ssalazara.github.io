# 🔧 URL Routing Fix - Action Checklist

**Goal:** Change from `https://ssalazara.github.io/simon/` to `https://ssalazara.github.io/`

---

## ✅ Step-by-Step Checklist

### 1️⃣ Rename GitHub Repository

- [ ] Go to: https://github.com/ssalazara/simon/settings
- [ ] Scroll to "Repository name" section
- [ ] Change from `simon` to `ssalazara.github.io`
- [ ] Type new name to confirm
- [ ] Click "Rename" button
- [ ] **Result:** Repository is now at `https://github.com/ssalazara/ssalazara.github.io`

---

### 2️⃣ Update Local Git Remote

Open terminal and run:

```bash
cd /Users/simon.salazar/Documents/Apply\ Digital/github-page

# Update remote URL
git remote set-url origin https://github.com/ssalazara/ssalazara.github.io.git

# Verify it worked
git remote -v
```

**Expected output:**
```
origin	https://github.com/ssalazara/ssalazara.github.io.git (fetch)
origin	https://github.com/ssalazara/ssalazara.github.io.git (push)
```

- [ ] Remote URL updated successfully

---

### 3️⃣ Update Contentful Homepage Entry

- [ ] Login to: https://app.contentful.com
- [ ] Navigate to: **Content** tab
- [ ] Find entry: **"Homepage"** or **"Homepage >"**
- [ ] Click to edit
- [ ] Find field: **"URL Slug"** or **"url"**
- [ ] Change value from `/simon` to `/`
- [ ] Click **"Publish"** button (top right)
- [ ] **Confirmation:** Green success message appears

---

### 4️⃣ Re-Run Transformation Script

Open terminal and run:

```bash
cd /Users/simon.salazar/Documents/Apply\ Digital/github-page

# Activate Python virtual environment
source venv/bin/activate

# Run transformation
PYTHONPATH=$(pwd) python scripts/contentful_to_jekyll.py
```

**Expected output:**
```
✅ HERO_BANNER_TRANSFORMED entry_id=...
📊 BUILD_COMPLETE duration=1.4s total_entries=6 successful=6 failed=0
```

- [ ] Transformation completed successfully

---

### 5️⃣ Verify Homepage URL Updated

Run in terminal:

```bash
cat _data/homepage-en.yml | grep "^url:"
```

**Expected output:**
```
url: /
```

**If still shows `/simon`:** Go back to Step 3 and ensure you published the change in Contentful.

- [ ] Homepage URL is now `/` (not `/simon`)

---

### 6️⃣ Rebuild Jekyll Site

Run in terminal:

```bash
bundle exec jekyll build
```

**Expected:** Build completes without errors

- [ ] Jekyll build successful

---

### 7️⃣ Configure GitHub Pages (if not already done)

- [ ] Go to: https://github.com/ssalazara/ssalazara.github.io/settings/pages
- [ ] **Source:** Select "Deploy from a branch"
- [ ] **Branch:** Select `main` (or your default branch)
- [ ] **Folder:** Select `/ (root)`
- [ ] Click **"Save"**
- [ ] Wait for green "Your site is live at..." message (1-2 minutes)

---

### 8️⃣ Test Live Site

- [ ] Visit: https://ssalazara.github.io/
- [ ] **Expected:** Homepage loads with hero banner
- [ ] **Expected:** Title shows "Simon Salazar Albornoz"
- [ ] **Expected:** CTA button says "Learn More"
- [ ] **Expected:** No 404 errors

**Test additional URLs:**
- [ ] Blog archive: https://ssalazara.github.io/en/blog/
- [ ] Spanish homepage: https://ssalazara.github.io/es/

---

## 🐛 Troubleshooting

### Issue: "Repository name already exists"
- **Cause:** Someone else has `ssalazara.github.io` repository
- **Fix:** Ensure you're logged in as `ssalazara` user
- **Alternative:** Contact GitHub support if you believe it's your old repo

### Issue: Homepage still shows `/simon`
- **Cause:** Contentful change not published
- **Fix:** Ensure you clicked "Publish" (not just "Save as draft")
- **Verify:** Check Contentful entry status shows "Published" badge

### Issue: GitHub Pages not building
- **Cause:** GitHub Actions may need configuration
- **Fix:** Check `.github/workflows/` folder exists
- **Alternative:** Push a small change to trigger rebuild: `git commit --allow-empty -m "Trigger deploy" && git push`

### Issue: 404 on homepage
- **Cause:** GitHub Pages source not configured correctly
- **Fix:** Go to Settings > Pages, ensure "Deploy from branch" is selected
- **Check:** Branch should be `main`, folder should be `/ (root)`

---

## ✅ Success Criteria

When complete, you should have:

✅ Repository name: `ssalazara.github.io`  
✅ Live URL: `https://ssalazara.github.io/`  
✅ Homepage data: `url: /`  
✅ Hero banner visible on homepage  
✅ No 404 errors  

---

## 📝 Notes

- GitHub Pages may take 1-2 minutes to deploy after changes
- Clear browser cache if you see old content (`Cmd+Shift+R` on Mac)
- DNS propagation is instant for `github.io` domains
- Once complete, you're ready for Part B (Homepage Integration)!

---

**When all checkboxes are complete, you're ready for Part B!** 🚀

**Questions?** Come back here or check the full guide: `_bmad-output/URL-ROUTING-GUIDE.md`
