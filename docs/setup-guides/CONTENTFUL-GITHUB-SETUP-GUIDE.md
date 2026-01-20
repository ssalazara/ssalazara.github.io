# Contentful CLI & GitHub Pages Setup Guide

**Project:** GitHub Page  
**Date:** 2026-01-19  
**Author:** Dev Agent (Amelia)

---

## Table of Contents

1. [GitHub Repository Setup](#github-repository-setup)
2. [Contentful CLI Setup](#contentful-cli-setup)
3. [Push Content Schemas to Contentful](#push-content-schemas-to-contentful)
4. [Git Workflow Reference](#git-workflow-reference)

---

## GitHub Repository Setup

### Prerequisites
- GitHub account
- Git installed locally
- Terminal/command line access

### Step 1: Create GitHub Pages Repository

#### Option A: Using GitHub Web Interface

1. **Navigate to GitHub:**
   - Go to [github.com](https://github.com)
   - Click the `+` icon in the top-right corner
   - Select **New repository**

2. **Repository Configuration:**
   ```
   Repository name: <username>.github.io
   OR: <your-project-name>
   
   Description: [Optional] Personal GitHub Page
   Visibility: Public (required for free GitHub Pages)
   Initialize: ✓ Add a README file (optional, but recommended)
   ```

3. **Create Repository:**
   - Click **Create repository**
   - Note the repository URL: `https://github.com/<username>/<repo-name>.git`

#### Option B: Using GitHub CLI

1. **Install GitHub CLI (if not installed):**
   ```bash
   # macOS
   brew install gh
   
   # Verify installation
   gh --version
   ```

2. **Authenticate with GitHub:**
   ```bash
   gh auth login
   ```
   - Select: `GitHub.com`
   - Select: `HTTPS` (or SSH if you prefer)
   - Authenticate via: `Login with a web browser` (recommended)
   - Copy the one-time code shown
   - Press Enter to open browser
   - Paste the code and authorize

3. **Create Repository:**
   ```bash
   # For personal GitHub Page
   gh repo create <username>.github.io --public --clone
   
   # OR for project repository
   gh repo create github-page --public --clone --description "Personal portfolio site"
   ```

### Step 2: Connect Local Repository to GitHub

#### If you already have a local project (your case):

1. **Navigate to your project directory:**
   ```bash
   cd "/Users/simon.salazar/Documents/Apply Digital/github-page"
   ```

2. **Initialize Git (if not already initialized):**
   ```bash
   # Check if already initialized
   git status
   
   # If not, initialize:
   git init
   ```

3. **Add remote repository:**
   ```bash
   # Add GitHub repository as remote
   git remote add origin https://github.com/<username>/<repo-name>.git
   
   # Verify remote was added
   git remote -v
   ```

4. **Set default branch:**
   ```bash
   # Rename current branch to main (if needed)
   git branch -M main
   ```

### Step 3: Enable GitHub Pages

#### Option A: Via GitHub Web Interface

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)` or `/docs` (if using docs folder)
5. Click **Save**
6. Your site will be published at: `https://<username>.github.io/<repo-name>/`

#### Option B: Using GitHub CLI

```bash
gh repo edit --enable-pages --pages-branch main
```

---

## Contentful CLI Setup

### Step 1: Install Contentful CLI

```bash
# Using npm (Node.js required)
npm install -g contentful-cli

# Verify installation
contentful --version
```

**Expected output:** `contentful-cli/3.x.x` (or current version)

### Step 2: Authenticate with Contentful

1. **Login to Contentful:**
   ```bash
   contentful login
   ```
   
   This will:
   - Open your default browser
   - Prompt you to log in to Contentful
   - Request authorization for the CLI
   - Save authentication token locally

2. **Verify authentication:**
   ```bash
   contentful space list
   ```
   
   This should display all Contentful spaces you have access to.

### Step 3: Get Your Space ID and Environment

1. **List available spaces:**
   ```bash
   contentful space list
   ```
   
   **Sample output:**
   ```
   Space name                     Space ID
   ──────────────────────────────────────────
   My Personal Site               abc123def456
   Production Blog                xyz789uvw012
   ```

2. **Note your Space ID** - you'll need this for all subsequent commands

3. **Check available environments:**
   ```bash
   contentful space environment list --space-id <YOUR_SPACE_ID>
   ```
   
   Common environments: `master`, `staging`, `development`

### Step 4: Configure Space for This Project

**Option A: Create a config file (recommended)**

Create `.contentfulrc.json` in your project root:

```json
{
  "spaceId": "YOUR_SPACE_ID",
  "managementToken": "YOUR_CMA_TOKEN",
  "activeEnvironmentId": "master"
}
```

**To get Management Token:**
1. Go to [app.contentful.com](https://app.contentful.com)
2. Navigate to: **Settings** → **API keys** → **Content management tokens**
3. Click **Generate personal token**
4. Name it: "CLI Access - GitHub Page Project"
5. Copy the token (you won't see it again!)

**Option B: Use environment variables**

Add to your `~/.zshrc` or `~/.bash_profile`:

```bash
export CONTENTFUL_SPACE_ID="YOUR_SPACE_ID"
export CONTENTFUL_MANAGEMENT_TOKEN="YOUR_CMA_TOKEN"
export CONTENTFUL_ENVIRONMENT="master"
```

Then reload:
```bash
source ~/.zshrc
```

---

## Push Content Schemas to Contentful

### Current Schema Files

Your project has the following content type schemas in `contentful-schemas/`:

```
- blogpage.json
- component-card.json
- component-carousel.json
- component-image.json
- component-quote.json
- footer.json
- hero-banner.json
- homepage.json
- menu-item.json
- or-header.json
- profile.json
- rich-text-block.json
- seo.json
- social-link.json
- text-with-image.json
```

### Step 1: Validate Schema Files

Before pushing, ensure your schemas are properly formatted:

```bash
# Navigate to schema directory
cd contentful-schemas

# Validate a single schema
cat blogpage.json | jq .

# Validate all schemas
for file in *.json; do
  echo "Validating $file..."
  cat "$file" | jq . > /dev/null && echo "✓ Valid" || echo "✗ Invalid JSON"
done
```

### Step 2: Import Content Types (Individual)

**For a single content type:**

```bash
contentful space import \
  --space-id <YOUR_SPACE_ID> \
  --environment-id master \
  --content-file contentful-schemas/homepage.json
```

### Step 3: Import All Content Types (Batch)

**Option A: Using Contentful Space Import**

1. **Create import manifest** (`contentful-import.json`):

```json
{
  "contentTypes": [
    { "sys": { "id": "blogpage" } },
    { "sys": { "id": "componentCard" } },
    { "sys": { "id": "componentCarousel" } },
    { "sys": { "id": "componentImage" } },
    { "sys": { "id": "componentQuote" } },
    { "sys": { "id": "footer" } },
    { "sys": { "id": "heroBanner" } },
    { "sys": { "id": "homepage" } },
    { "sys": { "id": "menuItem" } },
    { "sys": { "id": "orHeader" } },
    { "sys": { "id": "profile" } },
    { "sys": { "id": "richTextBlock" } },
    { "sys": { "id": "seo" } },
    { "sys": { "id": "socialLink" } },
    { "sys": { "id": "textWithImage" } }
  ]
}
```

2. **Run batch import:**

```bash
contentful space import \
  --space-id <YOUR_SPACE_ID> \
  --environment-id master \
  --content-file contentful-schemas/
```

**Option B: Using a shell script**

Create `push-schemas.sh`:

```bash
#!/bin/bash

SPACE_ID="YOUR_SPACE_ID"
ENVIRONMENT="master"

echo "🚀 Starting Contentful schema import..."

cd contentful-schemas

for schema in *.json; do
  echo "📤 Importing $schema..."
  
  contentful space import \
    --space-id $SPACE_ID \
    --environment-id $ENVIRONMENT \
    --content-file "$schema"
  
  if [ $? -eq 0 ]; then
    echo "✅ Successfully imported $schema"
  else
    echo "❌ Failed to import $schema"
    exit 1
  fi
done

echo "🎉 All schemas imported successfully!"
```

Make executable and run:

```bash
chmod +x push-schemas.sh
./push-schemas.sh
```

**Option C: Using Contentful Migration CLI (Recommended for production)**

1. **Install migration CLI:**
   ```bash
   npm install -g contentful-migration
   ```

2. **Create migration script** (`migrations/create-content-types.js`):

```javascript
module.exports = function(migration) {
  const fs = require('fs');
  const path = require('path');
  
  const schemasDir = path.join(__dirname, '../contentful-schemas');
  const schemas = fs.readdirSync(schemasDir)
    .filter(file => file.endsWith('.json'));
  
  schemas.forEach(schemaFile => {
    const schema = require(path.join(schemasDir, schemaFile));
    const contentType = migration.createContentType(schema.sys.id, schema);
    
    // Add fields
    schema.fields.forEach(field => {
      contentType.createField(field.id, {
        name: field.name,
        type: field.type,
        localized: field.localized,
        required: field.required,
        validations: field.validations,
        disabled: field.disabled,
        omitted: field.omitted
      });
    });
  });
};
```

3. **Run migration:**

```bash
contentful-migration \
  --space-id <YOUR_SPACE_ID> \
  --environment-id master \
  migrations/create-content-types.js
```

### Step 4: Verify Import

```bash
# List all content types in space
contentful space list-content-types \
  --space-id <YOUR_SPACE_ID> \
  --environment-id master

# Or view in Contentful web app
# Navigate to: Content model → All content types
```

### Step 5: Publish Content Types

After importing, content types need to be published:

```bash
# Publish all content types
contentful space publish-content-types \
  --space-id <YOUR_SPACE_ID> \
  --environment-id master
```

---

## Git Workflow Reference

### Basic Git Commands

#### Check Status
```bash
git status
```

Shows:
- Modified files (red)
- Staged files (green)
- Untracked files
- Current branch

#### Add Files to Staging

```bash
# Add specific file
git add path/to/file.html

# Add all files in directory
git add contentful-schemas/

# Add all changed files
git add .

# Add all files (including deleted)
git add -A
```

#### Commit Changes

```bash
# Commit with message
git commit -m "Add Contentful schema files"

# Commit with detailed message
git commit -m "Add Contentful schema files" -m "Includes homepage, blog, and component schemas for GitHub Pages integration"

# Amend last commit (before push)
git commit --amend -m "Updated commit message"
```

#### Push to Remote

```bash
# First push (set upstream)
git push -u origin main

# Subsequent pushes
git push

# Force push (use with caution!)
git push --force
```

#### Pull from Remote

```bash
# Pull latest changes
git pull origin main

# Pull and rebase
git pull --rebase origin main
```

### Complete Workflow Example

**Scenario:** You've updated your Contentful schemas and want to push to GitHub

```bash
# 1. Check current status
git status

# 2. Add all schema files
git add contentful-schemas/

# 3. Add any other changed files
git add _data/ _includes/ _layouts/

# 4. Commit with descriptive message
git commit -m "Update Contentful content type schemas

- Add hero-banner schema for homepage
- Update blogpage schema with new SEO fields
- Add social-link component for footer integration"

# 5. Pull latest changes (if working with others)
git pull origin main

# 6. Push to GitHub
git push origin main
```

### Branch Workflow (Best Practice)

```bash
# Create and switch to new branch
git checkout -b feature/update-schemas

# Make changes, add, commit
git add .
git commit -m "Update schemas"

# Push branch to remote
git push -u origin feature/update-schemas

# Switch back to main
git checkout main

# Merge feature branch
git merge feature/update-schemas

# Delete local branch
git branch -d feature/update-schemas

# Delete remote branch
git push origin --delete feature/update-schemas
```

### Common Git Commands

```bash
# View commit history
git log --oneline

# View changes before staging
git diff

# View staged changes
git diff --staged

# Discard changes in file
git checkout -- path/to/file

# Unstage file
git reset HEAD path/to/file

# Create .gitignore
echo "node_modules/" >> .gitignore
echo ".env" >> .gitignore
echo ".contentfulrc.json" >> .gitignore
```

### GitHub Pages Specific

```bash
# After pushing to main, GitHub Actions will:
# 1. Detect changes
# 2. Build Jekyll site
# 3. Deploy to GitHub Pages
# 4. Site available at: https://<username>.github.io/<repo>/

# Check deployment status
gh run list

# View specific run
gh run view <run-id>
```

---

## Complete Setup Checklist

### GitHub Setup
- [ ] Create GitHub repository
- [ ] Connect local repository to GitHub remote
- [ ] Configure GitHub Pages in repository settings
- [ ] Push initial code to main branch
- [ ] Verify site is live at GitHub Pages URL

### Contentful Setup
- [ ] Install Contentful CLI globally
- [ ] Authenticate with Contentful account
- [ ] Get Space ID and Management Token
- [ ] Create `.contentfulrc.json` configuration
- [ ] Validate all schema JSON files
- [ ] Import content types to Contentful space
- [ ] Publish content types
- [ ] Verify content types in Contentful web app

### Git Workflow
- [ ] Add `.gitignore` file (exclude `.contentfulrc.json`, `.env`)
- [ ] Stage changes with `git add`
- [ ] Commit changes with descriptive message
- [ ] Push to main branch
- [ ] Verify deployment on GitHub Pages

---

## Quick Reference Commands

### Contentful
```bash
# Login
contentful login

# List spaces
contentful space list

# Import schema
contentful space import --space-id <SPACE_ID> --content-file schema.json

# List content types
contentful space list-content-types --space-id <SPACE_ID>
```

### Git
```bash
# Basic workflow
git status
git add .
git commit -m "message"
git push origin main

# Pull latest
git pull origin main

# Create branch
git checkout -b branch-name
```

### GitHub CLI
```bash
# Create repo
gh repo create <name> --public

# View PRs
gh pr list

# Check deployment
gh run list
```

---

## Troubleshooting

### Contentful Issues

**Error: "Space not found"**
```bash
# Verify space ID
contentful space list

# Re-authenticate
contentful logout
contentful login
```

**Error: "Invalid content type"**
- Validate JSON: `cat schema.json | jq .`
- Check required fields: `sys.id`, `name`, `fields`

**Error: "Content type already exists"**
- Use migrations or update existing type
- Delete and recreate (caution: loses content)

### Git Issues

**Error: "remote origin already exists"**
```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin <URL>
```

**Error: "rejected - non-fast-forward"**
```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

**Error: "Permission denied (publickey)"**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy and add to GitHub: Settings → SSH Keys
```

---

## Next Steps

1. **Set up CI/CD:** Automate Contentful → GitHub Pages deployment
2. **Content Preview:** Configure preview environments
3. **Webhooks:** Auto-deploy on content changes
4. **Environment Strategy:** Set up staging/production environments

---

**Document Status:** ✅ Complete  
**Last Updated:** 2026-01-19  
**Maintained by:** Dev Agent (Amelia)
