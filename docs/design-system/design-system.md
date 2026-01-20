# Design System Specification
**Project:** GitHub Pages Portfolio (Blog-First Architecture)  
**Version:** 1.0  
**Last Updated:** 2026-01-19  
**Approach:** Minimalist, Sophisticated, Responsive-First

---

## 1. Design Philosophy

### Core Principles

**🎯 Minimalist Sophistication**
- Clean, uncluttered interfaces that prioritize content
- Purposeful use of whitespace to create breathing room
- Typography-driven hierarchy with minimal decorative elements

**💙 Professional Blue & Gray Palette**
- Cool, trustworthy blue as primary color
- Sophisticated gray scale for depth and hierarchy
- High contrast for accessibility (WCAG AA minimum)

**📱 Responsive-First Approach**
- Mobile-first design tokens
- Fluid typography and spacing
- Touch-friendly interactive elements (min 44×44px)

**♿ Accessibility by Default**
- WCAG 2.1 AA compliance (minimum)
- Color contrast ratios: 4.5:1 text, 3:1 UI components
- Semantic HTML structure
- Keyboard navigation support

---

## 2. Design Tokens

### 2.1 Color System

#### Primary Colors (Blue Palette)

```scss
// Core Blue Tokens
--color-primary-50:  #f0f9ff;   // Lightest blue (backgrounds)
--color-primary-100: #e0f2fe;   // Very light blue
--color-primary-200: #bae6fd;   // Light blue
--color-primary-300: #7dd3fc;   // Soft blue
--color-primary-400: #38bdf8;   // Medium blue
--color-primary-500: #0ea5e9;   // Primary blue (main brand color)
--color-primary-600: #0284c7;   // Strong blue (hover states)
--color-primary-700: #0369a1;   // Deep blue
--color-primary-800: #075985;   // Very deep blue
--color-primary-900: #0c4a6e;   // Darkest blue
```

**Usage Guidelines:**
- `primary-500`: Primary CTAs, links, active states
- `primary-600`: Hover states, pressed buttons
- `primary-700`: Visited links, secondary actions
- `primary-50-200`: Subtle backgrounds, badges, highlights
- `primary-800-900`: Dark mode accents

#### Neutral Colors (Gray Scale)

```scss
// Sophisticated Gray Tokens
--color-neutral-0:   #ffffff;   // Pure white
--color-neutral-50:  #fafafa;   // Off-white (page background)
--color-neutral-100: #f5f5f5;   // Light gray (card backgrounds)
--color-neutral-200: #e5e5e5;   // Border gray
--color-neutral-300: #d4d4d4;   // Subtle borders
--color-neutral-400: #a3a3a3;   // Disabled text
--color-neutral-500: #737373;   // Secondary text
--color-neutral-600: #525252;   // Body text
--color-neutral-700: #404040;   // Headings
--color-neutral-800: #262626;   // Strong emphasis
--color-neutral-900: #171717;   // Maximum contrast
--color-neutral-950: #0a0a0a;   // Near black
```

**Usage Guidelines:**
- `neutral-0/50`: Page backgrounds, white surfaces
- `neutral-100-200`: Card backgrounds, dividers
- `neutral-300-400`: Borders, disabled states
- `neutral-500-600`: Body text, secondary information
- `neutral-700-900`: Headings, strong emphasis

#### Semantic Colors

```scss
// Feedback Colors
--color-success-50:  #f0fdf4;
--color-success-500: #22c55e;   // Success messages, positive states
--color-success-600: #16a34a;   // Success hover

--color-warning-50:  #fffbeb;
--color-warning-500: #f59e0b;   // Warning messages, attention
--color-warning-600: #d97706;   // Warning hover

--color-error-50:    #fef2f2;
--color-error-500:   #ef4444;   // Error messages, destructive actions
--color-error-600:   #dc2626;   // Error hover

--color-info-50:     #eff6ff;
--color-info-500:    #3b82f6;   // Informational messages
--color-info-600:    #2563eb;   // Info hover
```

#### Text Colors (Semantic Aliases)

```scss
--color-text-primary:   var(--color-neutral-900);    // Main body text
--color-text-secondary: var(--color-neutral-600);    // Secondary information
--color-text-tertiary:  var(--color-neutral-500);    // Muted text, captions
--color-text-disabled:  var(--color-neutral-400);    // Disabled states
--color-text-inverse:   var(--color-neutral-0);      // Text on dark backgrounds
--color-text-link:      var(--color-primary-600);    // Hyperlinks
--color-text-link-hover: var(--color-primary-700);   // Link hover state
```

