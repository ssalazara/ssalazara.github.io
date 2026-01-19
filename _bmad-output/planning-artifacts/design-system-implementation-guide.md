# Design System Implementation Guide
**Project:** GitHub Pages Portfolio  
**Version:** 1.0  
**Last Updated:** 2026-01-19

---

## Quick Start

### Step 1: Import Design Tokens

In your main stylesheet (`assets/css/style.scss`):

```scss
// Import design tokens
@import '../sass/variables';
@import '../sass/mixins';
@import '../sass/base';

// Import component styles
@import '../sass/components/buttons';
@import '../sass/components/cards';
@import '../sass/components/forms';
// ... more components
```

### Step 2: Use the Container

```html
<div class="container">
  <!-- Your content here -->
</div>
```

```scss
.container {
  @include container;
}
```

---

## Component Examples

### 1. Buttons

#### HTML Structure
```html
<!-- Primary Button -->
<button class="btn btn-primary">Primary Action</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">Secondary Action</button>

<!-- Ghost Button -->
<button class="btn btn-ghost">Ghost Action</button>

<!-- Icon Button -->
<button class="btn btn-icon" aria-label="Close">
  <svg><!-- icon --></svg>
</button>

<!-- Button Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-md">Medium</button>
<button class="btn btn-primary btn-lg">Large</button>
```

#### SCSS Implementation
```scss
.btn {
  @include button-base;
  @include button-md; // Default size
  
  // Size variants
  &-sm {
    @include button-sm;
  }
  
  &-lg {
    @include button-lg;
  }
  
  // Color variants
  &-primary {
    @include button-primary;
  }
  
  &-secondary {
    @include button-secondary;
  }
  
  &-ghost {
    @include button-ghost;
  }
  
  // Icon-only variant
  &-icon {
    @include button-icon;
  }
}
```

---

### 2. Form Inputs

#### HTML Structure
```html
<!-- Text Input -->
<div class="form-group">
  <label for="email" class="form-label">Email</label>
  <input type="email" id="email" class="input" placeholder="you@example.com">
</div>

<!-- Textarea -->
<div class="form-group">
  <label for="message" class="form-label">Message</label>
  <textarea id="message" class="input input-textarea" rows="4"></textarea>
</div>

<!-- Input with Error -->
<div class="form-group">
  <label for="username" class="form-label">Username</label>
  <input type="text" id="username" class="input input-error" aria-invalid="true">
  <p class="form-error">This username is already taken</p>
</div>
```

#### SCSS Implementation
```scss
.form-group {
  margin-bottom: $spacing-4;
}

.form-label {
  display: block;
  margin-bottom: $spacing-2;
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  color: $color-text-primary;
}

.input {
  @include input-base;
  @include input-md;
  
  &-sm {
    @include input-sm;
  }
  
  &-lg {
    @include input-lg;
  }
  
  &-error {
    @include input-error;
  }
  
  &-success {
    @include input-success;
  }
  
  &-textarea {
    height: auto;
    padding: $input-padding-x-md;
    resize: vertical;
  }
}

.form-error {
  margin-top: $spacing-2;
  font-size: $font-size-sm;
  color: $color-error-500;
}
```

---

### 3. Cards

#### HTML Structure
```html
<!-- Blog Post Card -->
<article class="card card-blog-post">
  <img src="/path/to/image.jpg" alt="Blog post thumbnail" class="card-image">
  <div class="card-content">
    <h3 class="card-title">Understanding Design Systems</h3>
    <p class="card-excerpt">
      A comprehensive guide to building scalable and maintainable design systems...
    </p>
    <div class="card-meta">
      <time datetime="2026-01-19">January 19, 2026</time>
      <span class="card-category">Design</span>
    </div>
    <a href="/blog/post-slug" class="card-link">Read more</a>
  </div>
</article>
```

