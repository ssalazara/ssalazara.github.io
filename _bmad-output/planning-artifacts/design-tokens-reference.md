# Design Tokens Quick Reference
**Project:** GitHub Pages Portfolio  
**Version:** 1.0  
**Last Updated:** 2026-01-19

---

## Color Tokens

### Primary (Blue) Palette

| Token | Hex | Usage | Sample |
|-------|-----|-------|--------|
| `$color-primary-50` | `#f0f9ff` | Backgrounds, subtle highlights | <span style="background:#f0f9ff;padding:4px 12px;border:1px solid #ddd">Sample</span> |
| `$color-primary-100` | `#e0f2fe` | Light backgrounds | <span style="background:#e0f2fe;padding:4px 12px;border:1px solid #ddd">Sample</span> |
| `$color-primary-200` | `#bae6fd` | Borders, badges | <span style="background:#bae6fd;padding:4px 12px;border:1px solid #ddd">Sample</span> |
| `$color-primary-300` | `#7dd3fc` | Soft accents | <span style="background:#7dd3fc;padding:4px 12px;border:1px solid #ddd">Sample</span> |
| `$color-primary-400` | `#38bdf8` | Medium blue | <span style="background:#38bdf8;padding:4px 12px;color:white">Sample</span> |
| `$color-primary-500` | `#0ea5e9` | **Main brand color** | <span style="background:#0ea5e9;padding:4px 12px;color:white;font-weight:bold">Sample</span> |
| `$color-primary-600` | `#0284c7` | **Hover states, links** | <span style="background:#0284c7;padding:4px 12px;color:white;font-weight:bold">Sample</span> |
| `$color-primary-700` | `#0369a1` | Deep blue | <span style="background:#0369a1;padding:4px 12px;color:white">Sample</span> |
| `$color-primary-800` | `#075985` | Very deep | <span style="background:#075985;padding:4px 12px;color:white">Sample</span> |
| `$color-primary-900` | `#0c4a6e` | Darkest blue | <span style="background:#0c4a6e;padding:4px 12px;color:white">Sample</span> |

### Neutral (Gray) Palette

| Token | Hex | Usage | Contrast Ratio |
|-------|-----|-------|----------------|
| `$color-neutral-0` | `#ffffff` | Pure white, cards | N/A |
| `$color-neutral-50` | `#fafafa` | **Page background** | 1.04:1 |
| `$color-neutral-100` | `#f5f5f5` | **Card backgrounds** | 1.09:1 |
| `$color-neutral-200` | `#e5e5e5` | Borders, dividers | 1.25:1 |
| `$color-neutral-300` | `#d4d4d4` | Subtle borders | 1.48:1 |
| `$color-neutral-400` | `#a3a3a3` | Disabled text | 2.88:1 |
| `$color-neutral-500` | `#737373` | Secondary text | 4.61:1 ✅ |
| `$color-neutral-600` | `#525252` | **Body text** | 7.93:1 ✅ |
| `$color-neutral-700` | `#404040` | **Headings** | 10.41:1 ✅ |
| `$color-neutral-800` | `#262626` | Strong emphasis | 14.79:1 ✅ |
| `$color-neutral-900` | `#171717` | Maximum contrast | 18.25:1 ✅ |
| `$color-neutral-950` | `#0a0a0a` | Near black | 20.05:1 ✅ |

**✅ = WCAG AA Compliant (4.5:1 minimum for normal text)**

### Semantic Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `$color-success-500` | `#22c55e` | Success messages, positive states |
| `$color-warning-500` | `#f59e0b` | Warning messages, attention |
| `$color-error-500` | `#ef4444` | Error messages, destructive actions |
| `$color-info-500` | `#3b82f6` | Informational messages |

### Semantic Aliases

```scss
// Text Colors
$color-text-primary:    #171717  // neutral-900
$color-text-secondary:  #525252  // neutral-600
$color-text-tertiary:   #737373  // neutral-500
$color-text-disabled:   #a3a3a3  // neutral-400
$color-text-link:       #0284c7  // primary-600
$color-text-link-hover: #0369a1  // primary-700

// Background Colors
$color-bg-page:      #fafafa  // neutral-50
$color-bg-surface:   #ffffff  // neutral-0
$color-bg-secondary: #f5f5f5  // neutral-100

// Border Colors
$color-border-light:   #e5e5e5  // neutral-200
$color-border-default: #d4d4d4  // neutral-300
$color-border-strong:  #a3a3a3  // neutral-400
$color-border-focus:   #0ea5e9  // primary-500
```

