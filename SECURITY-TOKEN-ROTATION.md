# 🔐 SECURITY: Contentful API Token Rotation Required

**Status:** ⚠️ **ACTION REQUIRED BEFORE FIRST USE**

## Why This Matters

API tokens were previously exposed in a draft specification file (now deleted). As a security best practice, these tokens must be rotated immediately.

## Steps to Rotate Tokens

### 1. Log into Contentful

Visit: https://app.contentful.com

### 2. Navigate to API Keys

Go to: **Settings > API keys**

### 3. Delete Old Tokens

- Find and **delete** the existing Content Delivery API token
- Find and **delete** the existing Content Preview API token

### 4. Generate New Tokens

**Content Delivery API Token (Production):**
1. Click "Add API key" or use existing key
2. Select "Content Delivery API"
3. Copy the new token immediately

**Content Preview API Token (Draft Preview):**
1. Click "Add API key" or use existing key  
2. Select "Content Preview API"
3. Copy the new token immediately

### 5. Store Tokens Securely

**Local Development:**
Create `.env` file in project root:

```bash
CONTENTFUL_SPACE_ID=co4wdyhrijid
CONTENTFUL_ACCESS_TOKEN=<NEW_DELIVERY_TOKEN>
CONTENTFUL_PREVIEW_TOKEN=<NEW_PREVIEW_TOKEN>
CONTENTFUL_MODE=production
```

**GitHub Secrets (For CI/CD):**
1. Go to: Repository Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Add:
   - `CONTENTFUL_SPACE_ID` = `co4wdyhrijid`
   - `CONTENTFUL_ACCESS_TOKEN` = `<NEW_DELIVERY_TOKEN>`
   - `CONTENTFUL_PREVIEW_TOKEN` = `<NEW_PREVIEW_TOKEN>`

**Password Manager:**
- Store tokens in your password manager (1Password, LastPass, etc.)
- Label clearly: "Contentful Delivery API - github-page project"

### 6. Verify Tokens Work

Test locally:

```bash
# Activate virtual environment
source venv/bin/activate

# Run transformation script
python scripts/contentful_to_jekyll.py

# Should complete successfully with:
# ✅ CONFIG_LOADED space_id=co4wdyhrijid mode=production ...
```

## Security Best Practices

✅ **DO:**
- Rotate tokens immediately after exposure
- Store tokens in `.env` file (never commit to git)
- Use GitHub Secrets for CI/CD
- Use read-only tokens (Delivery/Preview API, not Management API)
- Store backups in password manager

❌ **DON'T:**
- Commit tokens to git
- Share tokens in chat/email
- Use Management API tokens in CI/CD (full write access)
- Hardcode tokens in source files

## Confirmation

Once tokens are rotated and configured:

- [ ] Old tokens deleted from Contentful
- [ ] New tokens generated
- [ ] `.env` file created locally
- [ ] GitHub Secrets configured
- [ ] Tokens stored in password manager
- [ ] Test run successful (`python scripts/contentful_to_jekyll.py`)

## Questions?

See: `_bmad-output/CONTENTFUL-GITHUB-SETUP-GUIDE.md` for complete setup guide.

---

**Security Incident Timeline:**
- 2026-01-19: Tokens exposed in draft spec (tech-spec-wip.md)
- 2026-01-19: Draft spec deleted, token rotation documented
- 2026-01-19: Production-ready secure implementation complete

**Next Action:** Rotate tokens before first deployment.