#### SCSS Implementation
```scss
.card {
  @include card;
  
  // Interactive variant
  &-interactive {
    @include card-interactive;
  }
  
  // Blog post specific styles
  &-blog-post {
    @include card-interactive;
    display: flex;
    flex-direction: column;
    min-height: $card-min-height;
  }
}

.card-image {
  @include aspect-ratio(16, 9);
  width: 100%;
  object-fit: cover;
  border-radius: $radius-md;
  margin-bottom: $spacing-4;
}

.card-content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-title {
  font-size: $font-size-xl;
  font-weight: $font-weight-bold;
  margin-bottom: $spacing-2;
  color: $color-text-primary;
  
  @include line-clamp(2); // Truncate to 2 lines
}

.card-excerpt {
  font-size: $font-size-sm;
  color: $color-text-secondary;
  line-height: $line-height-relaxed;
  margin-bottom: $spacing-4;
  flex-grow: 1;
  
  @include line-clamp(3); // Truncate to 3 lines
}

.card-meta {
  display: flex;
  align-items: center;
  gap: $spacing-3;
  font-size: $font-size-xs;
  color: $color-text-tertiary;
  margin-bottom: $spacing-4;
}

.card-category {
  padding: $spacing-1 $spacing-2;
  background-color: $color-primary-50;
  color: $color-primary-700;
  border-radius: $radius-sm;
  font-weight: $font-weight-medium;
}

.card-link {
  color: $color-text-link;
  font-weight: $font-weight-semibold;
  text-decoration: none;
  
  &:hover {
    text-decoration: underline;
  }
}
```

---

### 4. Profile Card (Homepage Hero)

#### HTML Structure
```html
<section class="profile-section">
  <div class="container-narrow">
    <div class="profile-card">
      <img src="/path/to/profile.jpg" alt="Simon Salazar" class="profile-image">
      <div class="profile-content">
        <h1 class="profile-name">Simon Salazar</h1>
        <p class="profile-title">Full Stack Developer & Design Enthusiast</p>
        <p class="profile-bio">
          I'm passionate about building beautiful, accessible web experiences 
          that make a difference. Currently exploring the intersection of design 
          systems and modern web technologies.
        </p>
        <div class="profile-actions">
          <a href="/blog" class="btn btn-primary">Read My Blog</a>
          <a href="/contact" class="btn btn-secondary">Get in Touch</a>
        </div>
        <div class="profile-social">
          <a href="https://github.com" aria-label="GitHub">
            <svg><!-- icon --></svg>
          </a>
          <a href="https://linkedin.com" aria-label="LinkedIn">
            <svg><!-- icon --></svg>
          </a>
          <a href="https://twitter.com" aria-label="Twitter">
            <svg><!-- icon --></svg>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
```

#### SCSS Implementation
```scss
.profile-section {
  padding: $spacing-12 0;
  background: linear-gradient(
    to bottom,
    $color-bg-surface,
    $color-bg-secondary
  );
}

.container-narrow {
  @include container-narrow;
}

.profile-card {
  display: grid;
  gap: $spacing-8;
  grid-template-columns: 1fr;
  
  @include md {
    grid-template-columns: 200px 1fr;
    gap: $spacing-10;
  }
}

.profile-image {
  width: 100%;
  max-width: 200px;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: $radius-2xl;
  box-shadow: $shadow-lg;
  margin: 0 auto;
  
  @include md {
    margin: 0;
  }
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: $spacing-4;
  text-align: center;
  
  @include md {
    text-align: left;
  }
}

.profile-name {
  font-size: $font-size-3xl;
  font-weight: $font-weight-bold;
  color: $color-text-primary;
  margin: 0;
}

.profile-title {
  font-size: $font-size-xl;
  color: $color-text-secondary;
  font-weight: $font-weight-medium;
}

.profile-bio {
  font-size: $font-size-base;
  line-height: $line-height-relaxed;
  color: $color-text-secondary;
  max-width: 600px;
}

.profile-actions {
  display: flex;
  gap: $spacing-3;
  flex-wrap: wrap;
  justify-content: center;
  
  @include md {
    justify-content: flex-start;
  }
}

.profile-social {
  display: flex;
  gap: $spacing-4;
  justify-content: center;
  
  @include md {
    justify-content: flex-start;
  }
  
  a {
    @include flex-center;
    width: $button-icon-md;
    height: $button-icon-md;
    color: $color-text-secondary;
    transition: $transition-colors;
    border-radius: $radius-full;
    
    @include hover {
      color: $color-primary-500;
      background-color: $color-primary-50;
    }
    
    svg {
      width: $icon-size-lg;
      height: $icon-size-lg;
    }
  }
}
```