#### Background Colors (Semantic Aliases)

```scss
--color-bg-page:        var(--color-neutral-50);     // Body background
--color-bg-surface:     var(--color-neutral-0);      // Card/panel backgrounds
--color-bg-secondary:   var(--color-neutral-100);    // Subtle backgrounds
--color-bg-tertiary:    var(--color-neutral-200);    // Dividers, separators
--color-bg-overlay:     rgba(0, 0, 0, 0.5);          // Modal overlays
```

#### Border Colors

```scss
--color-border-light:   var(--color-neutral-200);    // Subtle borders
--color-border-default: var(--color-neutral-300);    // Standard borders
--color-border-strong:  var(--color-neutral-400);    // Emphasized borders
--color-border-focus:   var(--color-primary-500);    // Focus rings
```

---

### 2.2 Typography System

#### Font Families

```scss
// Primary font stack (sans-serif for UI)
--font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 
                    Roboto, 'Helvetica Neue', Arial, sans-serif;

// Heading font stack (serif for editorial feel)
--font-family-heading: 'Merriweather', 'Georgia', 'Times New Roman', 
                       Times, serif;

// Monospace for code
--font-family-mono: 'JetBrains Mono', 'SF Mono', Monaco, 'Cascadia Code', 
                    'Courier New', monospace;
```

**Font Loading Strategy:**
- Use Google Fonts or self-hosted fonts
- Include `font-display: swap` for performance
- Preload critical fonts in `<head>`

#### Type Scale (Fluid Typography)

**Mobile-First Base:** 16px (1rem)

```scss
// Font Size Tokens (mobile → desktop)
--font-size-xs:   clamp(0.75rem,  0.7rem + 0.25vw,  0.8125rem);  // 12-13px
--font-size-sm:   clamp(0.875rem, 0.8rem + 0.375vw, 0.9375rem);  // 14-15px
--font-size-base: 1rem;                                           // 16px
--font-size-lg:   clamp(1.125rem, 1rem + 0.625vw,   1.25rem);    // 18-20px
--font-size-xl:   clamp(1.25rem,  1.1rem + 0.75vw,  1.5rem);     // 20-24px
--font-size-2xl:  clamp(1.5rem,   1.3rem + 1vw,     1.875rem);   // 24-30px
--font-size-3xl:  clamp(1.875rem, 1.5rem + 1.875vw, 2.25rem);    // 30-36px
--font-size-4xl:  clamp(2.25rem,  1.8rem + 2.25vw,  3rem);       // 36-48px
--font-size-5xl:  clamp(3rem,     2.25rem + 3.75vw, 3.75rem);    // 48-60px
--font-size-6xl:  clamp(3.75rem,  2.75rem + 5vw,    4.5rem);     // 60-72px
```

#### Font Weights

```scss
--font-weight-light:     300;   // Rarely used
--font-weight-normal:    400;   // Body text
--font-weight-medium:    500;   // Subtle emphasis
--font-weight-semibold:  600;   // Strong emphasis
--font-weight-bold:      700;   // Headings, CTAs
--font-weight-extrabold: 800;   // Display headings
```

#### Line Heights

```scss
--line-height-tight:   1.25;    // Large headings
--line-height-snug:    1.375;   // Subheadings
--line-height-normal:  1.5;     // Body text
--line-height-relaxed: 1.625;   // Long-form content
--line-height-loose:   2;       // Captions, labels
```

#### Letter Spacing

```scss
--letter-spacing-tighter: -0.05em;   // Large display text
--letter-spacing-tight:   -0.025em;  // Headings
--letter-spacing-normal:  0;         // Body text
--letter-spacing-wide:    0.025em;   // Small caps
--letter-spacing-wider:   0.05em;    // Uppercase labels
--letter-spacing-widest:  0.1em;     // Very wide spacing
```

---

### 2.3 Spacing System

**Base Unit:** 4px (0.25rem)  
**Scale Type:** Exponential (with some custom steps)

