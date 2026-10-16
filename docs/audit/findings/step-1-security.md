# Step 1 — Security & Secrets Audit Findings

**Repo:** ssalazara/ssalazara.github.io (public, Jekyll + GitHub Pages, Contentful CMS at CI build time, GA4) — audited at `/Users/simon.salazar/Documents/Apply Digital/ssalazara-Github-Page`
**Date:** 2026-07-03 · **Read-only audit, no repo/GitHub-settings changes applied.**
**Tools available:** `gh` v2.85.0 (authenticated, both collaborator and owner accounts), `npm` (audit ran), `git` (log/grep/diff/show), `bundle`/rbenv present.
**Tools missing:** `trufflehog`, `gitleaks`, `bundle-audit` (gem not installed), `pip-audit`. None installed per scope rules; manual fallbacks used instead.

## Summary

No live secrets were found in the current tree or across the repo's 29-commit history — `.env` was never committed (only the placeholder `.env.example`), and no Contentful/GitHub API key patterns appear with real values anywhere in history. The GitHub Actions setup is directionally sound (least-privilege `permissions:`, no fork-triggered workflows, no secret echoing) but all third-party Actions are pinned to mutable version tags rather than commit SHAs, which is the one clear FAIL. The more material governance gaps are repo-level: branch protection on `main` is genuinely absent, and Dependabot alerts are disabled — both confirmed authoritatively via the repo-owner GitHub account, while secret scanning + push protection are already enabled with zero open alerts.

## Findings by item

### 1. Full-history secret scan
**STATUS: PARTIAL** (automated scanners unavailable — manual fallback executed)
- EVIDENCE: `trufflehog` and `gitleaks` are not installed (`which` returned nothing for either). Per scope, no installation was attempted.
- Fallback executed: `git grep -nEI '(api[_-]?key|secret|token|password|CFPAT|AKIA|-----BEGIN)' $(git rev-list --all)` across all 29 commits (no cap needed — small history), plus `git log --all -p -- '.env' '.env.local' '.env.*.local'`.
- Result: all matches are either (a) `${{ secrets.CONTENTFUL_* }}` GitHub Actions references, (b) placeholder text in `README.md` / `docs/*.md` / `.env.example` (e.g. `CONTENTFUL_ACCESS_TOKEN=your_delivery_api_token_here`), or (c) unrelated uses of the word "token" in design-system documentation ("design tokens"). No `-----BEGIN`, `AKIA`, or `CFPAT-`-prefixed strings with real-looking values were found in any commit.
- LIMITATION: this is a pattern-based manual grep, not an entropy-based scan; it would not catch a high-entropy secret with no keyword nearby. Recommend running a real scanner (trufflehog/gitleaks) in CI or locally as a follow-up, outside this read-only step.

### 2. `.env` never tracked
**STATUS: PASS** (with one caveat noted, not a failure)
- EVIDENCE: `git log --all --oneline -- .env .env.*` → one hit: commit `500cb64286c253e1b3e1215c255af7df7f96ae3c` ("jekyll updates, front end updates"). `git show --stat 500cb64` confirms the only file touched matching that pattern is `.env.example` (new file, 14 lines), and `git show 500cb64 -- .env.example` shows only placeholder values (`your_space_id_here`, `your_delivery_api_token_here`, etc.). `git ls-tree -r HEAD --name-only | grep -i '\.env'` confirms only `.env.example` is tracked at HEAD — no real `.env` file has ever been committed.

### 3. `.gitignore` covers secret-shaped patterns
**STATUS: PASS**
- EVIDENCE: `.gitignore` lines 5–9 contain `.env`, `.env.local`, `.env.*.local`, `*.pem`, `*.key`. All required patterns from the checklist are present.
- Additional observation (not a gap, informational): `.gitignore` also excludes `Gemfile.lock`, `package-lock.json`, and `yarn.lock` from version control (lines under "RUBY"/"NODE.JS" sections). This is not a secret-exposure issue but does affect item 10 below (dependency audits run against local, not repo-pinned, lockfiles). RECOMMEND ONLY: consider tracking lockfiles for reproducible builds and supply-chain auditability — not applied.