---

### 5. Blog Carousel

#### HTML Structure
```html
<section class="blog-carousel-section">
  <div class="container">
    <h2 class="section-title">Latest Blog Posts</h2>
    <div class="blog-carousel">
      <!-- Repeat for each blog post -->
      <article class="card card-blog-post">
        <!-- Card content here -->
      </article>
    </div>
  </div>
</section>
```

#### SCSS Implementation
```scss
.blog-carousel-section {
  padding: $spacing-12 0;
}

.section-title {
  font-size: $font-size-3xl;
  font-weight: $font-weight-bold;
  color: $color-text-primary;
  margin-bottom: $spacing-8;
  text-align: center;
}

.blog-carousel {
  display: grid;
  gap: $spacing-6;
  
  // Mobile: 1 column with horizontal scroll
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  padding-bottom: $spacing-4;
  
  // Tablet: 2 columns
  @include md {
    grid-template-columns: repeat(2, 1fr);
    overflow-x: visible;
  }
  
  // Desktop: 3 columns
  @include lg {
    grid-template-columns: repeat(3, 1fr);
  }
  
  > * {
    scroll-snap-align: start;
  }
  
  // Hide scrollbar (optional)
  &::-webkit-scrollbar {
    display: none;
  }
  
  -ms-overflow-style: none;
  scrollbar-width: none;
}
```

---

### 6. Navigation Header

#### HTML Structure
```html
<header class="site-header">
  <div class="container">
    <div class="header-content">
      <a href="/" class="header-logo">
        <img src="/logo.svg" alt="Site Logo">
      </a>
      
      <nav class="header-nav" aria-label="Main navigation">
        <ul class="nav-list">
          <li><a href="/" class="nav-link">Home</a></li>
          <li><a href="/blog" class="nav-link">Blog</a></li>
          <li><a href="/about" class="nav-link">About</a></li>
          <li><a href="/contact" class="nav-link">Contact</a></li>
        </ul>
      </nav>
      
      <div class="header-actions">
        <button class="language-toggle" aria-label="Switch language">
          EN / ES
        </button>
      </div>
      
      <!-- Mobile menu toggle -->
      <button class="mobile-menu-toggle" aria-label="Toggle menu">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </div>
</header>
```

#### SCSS Implementation
```scss
.site-header {
  position: sticky;
  top: 0;
  z-index: $z-index-sticky;
  background-color: $color-bg-surface;
  border-bottom: 1px solid $color-border-light;
  box-shadow: $shadow-sm;
}

.header-content {
  @include flex-between;
  height: $header-height-mobile;
  
  @include lg {
    height: $header-height-desktop;
  }
}

.header-logo {
  @include flex-center;
  
  img {
    height: 32px;
    width: auto;
    
    @include lg {
      height: 40px;
    }
  }
}

.header-nav {
  display: none;
  
  @include lg {
    display: block;
  }
}

.nav-list {
  @include list-reset;
  @include flex-center;
  gap: $nav-item-spacing;
}

.nav-link {
  display: block;
  padding: $nav-item-padding $spacing-3;
  color: $color-text-secondary;
  font-weight: $font-weight-medium;
  text-decoration: none;
  transition: $transition-colors;
  border-radius: $radius-md;
  
  @include hover {
    color: $color-text-primary;
    background-color: $color-bg-secondary;
  }
  
  &.active {
    color: $color-primary-600;
    background-color: $color-primary-50;
  }
}

.header-actions {
  display: none;
  
  @include lg {
    display: flex;
    align-items: center;
    gap: $spacing-3;
  }
}

.language-toggle {
  @include button-reset;
  padding: $spacing-2 $spacing-3;
  color: $color-text-secondary;
  font-size: $font-size-sm;
  font-weight: $font-weight-medium;
  border-radius: $radius-md;
  transition: $transition-colors;
  
  @include hover {
    color: $color-text-primary;
    background-color: $color-bg-secondary;
  }
}

.mobile-menu-toggle {
  @include button-reset;
  @include flex-center;
  @include button-icon($button-icon-md);
  flex-direction: column;
  gap: 4px;
  
  @include lg {
    display: none;
  }
  
  span {
    display: block;
    width: 20px;
    height: 2px;
    background-color: $color-text-primary;
    transition: $transition-transform;
  }
  
  &[aria-expanded="true"] {
    span:nth-child(1) {
      transform: translateY(6px) rotate(45deg);
    }
    
    span:nth-child(2) {
      opacity: 0;
    }
    
    span:nth-child(3) {
      transform: translateY(-6px) rotate(-45deg);
    }
  }
}
```