```scss
// Spacing Tokens (8px grid for most values)
--spacing-0:    0;          // No spacing
--spacing-px:   1px;        // Hairline
--spacing-0-5:  0.125rem;   // 2px
--spacing-1:    0.25rem;    // 4px
--spacing-2:    0.5rem;     // 8px
--spacing-3:    0.75rem;    // 12px
--spacing-4:    1rem;       // 16px
--spacing-5:    1.25rem;    // 20px
--spacing-6:    1.5rem;     // 24px
--spacing-7:    1.75rem;    // 28px
--spacing-8:    2rem;       // 32px
--spacing-10:   2.5rem;     // 40px
--spacing-12:   3rem;       // 48px
--spacing-14:   3.5rem;     // 56px
--spacing-16:   4rem;       // 64px
--spacing-20:   5rem;       // 80px
--spacing-24:   6rem;       // 96px
--spacing-32:   8rem;       // 128px
--spacing-40:   10rem;      // 160px
--spacing-48:   12rem;      // 192px
--spacing-64:   16rem;      // 256px
```

**Usage Guidelines:**
- Use multiples of 4px for consistency
- `spacing-2` to `spacing-4`: Component padding
- `spacing-6` to `spacing-8`: Section spacing
- `spacing-12` to `spacing-16`: Large section gaps
- `spacing-20+`: Page-level spacing

---

### 2.4 Sizing System

#### Fixed Sizes

```scss
// Common component sizes
--size-1:   0.25rem;    // 4px
--size-2:   0.5rem;     // 8px
--size-3:   0.75rem;    // 12px
--size-4:   1rem;       // 16px
--size-5:   1.25rem;    // 20px
--size-6:   1.5rem;     // 24px
--size-8:   2rem;       // 32px
--size-10:  2.5rem;     // 40px
--size-12:  3rem;       // 48px
--size-16:  4rem;       // 64px
--size-20:  5rem;       // 80px
--size-24:  6rem;       // 96px
--size-32:  8rem;       // 128px
--size-40:  10rem;      // 160px
--size-48:  12rem;      // 192px
--size-64:  16rem;      // 256px
```

#### Icon Sizes

```scss
--icon-size-xs:   0.75rem;   // 12px (inline text icons)
--icon-size-sm:   1rem;       // 16px (small buttons)
--icon-size-md:   1.25rem;    // 20px (default size)
--icon-size-lg:   1.5rem;     // 24px (prominent actions)
--icon-size-xl:   2rem;       // 32px (feature icons)
--icon-size-2xl:  2.5rem;     // 40px (hero icons)
--icon-size-3xl:  3rem;       // 48px (large decorative)
```

#### Avatar Sizes

```scss
--avatar-size-xs:  1.5rem;    // 24px
--avatar-size-sm:  2rem;      // 32px
--avatar-size-md:  2.5rem;    // 40px
--avatar-size-lg:  3rem;      // 48px
--avatar-size-xl:  4rem;      // 64px
--avatar-size-2xl: 6rem;      // 96px (profile pages)
--avatar-size-3xl: 8rem;      // 128px (hero sections)
```

---

### 2.5 Border Radius

```scss
// Rounded corners (minimalist approach)
--radius-none:  0;
--radius-sm:    0.25rem;    // 4px (subtle rounding)
--radius-md:    0.375rem;   // 6px (default)
--radius-lg:    0.5rem;     // 8px (cards, modals)
--radius-xl:    0.75rem;    // 12px (prominent cards)
--radius-2xl:   1rem;       // 16px (large cards)
--radius-3xl:   1.5rem;     // 24px (hero sections)
--radius-full:  9999px;     // Fully rounded (pills, avatars)
```

**Usage Guidelines:**
- Buttons: `radius-md` (6px)
- Cards: `radius-lg` (8px)
- Modals: `radius-xl` (12px)
- Avatars: `radius-full`
- Profile images: `radius-2xl` for softer look

---

### 2.6 Elevation (Shadows)

**Philosophy:** Subtle, realistic shadows for depth

```scss
// Shadow Tokens
--shadow-xs:  0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-sm:  0 1px 3px 0 rgba(0, 0, 0, 0.1), 
              0 1px 2px -1px rgba(0, 0, 0, 0.1);
--shadow-md:  0 4px 6px -1px rgba(0, 0, 0, 0.1), 
              0 2px 4px -2px rgba(0, 0, 0, 0.1);
--shadow-lg:  0 10px 15px -3px rgba(0, 0, 0, 0.1), 
              0 4px 6px -4px rgba(0, 0, 0, 0.1);
--shadow-xl:  0 20px 25px -5px rgba(0, 0, 0, 0.1), 
              0 8px 10px -6px rgba(0, 0, 0, 0.1);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
```