---

## Typography Tokens

### Font Families

```scss
// Sans-serif (UI elements, body text)
$font-family-base: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 
                   Roboto, 'Helvetica Neue', Arial, sans-serif;

// Serif (headings, editorial)
$font-family-heading: 'Merriweather', 'Georgia', 'Times New Roman', 
                      Times, serif;

// Monospace (code)
$font-family-mono: 'JetBrains Mono', 'SF Mono', Monaco, 
                   'Courier New', monospace;
```

### Font Sizes (Fluid)

| Token | Mobile | Desktop | Usage |
|-------|--------|---------|-------|
| `$font-size-xs` | 12px | 13px | Captions, labels |
| `$font-size-sm` | 14px | 15px | Small text, metadata |
| `$font-size-base` | 16px | 16px | Body text |
| `$font-size-lg` | 18px | 20px | Large body, leads |
| `$font-size-xl` | 20px | 24px | Subheadings |
| `$font-size-2xl` | 24px | 30px | H3 headings |
| `$font-size-3xl` | 30px | 36px | H2 headings |
| `$font-size-4xl` | 36px | 48px | H1 headings |
| `$font-size-5xl` | 48px | 60px | Display headings |
| `$font-size-6xl` | 60px | 72px | Hero headings |

### Font Weights

| Token | Value | Usage |
|-------|-------|-------|
| `$font-weight-light` | 300 | Rarely used |
| `$font-weight-normal` | 400 | Body text |
| `$font-weight-medium` | 500 | Subtle emphasis |
| `$font-weight-semibold` | 600 | Strong emphasis |
| `$font-weight-bold` | 700 | Headings, CTAs |
| `$font-weight-extrabold` | 800 | Display headings |

### Line Heights

| Token | Value | Usage |
|-------|-------|-------|
| `$line-height-tight` | 1.25 | Large headings (H1, H2) |
| `$line-height-snug` | 1.375 | Subheadings (H3, H4) |
| `$line-height-normal` | 1.5 | Body text |
| `$line-height-relaxed` | 1.625 | Long-form content |
| `$line-height-loose` | 2 | Captions, labels |

---

## Spacing Tokens

### Base Scale (8px Grid)

| Token | Value | Pixels | Usage |
|-------|-------|--------|-------|
| `$spacing-0` | 0 | 0px | No spacing |
| `$spacing-px` | 1px | 1px | Hairline |
| `$spacing-0-5` | 0.125rem | 2px | Very tight |
| `$spacing-1` | 0.25rem | 4px | Tight spacing |
| `$spacing-2` | 0.5rem | 8px | Small gaps |
| `$spacing-3` | 0.75rem | 12px | Default gap |
| `$spacing-4` | 1rem | 16px | **Component padding** |
| `$spacing-5` | 1.25rem | 20px | Medium spacing |
| `$spacing-6` | 1.5rem | 24px | **Section spacing** |
| `$spacing-8` | 2rem | 32px | Large gaps |
| `$spacing-10` | 2.5rem | 40px | Extra large |
| `$spacing-12` | 3rem | 48px | **Large sections** |
| `$spacing-16` | 4rem | 64px | **Page-level spacing** |
| `$spacing-20` | 5rem | 80px | Extra spacing |
| `$spacing-24` | 6rem | 96px | Hero spacing |

### Common Spacing Patterns

```scss
// Card padding
padding: $spacing-4;  // 16px (mobile)
padding: $spacing-6;  // 24px (tablet)
padding: $spacing-8;  // 32px (desktop)

// Section spacing
margin-bottom: $spacing-8;   // Between sections (mobile)
margin-bottom: $spacing-12;  // Between sections (desktop)

// Component gaps
gap: $spacing-4;  // Between related items
gap: $spacing-6;  // Between components
gap: $spacing-8;  // Between major sections
```

---

## Border Radius Tokens