---

### 7. Footer

#### HTML Structure
```html
<footer class="site-footer">
  <div class="container">
    <div class="footer-content">
      <div class="footer-column">
        <h3 class="footer-title">About</h3>
        <p class="footer-text">
          Personal blog and portfolio showcasing my work in web development 
          and design.
        </p>
      </div>
      
      <div class="footer-column">
        <h3 class="footer-title">Quick Links</h3>
        <ul class="footer-links">
          <li><a href="/">Home</a></li>
          <li><a href="/blog">Blog</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </div>
      
      <div class="footer-column">
        <h3 class="footer-title">Connect</h3>
        <div class="footer-social">
          <a href="#" aria-label="GitHub">GitHub</a>
          <a href="#" aria-label="LinkedIn">LinkedIn</a>
          <a href="#" aria-label="Twitter">Twitter</a>
        </div>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; 2026 Simon Salazar. All rights reserved.</p>
    </div>
  </div>
</footer>
```

#### SCSS Implementation
```scss
.site-footer {
  background-color: $color-neutral-900;
  color: $color-neutral-300;
  padding: $spacing-12 0 $spacing-6;
  margin-top: $spacing-16;
}

.footer-content {
  display: grid;
  gap: $spacing-8;
  grid-template-columns: 1fr;
  
  @include md {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @include lg {
    grid-template-columns: repeat(3, 1fr);
  }
}

.footer-column {
  display: flex;
  flex-direction: column;
  gap: $spacing-4;
}

.footer-title {
  font-size: $font-size-lg;
  font-weight: $font-weight-bold;
  color: $color-neutral-0;
  margin: 0;
}

.footer-text {
  font-size: $font-size-sm;
  line-height: $line-height-relaxed;
  margin: 0;
}

.footer-links {
  @include list-reset;
  display: flex;
  flex-direction: column;
  gap: $spacing-2;
  
  a {
    color: $color-neutral-300;
    text-decoration: none;
    transition: $transition-colors;
    
    @include hover {
      color: $color-neutral-0;
      padding-left: $spacing-2;
    }
  }
}

.footer-social {
  display: flex;
  gap: $spacing-4;
  
  a {
    color: $color-neutral-300;
    font-size: $font-size-sm;
    text-decoration: none;
    transition: $transition-colors;
    
    @include hover {
      color: $color-primary-400;
    }
  }
}

.footer-bottom {
  margin-top: $spacing-8;
  padding-top: $spacing-6;
  border-top: 1px solid $color-neutral-800;
  text-align: center;
  
  p {
    font-size: $font-size-sm;
    color: $color-neutral-500;
    margin: 0;
  }
}
```

---

## Responsive Patterns

### Mobile-First Grid

```scss
.grid {
  display: grid;
  gap: $spacing-4;
  
  // Mobile: 1 column
  grid-template-columns: 1fr;
  
  // Tablet: 2 columns
  @include md {
    gap: $spacing-6;
    grid-template-columns: repeat(2, 1fr);
  }
  
  // Desktop: 3 columns
  @include lg {
    gap: $spacing-8;
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Fluid Typography

```scss
.heading {
  // Automatically scales from 24px to 36px
  font-size: $font-size-3xl;
  
  // Or use custom fluid sizing
  @include fluid-type(1.5rem, 2.25rem);
}
```

---

## Accessibility Checklist

### ✅ Color Contrast
- Text: Minimum 4.5:1 (use `neutral-600` or darker on white)
- Large text: Minimum 3:1
- UI components: Minimum 3:1

### ✅ Focus States
- Always visible on keyboard navigation
- Use `@include focus-visible` mixin
- Never use `outline: none` without replacement

### ✅ Touch Targets
- Minimum 44×44px for interactive elements
- Use `$button-height-md` or larger

### ✅ Semantic HTML
```html
<!-- Good: Semantic structure -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<!-- Bad: Non-semantic -->
<div class="header">
  <div class="nav">
    <div><span onclick="...">Home</span></div>
  </div>