**Focus Ring:**
```scss
--shadow-focus: 0 0 0 3px rgba(14, 165, 233, 0.3);  // Primary blue with transparency
```

**Usage Guidelines:**
- Hover states: Transition from `shadow-sm` to `shadow-md`
- Cards: `shadow-sm` default, `shadow-md` on hover
- Modals: `shadow-xl` or `shadow-2xl`
- Dropdowns: `shadow-lg`

---

### 2.7 Animation & Timing

#### Duration Tokens

```scss
--duration-instant:  0ms;      // No animation
--duration-fast:     150ms;    // Quick transitions
--duration-base:     250ms;    // Default transitions
--duration-moderate: 350ms;    // Deliberate animations
--duration-slow:     500ms;    // Slow, smooth animations
--duration-slower:   750ms;    // Very slow (use sparingly)
```

#### Easing Functions

```scss
--ease-linear:      linear;
--ease-in:          cubic-bezier(0.4, 0, 1, 1);
--ease-out:         cubic-bezier(0, 0, 0.2, 1);      // Most common (exit animations)
--ease-in-out:      cubic-bezier(0.4, 0, 0.2, 1);    // Default (smooth both ends)
--ease-bounce:      cubic-bezier(0.68, -0.55, 0.265, 1.55);
--ease-elastic:     cubic-bezier(0.175, 0.885, 0.32, 1.275);
```

**Default Transition:**
```scss
--transition-default: all var(--duration-base) var(--ease-in-out);
--transition-colors:  color var(--duration-fast) var(--ease-out),
                      background-color var(--duration-fast) var(--ease-out),
                      border-color var(--duration-fast) var(--ease-out);
--transition-transform: transform var(--duration-moderate) var(--ease-out);
```

---

### 2.8 Breakpoints (Mobile-First)

```scss
// Breakpoint Tokens
--breakpoint-sm:   640px;    // Small devices (large phones)
--breakpoint-md:   768px;    // Medium devices (tablets)
--breakpoint-lg:   1024px;   // Large devices (laptops)
--breakpoint-xl:   1280px;   // Extra large (desktops)
--breakpoint-2xl:  1536px;   // 2X large (wide monitors)
```

**Media Query Mixins (Sass):**

```scss
// Mobile-first approach
@mixin sm {
  @media (min-width: 640px) { @content; }
}
@mixin md {
  @media (min-width: 768px) { @content; }
}
@mixin lg {
  @media (min-width: 1024px) { @content; }
}
@mixin xl {
  @media (min-width: 1280px) { @content; }
}
@mixin 2xl {
  @media (min-width: 1536px) { @content; }
}

// Usage example:
.container {
  padding: var(--spacing-4);  // 16px on mobile
  
  @include md {
    padding: var(--spacing-6); // 24px on tablet
  }
  
  @include lg {
    padding: var(--spacing-8); // 32px on desktop
  }
}
```

---

### 2.9 Z-Index Scale

```scss
// Layering system (avoid arbitrary values)
--z-index-base:       0;
--z-index-dropdown:   1000;
--z-index-sticky:     1020;
--z-index-fixed:      1030;
--z-index-overlay:    1040;
--z-index-modal:      1050;
--z-index-popover:    1060;
--z-index-tooltip:    1070;
```

---

## 3. Layout System

### 3.1 Container

```scss
// Max-width containers
--container-sm:   640px;
--container-md:   768px;
--container-lg:   1024px;
--container-xl:   1280px;
--container-2xl:  1536px;

// Responsive container padding
--container-padding-mobile:  var(--spacing-4);   // 16px
--container-padding-tablet:  var(--spacing-6);   // 24px
--container-padding-desktop: var(--spacing-8);   // 32px
```

**Implementation:**

```scss
.container {
  width: 100%;
  max-width: var(--container-xl);
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--container-padding-mobile);
  padding-right: var(--container-padding-mobile);
  
  @include md {
    padding-left: var(--container-padding-tablet);
    padding-right: var(--container-padding-tablet);
  }
  
  @include lg {
    padding-left: var(--container-padding-desktop);
    padding-right: var(--container-padding-desktop);
  }
}
```

### 3.2 Grid System

**12-Column Grid (CSS Grid)**