### 4. Workflow-level `permissions:` least privilege
**STATUS: PASS**
- EVIDENCE: `.github/workflows/preview-deploy.yml:16-19` → `permissions: { contents: read, pages: write, id-token: write }`. `.github/workflows/production-deploy.yml:10-13` → identical block. Both match GitHub's documented least-privilege template for Pages deployment via `actions/deploy-pages`. No repo-wide `write-all` or default (unset) permissions found.

### 5. Contentful token scoping
**STATUS: PASS**
- EVIDENCE: `production-deploy.yml:49-50` uses `CONTENTFUL_ACCESS_TOKEN` (Content **Delivery** API, per `docs/architecture.md:1768` and `README.md:165`) with `CONTENTFUL_MODE: production`. `preview-deploy.yml:52-53` uses `CONTENTFUL_PREVIEW_TOKEN` (Content **Preview** API, `docs/architecture.md:1775`) with `CONTENTFUL_MODE: preview`. `grep -rn "MANAGEMENT" .github/workflows/` returned no matches — no Content **Management** API token (which would carry a `CFPAT-` prefix and write access) is referenced in either workflow. `.env.example` also only lists Delivery/Preview token placeholders, confirming no Management token is expected locally either. Token scoping matches least-privilege intent (read-only tokens for read-only build-time content fetch).
- Note: `docs/project-context.md:827` mentions `CONTENTFUL_MANAGEMENT_TOKEN` in an illustrative/documentation code sample only — it is not wired into any actual workflow file.

### 6. Fork-triggered workflows with secret exposure
**STATUS: PASS** (documented, no risk found)
- EVIDENCE: `preview-deploy.yml:3-4` triggers only on `workflow_dispatch` (manual, requires repo write access to invoke). `production-deploy.yml:3-7` triggers on `push: branches: [main]`, `workflow_dispatch`, and `repository_dispatch: types: [contentful-publish]` (server-to-server webhook from Contentful, not a GitHub event from a fork). Neither workflow uses `pull_request` or `pull_request_target`, so no fork-submitted PR can trigger a build that has Contentful secrets in scope. No fork-PR secret-leakage vector exists.

### 7. Third-party Actions pinned to commit SHA
**STATUS: FAIL** — Severity: **Medium**
- EVIDENCE (all `uses:` lines, both files use mutable tags, zero are SHA-pinned):
  - `production-deploy.yml:28 uses: actions/checkout@v4`
  - `production-deploy.yml:31 uses: actions/setup-python@v5`
  - `production-deploy.yml:36 uses: actions/cache@v4`
  - `production-deploy.yml:57 uses: ruby/setup-ruby@v1`
  - `production-deploy.yml:69 uses: actions/upload-pages-artifact@v3`
  - `production-deploy.yml:75 uses: actions/deploy-pages@v4`
  - `preview-deploy.yml:31 uses: actions/checkout@v4`
  - `preview-deploy.yml:34 uses: actions/setup-python@v5`
  - `preview-deploy.yml:39 uses: actions/cache@v4`
  - `preview-deploy.yml:60 uses: ruby/setup-ruby@v1`
  - `preview-deploy.yml:72 uses: actions/upload-pages-artifact@v3`
  - `preview-deploy.yml:78 uses: actions/deploy-pages@v4`
- `ruby/setup-ruby@v1` is the sharpest exposure — a floating major-version tag maintained by a third party (not `actions/*` org), giving the maintainer standing ability to change what code runs in CI with secrets (`CONTENTFUL_ACCESS_TOKEN`/`CONTENTFUL_PREVIEW_TOKEN`) in scope, without any PR review on this repo.
- RECOMMENDATION (not applied): pin every `uses:` to its full 40-character commit SHA with a version comment, e.g. `uses: actions/checkout@<sha> # v4.x.x`.

### 8. `id-token: write` justification and secret-echo check
**STATUS: PASS**
- EVIDENCE: `id-token: write` appears in both workflows (`preview-deploy.yml:19`, `production-deploy.yml:13`) alongside `uses: actions/deploy-pages@v4` (`preview-deploy.yml:78`, `production-deploy.yml:75`). `actions/deploy-pages@v4` requires an OIDC token to authenticate the deployment to GitHub Pages — this is GitHub's documented, textbook least-privilege pattern for Pages deployment (`contents: read` + `pages: write` + `id-token: write`), not an unjustified grant.
- Secret-echo check: `grep -n "echo\|printf\|set -x"` on both workflow files found only `preview-deploy.yml:82-85`, a "Preview Summary" step printing static text and `${{ github.event.inputs.locale }}` / `${{ github.repository_owner }}` / `${{ github.event.repository.name }}` — none of these are secret-typed context values. No `${{ secrets.* }}` value is ever echoed, printed, or exposed via `set -x` in either workflow.

