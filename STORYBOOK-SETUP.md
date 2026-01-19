# Storybook Setup Guide

This project includes a fully configured **Storybook** instance for developing and showcasing design system components in isolation.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

This will install:
- Storybook 7.6
- Sass compiler
- Accessibility addon
- Testing utilities

### 2. Run Storybook

```bash
npm run dev
```

This command will:
1. Compile Sass files to CSS
2. Start Storybook development server
3. Open your browser to `http://localhost:6006`

**Alternative commands:**

```bash
# Run Storybook only (if Sass already compiled)
npm run storybook

# Build static Storybook site
npm run build-storybook

# Watch Sass files for changes
npm run sass:watch
```

## 📚 What's Included

### Foundation Stories
- **Colors** - Complete color palette with contrast ratios
- **Typography** - Font scales, weights, and line heights
- **Spacing** - Spacing tokens and grid system
- **Shadows** - Elevation system

### Component Stories
- **Buttons** - Primary, secondary, ghost variants in multiple sizes
- **Cards** - Basic cards, blog post cards, interactive cards
- **Forms** - Text inputs, textareas, validation states
- **Profile** - Profile card component (coming soon)
- **Navigation** - Header and footer components (coming soon)

### Features
- ✅ **Interactive Controls** - Modify component props in real-time
- ✅ **Accessibility Testing** - Built-in a11y addon
- ✅ **Responsive Preview** - Test at different viewport sizes
- ✅ **Theme Toggle** - Switch between light/dark backgrounds
- ✅ **Auto-docs** - Automatic documentation generation
- ✅ **Keyboard Shortcuts** - Fast navigation

## 🎨 Using Storybook

### Navigation

Use the sidebar to browse:
- **Design System/Introduction** - Overview and getting started
- **Foundation/** - Design tokens (colors, typography, etc.)
- **Components/** - UI components

### Controls Panel

Each story has an interactive Controls panel where you can:
- Change button variants and sizes
- Toggle disabled states
- Modify text content
- Test different props

### Accessibility Panel

Every component is automatically audited for:
- Color contrast issues
- Missing ARIA labels
- Keyboard navigation problems
- Screen reader compatibility

Click the **Accessibility** tab to see results.

### Viewport Toolbar

Test components at different screen sizes:
- Mobile (375px)
- Tablet (768px)
- Desktop (1280px)

### Keyboard Shortcuts

- `⌘/Ctrl + Shift + F` - Search stories
- `⌘/Ctrl + Shift + A` - Toggle addons panel
- `⌘/Ctrl + Shift + D` - Toggle docs/canvas
- `A` - Toggle accessibility panel

## 📁 Project Structure

```
.storybook/
├── main.js          # Storybook configuration
└── preview.js       # Global decorators and parameters

stories/
├── Introduction.mdx                 # Welcome page
├── foundations/
│   ├── Colors.stories.js           # Color palette
│   └── Typography.stories.js       # Type system
└── components/
    ├── Button.stories.js           # Button variants
    ├── Card.stories.js             # Card components
    └── Input.stories.js            # Form inputs
```

## ✍️ Writing Stories

### Basic Story Structure

```javascript
// stories/components/MyComponent.stories.js

export default {
  title: 'Components/MyComponent',
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary'],
    },
  },
};

const Template = ({ variant }) => `
  <div class="my-component my-component--${variant}">
    Content here
  </div>
`;

export const Primary = {
  args: {
    variant: 'primary',
  },
  render: Template,
};
```

### Story Types

**1. Simple Static Story**
```javascript
export const Example = {
  render: () => `<button>Click me</button>`,
};
```

**2. Interactive Story with Controls**
```javascript
export const Interactive = {
  args: {
    label: 'Button',
    variant: 'primary',
  },
  render: ({ label, variant }) => `
    <button class="btn btn-${variant}">${label}</button>
  `,
};
```

**3. Multiple Variants**
```javascript
export const AllVariants = {
  render: () => `
    <div style="display: flex; gap: 16px;">
      <button class="btn btn-primary">Primary</button>
      <button class="btn btn-secondary">Secondary</button>
    </div>
  `,
};
```

## 🎯 Design Tokens Integration

Storybook uses the same Sass design tokens defined in `_sass/_variables.scss`:

```scss
// Colors
$color-primary-500: #0ea5e9;
$color-neutral-900: #171717;

// Typography
$font-size-base: 1rem;
$font-weight-semibold: 600;

// Spacing
$spacing-4: 1rem;
$spacing-6: 1.5rem;
```

Stories use inline styles that match these tokens for consistency.

## 🧪 Testing Components

### Visual Testing

Use Storybook to:
1. Develop components in isolation
2. Test different states and variants
3. Validate responsive behavior
4. Check accessibility compliance

### Accessibility Testing

The **a11y addon** automatically checks:
- ✅ Color contrast ratios (WCAG AA)
- ✅ Missing ARIA labels
- ✅ Keyboard navigation
- ✅ Screen reader compatibility

Fix any violations shown in the Accessibility panel.

### Responsive Testing

Use the viewport toolbar to test:
- Mobile (375px) - Single column layouts
- Tablet (768px) - 2-column layouts
- Desktop (1280px) - Full layouts

## 📦 Building Static Storybook

To create a production build:

```bash
npm run build-storybook
```

This generates a static site in `storybook-static/` that can be:
- Deployed to GitHub Pages
- Hosted on Netlify/Vercel
- Shared with your team

## 🔧 Configuration

### Adding Stories

Create new story files in the `stories/` directory:

```
stories/
├── components/
│   └── YourComponent.stories.js
└── patterns/
    └── YourPattern.stories.js
```

Stories are auto-discovered based on the pattern in `.storybook/main.js`:
```javascript
stories: ['../stories/**/*.mdx', '../stories/**/*.stories.@(js|jsx|mjs|ts|tsx)']
```

### Adding Addons

Install addon packages:
```bash
npm install --save-dev @storybook/addon-name
```

Register in `.storybook/main.js`:
```javascript
addons: [
  '@storybook/addon-name',
]
```

## 🐛 Troubleshooting

### Port Already in Use

If port 6006 is busy, specify a different port:
```bash
npm run storybook -- -p 6007
```

### Sass Compilation Errors

Ensure Sass is compiled before running Storybook:
```bash
npm run sass:build
npm run storybook
```

### Stories Not Showing

Check that:
1. Story files follow naming convention (`*.stories.js`)
2. Files are in the `stories/` directory
3. Story exports are correct

### Hot Reload Not Working

Restart Storybook:
```bash
# Stop with Ctrl+C
npm run dev
```

## 📚 Resources

### Official Documentation
- [Storybook Docs](https://storybook.js.org/docs)
- [Writing Stories](https://storybook.js.org/docs/html/writing-stories/introduction)
- [Accessibility Addon](https://storybook.js.org/addons/@storybook/addon-a11y)

### Design System Documentation
- `_bmad-output/planning-artifacts/design-system.md` - Complete specification
- `_bmad-output/planning-artifacts/design-system-implementation-guide.md` - Implementation guide
- `_bmad-output/planning-artifacts/design-tokens-reference.md` - Token reference

## 🎉 Next Steps

1. **Explore existing stories** - Browse the foundation and component stories
2. **Add new components** - Create story files for additional components
3. **Test accessibility** - Use the a11y addon to validate WCAG compliance
4. **Share with team** - Build and deploy static Storybook
5. **Document patterns** - Add stories for common UI patterns

---

**Version:** 1.0  
**Storybook Version:** 7.6.10  
**Status:** ✅ Ready to Use  
**Last Updated:** 2026-01-19