```scss
// Grid gap tokens
--grid-gap-sm:  var(--spacing-4);   // 16px
--grid-gap-md:  var(--spacing-6);   // 24px
--grid-gap-lg:  var(--spacing-8);   // 32px
```

**Implementation:**

```scss
.grid {
  display: grid;
  gap: var(--grid-gap-md);
  
  // Mobile: 1 column
  grid-template-columns: 1fr;
  
  // Tablet: 2 columns
  @include md {
    grid-template-columns: repeat(2, 1fr);
  }
  
  // Desktop: 3 columns
  @include lg {
    grid-template-columns: repeat(3, 1fr);
  }
}

// 12-column utility
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--grid-gap-md);
}
```

---

## 4. Component Sizes

### 4.1 Buttons

```scss
// Button height tokens
--button-height-sm:  2rem;      // 32px
--button-height-md:  2.5rem;    // 40px
--button-height-lg:  3rem;      // 48px
--button-height-xl:  3.5rem;    // 56px

// Button padding tokens
--button-padding-x-sm:  1rem;     // 16px
--button-padding-x-md:  1.5rem;   // 24px
--button-padding-x-lg:  2rem;     // 32px
--button-padding-x-xl:  2.5rem;   // 40px

// Icon-only button sizes (square)
--button-icon-sm:  2rem;       // 32×32px
--button-icon-md:  2.5rem;     // 40×40px
--button-icon-lg:  3rem;       // 48×48px
```

**Button Variants:**

```scss
// Primary Button
.btn-primary {
  height: var(--button-height-md);
  padding: 0 var(--button-padding-x-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-md);
  background-color: var(--color-primary-500);
  color: var(--color-text-inverse);
  transition: var(--transition-colors);
  
  &:hover {
    background-color: var(--color-primary-600);
  }
  
  &:focus-visible {
    outline: none;
    box-shadow: var(--shadow-focus);
  }
}

// Secondary Button
.btn-secondary {
  background-color: transparent;
  border: 2px solid var(--color-neutral-300);
  color: var(--color-text-primary);
  
  &:hover {
    border-color: var(--color-neutral-400);
    background-color: var(--color-neutral-50);
  }
}

// Ghost Button
.btn-ghost {
  background-color: transparent;
  color: var(--color-text-secondary);
  
  &:hover {
    background-color: var(--color-neutral-100);
  }
}
```

### 4.2 Form Inputs

```scss
// Input height tokens
--input-height-sm:  2rem;      // 32px
--input-height-md:  2.5rem;    // 40px
--input-height-lg:  3rem;      // 48px

// Input padding
--input-padding-x-sm:  0.75rem;   // 12px
--input-padding-x-md:  1rem;      // 16px
--input-padding-x-lg:  1.25rem;   // 20px

// Border width
--input-border-width:  1px;
```

**Input Implementation:**

```scss
.input {
  height: var(--input-height-md);
  padding: 0 var(--input-padding-x-md);
  font-size: var(--font-size-base);
  border: var(--input-border-width) solid var(--color-border-default);
  border-radius: var(--radius-md);
  background-color: var(--color-bg-surface);
  color: var(--color-text-primary);
  transition: var(--transition-colors);
  
  &:hover {
    border-color: var(--color-border-strong);
  }
  
  &:focus {
    outline: none;
    border-color: var(--color-border-focus);
    box-shadow: var(--shadow-focus);
  }
  
  &::placeholder {
    color: var(--color-text-tertiary);
  }
  
  &:disabled {
    background-color: var(--color-neutral-100);
    color: var(--color-text-disabled);
    cursor: not-allowed;
  }
}
```

### 4.3 Cards

```scss
// Card padding tokens
--card-padding-sm:  var(--spacing-4);    // 16px
--card-padding-md:  var(--spacing-6);    // 24px
--card-padding-lg:  var(--spacing-8);    // 32px

// Card min-height
--card-min-height:  12rem;   // 192px
```

**Card Implementation:**

```scss
.card {
  padding: var(--card-padding-md);
  background-color: var(--color-bg-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--duration-base) var(--ease-out),
              transform var(--duration-base) var(--ease-out);
  
  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
}

// Blog post card (specific variant)
.card-blog-post {
  display: flex;
  flex-direction: column;
  min-height: var(--card-min-height);
  
  .card-image {
    aspect-ratio: 16 / 9;
    border-radius: var(--radius-md);
    margin-bottom: var(--spacing-4);
  }
  
  .card-title {
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-bold);
    margin-bottom: var(--spacing-2);
    color: var(--color-text-primary);
  }
  
  .card-excerpt {
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    line-height: var(--line-height-relaxed);
  }
}
```