| Token | Value | Pixels | Usage |
|-------|-------|--------|-------|
| `$radius-none` | 0 | 0px | No rounding |
| `$radius-sm` | 0.25rem | 4px | Subtle rounding |
| `$radius-md` | 0.375rem | 6px | **Buttons, inputs** |
| `$radius-lg` | 0.5rem | 8px | **Cards, modals** |
| `$radius-xl` | 0.75rem | 12px | Prominent cards |
| `$radius-2xl` | 1rem | 16px | Large cards, profile images |
| `$radius-3xl` | 1.5rem | 24px | Hero sections |
| `$radius-full` | 9999px | Full | Pills, avatars, icon buttons |

---

## Shadow Tokens (Elevation)

| Token | Usage | Shadow Definition |
|-------|-------|-------------------|
| `$shadow-xs` | Subtle elevation | `0 1px 2px 0 rgba(0, 0, 0, 0.05)` |
| `$shadow-sm` | **Default cards** | `0 1px 3px 0 rgba(0, 0, 0, 0.1)` |
| `$shadow-md` | **Hover states** | `0 4px 6px -1px rgba(0, 0, 0, 0.1)` |
| `$shadow-lg` | Dropdowns, popovers | `0 10px 15px -3px rgba(0, 0, 0, 0.1)` |
| `$shadow-xl` | **Modals** | `0 20px 25px -5px rgba(0, 0, 0, 0.1)` |
| `$shadow-2xl` | Large overlays | `0 25px 50px -12px rgba(0, 0, 0, 0.25)` |
| `$shadow-focus` | Focus ring | `0 0 0 3px rgba(14, 165, 233, 0.3)` |

---

## Animation Tokens

### Duration

| Token | Value | Usage |
|-------|-------|-------|
| `$duration-instant` | 0ms | No animation |
| `$duration-fast` | 150ms | Quick transitions |
| `$duration-base` | 250ms | **Default transitions** |
| `$duration-moderate` | 350ms | Deliberate animations |
| `$duration-slow` | 500ms | Slow animations |

### Easing Functions

| Token | Value | Usage |
|-------|-------|-------|
| `$ease-linear` | `linear` | Constant speed |
| `$ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Accelerate |
| `$ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | **Decelerate (most common)** |
| `$ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | **Smooth both ends** |

### Common Transitions

```scss
// Default transition
transition: all $duration-base $ease-in-out;

// Color transitions
transition: color $duration-fast $ease-out,
            background-color $duration-fast $ease-out,
            border-color $duration-fast $ease-out;

// Transform transitions
transition: transform $duration-moderate $ease-out;
```

---

## Breakpoint Tokens

| Token | Min Width | Device Type |
|-------|-----------|-------------|
| `$breakpoint-sm` | 640px | Large phones, small tablets |
| `$breakpoint-md` | 768px | **Tablets** |
| `$breakpoint-lg` | 1024px | **Laptops, desktops** |
| `$breakpoint-xl` | 1280px | Large desktops |
| `$breakpoint-2xl` | 1536px | Wide monitors |

### Usage with Mixins

```scss
.component {
  // Mobile (base)
  padding: $spacing-4;
  
  // Tablet and up
  @include md {
    padding: $spacing-6;
  }
  
  // Desktop and up
  @include lg {
    padding: $spacing-8;
  }
}
```

---

## Component-Specific Tokens

### Buttons

```scss
// Heights
$button-height-sm:  2rem;      // 32px
$button-height-md:  2.5rem;    // 40px ← Default
$button-height-lg:  3rem;      // 48px

// Horizontal padding
$button-padding-x-sm:  1rem;     // 16px
$button-padding-x-md:  1.5rem;   // 24px ← Default
$button-padding-x-lg:  2rem;     // 32px

// Icon-only buttons (square)
$button-icon-sm:  2rem;       // 32×32px
$button-icon-md:  2.5rem;     // 40×40px ← Default
$button-icon-lg:  3rem;       // 48×48px
```

### Form Inputs

```scss
// Heights
$input-height-sm:  2rem;      // 32px
$input-height-md:  2.5rem;    // 40px ← Default
$input-height-lg:  3rem;      // 48px

