# 📝 Contentful Blog Post Creation Guide

**Last Updated:** 2026-01-19  
**Target Audience:** Content Editors, Marketing Team

This guide walks you through creating blog posts in Contentful that will automatically sync to your Jekyll website.

---

## 🎯 Prerequisites

Before you begin, ensure you have:
- ✅ Access to the Contentful space
- ✅ Editor or Admin permissions
- ✅ Familiarity with the Contentful UI

---

## 📋 Quick Start Checklist

When creating a new blog post, you'll need:

1. **Title** (required) - The headline of your blog post
2. **URL Slug** (required) - Lowercase URL-friendly version (e.g., `my-first-post`)
3. **Publish Date** (required) - When the post should be published
4. **Author Name** (required) - Who wrote the post
5. **Featured Image** (required) - Hero image for the post
6. **Body Content** (required) - The main article content (rich text)
7. **SEO Metadata** (required) - Search engine optimization settings
8. **Excerpt** (optional) - Short preview text for cards/carousels

---

## 🚀 Step-by-Step Instructions

### Step 1: Navigate to Content

1. Log in to [Contentful](https://app.contentful.com)
2. Select your space
3. Click **"Content"** in the left sidebar
4. Click **"Add entry"** button (top right)
5. Select **"🦠 Blog Page"** from the content type list

### Step 2: Fill Required Fields

#### **Title** (Symbol)
- **What it is:** The main headline of your blog post
- **Best practices:**
  - Keep it under 60 characters for SEO
  - Make it compelling and descriptive
  - Use title case (e.g., "How to Build a Modern Portfolio")
- **Example:** `Building a Modern Portfolio with Jekyll and Contentful`

#### **URL Slug** (Symbol)
- **What it is:** The URL path for your post (appears after `/blog/`)
- **Format rules:**
  - Lowercase letters only
  - Use hyphens to separate words (no spaces or underscores)
  - No special characters except hyphens
  - Must be unique across all blog posts
- **Example:** `building-modern-portfolio-jekyll-contentful`
- **Result URL:** `https://yoursite.com/en/blog/building-modern-portfolio-jekyll-contentful`

#### **Publish Date** (Date & Time)
- **What it is:** When the post should be published/visible
- **Tips:**
  - Use future dates to schedule posts
  - Time is in UTC timezone
  - Posts are sorted by this date (newest first)
- **Example:** `2026-01-20 10:00 AM`

#### **Author** (Symbol)
- **What it is:** Name of the person who wrote the post
- **Best practices:**
  - Use consistent naming (e.g., always "Simon Salazar" not "S. Salazar")
  - Full name preferred
- **Example:** `Simon Salazar`

#### **Featured Image** (Asset - Image)
- **What it is:** The main hero image for your blog post
- **Requirements:**
  - **Format:** JPG, PNG, or WebP
  - **Recommended size:** 1200x630px (for social sharing)
  - **Max file size:** 2MB
- **Upload steps:**
  1. Click "Add existing media" or "Add new media"
  2. Select an image from Media library or upload new
  3. Ensure image has descriptive alt text for accessibility

#### **Body** (Rich Text)
- **What it is:** The main content of your blog post
- **Supported features:**
  - **Headings:** Use H2 for main sections, H3 for subsections
  - **Paragraphs:** Standard text blocks
  - **Bold/Italic:** Text formatting
  - **Links:** Hyperlinks to external resources
  - **Lists:** Bulleted and numbered lists
  - **Code blocks:** For technical content
  - **Embedded entries:** Reference other content types (future)
- **Best practices:**
  - Break content into scannable sections with headings
  - Use short paragraphs (3-4 sentences max)
  - Include lists for easy reading
  - Add links to relevant resources

#### **SEO** (Reference to SEO entry)
- **What it is:** Metadata for search engines and social media
- **Steps:**
  1. Click "Add existing entry" or "Create new entry and link"
  2. Fill out SEO fields:
     - **Title:** SEO title (can differ from post title, 50-60 chars)
     - **Description:** Meta description (150-160 characters)
     - **Keywords:** Comma-separated keywords (optional)
     - **Image:** Open Graph image (use featured image)
  3. Click "Create and link" or "Save"

### Step 3: Optional Fields

#### **Excerpt** (Text)
- **What it is:** A short preview/teaser for the post
- **Character limit:** 200 characters
- **Usage:** Displayed in blog cards, carousels, and archive pages
- **Best practices:**
  - Write a compelling hook
  - Include main benefit or key takeaway
  - Don't just copy first paragraph
- **Example:** `Learn how to build a stunning portfolio website using Jekyll static site generator and Contentful CMS. No React required!`

#### **Tags** (Array of Symbols - if available)
- **What it is:** Categories or topics for filtering/grouping
- **Examples:** `Tutorial`, `Web Development`, `Jekyll`, `Contentful`

### Step 4: Localization (Multi-Language)

If your site supports multiple languages (e.g., English + Spanish):

1. Click the **locale switcher** in the top toolbar (e.g., "English (United States)")
2. Select your target locale (e.g., "Español")
3. Fill out **localized fields**:
   - Title (in Spanish)
   - Body content (in Spanish)
   - SEO metadata (in Spanish)
4. **Non-localized fields** (like slug, author, dates) stay the same across locales

### Step 5: Preview & Publish

1. **Save as Draft:** Click "Save" to save without publishing
2. **Preview:** (Optional) Use preview functionality to see how it looks
3. **Publish:**
   - Click **"Publish"** button (top right)
   - Confirm publication
   - Your post will appear on the website within 5-10 minutes (after next build)

---

## 💡 Content Writing Tips

### Headline Best Practices
- ✅ Be specific and descriptive
- ✅ Use numbers when possible ("5 Ways to...", "Top 10...")
- ✅ Include power words (Guide, Ultimate, Essential, Proven)
- ❌ Avoid clickbait or misleading titles

### Body Content Tips
- **Opening paragraph:** Hook the reader immediately, explain what they'll learn
- **Structure:** Use headings (H2, H3) to break content into sections
- **Visuals:** Add images or code blocks to illustrate points
- **Conclusion:** Summarize key takeaways and include a call-to-action

### SEO Optimization
- **Title tag:** Include primary keyword near the beginning
- **Meta description:** Write a compelling summary with a call-to-action
- **URL slug:** Keep it short, descriptive, and keyword-rich
- **Headings:** Use keywords naturally in H2/H3 headings
- **Internal links:** Link to other blog posts or pages on your site

---

## 📚 Sample Blog Post Ideas

Need inspiration? Here are some starter ideas:

### Technical Tutorials
- "Building a RESTful API with Node.js and Express"
- "Mastering CSS Grid: A Complete Guide"
- "Getting Started with React Hooks"

### Career & Industry
- "5 Soft Skills Every Developer Needs"
- "My Journey from Bootcamp to Senior Developer"
- "How to Prepare for Technical Interviews"

### Portfolio & Projects
- "Behind the Scenes: How I Built My Portfolio"
- "Lessons Learned from My First Freelance Project"
- "Open Source Contributions That Changed My Career"

### Tools & Productivity
- "My VS Code Setup for Maximum Productivity"
- "10 Chrome Extensions Every Developer Should Use"
- "How I Organize My Development Workflow"

---

## 🐛 Troubleshooting

### "Entry validation failed"
- **Cause:** Required field is missing or invalid format
- **Solution:** Check all required fields are filled and follow format rules

### "Slug already exists"
- **Cause:** Another post has the same URL slug
- **Solution:** Use a unique slug (add date or modify wording)

### "Image too large"
- **Cause:** Featured image exceeds 2MB limit
- **Solution:** Compress image using [TinyPNG](https://tinypng.com) or similar tool

### "Post not appearing on website"
- **Cause:** Post is saved as draft or build hasn't run yet
- **Solution:** Ensure post is **published** (not just saved), wait 5-10 minutes for build

---

## 📞 Need Help?

If you encounter issues or have questions:

1. **Check Contentful Documentation:** [https://www.contentful.com/help/](https://www.contentful.com/help/)
2. **Contact Development Team:** Reach out to your technical team for assistance
3. **Review this guide:** Double-check you've followed all steps correctly

---

## 🎉 You're Ready!

You now have everything you need to create compelling blog posts in Contentful. Start writing and watch your content come to life on your Jekyll website!

**Happy blogging! ✍️**
