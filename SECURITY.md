# Security Policy

## About This Site

This is a personal static site (Jekyll + GitHub Pages). There are no user accounts, databases, backend APIs, or session management. Content is pulled from Contentful at **build time** — no CMS tokens are ever shipped to the browser.

## Supported Versions

This is a personal project with a single production branch (`main`). Only the latest deployed version is supported.

## Reporting a Vulnerability

If you find a security issue — leaked credentials in git history, misconfigured CSP, vulnerable dependencies, or a misconfigured GitHub Actions workflow — please report it responsibly:

1. **GitHub Security Advisories (preferred):** [Report a vulnerability](../../security/advisories/new)  
2. **Email:** Open a GitHub issue and request a private channel.

Please **do not** open a public issue for security vulnerabilities.

## What's In Scope

| Area | In scope |
|------|----------|
| GitHub Actions workflow vulnerabilities | ✅ |
| Dependency vulnerabilities (Gemfile, package.json, requirements.txt) | ✅ |
| Leaked secrets in git history | ✅ |
| CSP / security header misconfiguration | ✅ |
| GitHub Pages CDN infrastructure | ❌ (report to GitHub) |
| Contentful SaaS platform | ❌ (report to Contentful) |

## Response Time

Personal project — best-effort response within 7 days.

## Security Controls in Place

- Contentful tokens are **only** used at CI build time via GitHub Actions secrets (never client-side)
- GitHub secret scanning + push protection: **enabled**
- GitHub Actions: all third-party Actions pinned to commit SHA
- Content Security Policy: set in `_layouts/default.html`
- No user-submitted data, no forms, no API endpoints