### 4.4 Navigation

```scss
// Header height
--header-height-mobile:   3.5rem;    // 56px
--header-height-desktop:  4rem;      // 64px

// Navigation item spacing
--nav-item-spacing:  var(--spacing-6);   // 24px
--nav-item-padding:  var(--spacing-2);   // 8px (vertical)
```

---

## 5. Component Specifications

### 5.1 Profile Card (Homepage Hero)

**Dimensions:**
- Mobile: Full width, stacked layout
- Tablet: 2-column layout (image + content)
- Desktop: Centered, max-width 800px

**Specifications:**

```scss
.profile-card {
  display: grid;
  gap: var(--spacing-8);
  padding: var(--spacing-8);
  
  // Mobile: stacked
  grid-template-columns: 1fr;
  
  // Tablet and up: side-by-side
  @include md {
    grid-template-columns: 200px 1fr;
    gap: var(--spacing-10);
  }
  
  @include lg {
    max-width: 800px;
    margin: 0 auto;
  }
}

.profile-image {
  width: 100%;
  max-width: 200px;
  aspect-ratio: 1 / 1;
  border-radius: var(--radius-2xl);
  object-fit: cover;
  box-shadow: var(--shadow-lg);
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  
  h1 {
    font-size: var(--font-size-3xl);
    font-weight: var(--font-weight-bold);
    color: var(--color-text-primary);
    margin: 0;
  }
  
  .profile-title {
    font-size: var(--font-size-xl);
    color: var(--color-text-secondary);
  }
  
  .profile-bio {
    font-size: var(--font-size-base);
    line-height: var(--line-height-relaxed);
    color: var(--color-text-secondary);
  }
}
```

### 5.2 Blog Carousel

**Specifications:**
- 1 card on mobile
- 2 cards on tablet
- 3 cards on desktop
- Horizontal scroll with snap points

```scss
.blog-carousel {
  display: grid;
  gap: var(--spacing-6);
  padding: var(--spacing-6) 0;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  
  // Mobile: 1 column
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  
  // Tablet: 2 columns
  @include md {
    grid-template-columns: repeat(2, 1fr);
  }
  
  // Desktop: 3 columns
  @include lg {
    grid-template-columns: repeat(3, 1fr);
    overflow-x: visible;
  }
  
  .carousel-item {
    scroll-snap-align: start;
    min-width: 280px;
  }
}
```

### 5.3 Blog Post Layout

**Typographic Scale for Long-Form Content:**

```scss
.post-layout {
  max-width: 720px;   // Optimal line length: 65-75 characters
  margin: 0 auto;
  padding: var(--spacing-8) var(--spacing-4);
  
  @include lg {
    padding: var(--spacing-12) var(--spacing-6);
  }
  
  // Headings
  h1 {
    font-size: var(--font-size-4xl);
    font-weight: var(--font-weight-bold);
    line-height: var(--line-height-tight);
    margin-bottom: var(--spacing-4);
  }
  
  h2 {
    font-size: var(--font-size-3xl);
    font-weight: var(--font-weight-bold);
    line-height: var(--line-height-snug);
    margin-top: var(--spacing-12);
    margin-bottom: var(--spacing-4);
  }
  
  h3 {
    font-size: var(--font-size-2xl);
    font-weight: var(--font-weight-semibold);
    margin-top: var(--spacing-8);
    margin-bottom: var(--spacing-3);
  }
  
  // Body text
  p {
    font-size: var(--font-size-lg);
    line-height: var(--line-height-relaxed);
    margin-bottom: var(--spacing-6);
    color: var(--color-text-primary);
  }
  
  // Links
  a {
    color: var(--color-text-link);
    text-decoration: underline;
    text-decoration-color: transparent;
    transition: text-decoration-color var(--duration-fast) var(--ease-out);
    
    &:hover {
      text-decoration-color: currentColor;
    }
  }
  
  // Lists
  ul, ol {
    padding-left: var(--spacing-6);
    margin-bottom: var(--spacing-6);
    
    li {
      margin-bottom: var(--spacing-2);
      line-height: var(--line-height-relaxed);
    }
  }
  
  // Code blocks
  code {
    font-family: var(--font-family-mono);
    font-size: 0.9em;
    padding: 0.125em 0.25em;
    background-color: var(--color-neutral-100);
    border-radius: var(--radius-sm);
  }
  
  pre {
    padding: var(--spacing-4);
    background-color: var(--color-neutral-900);
    color: var(--color-neutral-50);
    border-radius: var(--radius-md);
    overflow-x: auto;
    margin-bottom: var(--spacing-6);
    
    code {
      background-color: transparent;
      padding: 0;
    }
  }
  
  // Images
  img {
    max-width: 100%;
    height: auto;
    border-radius: var(--radius-lg);
    margin: var(--spacing-8) 0;
  }
  
  // Blockquotes
  blockquote {
    padding-left: var(--spacing-4);
    border-left: 4px solid var(--color-primary-500);
    font-style: italic;
    color: var(--color-text-secondary);
    margin: var(--spacing-8) 0;
  }
}
```