### 9. Branch protection, secret scanning, Dependabot, alert triage
**STATUS: PARTIAL / FAIL (mixed, now confirmed with owner-level access)**
- IMPORTANT METHODOLOGY NOTE: the default authenticated `gh` account (`simon-sa-apply`) is a non-admin collaborator (`"permissions":{"admin":false}` on the repo object), under which GitHub's API returns ambiguous 404s / omits the `security_and_analysis` block regardless of actual configuration. To get authoritative results, `gh auth switch -h github.com -u ssalazara` was used (the already-authenticated repo-owner account, a read-only auth switch — no config changed), confirmed via `permissions: {'admin': True, ...}`, then switched back to the original account (`simon-sa-apply`) at the end of the audit to leave session state as found.
- **Branch protection — FAIL (Medium).** `gh api repos/ssalazara/ssalazara.github.io/branches/main/protection` under the owner account → `{"message":"Branch not protected", ... "status":"404"}`. This specific message (as opposed to a generic 404) confirms `main` genuinely has no branch protection rule — not an access artifact.
- **Secret scanning — PASS.** `security_and_analysis` (owner account) → `secret_scanning: enabled`, `secret_scanning_push_protection: enabled`. `secret_scanning_non_provider_patterns: disabled` and `secret_scanning_validity_checks: disabled` (both optional/advanced features, not required for baseline coverage).
- **Dependabot alerts — FAIL (Low, public repo with no known current CVEs found elsewhere).** `gh api .../dependabot/alerts` (owner account) → `403 "Dependabot alerts are disabled for this repository."` This 403 message (distinct from a permissions-scope 403) is authoritative confirmation the feature is off, not enabled-but-hidden. `dependabot_security_updates: disabled` in the `security_and_analysis` block corroborates this.
- **Alert triage — N/A.** No alerts exist to triage because the feature is disabled; nothing to list/assess.
- **Secret-scanning alerts — PASS.** `gh api .../secret-scanning/alerts` (owner account) → `[]` (empty list). Zero open secret-scanning alerts, consistent with the item-1 manual scan finding no live secrets.

