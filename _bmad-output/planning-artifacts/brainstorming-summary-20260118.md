---
stepsCompleted: [1, 2, 3, 4]
inputDocuments: ["Session Context: Python, Contentful, ISO codes, Top-right toggle", "User Story Drafts: al-folio Jekyll reference"]
session_topic: 'GitHub Page Portfolio with Contentful & Python'
session_goals: 'Create a localized, content-driven academic portfolio'
selected_approach: 'Structured Technical Innovation'
techniques_used: ['Theme Clustering', 'Prioritization Matrix']
date: 2026-01-18
author: Simon
---

# Brainstorming Session Summary: github-page

## 1. Session Overview
**Topic:** Building a modern, localized portfolio site using GitHub Pages, Contentful, and Python.
**Goal:** Transitioning from a standard Jekyll theme (al-folio) to a dynamic, headless-CMS-driven architecture with multi-language support.

---

## 2. Thematic Organization of Ideas

### Theme 1: The "Content Engine" (Headless CMS & Python)
*Focus: Decoupling content management from the presentation layer.*

- **Headless Content Integration:** Use **Contentful** as the primary CMS for managing publications, projects, and biography data.
- **Python Transformation Layer:** A custom **Python script** to fetch JSON from Contentful and generate Jekyll-compatible Markdown files (collections).
- **Automated Deployment:** GitHub Actions triggered by Contentful webhooks to ensure "push-to-publish" simplicity.
- **Pattern Insight:** This moves the project from "Static-Static" to "Dynamic-Static," offering CMS ease with GitHub Pages performance.

### Theme 2: The "Global Reach" (ISO Localization)
*Focus: Implementing professional-grade multi-language support.*

- **ISO 639-1 Compliance:** Using standard ISO codes (e.g., `en`, `es`, `fr`) for URL routing and metadata.
- **Localized Content Models:** Configuring Contentful fields to support parallel translations.
- **Language-Aware Search:** Ensuring the site search respects the current ISO language context.
- **Pattern Insight:** Standardizing on ISO codes ensures future-proofing and SEO compatibility for a global audience.

### Theme 3: The "User Interface" (UX & Aesthetic)
*Focus: Refining the al-folio base for better interaction.*

- **Dual-Purpose Toggle:** A unified **top-right toggle** that manages both Dark/Light mode and Language switching.
- **Enhanced al-folio Integration:** Adapting the popular `al-folio` Jekyll theme to consume the Python-generated Markdown.
- **Sticky ISO Selector:** Ensuring the language toggle is always accessible, regardless of scroll position.
- **Pattern Insight:** Combining the theme and language toggle simplifies the header and focuses user attention.

---

## 3. Prioritization Results

| Feature | Impact | Feasibility | Priority |
| :--- | :--- | :--- | :--- |
| **Python-Contentful Sync** | High | Medium | **P0 (Critical)** |
| **ISO URL Routing** | High | High | **P0 (Critical)** |
| **Top-right Toggle UI** | Medium | High | **P1 (Important)** |
| **Automated Webhooks** | Medium | Medium | **P2 (Later)** |

### Top Priority: **The Python-Contentful Bridge**
This is the "brain" of the operation. Without the script to transform CMS data into Jekyll files, the localization and UI features have no data to display.

---

## 4. Action Plan: Next Steps

1. **Architecture (Today):** Define the Contentful Content Model (schema) matching the `al-folio` data structures.
2. **Development (Week 1):** Create the Python script using `contentful.py` to pull data and generate `.md` files in `_posts/` and `_projects/`.
3. **UI/UX (Week 1):** Implement the ISO-compliant routing and the top-right toggle in the Jekyll `_layouts`.
4. **Automation (Week 2):** Set up the GitHub Action workflow for automatic rebuilds on Contentful updates.

---

## 5. Session Insights
- **The Breakthrough:** Realizing that Python acts as a better "middleman" for complex transformations than Jekyll's Liquid templates alone.
- **The Challenge:** Maintaining ISO consistency across both Contentful and the Jekyll routing system.
- **Outcome:** A clear technical roadmap that elevates a standard portfolio into a professional, multi-lingual platform.