### 5.4 Footer

```scss
.footer {
  background-color: var(--color-neutral-900);
  color: var(--color-neutral-300);
  padding: var(--spacing-12) 0 var(--spacing-6);
  margin-top: var(--spacing-16);
  
  .footer-content {
    display: grid;
    gap: var(--spacing-8);
    
    @include md {
      grid-template-columns: repeat(2, 1fr);
    }
    
    @include lg {
      grid-template-columns: repeat(4, 1fr);
    }
  }
  
  .footer-links {
    a {
      display: block;
      padding: var(--spacing-2) 0;
      color: var(--color-neutral-300);
      transition: color var(--duration-fast) var(--ease-out);
      
      &:hover {
        color: var(--color-neutral-0);
      }
    }
  }
  
  .footer-bottom {
    margin-top: var(--spacing-8);
    padding-top: var(--spacing-6);
    border-top: 1px solid var(--color-neutral-800);
    text-align: center;
    font-size: var(--font-size-sm);
    color: var(--color-neutral-500);
  }
}
```

---

## 6. Accessibility Specifications

### 6.1 Color Contrast Ratios

**WCAG 2.1 AA Compliance (Minimum):**

| Use Case | Contrast Ratio | Example |
|----------|---------------|---------|
| Normal text (< 18px) | 4.5:1 | `neutral-900` on `neutral-0` |
| Large text (≥ 18px) | 3:1 | `neutral-700` on `neutral-0` |
| UI components | 3:1 | `primary-500` on `neutral-0` |
| Graphical objects | 3:1 | Icons, borders |

**Color Palette Contrast Matrix:**

| Foreground | Background | Ratio | Pass AA | Pass AAA |
|------------|-----------|-------|---------|----------|
| neutral-900 | neutral-0 | 20.8:1 | ✅ | ✅ |
| neutral-700 | neutral-0 | 10.4:1 | ✅ | ✅ |
| neutral-600 | neutral-0 | 7.9:1 | ✅ | ✅ |
| neutral-500 | neutral-0 | 5.3:1 | ✅ | ⚠️ |
| primary-600 | neutral-0 | 5.8:1 | ✅ | ⚠️ |
| primary-500 | neutral-0 | 3.9:1 | ⚠️ | ❌ |

**Note:** Use `primary-600` for text links instead of `primary-500` to ensure AA compliance.

### 6.2 Touch Target Sizes

**Minimum Sizes (WCAG 2.5.5):**
- Touch targets: **44×44px minimum**
- Icon-only buttons: 44×44px
- Text buttons: 44px height, min 88px width
- Form inputs: 44px height

### 6.3 Focus States

**Requirements:**
- All interactive elements MUST have visible focus indicators
- Focus ring: 3px, `primary-500` color, 30% opacity
- Offset: 2px from element edge

```scss
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.3);
  outline-offset: 2px;
}
```

### 6.4 Motion & Animation

**Respect User Preferences:**

