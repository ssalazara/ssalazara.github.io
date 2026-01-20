# Contentful Webhook Setup Guide

**Date:** 2026-01-20  
**Repository:** ssalazara/ssalazara.github.io  
**Purpose:** Auto-deploy to GitHub Pages when content is published in Contentful

---

## 🔑 Step 1: Create GitHub Personal Access Token (PAT)

### Why You Need This:
Contentful needs permission to trigger your GitHub Actions workflow. A PAT is like a password that gives Contentful limited access to your repo.

### Create the Token:

1. **Go to GitHub Settings:**
   - Visit: https://github.com/settings/tokens
   - Or: GitHub.com → Click your profile (top right) → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token (Classic):**
   - Click: **"Generate new token"** → **"Generate new token (classic)"**
   - Note: "Contentful Webhook for ssalazara.github.io"
   - Expiration: **No expiration** (or 1 year if you prefer to rotate)
   
3. **Select Scopes:**
   - ✅ **`repo`** (Full control of private repositories)
     - This includes: repo:status, repo_deployment, public_repo, repo:invite, security_events
   - ⚠️ **ONLY check `repo`** - nothing else needed

4. **Generate Token:**
   - Click: **"Generate token"** (green button at bottom)
   - **⚠️ CRITICAL:** Copy the token NOW - you'll never see it again!
   - Token format: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

5. **Store Securely:**
   - Save in password manager (1Password, LastPass, etc.)
   - Label: "GitHub PAT - Contentful Webhook - ssalazara.github.io"
   - **NEVER commit to git or share publicly**

---

## 🪝 Step 2: Configure Contentful Webhook

### Navigate to Contentful:

1. **Log into Contentful:**
   - Visit: https://app.contentful.com
   - Select Space: **ssa-personal** (Space ID: `co4wdyhrijid`)

2. **Go to Webhooks:**
   - Click: **Settings** (top navigation)
   - Click: **Webhooks** (left sidebar)
   - Click: **Add Webhook** (top right button)

### Configure Webhook:

**Basic Settings:**

```
Name: GitHub Actions Production Deploy
Description: Triggers production deployment when blog posts or navigation content is published
```

**URL and Method:**

```
URL: https://api.github.com/repos/ssalazara/ssalazara.github.io/dispatches
Method: POST
```

**Headers:**

Add these 3 headers exactly:

| Key | Value |
|-----|-------|
| `Authorization` | `Bearer ghp_YOUR_TOKEN_HERE` |
| `Accept` | `application/vnd.github+json` |
| `Content-Type` | `application/json` |

⚠️ **Replace `ghp_YOUR_TOKEN_HERE` with your actual GitHub PAT from Step 1**

**Payload (Custom):**

Select: **Custom payload**

Paste this JSON:

```json
{
  "event_type": "contentful-publish"
}
```

**Triggers:**

Select: **Select specific triggering events**

Check these content types:
- ✅ **blogPage** (Entry.publish, Entry.unpublish)
- ✅ **profile** (Entry.publish, Entry.unpublish)
- ✅ **orHeader** (Entry.publish, Entry.unpublish)
- ✅ **orFooter** (Entry.publish, Entry.unpublish)
- ✅ **homePage** (Entry.publish, Entry.unpublish)

**Actions to trigger on:**
- ✅ **Entry.publish** (when you publish content)
- ✅ **Entry.unpublish** (when you unpublish content - triggers rebuild without that content)

**Filters (Optional):**

Leave empty for now (triggers on all environments)

**Settings:**

- ✅ **Active:** ON (enabled)
- ✅ **Retry on failure:** ON (Contentful will retry 3 times if webhook fails)

### Save Webhook:

Click: **Save** (top right)

---

## ✅ Step 3: Test the Webhook

### Option A: Test from Contentful UI

1. **In Contentful Webhook Settings:**
   - Find your webhook in the list
   - Click: **View details**
   - Scroll to: **Activity log**
   - Click: **Trigger test call** (button)