// Horizontal padding
$input-padding-x-sm:  0.75rem;   // 12px
$input-padding-x-md:  1rem;      // 16px ← Default
$input-padding-x-lg:  1.25rem;   // 20px
```

### Cards

```scss
// Padding
$card-padding-sm:  $spacing-4;    // 16px
$card-padding-md:  $spacing-6;    // 24px ← Default
$card-padding-lg:  $card-padding-8;    // 32px

// Minimum height
$card-min-height:  12rem;         // 192px
```

### Navigation

```scss
// Header height
$header-height-mobile:   3.5rem;    // 56px
$header-height-desktop:  4rem;      // 64px

// Navigation spacing
$nav-item-spacing:  $spacing-6;     // 24px between items
$nav-item-padding:  $spacing-2;     // 8px vertical padding
```

---

## Z-Index Scale

| Token | Value | Usage |
|-------|-------|-------|
| `$z-index-base` | 0 | Default layer |
| `$z-index-dropdown` | 1000 | Dropdown menus |
| `$z-index-sticky` | 1020 | Sticky headers |
| `$z-index-fixed` | 1030 | Fixed elements |
| `$z-index-overlay` | 1040 | Modal backdrops |
| `$z-index-modal` | 1050 | **Modal dialogs** |
| `$z-index-popover` | 1060 | Popovers |
| `$z-index-tooltip` | 1070 | Tooltips (highest) |

---

## Layout Tokens

### Container Widths

```scss
$container-sm:   640px;
$container-md:   768px;
$container-lg:   1024px;
$container-xl:   1280px;   // Default max-width
$container-2xl:  1536px;

// Special containers
$content-max-width:  720px;  // For long-form content (65-75 characters)
```

### Container Padding (Responsive)

```scss
$container-padding-mobile:  16px;   // $spacing-4
$container-padding-tablet:  24px;   // $spacing-6
$container-padding-desktop: 32px;   // $spacing-8
```

### Grid Gaps

```scss
$grid-gap-sm:  $spacing-4;   // 16px
$grid-gap-md:  $spacing-6;   // 24px ← Default
$grid-gap-lg:  $spacing-8;   // 32px
```

---

## Quick Reference Card

### Most Used Tokens

```scss
// Colors
$color-primary-500      // Brand color
$color-primary-600      // Links, hover
$color-text-primary     // Body text (#171717)
$color-text-secondary   // Secondary text (#525252)
$color-bg-page          // Page background (#fafafa)
$color-bg-surface       // Cards, panels (white)
$color-border-default   // Standard borders

// Typography
$font-size-base         // 16px (body text)
$font-size-lg           // 18-20px (leads)
$font-size-2xl          // 24-30px (H3)
$font-size-3xl          // 30-36px (H2)
$font-size-4xl          // 36-48px (H1)
$font-weight-normal     // 400 (body)
$font-weight-semibold   // 600 (emphasis)
$font-weight-bold       // 700 (headings)

// Spacing
$spacing-2              // 8px (small gap)
$spacing-4              // 16px (component padding)
$spacing-6              // 24px (section spacing)
$spacing-8              // 32px (large gap)
$spacing-12             // 48px (section breaks)

// Border Radius
$radius-md              // 6px (buttons, inputs)
$radius-lg              // 8px (cards)
$radius-full            // Pills, avatars

// Shadows
$shadow-sm              // Default cards
$shadow-md              // Hover states
$shadow-focus           // Focus ring

// Animation
$duration-base          // 250ms (default)
$ease-in-out            // Smooth transitions
```

---

## Token Naming Convention

```
--{category}-{property}-{variant}
```

**Examples:**
- `$color-primary-500`
- `$spacing-4`
- `$font-size-xl`
- `$button-height-md`
- `$shadow-lg`

**Categories:**
- `color` - Color values
- `font` - Typography
- `spacing` - Spacing and sizing
- `radius` - Border radius
- `shadow` - Box shadows
- `duration` - Animation timing
- `ease` - Easing functions
- `breakpoint` - Responsive breakpoints
- `z-index` - Layering
- `button` - Button-specific
- `input` - Input-specific
- `card` - Card-specific

---

**Version:** 1.0  
**Last Updated:** 2026-01-19  
**Total Tokens:** 300+  
**Status:** ✅ Production Ready