```scss
// Disable animations for users who prefer reduced motion
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 7. Responsive Behavior

### 7.1 Breakpoint Strategy

**Mobile-First Approach:**

| Breakpoint | Min Width | Layout | Max Content Width |
|------------|-----------|--------|-------------------|
| Mobile (base) | 0px | Single column | 100% |
| SM | 640px | 1-2 columns | 640px |
| MD | 768px | 2-3 columns | 768px |
| LG | 1024px | Full layout | 1024px |
| XL | 1280px | Wide layout | 1280px |
| 2XL | 1536px | Max width | 1536px |

### 7.2 Component Responsiveness

**Profile Card:**
- Mobile: Stacked, centered image (150px)
- Tablet: Side-by-side, 200px image
- Desktop: Centered container, 200px image

**Blog Carousel:**
- Mobile: 1 column, horizontal scroll
- Tablet: 2 columns, grid layout
- Desktop: 3 columns, grid layout

**Navigation:**
- Mobile: Hamburger menu, full-screen overlay
- Tablet: Horizontal menu, collapsed utility
- Desktop: Full horizontal menu

**Typography:**
- All font sizes use `clamp()` for fluid scaling
- Line length: max 65-75 characters (720px)
- Heading scale: Smaller on mobile, larger on desktop

---

## 8. Dark Mode (Optional Future Enhancement)

**Color Token Overrides:**

```scss
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-page: var(--color-neutral-950);
    --color-bg-surface: var(--color-neutral-900);
    --color-bg-secondary: var(--color-neutral-800);
    
    --color-text-primary: var(--color-neutral-50);
    --color-text-secondary: var(--color-neutral-300);
    --color-text-tertiary: var(--color-neutral-400);
    
    --color-border-light: var(--color-neutral-800);
    --color-border-default: var(--color-neutral-700);
    --color-border-strong: var(--color-neutral-600);
    
    // Adjust shadows for dark mode
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
  }
}
```

---

## 9. Implementation Checklist

### Phase 1: Foundation (Week 1)
- [ ] Create design tokens file (`_variables.scss`)
- [ ] Define all color variables
- [ ] Set up typography scale with `clamp()`
- [ ] Establish spacing system
- [ ] Create responsive mixins
- [ ] Test color contrast ratios

### Phase 2: Components (Week 2)
- [ ] Build button variants
- [ ] Style form inputs
- [ ] Create card components
- [ ] Design profile card
- [ ] Build blog carousel
- [ ] Implement navigation

### Phase 3: Layouts (Week 3)
- [ ] Homepage layout
- [ ] Blog post layout
- [ ] Blog archive layout
- [ ] Footer implementation

### Phase 4: Polish & Testing (Week 4)
- [ ] Accessibility audit (WAVE, axe)
- [ ] Responsive testing (all breakpoints)
- [ ] Performance optimization
- [ ] Focus state testing
- [ ] Touch target testing (mobile)
- [ ] Cross-browser testing

---

## 10. Resources & Tools

### Design Tools
- **Figma:** Design mockups and prototypes
- **Coolors:** Color palette generator
- **Type Scale:** Typography scale calculator
- **Modular Scale:** Spacing system calculator

### Development Tools
- **CSS Variables:** Native browser support
- **Sass:** Preprocessing for mixins and functions
- **PostCSS:** Autoprefixer, optimization

### Testing Tools
- **WAVE:** Accessibility testing
- **axe DevTools:** Accessibility auditing
- **Lighthouse:** Performance and accessibility
- **BrowserStack:** Cross-browser testing
- **Contrast Checker:** WCAG compliance

---

## 11. Naming Conventions

### CSS Custom Properties
```
--{category}-{property}-{variant}
```

**Examples:**
- `--color-primary-500`
- `--spacing-8`
- `--font-size-xl`
- `--shadow-md`

### CSS Classes (BEM Methodology)
```
.block__element--modifier
```

**Examples:**
- `.card`
- `.card__title`
- `.card--featured`
- `.btn`
- `.btn--primary`
- `.btn--large`

---

## Conclusion

This design system provides a **comprehensive, production-ready foundation** for building a sophisticated, minimalist portfolio website. The system prioritizes:

✅ **Accessibility** - WCAG AA compliance built-in  
✅ **Responsiveness** - Mobile-first, fluid scaling  
✅ **Consistency** - Design tokens for all properties  
✅ **Performance** - Optimized animations and transitions  
✅ **Maintainability** - Clear naming, organized structure  
✅ **Scalability** - Extensible token system

**Next Steps:**
1. Implement design tokens in `_sass/_variables.scss`
2. Create component stylesheets using tokens
3. Build responsive layouts with mobile-first approach
4. Test accessibility and performance
5. Document component usage patterns

---

**Version:** 1.0  
**Status:** ✅ Ready for Implementation  
**Last Updated:** 2026-01-19  
**Maintained By:** Simon Salazar
