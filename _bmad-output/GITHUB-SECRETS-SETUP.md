# 🔐 GitHub Secrets Setup Guide

**Issue:** Workflow fails with "Missing required environment variables"  
**Solution:** Add Contentful credentials to GitHub repository secrets (2 minutes)

---

## 🚀 **Quick Setup (Step-by-Step)**

### **Step 1: Open GitHub Secrets Settings**

Click this link (opens in new tab):

**[https://github.com/ssalazara/ssalazara.github.io/settings/secrets/actions](https://github.com/ssalazara/ssalazara.github.io/settings/secrets/actions)**

Or manually:
1. Go to your repository: https://github.com/ssalazara/ssalazara.github.io
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions** (in left sidebar)

---

### **Step 2: Add CONTENTFUL_SPACE_ID**

1. Click **"New repository secret"** button (green button, top right)
2. **Name:** `CONTENTFUL_SPACE_ID`
3. **Secret:** `co4wdyhrijid`
4. Click **"Add secret"**

**✅ First secret added!**

---

### **Step 3: Add CONTENTFUL_ACCESS_TOKEN**

1. Click **"New repository secret"** again
2. **Name:** `CONTENTFUL_ACCESS_TOKEN`
3. **Secret:** Copy from your `.env` file (the long token starting with `5WtbBRlN...`)
4. Click **"Add secret"**

**✅ Second secret added!**

---

### **Step 4: Add CONTENTFUL_PREVIEW_TOKEN (Optional)**

Only needed for preview deployments:

1. Click **"New repository secret"** again
2. **Name:** `CONTENTFUL_PREVIEW_TOKEN`
3. **Secret:** Copy from your `.env` file (the long token starting with `9pnndU...`)
4. Click **"Add secret"**

**✅ Third secret added!**

---

## 📋 **Verification Checklist**

After adding secrets, you should see:

- [x] **CONTENTFUL_SPACE_ID** - created X minutes ago
- [x] **CONTENTFUL_ACCESS_TOKEN** - created X minutes ago
- [x] **CONTENTFUL_PREVIEW_TOKEN** - created X minutes ago (optional)

**Screenshot:** The secrets page should show 3 secrets (values are hidden for security).

---

## 🔄 **Step 5: Re-Run the Workflow**

After adding secrets:

**Option A: Wait for automatic trigger (1 minute)**
- Just wait - the next push will use the secrets

**Option B: Manually trigger (instant)**
1. Go to: https://github.com/ssalazara/ssalazara.github.io/actions
2. Click "**Production Deploy**" (left sidebar)
3. Click **"Run workflow"** button (top right)
4. Keep branch as `main`
5. Click **"Run workflow"** (green button)
6. Watch the workflow run with secrets available ✅

---

## ⚠️ **Security Notes**

### **What Are GitHub Secrets?**
- Encrypted environment variables stored in your repository
- Never exposed in logs or public views
- Only accessible to GitHub Actions workflows
- Cannot be viewed after creation (only updated/deleted)

### **What Tokens Do:**
- **CONTENTFUL_SPACE_ID**: Identifies your Contentful space
- **CONTENTFUL_ACCESS_TOKEN**: Read access to published content (Delivery API)
- **CONTENTFUL_PREVIEW_TOKEN**: Read access to draft content (Preview API)

### **Safety:**
- ✅ Safe to use in public repositories
- ✅ Tokens are read-only (cannot modify content)
- ✅ Can be revoked anytime in Contentful dashboard
- ❌ Never commit `.env` file to git (already in `.gitignore`)

---

## 🎯 **Expected Result**

After adding secrets and re-running workflow:

**Before:**
```
❌ CONFIG_ERROR: Missing required environment variables
Error: Process completed with exit code 1
```

**After:**
```
✅ CONFIG_LOADED space_id=co4wdyhrijid mode=production
✅ CLIENT_INITIALIZED space_id=co4wdyhrijid
✅ TRANSFORM_SUCCESS
📊 BUILD_COMPLETE duration=1.4s total_entries=6 successful=6
```

---

## 🚀 **Quick Action Commands**

### **Copy Secrets from .env (for reference)**

Run this to see your values:

```bash
cd /Users/simon.salazar/Documents/Apply\ Digital/github-page
cat .env | grep "^CONTENTFUL_"
```

**Output:**
```
CONTENTFUL_SPACE_ID=co4wdyhrijid
CONTENTFUL_ACCESS_TOKEN=5WtbBRlN... (copy full value)
CONTENTFUL_PREVIEW_TOKEN=9pnndU... (copy full value)
```

**Copy these values into GitHub Secrets (one at a time)**

---

## 📝 **Troubleshooting**

### **Issue: "Secret name already exists"**
**Solution:** The secret exists but has wrong value
- Click the secret name
- Click "Update secret"
- Paste new value
- Click "Update secret"

### **Issue: "Workflow still fails after adding secrets"**
**Solution:** Secrets might be added but workflow hasn't re-run
- Wait 1 minute for automatic trigger, OR
- Manually trigger workflow (see Step 5 Option B)

### **Issue: "Cannot find secrets page"**
**Solution:** You might not have admin access to the repository
- Ensure you're the repository owner
- If org repo, ensure you have admin permissions
- Try opening the direct link: https://github.com/ssalazara/ssalazara.github.io/settings/secrets/actions

---

## ✅ **Completion Checklist**

- [ ] Opened GitHub Secrets page
- [ ] Added `CONTENTFUL_SPACE_ID`
- [ ] Added `CONTENTFUL_ACCESS_TOKEN`
- [ ] Added `CONTENTFUL_PREVIEW_TOKEN` (optional)
- [ ] Verified all 3 secrets appear in list
- [ ] Re-ran workflow (or waited for next push)
- [ ] Workflow succeeded with green checkmarks ✅
- [ ] Site is live at https://ssalazara.github.io/

---

## 🎯 **Next Steps After Setup**

Once secrets are working and workflow succeeds:

1. ✅ **Verify homepage is live**
   - Visit: https://ssalazara.github.io/
   - Should see hero banner

2. ✅ **Fix Contentful homepage URL**
   - Change `/simon` to `/`
   - Re-run transformation

3. ✅ **Complete Part B**
   - Add profile + blog carousel to homepage
   - Full Epic 4 completion

---

**Do this now - it only takes 2 minutes!** 🚀

**Direct link to add secrets:** [GitHub Secrets Settings](https://github.com/ssalazara/ssalazara.github.io/settings/secrets/actions)