</div>
```

### ✅ ARIA Labels
```html
<!-- Icon-only buttons MUST have labels -->
<button class="btn-icon" aria-label="Close modal">
  <svg><!-- X icon --></svg>
</button>

<!-- Language toggle -->
<button aria-label="Switch to Spanish" lang="es">ES</button>
```

---

## Performance Best Practices

### 1. Load Critical CSS First
```html
<head>
  <!-- Critical above-the-fold styles -->
  <style>
    /* Inline critical CSS here */
  </style>
  
  <!-- Defer non-critical styles -->
  <link rel="preload" href="/css/style.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
</head>
```

### 2. Optimize Images
- Use Contentful CDN URLs (never download)
- Specify width and height attributes
- Use modern formats (WebP with fallback)

```html
<picture>
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description" width="800" height="600" loading="lazy">
</picture>
```

### 3. Reduce Motion
```scss
// Always include this global rule
@include reduce-motion;
```

---

## Testing Checklist

### Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Mobile Chrome (Android)

### Responsive Testing
- [ ] Mobile (375px - iPhone SE)
- [ ] Mobile (414px - iPhone Pro Max)
- [ ] Tablet (768px - iPad)
- [ ] Desktop (1280px)
- [ ] Wide (1920px)

### Accessibility Testing
- [ ] WAVE browser extension
- [ ] axe DevTools
- [ ] Lighthouse audit (score > 90)
- [ ] Keyboard navigation (Tab, Enter, Esc)
- [ ] Screen reader testing (VoiceOver/NVDA)

### Performance Testing
- [ ] Lighthouse Performance (score > 85)
- [ ] Total page size < 1MB
- [ ] First Contentful Paint < 2s
- [ ] Time to Interactive < 3s

---

## Common Gotchas

### ❌ Don't Mix Naming Conventions
```scss
// Bad
.blogCard {
  background: $color_primary;
}

// Good
.blog-card {
  background: $color-primary-500;
}
```

### ❌ Don't Use Arbitrary Values
```scss
// Bad
.card {
  padding: 18px;
  margin-top: 35px;
}

// Good
.card {
  padding: $spacing-4;  // 16px
  margin-top: $spacing-8; // 32px
}
```

### ❌ Don't Skip Focus States
```scss
// Bad
button:focus {
  outline: none; // ❌ Removes accessibility
}

// Good
button {
  @include focus-visible; // ✅ Custom accessible focus
}
```

---

## Resources

### Design Tools
- [Figma Community - Design System Templates](https://www.figma.com/community)
- [Coolors - Color Palette Generator](https://coolors.co/)
- [Type Scale Calculator](https://type-scale.com/)

### Development Tools
- [Sass Documentation](https://sass-lang.com/documentation)
- [CSS Grid Generator](https://cssgrid-generator.netlify.app/)
- [Flexbox Cheatsheet](https://flexbox.malven.co/)

### Testing Tools
- [WAVE (Web Accessibility Evaluation Tool)](https://wave.webaim.org/)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)

---

## Summary

This design system provides:

✅ **Comprehensive design tokens** for colors, typography, spacing  
✅ **Reusable Sass mixins** for components and layouts  
✅ **Mobile-first responsive** patterns  
✅ **Accessibility-first** approach (WCAG AA)  
✅ **Performance-optimized** practices  
✅ **Production-ready** component examples

**Next Steps:**
1. Import variables and mixins into your stylesheet
2. Build components using the provided examples
3. Test across devices and browsers
4. Run accessibility audits
5. Optimize for performance

---

**Version:** 1.0  
**Status:** ✅ Ready for Use  
**Maintained By:** Simon Salazar