2. **Expected Response:**
   - Status: `204 No Content` ✅ (Success!)
   - Or: `202 Accepted` ✅ (Also success!)
   - ❌ If you see `401 Unauthorized`: Check your PAT token
   - ❌ If you see `404 Not Found`: Check repo owner/name in URL

### Option B: Publish Content

1. **Create or Edit a Blog Post:**
   - Go to: Content → Entries
   - Create new blog post or edit existing
   - Fill in required fields (title, slug, publishDate, author, SEO, etc.)

2. **Publish:**
   - Click: **Publish** (top right)
   - Webhook fires automatically

3. **Verify Deployment:**
   - Go to GitHub: https://github.com/ssalazara/ssalazara.github.io/actions
   - You should see: **"Production Deploy"** workflow running
   - Status: 🟡 In progress → 🟢 Success (takes ~3-5 min)

---

## 🔍 Step 4: Monitor & Debug

### Check Webhook Activity:

**In Contentful:**
- Settings → Webhooks → Your webhook → **Activity log**
- Shows: All webhook calls, status codes, response times
- Green = Success, Red = Failed

**In GitHub:**
- Repository → Actions tab
- Shows: All workflow runs triggered by webhook
- Click run for detailed logs

### Common Issues:

**❌ 401 Unauthorized:**
- **Cause:** Invalid or expired GitHub PAT
- **Fix:** Generate new PAT, update webhook Authorization header

**❌ 404 Not Found:**
- **Cause:** Wrong repo owner/name in webhook URL
- **Fix:** Verify URL is exactly: `https://api.github.com/repos/ssalazara/ssalazara.github.io/dispatches`

**❌ Webhook fires but workflow doesn't run:**
- **Cause:** Workflow file not on `main` branch
- **Fix:** Ensure `.github/workflows/production-deploy.yml` is committed and pushed to main

**❌ Workflow runs but fails:**
- **Cause:** Missing GitHub Secrets or Python errors
- **Fix:** Check GitHub Actions logs for specific error

### Webhook Retry Logic:

Contentful automatically retries failed webhooks:
- **Retry 1:** After 1 minute
- **Retry 2:** After 5 minutes  
- **Retry 3:** After 15 minutes
- After 3 failures: Webhook marked as failed (check Activity log)

---

## 📊 Expected Flow:

```
1. Content Editor publishes blog post in Contentful
   ↓
2. Contentful webhook fires (< 5 seconds)
   ↓
3. GitHub receives webhook, triggers "Production Deploy" workflow
   ↓
4. Workflow runs:
   - Fetches content from Contentful (Delivery API)
   - Transforms to Jekyll files
   - Builds Jekyll site
   - Deploys to GitHub Pages
   ↓
5. New content live on https://ssalazara.github.io (3-5 min total)
```

---

## 🎯 Success Criteria:

✅ Webhook shows green status in Contentful Activity log  
✅ GitHub Actions workflow triggered automatically  
✅ Workflow completes successfully (green checkmark)  
✅ New content visible on live site within 5 minutes  

---

## 🔒 Security Notes:

- **NEVER commit GitHub PAT to git**
- Store PAT in password manager
- Rotate PAT every 6-12 months (good practice)
- If PAT is exposed: Revoke immediately and generate new one
- Webhook uses HTTPS (encrypted in transit)
- GitHub Secrets are encrypted at rest

---

## 📞 Need Help?

**Webhook not firing:**
- Check Contentful Activity log for errors
- Verify content type is in webhook triggers list

**Workflow not running:**
- Check GitHub Actions tab for runs
- Verify workflow file exists on main branch

**Deployment failing:**
- Check GitHub Actions logs for Python/Jekyll errors
- Verify GitHub Secrets are set correctly

---

**Last Updated:** 2026-01-20  
**Status:** Ready for production ✅