### 10. Dependency CVEs (Gemfile.lock / package-lock.json / requirements.txt)
**STATUS: PARTIAL**
- **npm — PASS (clean), with caveat.** `package-lock.json` exists; `npm audit --omit=dev --json` → `{"vulnerabilities": {}, "metadata": {"vulnerabilities": {"critical":0,"high":0,"moderate":0,"low":0,"info":0}}, "dependencies": {"prod": 1, "dev": 954, ...}}`. Zero vulnerabilities in the 1 production dependency (Storybook and its ~954 deps are all devDependencies, expected for a design-system tooling setup that isn't shipped to the live site). CAVEAT: `package-lock.json` is gitignored (confirmed in item 3), so this audit ran against the local, not repo-committed/pinned, lockfile — results may not be reproducible for another contributor or CI run.
- **Ruby/Bundler — BLOCKED.** `bundle-audit` gem is not installed (`bundler: command not found: bundle-audit`). Per scope, not installed. `Gemfile.lock` was inspected manually (head of file reviewed: `addressable 2.8.8`, `google-protobuf 4.33.4`, etc. — versions look current) but no CVE database cross-reference was performed manually; this is a genuine tooling gap, not a clean bill of health. CAVEAT: `Gemfile.lock` is also gitignored, same reproducibility caveat as npm.
- **Python — BLOCKED.** `pip-audit` not installed; not installed per scope. `scripts/requirements.txt` reviewed manually: `contentful==1.13.1`, `python-frontmatter==1.0.0`, `PyYAML>=6.0.2`, `requests==2.31.0`, `pytest`, `pytest-cov`, `python-dotenv`. Manual observation (not a full-CVE-DB check): `requests==2.31.0` is an older pin; there have been advisories against `requests` in versions prior to 2.32.x. This dependency is build-time only (Contentful→Jekyll transform script), never shipped client-side, so exposure is Low even if the version needs a bump.

### 11. CSP review (`_layouts/default.html`)
**STATUS: PASS** (working-tree/dirty version reviewed, as instructed)
- EVIDENCE: `_layouts/default.html` has an uncommitted local modification. `git diff _layouts/default.html` shows the only change is whitespace/comment reformatting around the Google-tag `<script>` block (a blank line added before `<!-- Google tag (gtag.js) -->`) — **no CSP content changed** between the committed and working-tree versions. The CSP itself (line 18) is unchanged and is what was audited:
  `default-src 'self'; script-src 'self' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' https://images.ctfassets.net data: https://www.google-analytics.com; connect-src 'self' https://www.google-analytics.com https://analytics.google.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self';`
- Origin-to-usage mapping:
  - `googletagmanager.com` (script-src) → used, `default.html:35` loads `gtag/js?id=G-5L3JXSEP1Z`. Matches.
  - `fonts.googleapis.com` (style-src) → used, `default.html:24,26` preconnect + stylesheet link for Google Fonts. Matches.
  - `fonts.gstatic.com` (font-src) → used, `default.html:25` preconnect for font file delivery. Matches.
  - `images.ctfassets.net` (img-src) → used, confirmed via grep hits in `_data/homepage-en.yml`, `_data/homepage-es.yml`, `_data/header-en.yml`, `_data/header-es.yml`, `_data/footer-en.yml`, `_data/footer-es.yml` (Contentful-hosted image URLs rendered into the built site). Matches.
  - `google-analytics.com` / `analytics.google.com` (connect-src) → no direct `fetch`/`XMLHttpRequest` call to these hosts found in the repo's own source; they are used internally by the loaded `gtag.js` script at runtime for GA4 event collection, which is standard GA4 behavior. Not a tightening candidate — this is expected, not unnecessary, but it is *inferred* from the presence of gtag.js rather than directly observed in first-party code, so noted as such rather than a clean "confirmed usage."
- No overly broad directives found (no wildcard origins, no `unsafe-eval`, `unsafe-inline` is scoped only to `style-src` which is a common/acceptable trade-off for inline `<style>` blocks in Jekyll templates).

### 12. Token inventory
**STATUS: PASS** (informational — no rotation/scope defects found)

See consolidated table below.

## Token Inventory Table

| Token / ID | Type & Scope | Location | Rotation Note |
|---|---|---|---|
| `CONTENTFUL_ACCESS_TOKEN` | Contentful **Delivery API** (read-only, published content) | GitHub Actions secret, referenced in `production-deploy.yml:50`; placeholder only in `.env.example` (never a real value locally per item 2) | `docs/architecture.md` recommends 90-day rotation for read-only tokens; no evidence of an automated rotation schedule — manual process per `docs/architecture.md:1846-1854`. RECOMMEND verifying last rotation date in Contentful settings (out of scope to check here). |
| `CONTENTFUL_PREVIEW_TOKEN` | Contentful **Preview API** (read-only, draft + published content) | GitHub Actions secret, referenced in `preview-deploy.yml:53`; placeholder only in `.env.example` | Same 90-day manual rotation guidance as above; scoped correctly to the preview-only workflow (item 5), not exposed to production build. |
| `CONTENTFUL_SPACE_ID` | Contentful Space identifier — not a secret credential itself, but centralizing/scoping value | GitHub Actions secret in both workflows (`production-deploy.yml:49`, `preview-deploy.yml:52`); also in `.env.example` as placeholder | Static identifier, does not need rotation; stored as a secret out of convention/consistency rather than necessity. |
| `CONTENTFUL_MANAGEMENT_TOKEN` (CMA / `CFPAT-` prefix) | Contentful **Management API** — read/write, highest privilege | **Not present anywhere in actual workflows or `.env.example`.** Only appears as an illustrative code sample in `docs/project-context.md:827`. | No token of this type is in use — correctly absent from CI and local config. No action needed; documentation sample is fine as-is since it's clearly a doc/example, not a real value. |
| GA4 Measurement ID `G-5L3JXSEP1Z` | Google Analytics 4 Measurement ID | Hardcoded in `_layouts/default.html:35,42` (public HTML, shipped to every visitor's browser) | **Not a leak** — GA4 Measurement IDs are public by design (they must be embedded in client-side page source to function) and carry no write/management privilege. No rotation needed; flagging this would be a false positive. |
| GitHub PAT (referenced in `docs/setup-guides/WEBHOOK-SETUP-GUIDE.md`) | Classic GitHub Personal Access Token, used for `repository_dispatch: contentful-publish` webhook trigger | Described only in setup documentation; actual token value (if configured) would live in **Contentful's webhook configuration**, not in this repo | Documentation explicitly instructs "Store PAT in password manager" (`WEBHOOK-SETUP-GUIDE.md:36`) and never to commit it. No evidence this token or its value is present anywhere in the repo. Recommend confirming its actual scope in GitHub (ideally a fine-grained PAT limited to `repository_dispatch` on this one repo) — outside this audit's read-only reach into Contentful's own settings. |

## RECOMMENDED REMEDIATIONS (NOT APPLIED)

These are deliberately **not** applied because this audit step is read-only. Each lists the exact change and target file for a future remediation step.

1. **Pin GitHub Actions to commit SHAs** (Item 7, Medium). In `.github/workflows/production-deploy.yml` and `preview-deploy.yml`, replace every mutable-tag `uses:` with a full 40-character SHA + version comment, e.g.:
   `uses: actions/checkout@<sha>  # v4.x.x` for lines: `production-deploy.yml:28,31,36,57,69,75` and `preview-deploy.yml:31,34,39,60,72,78`. Prioritize `ruby/setup-ruby@v1` first (third-party, floating major).

2. **Enable branch protection on `main`** (Item 9, Medium). Via repo Settings → Branches → Add rule for `main`: require PR review before merge, require status checks (Jekyll build) to pass, and (optionally) disallow force-push/deletion. No file change — a GitHub Settings change, deliberately not performed here.

3. **Enable Dependabot alerts (and ideally security updates)** (Item 9, Low–Medium given public repo). Via repo Settings → Code security and analysis → enable "Dependabot alerts" and "Dependabot security updates." `dependabot_security_updates` is currently `disabled`. No file change required beyond optionally adding a `.github/dependabot.yml` config for scheduled version updates — not created here.

4. **Track `Gemfile.lock` and `package-lock.json` in git** (Item 3/10, Low). Remove `Gemfile.lock` and `package-lock.json` from `.gitignore` (currently listed) so dependency versions are reproducible and auditable in CI/PRs, not just on the local machine. Exact lines to remove from `.gitignore`: the `Gemfile.lock` line under the "RUBY" section and the `package-lock.json` line under the "NODE.JS / NPM" section. Not edited here.

5. **Install and run `bundle-audit` and `pip-audit`** (Item 10, Low–Med). Add `bundler-audit` gem (e.g. to a dev-only Gemfile group) and run `bundle-audit check --update`; add `pip-audit` to a CI or local dev workflow for `scripts/requirements.txt`. Not installed here per scope.

6. **Bump `requests` in `scripts/requirements.txt`** (Item 10, Low). Update `requests==2.31.0` to a current 2.32.x+ release to close any outstanding advisories against older 2.3x releases. Build-time only exposure, but a one-line pin bump. Not edited here.

7. **Consider a real secret-scanning tool run** (Item 1, Low, since manual grep + GitHub's own secret scanning already returned clean). Run `trufflehog git file://.` or `gitleaks detect` locally or in CI for entropy-based detection that a keyword grep cannot catch. Not installed/run here.

## Overall Risk Assessment

**No confirmed secret exposure exists in this repository, past or present.** The one real code-level finding is unpinned Action tags (Medium) — a supply-chain integrity gap, not a live vulnerability, since there are no fork-triggered workflows that would let an attacker exploit it via a malicious PR. The more consequential gaps are governance-level rather than code-level: `main` has no branch protection (Medium — a bad actor or accidental push with maintainer credentials could go straight to production with no review gate, and the production workflow deploys directly on `push: branches: [main]`), and Dependabot alerts are switched off on a public repo (Low–Medium — reduces visibility into future dependency CVEs, though today's manual `npm audit` and Gemfile.lock spot-check show nothing acutely alarming). Secret scanning + push protection are already correctly enabled with zero open alerts, which is the most important preventive control and it is in good shape. Net assessment: **Low immediate risk, Medium residual risk from process gaps (branch protection, Dependabot, SHA-pinning) that should be closed as follow-up actions**, none of which required or received any write action during this audit.
